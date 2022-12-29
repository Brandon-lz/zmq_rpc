# 服务端中间件
from threading import Thread
import zmq
from .zhelpers import zpipe
from zmq.devices import monitored_queue


def listener_thread (pipe):
    print('proxy start listening')
    # Print everything that arrives on pipe
    while True:
        try:
            # print (pipe.recv_multipart())
            pipe.recv_multipart()               # 接收到管道里
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted



def main():
    import json
    ctx = zmq.Context.instance()

    pipe = zpipe(ctx)

    l_thread = Thread(target=listener_thread, args=(pipe[1],),daemon=True)
    l_thread.start()

    with open('msg_config.json','r') as f:
        mesconfig = json.load(f)
    
    # print(mesconfig)
    in_url = f"tcp://*:{mesconfig['in_proxy_port']}"
    out_url = f"tcp://{mesconfig['proxy_host']}:{mesconfig['out_proxy_port']}"

    subscriber = ctx.socket(zmq.XSUB)
    subscriber.bind(in_url)

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind(out_url)


    try:
        monitored_queue(subscriber, publisher, pipe[0], b'pub', b'sub')
    except KeyboardInterrupt:
        print ("Interrupted")


if __name__ == '__main__':
    main()
