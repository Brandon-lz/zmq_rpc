'''
 * @Author: wl.liuzhao 
 * @Date: 2022-11-07 23:50:43 
 * @Last Modified by:   wl.liuzhao 
 * @Last Modified time: 2022-11-07 23:50:43 

'''


# zmq 服务端代码
import zmq
import json
from datetime import datetime
from threading import Thread
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
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



# # 定义zmq接口函数
# class BaseView():
#     path = '/'
#     def __init__(self) -> None:
#         assert type(self.path)==str
#         if self.path=='':
#             self.path = '/'
#     def list_action(self,request:Request):
#         ret_list = []
#         func_list =  self.__dir__()
#         for f in func_list:
#             if f[:1] != '_':
#                 ret_list.append(f)
#         return ret_list



class WorkerThread(Thread):
    def __init__(self, identity:int,views:list,worker_url:str,queue=None) -> None:
        super().__init__()
        self.identity = identity
        self.daemon = True
        self.path_view_map = self._register_views(views)
        self.worker_url = worker_url
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
        context = zmq.Context.instance()
        socket :Socket= context.socket(zmq.REQ)

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
                logger.info("%s: %s\n" % (socket.identity.decode('ascii'),
                                    str(request)))
               
                # views
                response = self.run_views(request)
                # 记录返回结果
                if response.get('zmqsuccess'):
                    logger.info(str(response))
                else:
                    logger.error(str(response))
                                
                response = json.dumps(response).encode('utf8')
                socket.send_multipart([address, b'', response])     # response

        except zmq.ContextTerminated:
            # context terminated so quit silently
            return
    
    def run_views(self,message) -> dict:
        #  Wait for next request from client
        try:
            ret = self.router(message)
            # response = Response()
            
        # 服务端错误，自定义视图异常继承
        except ServerBaseException as e:
            return({'Status':e.Status,'ErrorInfo':e.ErrorInfo})    
            # response = Response(e.Status,e.ErrorInfo)
            # logger.error(f"response:  :{response.Status} [ {response.ErrorInfo} ]")

        # 客户端的错误
        except ClientBaseException as e:
            return({'Status':e.Status,'ErrorInfo':e.ErrorInfo})    
            # response = Response(e.Status,e.ErrorInfo)
            # logger.error(f"response:  :{response.Status} [ {response.ErrorInfo} ]")
        
        
        except AssertionError as err:
            # response = Response(504,'与plc设备通信异常，请重试')
            # raise
            return({'Status':response.Status,'ErrorInfo':response.ErrorInfo})    
            logger.error(f"response:  :{response.Status} [ {response.ErrorInfo} ]")
        
        # except AttributeError as e:
        #     response = Response(400,f'未定义的视图函数({message["action"]})')
        #     return({'Error':response.Status,'ErrorInfo':response.ErrorInfo})  
        
        except Exception as err:
            # response = Response(500,f'发生了未知问题[{type(err)}:{err.__str__()}]')
            response = Response(500,f'发生了未知问题[{type(err)=}:{err=}]')
            return({'Status':500,'ErrorInfo':[err.__str__()]})    
            
        else:      # 200   不带'zmqsuccess'键的都是异常情况
            if isinstance(ret,dict):          # 删掉
                ret.update({'zmqsuccess':200})
                return(ret)
            else:
                return({'zmqsuccess':200,'response':ret})   # 应该只要这个

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


class LRUQueue(object):
    """LRUQueue class using ZMQStream/IOLoop for event dispatching"""

    def __init__(self, backend_socket, frontend_socket, thread_num):
        self.thread_num = thread_num
        self.available_workers = 0
        self.is_workers_ready = False
        self.workers = []
        self.client_nbr = NBR_CLIENTS

        self.backend = ZMQStream(backend_socket)
        self.frontend = ZMQStream(frontend_socket)
        self.backend.on_recv(self.handle_backend)

        self.loop = IOLoop.instance()

    def handle_backend(self, msg):
        # Queue worker address for LRU routing
        worker_addr, empty, client_addr = msg[:3]

        # assert self.available_workers < NBR_WORKERS
        assert self.available_workers < self.thread_num

        # add worker back to the list of workers
        self.available_workers += 1
        self.is_workers_ready = True
        self.workers.append(worker_addr)

        #   Second frame is empty
        assert empty == b""

        # Third frame is READY or else a client reply address
        # If client reply, send rest back to frontend
        if client_addr != b"READY":
            empty, reply = msg[3:]

            # Following frame is empty
            assert empty == b""

            self.frontend.send_multipart([client_addr, b'', reply])

            self.client_nbr -= 1

            if self.client_nbr == 0:
                # Exit after N messages
                # self.loop.add_timeout(time.time() + 1, self.loop.stop)
                # self.loop.add_timeout(time.time() + 1, callbackfunc)
                pass

        if self.is_workers_ready:
            # when atleast 1 worker is ready, start accepting frontend messages
            # print('ready')
            self.frontend.on_recv(self.handle_frontend)

    def handle_frontend(self, msg):
        # Now get next client request, route to LRU worker
        # Client request is [address][empty][request]
        client_addr, empty, request = msg

        assert empty == b""

        #  Dequeue and drop the next worker address
        self.available_workers -= 1
        worker_id = self.workers.pop()

        self.backend.send_multipart([worker_id, b'', client_addr, b'', request])
        if self.available_workers == 0:
            # stop receiving until workers become available again
            self.is_workers_ready = False
            self.frontend.stop_on_recv()



class MTZMQServer():
    def __init__(self,port:int=6789,*,views:Optional[List[BaseView]]=BaseView(),thread_num=5,queue=None) -> None:
        if isinstance(views,BaseView):
            views = [views]
        self._views = views
        self.queue = queue
        self.port = port
        self.thread_num = thread_num
        self.bind_url = f"tcp://*:{port}"


    def run(self,thread_num=None):
        
        NBR_WORKERS = thread_num or self.thread_num
        
        logger.info(f'ZMQServer UP at port:{self.port} {datetime.now()}')
        logger.info(f'listening request from clients ...')


        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        
        frontend.bind(self.bind_url)
        backend = context.socket(zmq.ROUTER)
        url_worker = "ipc://backend.ipc"
        backend.bind(url_worker)
        
        # create workers and clients threads
        for i in range(NBR_WORKERS):
            WorkerThread(i,views=self._views,worker_url=url_worker).start()

        # create queue with the sockets
        queue = LRUQueue(backend, frontend,thread_num=NBR_WORKERS)
        
        # import asyncio
        # start reactor
        # loop =  asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        
        IOLoop.instance().start()




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
    mtserver = MTZMQServer(port=6781,views=DIPView())      # 可以传递多个视图函数
    mtserver.run()

