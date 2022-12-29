
import zmq,time
from sys_config import get_config
config = get_config()


DeviceSeriesNum = config['serie_number']


class ZMQSender(object):
    def __init__(self, zmq_s:zmq.sugar.socket.Socket) -> None:
        self.zmq_s = zmq_s

    def send_string(self, data:str, **kwargs):
        data = f'device:{DeviceSeriesNum}:' + data
        ret = self.zmq_s.send(data.encode('utf-8'),**kwargs)
        time.sleep(0.05)                      # 防止发送阻塞
        return ret

    def close(self,linger=None):
        return self.zmq_s.close(linger)


def zmq_produce(url):
    """Produce messager"""
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.PUSH)
    s.connect(url)
    s.send_string
    s = ZMQSender(s)
    return s


if __name__ == '__main__':
    producer = zmq_produce()