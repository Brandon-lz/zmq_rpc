from pydantic import BaseModel,Field

class Request(BaseModel):
    remote_ip:str
    path:str = Field(default='/',description='视图路径')
    action:str = Field(description='视图方法名称')
    rqargs:dict = Field(default={},description='请求中附带的参数，可以理解为body')



# 定义zmq接口函数
class BaseView():
    path = '/'
    def __init__(self) -> None:
        assert type(self.path)==str
        if self.path=='':
            self.path = '/'
    def list_action(self,request:Request):
        ret_list = []
        func_list =  self.__dir__()
        for f in func_list:
            if f[:1] != '_':
                ret_list.append(f)
        return ret_list
