from opcua import Client
from opcua.common.node import Node
from opcua import ua
from opcua.common.subscription import Subscription
from opcua.ua.uatypes import LocalizedText
from opcua.ua.uatypes import NodeId
# from opcua import Da
from opcua.ua.uatypes import DataValue
from opcua.ua.uatypes import LocalizedText
from opcua.ua.uatypes import ExtensionObject
import time
from concurrent.futures._base import TimeoutError   # 超时报错

from opcua.common import utils

import sys,pathlib
crtpath = pathlib.Path(__file__)
sys.path.append(str(crtpath.parent.parent.absolute()))

from logs import logger
import os
from opcua.client.client import KeepAlive
import logging
_logger = logging.getLogger(__name__)



class MyKeepAlive(KeepAlive):
    def run(self):
        print("starting keepalive thread with period of %s milliseconds", self.timeout)
        self.client:Client
        server_state = self.client.get_node(ua.FourByteNodeId(ua.ObjectIds.Server_ServerStatus_State))
        while not self._dostop:
            with self._cond:
                self._cond.wait(self.timeout / 1000)
            if self._dostop:
                break
            # print("renewing channel")
            # try:
            #     self.client.open_secure_channel(renew=True)
            # except TimeoutError:
            #     print("keepalive failed: timeout on open_secure_channel()")
            #     break
            try:
                val = server_state.get_value()
                print(f"server state is: {val} ")
            except:
                # 编写重连函数
                raise
        print("keepalive thread has stopped")


    
# from .node import MyNode

# class MyClient(Client):
#     def __init__(self, url, timeout=4,do_keepalive=False):
#         super().__init__(url, timeout)
#         self.name = 'wl-lz'
#         self.do_keepalive = do_keepalive
    
#     def get_node(self, nodeid):
#         """
#         Get node using NodeId object or a string representing a NodeId
#         """
#         return MyNode(self.uaclient, nodeid)

    
#     def create_session(self):
#         """
#         send a CreateSessionRequest to server with reasonable parameters.
#         If you want o modify settings look at code of this methods
#         and make your own
#         """
#         desc = ua.ApplicationDescription()
#         desc.ApplicationUri = self.application_uri
#         desc.ProductUri = self.product_uri
#         desc.ApplicationName = ua.LocalizedText(self.name)
#         desc.ApplicationType = ua.ApplicationType.Client

#         params = ua.CreateSessionParameters()
#         # at least 32 random bytes for server to prove possession of private key (specs part 4, 5.6.2.2)
#         nonce = utils.create_nonce(32)
#         params.ClientNonce = nonce
#         params.ClientCertificate = self.security_policy.client_certificate
#         params.ClientDescription = desc
#         params.EndpointUrl = self.server_url.geturl()
#         params.SessionName = self.description + " Session" + str(self._session_counter)
#         params.RequestedSessionTimeout = self.session_timeout
#         params.MaxResponseMessageSize = 0  # means no max size
#         response = self.uaclient.create_session(params)
#         if self.security_policy.client_certificate is None:
#             data = nonce
#         else:
#             data = self.security_policy.client_certificate + nonce
#         self.security_policy.asymmetric_cryptography.verify(data, response.ServerSignature.Signature)
#         self._server_nonce = response.ServerNonce
#         if not self.security_policy.server_certificate:
#             self.security_policy.server_certificate = response.ServerCertificate
#         elif self.security_policy.server_certificate != response.ServerCertificate:
#             raise ua.UaError("Server certificate mismatch")
#         # remember PolicyId's: we will use them in activate_session()
#         ep = Client.find_endpoint(response.ServerEndpoints, self.security_policy.Mode, self.security_policy.URI)
#         self._policy_ids = ep.UserIdentityTokens
#         if self.session_timeout != response.RevisedSessionTimeout:
#             _logger.warning("Requested session timeout to be %dms, got %dms instead",
#                                 self.secure_channel_timeout,
#                                 response.RevisedSessionTimeout)
#             self.session_timeout = response.RevisedSessionTimeout
#         self.keepalive = MyKeepAlive(
#             self, min(self.session_timeout, self.secure_channel_timeout) * 0.7)  # 0.7 is from spec
#         if self.do_keepalive:
#             self.keepalive.start()
#         return response

#         # return super().create_session()

#     def connect(self):
#         self.connect_socket()
#         try:
#             self.send_hello()
#             self.open_secure_channel()
#             try:
#                 self.create_session()
#                 try:
#                     self.activate_session(username=self._username, password=self._password, certificate=self.user_certificate)
#                 except Exception:
#                     # clean up the session
#                     self.close_session()
#                     raise
#             except Exception:
#                 # clean up the secure channel
#                 self.close_secure_channel()
#                 raise
#         except Exception:
#             self.disconnect_socket()  # clean up open socket
#             raise

client = Client("opc.tcp://192.168.115.80:4840")   # 小线
# client = Client("opc.tcp://192.168.115.140:4840")   # 小线
# client = MyClient("opc.tcp://192.168.115.140:4840")    # 大线
client.keepalive

client.secure_channel_timeout = 3*1000    # 一个请求的超时3s
client.session_timeout = 10*1000       # 30s超时

res = client.connect()
# client.keepalive.stop()
root = client.get_root_node()
for i in root.get_child(['0:Objects','2:DeviceSet','3:KQL2-02PLC','3:DataBlocksGlobal','3:DB502_TCP_Server']).get_children():
    i:Node
    name:LocalizedText=(i.get_display_name())
    print(name.Text,'\t',i.get_path(as_string=True))
    
heart_beat = client.get_root_node().get_child(['0:Objects', '2:DeviceSet', '3:PLC_Line1', '3:DataBlocksGlobal','3:DB702_TCP_Server','3:HeartBeat'])
cmd_stuct = client.get_root_node().get_child(['0:Objects', '2:DeviceSet', '3:PLC_Line1', '3:DataBlocksGlobal','3:DB702_TCP_Server','3:MES_cmd'])
db702 = client.get_root_node().get_child(['0:Objects', '2:DeviceSet', '3:PLC_Line1', '3:DataBlocksGlobal','3:DB702_TCP_Server'])
# mes_cmd :Node= client.get_root_node().get_child(["0:Objects","3:KQL2-02PLC","3:DataBlocksGlobal","3:DB502_TCP_Server","3:MES_cmd"])
# print(mes_cmd)
# print(mes_cmd.get_children())
# heart_beat:Node = client.get_root_node().get_child(["0:Objects","3:KQL2-02PLC","3:DataBlocksGlobal","3:DB502_TCP_Server"]).get_variables()[0]
# print(111111111)
# value_name :LocalizedText= heart_beat.get_display_name()
# print(value_name.Text)

# heart_beat.set_writable(True)
# print(heart_beat.get_type_definition())
while True:
    try:
        # vartype :NodeId= (heart_beat.get_type_definition())
        # vartype = (heart_beat.get_data_type_as_variant_type())
        # print(type(vartype))
        # print(vartype.NodeIdType)
        # print(client.get_values(cmd_stuct.get_children()))
        # client.set_values()
        # cmd_values:ExtensionObject = cmd_stuct.get_value()
        # print(type(cmd_values))
        # print(cmd_values.Body)
        # continue
        # break
        value = ua.DataValue(ua.Variant(heart_beat.get_value()+1,ua.VariantType.UInt16))
        heart_beat.set_value(value)
        heart_beat
        # heart_beat.set_value()
        
        logger.debug(heart_beat.get_value())
        time.sleep(0.1)
        
    except TimeoutError:
        try:
            client = Client("opc.tcp://192.168.115.140:4840",timeout=2)    # 大线
            client.secure_channel_timeout = 3*1000    # 一个请求的超时3s
            client.session_timeout = 10*1000       # 30s超时
            client.connect()
            # client.keepalive.stop()
            # heart_beat = client.get_root_node().get_child(['0:Objects', '2:DeviceSet', '3:PLC_Line1', '3:DataBlocksGlobal','3:DB702_TCP_Server','3:HeartBeat'])
            heart_beat.server = client.uaclient
        except Exception as err:
            # print(err)
            # raise
            pass
            
        print(1111111111111)
        
    # except BrokenPipeError:       # 下载程序的时候出现这个错误，好像也不需要处理，正常报错即可
        # pass
        # logger.error(err)

# --------------------

# cmd_value :DataValue= mes_cmd.get_data_value()
# print(type(cmd_value))
# print(mes_cmd.get_value())
# print(11111111111)
# print(cmd_value.Value)
# print(root)
# objects_node = client.get_objects_node()
# print(objects_node)
# # print(type(res))
# objects_node.get_children()[2].get_children()[14].get_children()

# client.connect()
# dbs :Node= objects_node.get_children()[2].get_children()[13]

# print(type(dbs))

# print(dbs.get_value())
