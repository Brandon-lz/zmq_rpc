import reflex as rx
from front_end.template import template
from front_end.navigation import navbar
from .. import style


def content()->rx.Component:
    return rx.heading("这是侧边栏模板的内容，请按照index函数的结构进行开发",size="3"),


@template
def index():
    return rx.box(
        navbar("侧边栏模板"),
        rx.box(
            content(),
            margin_top=f"calc(50px + {style.Siderbar.margin_top})",    # 必须
            padding="2em",           # 对齐
        ),
        padding_left="250px",        # siderbar的宽度
    )