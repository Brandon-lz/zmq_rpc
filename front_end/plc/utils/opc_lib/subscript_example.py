'''
 * @Author: wl.liuzhao 
 * @Date: 2023-04-11 16:05:13 
 * @Last Modified by:   wl.liuzhao 
 * @Last Modified time: 2023-04-11 16:05:13 
 * OPC订阅功能使用示例，但是由于plc性能的问题，即便是西门子plc1500也支持不了多少个订阅句柄
'''

from plc_addr import arrival_sign_client
from opcua import Node
from opcua import ua
from opc_lib import SubHandler
from logs import logger
import traceback
from opcua.common.subscription import SubscriptionItemData
from concurrent.futures import ThreadPoolExecutor
import time

task_pool = ThreadPoolExecutor(20)


def log_exception(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as err:
            logger.error(f'error raise at {func.__name__}')
            logger.exception(err)
            logger.error(traceback.format_exc(err))
    return wrapper

@log_exception
def io_option(node:Node):
    """io耗时操作要用新线程去处理

    Args:
        node (Node): _description_
    """
    value = ua.DataValue(ua.Variant(0,ua.VariantType.UInt16))
    node.set_value(value)


class ResetSubHandler(SubHandler):
    @log_exception
    def datachange_notification(self, node: Node, val, data):
        if val==1:
            task_pool.submit(io_option,node=node)
            
    def event_notification(self, event):
        pass


arrival_sign_client.subscript(handler=ResetSubHandler(),node=arrival_sign_client['zjd-10-1'])
arrival_sign_client.subscript(handler=ResetSubHandler(),node=arrival_sign_client['zjd-10-2'])
arrival_sign_client.subscript(handler=ResetSubHandler(),node=arrival_sign_client['zjd-10-3'])
