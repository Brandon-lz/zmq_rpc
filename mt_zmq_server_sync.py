
# zmq 服务端代码
import zmq
import json
from datetime import datetime
from threading import Thread
from typing import List,Optional
from zmq.sugar.socket import Socket
from .exceptions import *
from .common import Request,BaseView

from logs import logger
# logger.basicConfig(format="%(levelname)s: %(message)s", level=logger.INFO)

class Response():
    def __init__(self,status:int=200,errorinfo='ok') -> None:
        self.Status:int=status
        self.ErrorInfo = errorinfo


class WorkerThread(Thread):
    def __init__(self, identity:int,views:list,worker_url:str,context,queue=None) -> None:
        super().__init__()
        self.identity = identity
        self.daemon = True
        self.path_view_map = self._register_views(views)
        self.worker_url = worker_url
        self.context = context
        # self.queue = queue
        
    def _register_views(self,views):
        '''注册路由及函数'''
        pvmap = {}
        for v in views:
            assert isinstance(v.path,str)
            # v.queue = self.queue            # 为每个视图函数添加消息队列，你可以做到更多
            if v.path in pvmap:
                logger.warning(f'重复的路径：{v.path}')
            pvmap.update({v.path:v})
        return pvmap

    
    def run(self):
        """ Worker using REQ socket to do LRU routing """
        socket:Socket = self.context.socket(zmq.REQ)

        # set worker identity
        socket.identity = (u"Worker-%d" % (self.identity)).encode('ascii')

        socket.connect(self.worker_url)

        # Tell the broker we are ready for work
        socket.send(b"READY")
        
        # 接收并返回结果
        try:
            while True:

                address, empty, request = socket.recv_multipart()
                # request:bytes

                try:
                    request = json.loads(request.decode('utf8'))
                except Exception as err:
                    logger.info("json.loads(request) ERROR: "+str(err))
                    socket.send_multipart([address, b'', str(err).encode('utf8')])     # response
                    continue
                # 访问日志 请求日志
                logger.info(f"{socket.identity.decode('ascii')}: request: {str(request)}" )
               
                # views
                response = self.run_views(request)
                
                 # 记录response
                if response.get('zmqsuccess'):
                    logger.info(f'{socket.identity} response:'+str(response))
                else:
                    logger.error(f'{socket.identity} response:'+str(response))
                    
                # logger.error(str(response))
                    
                response = json.dumps(response).encode('utf8')
                socket.send_multipart([address, b'', response])      # response

        except zmq.ContextTerminated:
            # context terminated so quit silently
            return
    
    def run_views(self,message)->dict:
        #  Wait for next request from client
        try:
            ret = self.router(message)
            
        # 服务端错误，自定义视图异常继承
        except ServerBaseException as e:
            error_json = ({'Status':e.Status,'ErrorInfo':e.ErrorInfo})    
            logger.error(f"response:  :{error_json}{e=} ]")
            return error_json

        # 客户端的错误
        except ClientBaseException as e:
            error_json = ({'Status':e.Status,'ErrorInfo':e.ErrorInfo})    
            logger.error(f"response:  :{error_json}{e=} ]")
            return error_json
            
        
        
        except AssertionError as err:
            error_json = {'Status':504,'ErrorInfo':'与plc设备通信异常，请重试'}
            logger.error(f"response:  :{error_json}{err=}")
            return error_json
        
      
        except Exception as err:
            # response = Response(500,f'发生了未知问题[{type(err)}:{err.__str__()}]')
            response = Response(500,f'发生了未知问题[{type(err)=}:{err=}]')
            return({'Status':500,'ErrorInfo':[err.__str__()]})    
            
        else:      # 200   不带'zmqsuccess'键的都是异常情况
            if isinstance(ret,dict):          # 删掉
                ret.update({'zmqsuccess':200})
                return(ret)
            else:
                return({'zmqsuccess':200,'response':ret})  

            # if response.Status<300:
            #     logger.info(f"response: {message['remote_ip']}/{message['action']} :{response.Status}")
            # else:
            #     logger.error(f"response: {message['remote_ip']}/{message['action']} :{response.Status} [ {response.ErrorInfo} ]")
        
        
    def router(self,message:dict):
        # 匹配路由
        try:
            view = self.path_view_map[message['path']]
        except KeyError:
            raise NoPathException(path=message['path'])
        return self.run_path(view,message)
    
    def run_path(self,view:BaseView,message:dict):
        '''DIP服务接口路由'''
        if not message.get('remote_ip',None):
            raise NoIPException
        if not message.get('action',None):
            raise NoActionException
    
        assert type(message['action']) is str
        try:
            view_func = getattr(view,message['action'])    
        except:
            raise NoActionFoundError
        try:
            return view_func(Request(**message))
        except TypeError:                                # 视图函数统一异常处理
            raise
            # raise ViewArgsException


NBR_CLIENTS = 20


class SyncMTZMQServer():
    def __init__(self,port:int=6789,*,views:Optional[List[BaseView]]=BaseView(),thread_num=5,queue=None) -> None:
        """同步多线程zmq请求响应式服务端

        Args:
            port (int, optional): 服务端口. Defaults to 6789.
            views (Optional[List[BaseView]], optional): 视图函数. Defaults to BaseView().
            thread_num (int, optional): 并发线程数量. Defaults to 5.
        """
        if isinstance(views,BaseView):
            views = [views]
        self._views = views
        self.queue = queue
        self.port = port
        self.thread_num = thread_num
        self.bind_url = f"tcp://*:{port}"


    def run(self,thread_num=None):
        logger.info(f'ZMQServer UP at port:{self.port} {datetime.now()}')
        logger.info(f'listening request from clients ...')
        
        NBR_WORKERS = thread_num or self.thread_num
        
        url_worker = "inproc://workers"
        # url_client = "tcp://127.0.0.1:5555"
        
        client_nbr = NBR_CLIENTS

        # Prepare our context and sockets
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind(self.bind_url)                 # 服务url
        backend = context.socket(zmq.ROUTER)
        backend.bind(url_worker)

        # create workers and clients threads
        for i in range(NBR_WORKERS):
            # thread = threading.Thread(target=worker_thread,
            #                         args=(url_worker, context, i, ))
            # thread.start()
            WorkerThread(i,views=self._views,worker_url=url_worker,context=context).start()
        
        # Queue of available workers
        available_workers = 0
        workers_list = []

        # init poller
        poller = zmq.Poller()

        # Always poll for worker activity on backend
        poller.register(backend, zmq.POLLIN)

        # Poll front-end only if we have available workers
        poller.register(frontend, zmq.POLLIN)

        while True:

            socks = dict(poller.poll())

            # Handle worker activity on backend
            if (backend in socks and socks[backend] == zmq.POLLIN):

                # Queue worker address for LRU routing
                message = backend.recv_multipart()
                assert available_workers < NBR_WORKERS

                worker_addr = message[0]

                # add worker back to the list of workers
                available_workers += 1
                workers_list.append(worker_addr)

                #   Second frame is empty
                empty = message[1]
                assert empty == b""

                # Third frame is READY or else a client reply address
                client_addr = message[2]

                # If client reply, send rest back to frontend
                if client_addr != b'READY':

                    # Following frame is empty
                    empty = message[3]
                    assert empty == b""

                    reply = message[4]

                    frontend.send_multipart([client_addr, b"", reply])

                    client_nbr -= 1

                    if client_nbr == 0:
                        # break  # Exit after N messages
                        # print(1111111111)
                        pass

            # poll on frontend only if workers are available
            if available_workers > 0:

                if (frontend in socks and socks[frontend] == zmq.POLLIN):
                    # Now get next client request, route to LRU worker
                    # Client request is [address][empty][request]

                    [client_addr, empty, request] = frontend.recv_multipart()

                    assert empty == b""

                    #  Dequeue and drop the next worker address
                    available_workers += -1
                    worker_id = workers_list.pop()

                    backend.send_multipart([worker_id, b"",
                                            client_addr, b"", request])
        
      


        # context = zmq.Context()
        # frontend = context.socket(zmq.ROUTER)
        
        # frontend.bind(self.bind_url)
        # backend = context.socket(zmq.ROUTER)
        # url_worker = "ipc://backend.ipc"
        # backend.bind(url_worker)
        
        # # create workers and clients threads
        # for i in range(NBR_WORKERS):
        #     WorkerThread(i,views=self._views,worker_url=url_worker).start()

        # # create queue with the sockets
        # queue = LRUQueue(backend, frontend,thread_num=NBR_WORKERS)
        
        # # import asyncio
        # # start reactor
        # # loop =  asyncio.new_event_loop()
        # # asyncio.set_event_loop(loop)
        
        # IOLoop.instance().start()




if __name__ == '__main__':
    # 服务端
    # 食用方法
    class DIPView(BaseView):
        path = '/'      # 定义路径，缺省则为/ ，注:定义相同路径会覆盖视图函数
    
        '''定义视图函数'''
        def read(self,request:Request):
            print(request.rqargs)
            # time.sleep(1)
            return
        def control(self,request):
            return None
        def is_connected(self,request):
            return True
        def errortest(self,request):
            """返回异常示例
            """
            from .exceptions import ServerBaseException
            class MyViewError(ServerBaseException):
                Status: int=555
                ErrorInfo: str = '自定义异常'
            raise MyViewError
            
        
    # 开启服务
    mtserver = SyncMTZMQServer(port=6781,views=DIPView())      # 可以传递多个视图函数
    mtserver.run()

