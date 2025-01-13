'''
 * @Author: wl.liuzhao 
 * @Date: 2023-03-31 18:19:45 
 * @Last Modified by:   wl.liuzhao 
 * @Last Modified time: 2023-03-31 18:19:45 
 - 变量订阅
'''

from opcua.common.subscription import Subscription
from opcua.common.node import Node
from opcua.common.subscription import DataChangeNotif


class SubHandler(object):
    """
        opc订阅句柄
        对于西门子plc不是很好用，最多支持
    Args:
        object (_type_): _description_
    """
    def datachange_notification(self, node:Node, val, data:DataChangeNotif):
        print("Python: New data change event", node, val,data)
        
    def event_notification(self, event):
        print("Python: New event", event)

# normal_subhandler = SubHandler()

# subscribing to a variable node
# sub = client.create_subscription(500, handler)    # 500ms的订阅
# handle = sub.subscribe_data_change(heart_beat)    # 订阅
