'''
 * @Author: wl.liuzhao 
 * @Date: 2023-03-31 18:15:21 
 * @Last Modified by:   wl.liuzhao 
 * @Last Modified time: 2023-03-31 18:15:21 
 - 使用用例
'''

from .client import MyOpcClient
from .node import MyNode
from opcua.ua.uatypes import LocalizedText
from logging import getLogger

logger = getLogger(__name__)

# 周期性的变量
period_client = MyOpcClient(url="opc.tcp://192.168.115.140:4840")
period_client.connect()

heart_beat = period_client.register_opcvar(
    ['0:Objects', '2:DeviceSet', '3:PLC_Line1', '3:DataBlocksGlobal','3:DB702_TCP_Server','3:HeartBeat'],
    name='heart_beat'
)

print(period_client.opc_vars_names)
period_client.heart_beat.set_word(100)


# 业务逻辑性变量
logic_client = MyOpcClient(url="opc.tcp://192.168.115.100:4840")
logic_client.connect()
node1 = logic_client.register_opcvar(
    ['0:Objects', '2:DeviceSet', '3:PLC_Line1', '3:DataBlocksGlobal','3:DB702_TCP_Server','3:MES_cmd'],
    name='cmd_struct'
)


print(node1.nodeid,node1.get_path(as_string=True))

# 使用
import time
while True:
    try:
        logger.info(period_client.heart_beat.get_value())
        period_client.heart_beat.set_word(period_client.heart_beat.get_value()+1)
    except Exception as err:
        logger.error(err)
    time.sleep(1)