# from ..state import BaseState

import reflex as rx
import asyncio


class IndexState(rx.State):
    title: str = "拧紧机控制系统"
    load_str: str = "正在加载"

    async def on_mount(self):
        # await asyncio.sleep(1.5)
        # self.load_str = "加载完毕，即将进入系统"
        # await asyncio.sleep(1)
        return rx.redirect("/control")

    def on_mount2(self):
        print(self.get_current_page(), "start")

    def on_page_load(self):
        print("page", self.get_current_page(), "loaded from:", self.get_client_ip())


class ProgressState(rx.State):
    value: int = 0

    @rx.background
    async def start_progress(self):
        async with self:
            self.value = 0
            index = await self.get_state(IndexState)
            index.load_str = "正在加载"
        await asyncio.sleep(0.5)

        while self.value < 92:
            await asyncio.sleep(0.1)
            async with self:
                self.value += 4
        async with self:
            index.load_str = "加载完成"
            await asyncio.sleep(0.2)
            return rx.redirect("/login")
