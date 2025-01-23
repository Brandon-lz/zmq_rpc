'''
 * @Author: wl.liuzhao 
 * @Date: 2023-03-31 18:13:45 
 * @Last Modified by:   wl.liuzhao 
 * @Last Modified time: 2023-03-31 18:13:45 
 - 后台连接保持，以及故障自动恢复
'''

from opcua.client.client import KeepAlive
# from .client import MyOpcClient
from opcua import ua
from concurrent.futures._base import TimeoutError   # 超时报错
from typing import TYPE_CHECKING
from logging import getLogger
logger = getLogger("uvicorn")
# logger.setLevel(level="DEBUG")

if TYPE_CHECKING: 
    from .client import MyOpcClient


class WLKeepAlive(KeepAlive):
    if TYPE_CHECKING:
        def __init__(self, client:MyOpcClient, timeout):
            self.client:MyOpcClient
            super().__init__(client, timeout)
    else:
        def __init__(self, client, timeout):
            super().__init__(client, timeout)
        
    def run(self):
        logger.info("starting keepalive thread with period of %s milliseconds", self.timeout)
        # self.client:MyOpcClient
        while not self._dostop:
            with self._cond:
                self._cond.wait(self.timeout / 1000)
            if self._dostop:
                break
                
            try:
                self.client._client.open_secure_channel(renew=True)
                self.client.reset_vars_uaclient()
                self.keep_nodes_alive()
                
                # server_state.get_value()
                # print(f"server state is: {val} ")
                # print(f'{self.client.client_name} keepalive running')
            except:
                # 编写重连函数
                logger.warning(f'与目标设备{self.client.plc_url}丢失连接，正在重连')
                try:
                    self.client._reconnect()
                    self.client.reset_vars_uaclient()
                    # server_state = self.client.get_node(ua.FourByteNodeId(ua.ObjectIds.Server_ServerStatus_State))
                except:
                    pass
        logger.info("keepalive thread has stopped")
    
    def keep_nodes_alive(self):
        self.client._client.get_root_node().get_browse_name()
        logger.info(f'server {self.client.client_name} is alive')
        # for _,n in self.client.opc_vars.items():
        #     if n._alive < 1:
        #         # print(f'server {self.client.client_name} node {n.name} keep alive')
        #         n.get_value()
        #     else:
        #         n._alive -= 1
            
            