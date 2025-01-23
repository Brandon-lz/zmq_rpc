import reflex as rx
import asyncio
from ..dashboard import DashboardState


class BigButtonState(rx.State):
    width = 3
    height = 3
    pressed: bool = False

    start_button_text: str = "start"

    process_max: float = 100
    process_min: float = 0
    process_count: float = process_min
    runing: bool = False

    jog_add_runing: bool = False
    jog_sub_runing: bool = False
    jog_add_count: int = 0
    jog_sub_count: int = 0

    @rx.var(cache=False)
    def button_width(self)->str:
        return f"{self.width}em"

    @rx.var(cache=False)
    def button_height(self)->str:
        return f"{self.height}em"

    @rx.var(cache=False)
    def animation_background(self)->str:
        persent = self.process_count / (self.process_max - self.process_min) * 1.5
        # if persent>=0.7:
        # persent = persent+(persent-persent*0.7)*1.5
        return f"linear-gradient(90deg, #a6fc06 0%, rgba(79, 209, 197, 1) {persent*100.0}%);"

    @rx.event(background=True)
    async def to_start(self):
        # 初始化逻辑必须写在这里面
        async with self:

            # only allow 1 concurrent task
            if self.runing:
                return

            self.click()
            if not self.pressed:
                return

            # State mutation is only allowed inside context block
            self.runing = True
            print("start--------------")

        # 后台任务
        while True:
            async with self:
                # Check for stopping conditions inside context
                if not self.runing or self.process_count >= self.process_max:
                    self.start_button_text = "finish"
                    self.runing = False
                    return

                self.process_count += 1
                self.start_button_text = (
                    "running "
                    + str(
                        self.process_count
                        * 100.0
                        / (self.process_max - self.process_min)
                    )
                    + "%"
                )

                # Await long operations outside the context to avoid blocking UI
            await asyncio.sleep(0.02)

    def click(self):
        self.pressed = not self.pressed
        if self.pressed:
            self.start_button_text = "running"
        else:
            self.start_button_text = "start"
            self.process_count = self.process_min

    @rx.event(background=True)
    async def jog_sub_pressed(self):
        async with self:
            if self.jog_sub_runing:
                return

            self.jog_sub_runing = True
            self.jog_add_runing = False

        while True:
            async with self:
                if not self.jog_sub_runing:
                    self.jog_sub_count = 0
                    return

                if self.jog_sub_count > 100:
                    self.jog_sub_count = 0
                self.jog_sub_count += 3
            await asyncio.sleep(0.02)

    def jog_sub_unpressed(self):
        self.jog_sub_runing = False

    @rx.var(cache=False)
    def jog_sub_press_anima(self)->str:
        if self.jog_sub_runing:
            return f"linear-gradient(90deg, #a6fc06 0%, #ffa500 {self.jog_sub_count}%);"
        else:
            return "#ffa500"

    @rx.event(background=True)
    async def jog_add_pressed(self):
        async with self:
            if self.jog_add_runing:
                return

            self.jog_add_runing = True
            self.jog_sub_runing = False

        while True:
            async with self:
                if not self.jog_add_runing:
                    self.jog_add_count = 0
                    return

                if self.jog_add_count > 100:
                    self.jog_add_count = 0
                self.jog_add_count += 3
            await asyncio.sleep(0.02)

    def jog_add_unpressed(self):
        self.jog_add_runing = False

    @rx.var(cache=False)
    def jog_add_press_anima(self)->str:
        if self.jog_add_runing:
            return f"linear-gradient(90deg, #a6fc06 0%, #e7dbca {self.jog_add_count}%);"
        else:
            return "#e7dbca"
