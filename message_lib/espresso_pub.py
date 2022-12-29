# 数据产生端  生产者
#
import time

import zmq
# from zmq.sugar.context import ST
import json


class Publisher:
    def __init__(self,to_url:str='tcp://192.168.222.129:5555',topic='') -> None:   
        """初始化一个消息发布者
        一条消息的结构是: "(topic)-(序列化成字符串的json)"   topic可能是空字符串，此时最前面是-
        Args:
            to_url (str, optional): 消息中间件的地址. Defaults to 'tcp://192.168.222.129:5555'.
            topic: 发布的主题，可以使用set_topic进行重新设置，Defaults to '',订阅所有topic.
            
        """
        self.to_url = to_url
        self.topic:str = topic
        ctx = zmq.Context.instance()

        self.publisher = ctx.socket(zmq.PUB)
        self.connect()
        print(f"pub to {self.to_url}")
    
    def set_topic(self,topic:str=''):
        """设置发布的主题

        Args:
            topic (str, optional): 发布的主题. Defaults to ''.
        """
        self.topic = topic
        
    
    def send_json(self,content:dict):
        """发送json数据

        Args:
            content (dict): 要发送的内容，必须是字典类型
        """
        assert type(content)==dict
        str_to_send = self.topic+'-'+json.dumps(content)
        print(str_to_send.encode())
        self.publisher.send(str_to_send.encode('utf-8'))
        time.sleep(0.001)         # 释放cpu资源
    
    def connect(self):
        """如果没有关闭连接，无需调用
        """
        self.publisher.connect(self.to_url)
        time.sleep(2)    # 等待pub和sub组成拓扑

    def close(self):
        self.publisher.close()




if __name__ == '__main__':
    import json,uuid
    with open('msg_config.json','r') as f:
        mesconfig = json.load(f)
    puber = Publisher(f"tcp://{mesconfig['proxy_host']}:{mesconfig['in_proxy_port']}")
    puber.set_topic('a')
    while True:
        try:
            puber.send_json({'aaaaaaaa':str(uuid.uuid4())})
        except InterruptedError:
            break
        
        