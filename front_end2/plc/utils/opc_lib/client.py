'''
 * @Author: wl.liuzhao 
 * @Date: 2023-03-31 18:13:31 
 * @Last Modified by:   wl.liuzhao 
 * @Last Modified time: 2023-03-31 18:13:31 
 - 自改opc客户端，使其达到工业生产标准
'''

from opcua import Client
from opcua import ua
from opcua.common.node import Node
from opcua.ua.uatypes import LocalizedText
from typing import List,Dict,Union
from concurrent.futures._base import TimeoutError   # 超时报错
from .node import MyNode
from opcua.common import utils
from .keepalive import WLKeepAlive
import atexit

import logging
_logger = logging.getLogger(__name__)


class MyClient(Client):
    def __init__(self, url, timeout=4,name='wl-lz'):
        """对opcua自带的客户端进行修改

        Args:
            url (_type_): _description_
            timeout (int, optional): _description_. Defaults to 4.
            do_keepalive (bool, optional): _description_. Defaults to False.
        """
        super().__init__(url, timeout)
        self.name = name
    
      
    def get_node(self, nodeid)->MyNode:
        """
        Get node using NodeId object or a string representing a NodeId
        """
        return MyNode(self.uaclient, nodeid)
    
    def get_root_node(self):
        return self.get_node(ua.TwoByteNodeId(ua.ObjectIds.RootFolder))
    
    def create_session(self):
        """
        send a CreateSessionRequest to server with reasonable parameters.
        If you want o modify settings look at code of this methods
        and make your own
        """
        desc = ua.ApplicationDescription()
        desc.ApplicationUri = self.application_uri
        desc.ProductUri = self.product_uri
        desc.ApplicationName = ua.LocalizedText(self.name)
        desc.ApplicationType = ua.ApplicationType.Client

        params = ua.CreateSessionParameters()
        # at least 32 random bytes for server to prove possession of private key (specs part 4, 5.6.2.2)
        nonce = utils.create_nonce(32)
        params.ClientNonce = nonce
        params.ClientCertificate = self.security_policy.client_certificate
        params.ClientDescription = desc
        params.EndpointUrl = self.server_url.geturl()
        params.SessionName = self.description + " Session" + str(self._session_counter)
        params.RequestedSessionTimeout = self.session_timeout
        params.MaxResponseMessageSize = 0  # means no max size
        response = self.uaclient.create_session(params)
        if self.security_policy.client_certificate is None:
            data = nonce
        else:
            data = self.security_policy.client_certificate + nonce
        self.security_policy.asymmetric_cryptography.verify(data, response.ServerSignature.Signature)
        self._server_nonce = response.ServerNonce
        if not self.security_policy.server_certificate:
            self.security_policy.server_certificate = response.ServerCertificate
        elif self.security_policy.server_certificate != response.ServerCertificate:
            raise ua.UaError("Server certificate mismatch")
        # remember PolicyId's: we will use them in activate_session()
        ep = Client.find_endpoint(response.ServerEndpoints, self.security_policy.Mode, self.security_policy.URI)
        self._policy_ids = ep.UserIdentityTokens
        if self.session_timeout != response.RevisedSessionTimeout:
            _logger.warning("Requested session timeout to be %dms, got %dms instead",
                                self.secure_channel_timeout,
                                response.RevisedSessionTimeout)
            self.session_timeout = response.RevisedSessionTimeout
        
        # 这样只能时间保活，不能实现重连，要在MyOpcClient里使用
        
        # self.keepalive = MyKeepAlive(
        #     self, min(self.session_timeout, self.secure_channel_timeout) * 0.7)  # 0.7 is from spec
        # self.keepalive.start()
        
        return response

        # return super().create_session()

    def connect(self):
        self.connect_socket()
        try:
            self.send_hello()
            self.open_secure_channel()
            try:
                self.create_session()
                try:
                    self.activate_session(username=self._username, password=self._password, certificate=self.user_certificate)
                except Exception:
                    # clean up the session
                    self.close_session()
                    raise
            except Exception:
                # clean up the secure channel
                self.close_secure_channel()
                raise
        except Exception:
            self.disconnect_socket()  # clean up open socket
            raise


class MyOpcClient:
    """生产环境用的opc client
    - 加入了连接保活，断线重连机制
    - 更加好用的opc变量访问方式   client[var_name]   client.var_name   
    """
    def __init__(self,url:str="opc.tcp://192.168.115.100:4840",client_name:str='wl-lz',secure_channel_timeout = 3*1000,session_timeout = 30*1000,keep_alive_and_reconnect:bool=True) -> None:
        """_summary_

        Args:
            url (_type_, optional): _description_. Defaults to "opc.tcp://192.168.115.100:4840".
            client_name (str, optional): _description_. Defaults to 'wl-lz'.
            secure_channel_timeout (_type_, optional): _description_. Defaults to 3*1000.
            session_timeout (_type_, optional): _description_. Defaults to 30*1000.
            keep_alive_and_reconnect (bool, optional): 保活以及掉线重连开关. Defaults to True.
        """
        self.plc_url = url
        self.client_name = client_name
        self.session_timeout = session_timeout
        self.secure_channel_timeout = secure_channel_timeout
        self.keep_alive_and_reconnect = keep_alive_and_reconnect
        self._reset_client()
        self.types = ua.VariantType
        self.opc_vars:Dict[str,MyNode] = {}
        self.keepalive = None
        print(f'create an OPC client {client_name}:{self}')
    
    @property
    def opc_vars_names(self):
        return self.opc_vars.keys()
    
    def _reset_client(self):
        if hasattr(self,"_client"):
            del self._client
        if hasattr(self,"uaclient"):
            del self.uaclient
        self._client:MyClient = MyClient(self.plc_url,timeout=3)
        self._client.name = self.client_name
        self._client.secure_channel_timeout = self.secure_channel_timeout    # 一个请求的超时3s
        self._client.session_timeout = self.session_timeout       # 30s超时
        self.uaclient = self._client.uaclient        # 用于给Node变量设置连接对象     

    def get_root_node(self) -> MyNode:
        return self._client.get_root_node()
    
    def get_node(self,nodeid)->MyNode:
        return self._client.get_node(nodeid)
       
    
    # def _refresh_node(self,node:MyNode):
    #     new_node = self.get_node(node.nodeid)
    #     new_node.name = node.name
    #     new_node.description = node.description
    #     return new_node
        
    def _get_opcvar(self,path:list)->MyNode:
        return self._client.get_root_node().get_child(path)

    def register_opcvar(self,path_or_node:Union[List[str],MyNode],name=None,description='plc Node variable'):
        if isinstance(path_or_node,list):
            opc_var = self._get_opcvar(path_or_node)
        elif isinstance(path_or_node,MyNode):
            opc_var = path_or_node
            opc_var.description = description
        else:
            raise Exception('参数错误')
        
        # 设置变量名以及变量描述词
        name = opc_var.get_display_name().Text if name==None else name
        opc_var.name = name
        opc_var.description = description+f'\tnamed:[{name}]'
        
        # 注册
        self.opc_vars[name]=opc_var
        return opc_var
    
    def __getitem__(self,key)->MyNode:
        return self.opc_vars[key]
        # return self._refresh_node(self.opc_vars[key])
    
    def __getattr__(self, attr_name):
        try:
            return self[attr_name]
        except:
            self.__getattribute__(attr_name)

    def connect(self):
        """
            - socket连接
            - 建立安全通道
            - 打开一个会话
            - 开始通信
            
            - 发生异常
            - 关闭会话
            - 关闭安全通道
            - 关闭socket连接
            
            - keepalive
        """
        self._client.connect()
        atexit.register(self.disconnect)
        if self.keep_alive_and_reconnect:
            self.keepalive = WLKeepAlive(
                self, min(self.session_timeout, self.secure_channel_timeout) * 0.7)  # 0.7 is from spec
            self.keepalive.start()
        
    
    def _reconnect(self):
        try:
            self._client.disconnect()
        except:
            pass
        self._reset_client()
        self._client.connect()
    
    def disconnect(self):
        try:
            self.keepalive.stop()
            self._client.disconnect()
        except:
            pass
    
    def subscript(self,handler,node:MyNode,period=500):
        # 订阅 
        sub = self._client.create_subscription(period,handler)
        sub.subscribe_data_change(node)   
    
    
    def reset_vars_uaclient(self):
        for _,n in self.opc_vars.items():
            n.server = self.uaclient
            
    
    def read_single_var(self,opc_var:Node=None,var_name:str=None):
        if opc_var:
            return opc_var.get_value()
        elif var_name:
            return self[var_name].get_value()
        else:
            raise Exception('param all is None')
    
    def read_vars(self,opc_vars:List[MyNode]):
        return self._client.get_values(opc_vars)
    
    # 在MyNode中定义   client.heart_beart.set_word(12)
    # def write_word(self,var_name:str,value:int):
    #     assert type(value)==int
    #     value = ua.DataValue(ua.Variant(value,ua.VariantType.UInt16))
    #     self[var_name].set_value(value)
    

