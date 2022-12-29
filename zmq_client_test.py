'''
 * @Author: wl.liuzhao 
 * @Date: 2022-11-11 16:09:14 
 * @Last Modified by:   wl.liuzhao 
 * @Last Modified time: 2022-11-11 16:09:14 
 * 框架测试脚本
'''

import zmq
import socket
# from logs import logger
from exceptions import ServerBaseException
from common import Request


class ResponseException(Exception):
    def __init__(self, *args: object,status,errorinfo) -> None:
        super().__init__(*args)

        self.Status:int = status
        self.ErrorInfo:str = errorinfo
    
    def __str__(self) -> str:
        return f'Error: {self.Status} {self.ErrorInfo}'


class NoResponseExcetion(Exception):
    '''服务端无回应，可能是网络错误'''
    def __init__(self, remote_host:str) -> None:
        self.remote_host = remote_host
    def __str__(self) -> str:
        return f'NoResponseExcetion:DIP服务{self.remote_host}在超时时间内无回应，可能是网络错误'


class ReplyError(ServerBaseException):
    Status:int = 507
    ErrorInfo:str = '服务器返回了一个错误'
    
    def __init__(self, response) -> None:
        print((response))
        self.Status = response['Status']
        self.ErrorInfo = response['ErrorInfo']
        self.response = response
    
    def __str__(self) -> str:
        return super().__str__() + f'response ：{self.response}'


class ZMQClient():
    def __init__(self,remote_host:str='localhost',port:int=6780,retry_times=1,REQUEST_TIMEOUT=10000,
    REQUEST_RETRIES=3) -> None:
        """zmq请求客户端

        Args:
            remote_host (str, optional): _description_. Defaults to 'localhost'.
            port (int, optional): _description_. Defaults to 6780.
            retry_times (int, optional): _description_. Defaults to 1.一般不用
            REQUEST_TIMEOUT (int, optional): _description_. Defaults to 10000 默认是10s
            REQUEST_RETRIES (int, optional): _description_. Defaults to 3. 请求重试3次
        """
        '''
        args:
        retry_times:连接失败后重试的次数
        REQUEST_RETRIES:每次请求最大尝试次数
        REQUEST_TIMEOUT:每次请求timeout    /ms
        '''

        self.port = port
        self.remote_host = remote_host
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # 获取本机ip
        self.local_ip:str = socket.gethostbyname(hostname)

        self.retry_times = retry_times
        self.REQUEST_TIMEOUT = REQUEST_TIMEOUT
        self.REQUEST_RETRIES = REQUEST_RETRIES
        self.SERVER_ENDPOINT = f"tcp://{remote_host}:{port}"

        self.context = zmq.Context()

        # Connecting to server
        self.client:zmq.sugar.socket.Socket = self.context.socket(zmq.REQ)
        self.client.connect(self.SERVER_ENDPOINT)
        self.path = '/'

    def set_path(self,path:str='/'):
        self.path = path
    
    def close(self):
        try:
            self.client.close()
        except:
            pass
    
    def request(self,action:str,path=None,rqargs:dict={}):
        '''
        params:
        action:请求动作，视图函数名
        path:路径
        rqargs:请求参数 格式 {"p1":1,"p2":example}，可以嵌套
        '''
        path = path if path else self.path
        request = {          # 优化，这个地方建议使用pydantic重写
            'remote_ip':self.local_ip,
            'path': path,
            'action':action,
            'rqargs':rqargs
            }
        request = Request(**request)
        # print(request)

        try:
            return self._request(request)
        except:
            raise

    def _request(self,request:Request):
        request = request.dict()
        for _ in range(self.retry_times):
            print("zmq: Sending (%s)", request)
            ret = self.client.send_json(request)

            retries_left = self.REQUEST_RETRIES
            while True:
                if (self.client.poll(self.REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                    reply = self.client.recv_json()
                    if reply.get('zmqsuccess',None) :          # 服务端返回了正确的内容
                        print(f"zmq:Server replied OK ({reply})")
                        retries_left = self.REQUEST_RETRIES
                        return reply
                    else:                       # 服务端返回了预期之外的内容(一般是客户端的问题)
                        # deal the fault
                        print(f"zmq: 服务端返回了一个错误: {reply}")
        
                        raise ReplyError(response=reply)
                        

                retries_left -= 1
                print("zmq: No response from server")
                # Socket is confused. Close and remove it.
                self.client.setsockopt(zmq.LINGER, 0)
                self.client.close()
                if retries_left == 0:
                    print("zmq: Server seems to be offline, abandoning")
                    raise NoResponseExcetion(remote_host=self.remote_host)
                    # sys.exit()       
                print("zmq: Reconnecting to server…")
                # Create new connection
                self.client :zmq.sugar.socket.Socket= self.context.socket(zmq.REQ)
                self.client.connect(self.SERVER_ENDPOINT)
                print(f"zmq: Resending ({request})")
                self.client.send_json(request)
                
import random
def reqeust_test(i):
    send_args = {"me":f'{random.randint(100,999)}'}
    res = ZMQClient(remote_host='localhost',port=6780).request(action='xingnnegtest',rqargs=send_args)
    print(send_args,res)
    # assert send_args['me']==res['me']
    
    
    

def reqeust_test2(i):
    # send_args = {"me":f'{random.randint(100,999)}'}
    print('send request')
    res = ZMQClient(remote_host='localhost',port=6780).request(action='plc_value_test',rqargs={123:'123'})
    print('response:',res)

def reqeust_test3(i):
    # send_args = {"me":f'{random.randint(100,999)}'}
    print('send request')
    res = ZMQClient(remote_host='localhost',port=6780).request(action='plc_xingnnegtest2',rqargs={'index':i})
    print('response:',res)


def reqeust_test4(i):
    print('send request')
    res = ZMQClient(remote_host='localhost',port=6780).request(action='plc_value_test',rqargs={'index':i})

def reqeust_test5(i):
    print('send request')
    res = ZMQClient(remote_host='localhost',port=6780).request(action='test')

def bingfa_test(i):
    import snap7
    
    client = snap7.client.Client()

    client.connect('192.168.111.1',0,0)

    print(client.get_connected())
    print(f'{i} # connect')
    # client.destroy()     # 彻底删除客户端对象
    # client.disconnect()

    print(client.ab_read(0,size=4))   # 
    # db62_data = client.db_read(62,start=0,size=20)
    # print


if __name__ == '__main__':
    # zmq 服务客户端 发起请求
    # 使用方法
    
    # 列出所有的方法
    # res = ZMQClient(remote_host='localhost',port=6780).request(action='list_action')
    
   
    # # 带参数的请求
    # res = ZMQClient(remote_host='localhost',port=6780).request(action='read',rqargs={'arg1':123})

    # # 一次客户端多次请求
    # client = ZMQClient(remote_host='localhost',port=6780)

    # res = client.request(action='is_connected',path='/')

    # # 指定path
    # res = client.request(action='is_connected',path='/to-path')
    # # print(res)
    
    # # 异常处理
    # try:
    #     res = client.request(action='error_test')
    # except ReplyError as e:     # 服务端返回了一条异常
    #     raise
    # except NoResponseExcetion as e:      # 服务端超时无响应
    #     raise
    import time
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(7) as mp_pool:
        mp_pool.map(reqeust_test,list(range(7)))
        # mp_pool.map(bingfa_test,list(range(5)))
        # for re in results:
        #     print(re)
    print(time.time()-t0)
    
    