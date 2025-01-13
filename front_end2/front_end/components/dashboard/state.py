import reflex as rx
import asyncio

import math
import numpy as np

def included_angle(a, b)->float:
    a_norm = np.sqrt(np.sum(a * a))
    b_norm = np.sqrt(np.sum(b * b))
    cos_value = np.dot(a, b) / (a_norm * b_norm)
    arc_value = np.arccos(cos_value)
    # angle_value = arc_value * 180 / np.pi   # 不要用计算公式转换弧度角度，误差有点大
    angle_value=math.degrees(arc_value)
    return angle_value

class DashboardState(rx.State):
    count:float=50.0
    runing:bool=False

    radius:float=10.0
    scope_min:float = 0.0
    scope_max:float = 100.0
    degree:float = 90.0


    @rx.background
    async def add_count(self):
        # 初始化逻辑必须写在这里面
        async with self:
            # only allow 1 concurrent task
            if self.runing:
                return
            print("start--------------")

            # State mutation is only allowed inside context block
            self.runing = True

        # 后台任务
        while True:
            async with self:
                # Check for stopping conditions inside context
                if not self.runing: 
                    return
                if self.count>=self.scope_max:
                    self.count=self.scope_max
                    return

                self.count += 1

            # Await long operations outside the context to avoid blocking UI
            await asyncio.sleep(0.01)

    @rx.background
    async def sub_count(self):
        # 初始化逻辑必须写在这里面
        async with self:
            # only allow 1 concurrent task
            if self.runing:
                return
            print("start--------------")

            # State mutation is only allowed inside context block
            self.runing = True

        # 后台任务
        while True:
            async with self:
                # Check for stopping conditions inside context
                if not self.runing:
                    return
                if self.count<=self.scope_min:
                    self.count=self.scope_min
                    return

                self.count -= 1

            # Await long operations outside the context to avoid blocking UI
            await asyncio.sleep(0.01)


    def stop_add_count(self):
        print("end--------------")
        self.runing = False

    @rx.var
    def board_num(self):
        return f"{self.count} N•m"

    def pin_angle(self)->float:
        
        self.calcu()
        point = (self.radius*math.cos(math.radians(180-self.degree)),self.radius*math.sin(math.radians(180-self.degree))-0.3*self.radius)

        x=np.array((point[0],point[1]))
        y=np.array((-self.radius,0.0))
        res = included_angle(x,y)
        if x[1]<0:
            res = -res
        return res
    
    def calcu(self)->float:
        if self.count>self.scope_max or self.count<self.scope_min:
            return
        self.degree = self.count/((self.scope_max-self.scope_min)/180)
        return self.degree
    
    @rx.var
    def color(self)->str:
        return f'''conic-gradient(#60e8fc {self.degree}deg,#072d5b {self.degree}deg ,#072d5b 185deg, #60e8fc 185deg);'''
    
    @rx.var
    def pin_angle_sytle(self)->float:
        return f"rotate({self.pin_angle()-90}deg)"

