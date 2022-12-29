
# zmq 服务端代码
import zmq,time
from datetime import datetime
from typing import List,Optional
from .exceptions import *
from .common import Request,BaseView
from logs import logger
# logger.basicConfig(format="%(levelname)s: %(message)s", level=logger.INFO)


class Response():
    def __init__(self,status:int=200,errorinfo='ok') -> None:
        self.Status:int=status
        self.ErrorInfo = errorinfo



class ZMQServer():
    def __init__(self,port:int=6789,*,views:Optional[List[BaseView]]=BaseView(),queue=None) -> None:
        """zmq单线程服务端，不支持并发，所以视图函数中不需要考虑线程锁的问题
        

        Args:
            port (int, optional): _description_. Defaults to 6789.
            views (Optional[List[BaseView]], optional): _description_. Defaults to BaseView().
            queue (_type_, optional): _description_. Defaults to None.
        """
        if isinstance(views,BaseView):
            views = [views]
        self._views = views
        self.queue = queue
        self.path_view_map = self._register_views()
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(f"tcp://0.0.0.0:{port}")
        # self.custom_excepts = tuple()
        
    def _register_views(self):
        '''注册路由及函数'''
        pvmap = {}
        for v in self._views:
            assert isinstance(v.path,str)
            # v.queue = self.queue            # 为每个视图函数添加消息队列，你可以做到更多
            if v.path in pvmap:
                logger.warning(f'重复的路径：{v.path}')
            pvmap.update({v.path:v})
        return pvmap


    def run(self):
        logger.info(f'ZMQServer UP at port:{self.port} {datetime.now()}')
        logger.info(f'listening request from clients ...')

        try:
            self._run()
        except KeyboardInterrupt:
            self.socket.close()
            logger.info(f'ZMQServer DOWN at {self.port} {datetime.now()}')
            return


    def _run(self):
        while True:
            #  Wait for next request from client
            try:
                message = self.socket.recv_json()
            except KeyboardInterrupt:
                self.socket.close()
                logger.info(f'ZMQServer DOWN at {self.port} {datetime.now()}')
                return
            try:
                ret = self.router(message)
                response = Response()
                
            # 服务端错误，自定义视图异常继承
            except ServerBaseException as e:
                self.socket.send_json({'Status':e.Status,'ErrorInfo':e.ErrorInfo})    
                response = Response(e.Status,e.ErrorInfo)
                logger.error(f"response:  :{response.Status} [ {response.ErrorInfo} ]")
                continue

            # 客户端的错误
            except ClientBaseException as e:
                self.socket.send_json({'Status':e.Status,'ErrorInfo':e.ErrorInfo})    
                response = Response(e.Status,e.ErrorInfo)
                logger.error(f"response:  :{response.Status} [ {response.ErrorInfo} ]")
                continue
            
            
            except AssertionError as err:
                response = Response(504,'与plc设备通信异常，请重试')
                raise
                self.socket.send_json({'Status':response.Status,'ErrorInfo':response.ErrorInfo})    
                logger.error(f"response:  :{response.Status} [ {response.ErrorInfo} ]")
                continue

            
            # except AttributeError as e:
            #     response = Response(400,f'未定义的视图函数({message["action"]})')
            #     self.socket.send_json({'Error':response.Status,'ErrorInfo':response.ErrorInfo})  
            
            except Exception as err:
                # response = Response(500,f'发生了未知问题[{type(err)}:{err.__str__()}]')
                response = Response(500,f'发生了未知问题[{type(err)=}:{err=}]')
                self.socket.send_json({'Status':500,'ErrorInfo':[err.__str__()]})    
                
            else:      # 200
                if isinstance(ret,dict):
                    ret.update({'zmqsuccess':200})
                    self.socket.send_json(ret)
                else:
                    self.socket.send_json({'zmqsuccess':200,'response':ret})

            if response.Status<300:
                logger.info(f"response: {message['remote_ip']}/{message['action']} :{response.Status}")
            else:
                logger.error(f"response: {message['remote_ip']}/{message['action']} :{response.Status} [ {response.ErrorInfo} ]")


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



if __name__ == '__main__':
    # 服务端
    # 食用方法
    class DIPView(BaseView):
        path = '/'      # 定义路径，缺省则为/ ，注:定义相同路径会覆盖视图函数
    
        '''定义视图函数'''
        def read(self,request:Request):
            print(request.rqargs)
            time.sleep(1)
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
    server = ZMQServer(port=6780,views=DIPView())      # 可以传递多个视图函数
    server.run()

