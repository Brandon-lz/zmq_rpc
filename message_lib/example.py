# host and port
proxy_host = 'localhost'
in_proxy_port = 5555
out_proxy_port = 5556



# 1 run freeMQ proxy, single process to run:
from message_lib import main_proxy
main_proxy(in_proxy_port,out_proxy_port)       # that's ok


# 2 run publisher, another process to run:
from message_lib import Publisher
puber = Publisher(f"tcp://{proxy_host}:{in_proxy_port}")
puber.set_topic('a')
while True:
    try:
        puber.send_json({'123':123456})
    except InterruptedError:
        break



# 3 run sublisher, another process to run:
from message_lib import Subscriber

subcriber = Subscriber(f"tcp://{proxy_host}:{out_proxy_port}")
subcriber.set_topic('a')
for i in range(100):            # receive 100 messages
    try:
        print(subcriber.rcv_json())
    except InterruptedError:
        break


# 4 run multi-sublisher, another process to run:
from message_lib import Subscriber

subcriber = Subscriber(f"tcp://{proxy_host}:{out_proxy_port}")
subcriber.set_topic('b')
for i in range(100):            # receive 100 messages
    try:
        print(subcriber.rcv_json())     # will not receive message because of different topic
    except InterruptedError:
        break
    