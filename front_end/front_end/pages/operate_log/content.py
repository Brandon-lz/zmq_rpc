import reflex as rx
from .state import LogState

from datetime import datetime


def content() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("时间筛选", size="2"),
            rx.input(
                placeholder="年",
                value=datetime.now().year,
                on_change=LogState.set_filter_year,
                on_blur=LogState.set_filter_year,
            ),
            rx.heading("年", size="2"),
            rx.input(
                placeholder="月",
                value=datetime.now().month,
                on_change=LogState.set_filter_month,
                on_blur=LogState.set_filter_month,
            ),
            rx.heading("月", size="2"),
            rx.input(
                placeholder="日",
                value=datetime.now().day,
                on_change=LogState.set_filter_day,
                on_blur=LogState.set_filter_day,
            ),
            rx.heading("日",size="2"),
            direction="row",
            align="center",
        ),
        rx.box(
            rx.data_table(
                data=LogState.data,
                pagination=True,
                search=True,
                sort=True,
            ),
            # transform="scale(0.5) translate(-100%, -100%);",
        )
       
    )
