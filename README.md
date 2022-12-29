# 框架使用示例

### 服务端

```python
from zmq_lib import ZMQServer,BaseView,ClientBaseException,ServerBaseException
from zmq_lib import MTZMQServer      # 并发版的服务端
import time

# 定义你的异常
class NoPermission(ServerBaseException):
    Status:int = 502
    ErrorInfo:str = '无权访问此方法'


# 定义你的视图函数及路径
class MyView(BaseView):
    path = '/'      # 定义路径，缺省则为/ ，注:定义相同路径会覆盖视图函数

    '''定义视图函数(可以什么都不返回)'''
    def read(self,request):
        '''必须有request参数，否则会报错'''
        time.sleep(1)

    def control(self,request):
        raise NoPermission
    def is_connected(self,request):
        return True


class MyView2(BaseView):
    path = '/2'      # 定义路径，缺省则为/ ，注:定义相同路径会覆盖视图函数

    '''定义视图函数(可以什么都不返回)'''
    def read(self):
        time.sleep(1)

    def control(self):
        return None
    def is_connected(self):
        return True

if __name__ == '__main__':
    # 开启服务
    # server = ZMQServer(port=6780,views=MyView())    # 传递单个视图对象
    # server = MTZMQServer(port=6780,views=MyView())    # 并发版

    server = ZMQServer(port=6780,views=[
        MyView(),
        MyView2()
        ])      # 可以传递多个视图函数
    server.run()
```

### 客户端

```python
from zmq_lib import ZMQClient


if __name__ == '__main__':
    # zmq 服务客户端 发起请求
    # 使用方法
    res = ZMQClient(remote_host='localhost',port=6780).request(action='list_action')
    # 带参数的请求
    res = ZMQClient(remote_host='localhost',port=6780).request(action='read',rqargs={'arg1':123})

    # 一次客户端多次请求
    client = ZMQClient(remote_host='localhost',port=6780)

    res = client.request(action='is_connected',path='/')

    # 指定path
    res = client.request(action='is_connected',path='/12')
    # print(res)
```

| 对于并发版的服务端，可以使用并发测试

```python
def reqeust_test(i):
    res = ZMQClient(remote_host='localhost',port=6780).request(action='read')
    print(res)

if __name__ == '__main__':
import time
t0 = time.time()
from multiprocessing import Pool
with Pool(5) as mp_pool:
    mp_pool.map(reqeust_test,list(range(10)))
    # for re in results:
    #     print(re)
print(time.time()-t0)
```