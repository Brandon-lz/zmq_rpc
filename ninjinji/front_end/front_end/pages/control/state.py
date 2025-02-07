from .ws import send_ws_json, get_heart_beat_ws, get_jog_add_ws, get_jog_sub_ws
from front_end.state import AppState
import reflex as rx
import asyncio
import json
import httpx
import time
import requests


import math
import numpy as np

with open("config.json") as f:
    config = json.load(f)

CONTROL_STOP_SIGN = {"value": False}

from threading import Lock

update_value_lock = Lock()
update_value_running = {"running": False, "time": 0.0}

send_heart_beat_lock = Lock()
send_heart_beat_running = {"running": False, "time": 0.0}

update_torque_lock = Lock()
update_torque_running = {"running": False, "time": 0.0}


set_torque_lock = {"running": False}


class SlidersState(rx.State):
    torque: float = 0.7
    first:bool = True

    @rx.var(cache=True)
    def get_torque(self) -> list[float]:
        if self.first:
            self.init_torque()
            self.first = False
        return [self.torque]

    def init_torque(self):
        try:
            res = requests.get(
                f"http://{config['opcua-middleware']}/getvalue/aim_torque",
                headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
            )
            res.raise_for_status()
            self.torque = float(res.json()["value"])
        except Exception as e:
            print(f"Error getting torque: {e}")

    @rx.event
    async def set_torque(self, value: list):
        set_torque_lock['running'] = True
        try:
            async with httpx.AsyncClient() as aclient:
                res = await aclient.put(
                    f"http://{config['opcua-middleware']}/set-torque",
                    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
                    json={
                        "aim_torque": {
                            "torque": float(value[0]),
                        }
                    },
                )
                res.raise_for_status()
            await self.init_torque()
        except Exception as e:
            print(f"Error setting torque: {e}")
        set_torque_lock["running"] = False


class ControlState(rx.State):
    plc_ok :bool = False
    _value: int = 0
    _n_tasks: int = 0
    _n_tasks_heart_beat: int = 0

    def _stop_update_value(self):
        with update_value_lock:
            if (
                update_value_running["running"]
                and time.time() - update_value_running["time"] < 2.0
            ):  # to fix unmount bug
                return
            update_value_running["running"] = False
        print("Stopping update_value...")
        self._n_tasks = 0

    @rx.event(background=True)
    async def update_heartbeat_value(self):
        async with self:  # 这是一个锁，不要在这里面sleep
            with update_value_lock:
                update_value_running["time"] = time.time()
                if update_value_running["running"]:
                    return
                update_value_running["running"] = True

            if self._n_tasks > 0:
                return
            self._n_tasks += 1

        while True:
            if self._n_tasks == 0:
                break
            try:
                res = None
                async with httpx.AsyncClient() as aclient:
                    res = await aclient.get(
                        f"http://{config['opcua-middleware']}/getvalue/heartbeat",
                        headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
                    )
                    res.raise_for_status()
                async with self:
                    self._value = int(res.json()["value"])
                    self.plc_ok = True
                    print(f"ControlState: {self._value}")
            except Exception as e:
                async with self:
                    self._value = -1
                    self.plc_ok = False
                print(f"ControlState: Error getting heartbeat value: {e}")
                print(self.plc_ok)

            await asyncio.sleep(1)

    
    @rx.event
    def changeplc_ok(self):
        self.plc_ok = not (self.plc_ok)

    @rx.event(background=True)
    async def send_heart_beat(self):
        async with self:  # 这是一个锁，不要在这里面sleep
            with send_heart_beat_lock:
                send_heart_beat_running["time"] = time.time()
                if send_heart_beat_running["running"]:
                    return
                send_heart_beat_running["running"] = True

        async with self:
            if self._n_tasks_heart_beat > 0:
                return
            self._n_tasks_heart_beat += 1
        try:
            ws = get_heart_beat_ws()
        except:
            pass

        while True:
            if self._n_tasks_heart_beat == 0:
                try:
                    ws.close()
                except:
                    pass
                break
            error = False
            try:
                send_ws_json(ws, {"type": "heartbeat"})
            except Exception as e:
                error = True
                print(f"Error sending 'heartbeat'，retry: {e}")

            if error:
                try:
                    ws = get_heart_beat_ws()
                except:
                    print("重连失败")

            print("Sending 'heartbeat'...")

            await asyncio.sleep(1)

    def _stop_send_heart_beat(self):
        with send_heart_beat_lock:
            if (
                send_heart_beat_running["running"]
                and time.time() - send_heart_beat_running["time"] < 2.0
            ):  # to fix unmount bug
                return
            send_heart_beat_running["running"] = False
        print("Stopping stop_send_heart_beat...")
        self._n_tasks_heart_beat = 0

    @rx.event
    async def quit_page(self):
        self._stop_send_heart_beat()
        self._stop_update_value()
        controldashboardstate:ControlDashboardState = await self.get_state(ControlDashboardState)
        controldashboardstate.stop_update()


def included_angle(a, b) -> float:
    a_norm = np.sqrt(np.sum(a * a))
    b_norm = np.sqrt(np.sum(b * b))
    cos_value = np.dot(a, b) / (a_norm * b_norm)
    arc_value = np.arccos(cos_value)
    # angle_value = arc_value * 180 / np.pi   # 不要用计算公式转换弧度角度，误差有点大
    angle_value = math.degrees(arc_value)
    return angle_value


class ControlDashboardState(rx.State):
    actual_torque: float = 0.0
    _couts: list = [1.0, 1.0, 1.0, 1.0, 1.0]
    _runing: bool = False

    radius: float = 10.0
    scope_min: float = 0.0
    scope_max: float = 100.0
    degree: float = 90.0

    # def set_degree(self, value: int):
    #     self.degree = value[0]

    _n_tasks: int = 0


    def stop_update(self):
        with update_torque_lock:
            if (
                update_torque_running["running"]
                and time.time() - update_torque_running["time"] < 2.0
            ):  # to fix unmount bug
                return
            update_torque_running["running"] = False
        print("Stopping update_value...")
        self._n_tasks = 0

    @rx.event(background=True)
    async def update_torque(self):
        async with self:  # 这是一个锁，不要在这里面sleep
            with update_torque_lock:
                update_torque_running["time"] = time.time()
                if update_torque_running["running"]:
                    return
                update_torque_running["running"] = True

            if self._n_tasks > 0:
                return
            self._n_tasks += 1

        while True:
            if self._n_tasks == 0:
                break
            try:
                res = None
                aim_torque_res = None
                async with httpx.AsyncClient() as aclient:
                    res = await aclient.get(
                        f"http://{config['opcua-middleware']}/getvalue/torque_value",
                        headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
                    )
                    res.raise_for_status()
                async with self:
                    # self.actual_torque = float(res.json()["value"]) + 1.0
                    self.actual_torque = float(res.json()["value"])
                    self._couts.append(self.actual_torque)
                    self._couts.pop(0)
                    self.actual_torque = sum(self._couts) / len(self._couts)
                    # print(f"ControlState: {self.count}")
                async with httpx.AsyncClient() as aclient:
                    aim_torque_res = await aclient.get(
                        f"http://{config['opcua-middleware']}/getvalue/aim_torque",
                        headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
                    )
                    aim_torque_res.raise_for_status()
                if not set_torque_lock['running']:
                    async with self:
                        siliderstate:SlidersState = await self.get_state(SlidersState)
                        siliderstate.torque = float(aim_torque_res.json()["value"])
            except Exception as e:
                async with self:
                    self.actual_torque = -1.0
                print(f"ControlState: Error getting torque_value value: {e}")

            await asyncio.sleep(0.2)

    @rx.event(background=True)
    async def add_count(self):
        # 初始化逻辑必须写在这里面
        async with self:
            # only allow 1 concurrent task
            if self._runing:
                return
            print("start--------------")

            # State mutation is only allowed inside context block
            self._runing = True

        # 后台任务
        while True:
            async with self:
                # Check for stopping conditions inside context
                if not self._runing:
                    return
                if self.actual_torque >= self.scope_max:
                    self.actual_torque = self.scope_max
                    self._runing = False
                    return

                self.actual_torque += 1

            # Await long operations outside the context to avoid blocking UI
            await asyncio.sleep(0.01)

    @rx.event(background=True)
    async def sub_count(self):
        # 初始化逻辑必须写在这里面
        async with self:
            # only allow 1 concurrent task
            if self._runing:
                return
            print("start--------------")

            # State mutation is only allowed inside context block
            self._runing = True

        # 后台任务
        while True:
            async with self:
                # Check for stopping conditions inside context
                if not self._runing:
                    return
                if self.actual_torque <= self.scope_min:
                    self.actual_torque = self.scope_min
                    self._runing = False
                    return

                self.actual_torque -= 1

            # Await long operations outside the context to avoid blocking UI
            await asyncio.sleep(0.01)

    def stop_add_count(self):
        print("end--------------")
        self._runing = False

    @rx.var(cache=False)
    def board_num(self)->str:
        return f"{self.actual_torque:.2f} N•m"

    def pin_angle(self) -> float:

        self.calcu()
        point = (
            self.radius * math.cos(math.radians(180 - self.degree)),
            self.radius * math.sin(math.radians(180 - self.degree)) - 0.3 * self.radius,
        )

        x = np.array((point[0], point[1]))
        y = np.array((-self.radius, 0.0))
        res = included_angle(x, y)
        if x[1] < 0:
            res = -res
        return res

    def calcu(self) -> float:
        if self.actual_torque > self.scope_max or self.actual_torque < self.scope_min:
            return
        self.degree = self.actual_torque / ((self.scope_max - self.scope_min) / 180)
        return self.degree

    @rx.var(cache=False)
    def color(self) -> str:
        return f"""conic-gradient(#60e8fc {self.degree}deg,#072d5b {self.degree}deg ,#072d5b 185deg, #60e8fc 185deg);"""

    @rx.var(cache=False)
    def pin_angle_sytle(self) -> str:
        return f"rotate({self.pin_angle()-90}deg)"


import functools
from front_end.models import add_operator_log

add_control_log = functools.partial(add_operator_log, operation_type="control")


class StartButtonState(rx.State):
    width = 3
    height = 3
    pressed: bool = False

    # start_button_text: str = "start"

    process_max: float = 100
    process_min: float = 0
    process_count: float = process_min
    _runing = False

    @rx.var(cache=True)
    def start_button_text(self) -> str:
        if self._runing:
            return (
                "拧紧中 "
                + str(
                    self.process_count * 100.0 / (self.process_max - self.process_min)
                )
                + "%"
            )
        else:
            if self.pressed:
                return "完成"
            return "开始"

    # @rx.var(cache=False)
    # def button_width(self)->str:
    #     return f"{self.width}em"

    # @rx.var(cache=False)
    # def button_height(self)->str:
    #     return f"{self.height}em"

    @rx.var(cache=False)
    def animation_background(self)->str:
        persent = self.process_count / (self.process_max - self.process_min) * 1.5
        # if persent>=0.7:
        # persent = persent+(persent-persent*0.7)*1.5
        return f"linear-gradient(90deg, #a6fc06 0%, rgba(79, 209, 197, 1) {persent*100.0}%);"

    @rx.event(background=True)
    async def on_click(self):
        # 初始化逻辑必须写在这里面
        async with self:

            # only allow 1 concurrent task
            if self._runing:
                return

            # self._click()
            self.pressed = not self.pressed

            if not self.pressed:
                self.process_count = self.process_min
                return

            # State mutation is only allowed inside context block
            self._runing = True
            print("start--------------")
        async with self:
            appstate: AppState = await self.get_state(AppState)
            worker = appstate.get_user()
            add_control_log(
                worker_name=worker.name,
                worker_id=worker.worker_id,
                class_group=worker.class_group,
                operation_content="开始拧紧",
                operation_result="success",
            )

            async with httpx.AsyncClient() as aclient:
                res = await aclient.put(
                    f"http://{config['opcua-middleware']}/torque-start",
                )
                res.raise_for_status()

        # 后台任务
        while True:
            async with self:
                # Check for stopping conditions inside context
                if not self._runing or self.process_count >= self.process_max:
                    self.start_button_text = "完成"
                    self._runing = False
                    return

                self.process_count += 1
                # self.start_button_text = (
                #     "running "
                #     + str(
                #         self.process_count
                #         * 100.0
                #         / (self.process_max - self.process_min)
                #     )
                #     + "%"
                # )

                # Await long operations outside the context to avoid blocking UI
            await asyncio.sleep(0.02)

    def _click(self):
        if self.pressed:
            self.start_button_text = "进行中"
        else:
            self.start_button_text = "开始"
            self.process_count = self.process_min


class StopButtonState(rx.State):
    _running = False
    button_text: str = "停止"

    @rx.var(cache=True)
    def backgroup_color(self) -> str:
        if not self._running:
            return "#ff3300"
        else:
            return "#ffc0b0"

    @rx.event(background=True)
    async def on_click(self):
        print("click stop-")

        # if self._running:
        #     return
        async with self:
            startstate: StartButtonState = await self.get_state(StartButtonState)
            startstate.start_button_text = "完成"
            startstate._runing = False
            # self._running = True

        async with httpx.AsyncClient() as aclient:
            res = await aclient.put(
                f"http://{config['opcua-middleware']}/torque-stop",
            )
            res.raise_for_status()

        await asyncio.sleep(0.5)
        # async with self:
        #     self._running = False


class JogAddButtonState(rx.State):
    _process_max: float = 100
    _process_min: float = 0
    _process_count: float = _process_min
    _running = False
    button_text: str = "点动+"

    @rx.event(background=True)
    async def on_pressed(self):
        async with self:
            if self._running:
                return
            self._running = True

        print("222222222222222222jog add on_pressed")
        async with self:
            self._process_count = 0
        ws = get_jog_add_ws()
        ws.send("add")
        while True:
            async with self:
                print(self._running)
                if not self._running:
                    self._process_count = 0
                    ws.send("exit")
                    ws.close()
                    return
                self._process_count += 10
                if self._process_count > 100:
                    self._process_count = 0
            await asyncio.sleep(0.1)

    def on_unpressed(self):
        print("111111111111111111111jog add on_unpressed-")
        self._running = False

    @rx.var(cache=True)
    def animation_background(self)->str:
        if self._running:
            return (
                f"linear-gradient(90deg, #a6fc06 0%, #e7dbca {self._process_count}%);"
            )
        else:
            return "#e7dbca"


class JogSubButtonState(rx.State):
    _process_max: float = 100
    _process_min: float = 0
    _process_count: float = _process_min
    _running = False
    button_text: str = "点动-"

    @rx.event(background=True)
    async def on_pressed(self):
        async with self:
            if self._running:
                return
            self._running = True
        print("jog sub on_pressed-")

        async with self:
            self._process_count = 0
        ws = get_jog_sub_ws()
        ws.send("sub")

        while True:
            async with self:
                if not self._running:
                    self._process_count = 0
                    ws.send("exit")
                    ws.close()
                    return
                self._process_count += 10
                if self._process_count > 100:
                    self._process_count = 0
            await asyncio.sleep(0.1)

    def on_unpressed(self):
        self._running = False
        print("jog sub on_unpressed-")

    @rx.var(cache=True)
    def animation_background(self)->str:
        if self._running:
            return (
                f"linear-gradient(90deg, #a6fc06 0%, #ffa500 {self._process_count}%);"
            )
        else:
            return "#ffa500"
