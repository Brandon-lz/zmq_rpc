
class ClientBaseException(Exception):
    Status:int = 401
    ErrorInfo:str = ''
    
    def __str__(self) -> str:
        return f'Error: {self.Status} {self.ErrorInfo}'

class ServerBaseException(ClientBaseException):
    Status:int = 500
    ErrorInfo:str = '服务端错误'
    
    def __str__(self) -> str:
        return f'Error: {self.Status} {self.ErrorInfo}'
    



# 在这里定义你的异常处理
class NoIPException(ClientBaseException):
    Status:int = 401
    ErrorInfo:str = '客户端未指定IP地址'
    

class NoActionException(ClientBaseException):
    Status:int = 401
    ErrorInfo:str = '客户端未指定请求action'


class NoActionFoundError(ClientBaseException):
    Status:int = 401
    ErrorInfo:str = '未找到请求action'


class NoPathException(ClientBaseException):
    Status:int = 401
    ErrorInfo:str = '没有这样的路径'
    def __init__(self, path:str,*args: object) -> None:
        super().__init__(*args)
        self.ErrorInfo += f'({path})'


class ViewArgsException(ServerBaseException):
    Status:int = 501
    ErrorInfo:str = '视图函数参数错误'

