# 数据收集处理    消费者
#
# from logs import logger


import zmq
# from zmq.sugar.context import ST
import json,time

# The subscriber thread requests messages starting with
# A and B, then reads and counts incoming messages.


class Subscriber:

    def __init__(self,from_url:str = 'tcp://192.168.222.129:5556',topic='') -> None:
        """创建一个订阅者

        Args:
            from_url (str, optional): 消息中间件proxy的输出端口地址. Defaults to 'tcp://192.168.222.129:5556'.
            topic (str, optional): 订阅的主题topic. Defaults to '',订阅所有.
        """
        self.from_url = from_url
        self.topic:str = topic
        
        ctx = zmq.Context.instance()

        # Subscribe to "A" and "B"
        self.subscriber = ctx.socket(zmq.SUB)
        self.connect()        
        print(f"pub to {self.from_url}")
        


    def set_topic(self,topic:str=''):
        '''
        设置订阅主题，缺省全部订阅
        '''
        self.topic = topic
        self.subscriber.setsockopt(zmq.SUBSCRIBE, self.topic.encode())
    
    def rcv_json(self):
        msg = self.subscriber.recv().decode('utf-8')
        rcvdict = json.loads(msg.removeprefix(self.topic+'-'))
        return rcvdict
        

    def connect(self):
        """如果没有关闭连接，则不需要调用
        """
        self.subscriber.connect(self.from_url)
        time.sleep(2)            # 等待网络拓扑形成

    def close(self):
        self.subscriber.close()

    
  

if __name__ == '__main__':
    import json 
    with open('msg_config.json','r') as f:
        mesconfig = json.load(f)

    subcriber = Subscriber(f"tcp://{mesconfig['proxy_host']}:{mesconfig['out_proxy_port']}")
    subcriber.set_topic('a')


    while True:
        try:
            print(subcriber.rcv_json())
        except InterruptedError:
            break
