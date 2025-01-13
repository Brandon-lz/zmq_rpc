import reflex as rx
from front_end.template import template
from front_end.navigation import navbar
from .. import style
from .state import SystemState


def content() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.text("开启日志"),
            rx.switch(checked=SystemState.open_log_record,on_change=SystemState.toggle_log_record),
            spacing="2",
        ),
        # rx.flex(
        #     rx.text("MES地址"),
        #     rx.input(value=SystemState.mes_url,on_change=SystemState.set_mes_url),  
        #     spacing="2",
        # ),
    )


@template
def index():
    return rx.box(
        navbar("系统配置"),
        rx.box(
            content(),
            margin_top=f"calc(50px + {style.Siderbar.margin_top})",  # 必须
            padding="2em",  # 对齐
        ),
        padding_left="250px",  # siderbar的宽度
    )
