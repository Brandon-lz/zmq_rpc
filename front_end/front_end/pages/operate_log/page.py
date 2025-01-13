import reflex as rx
from front_end.template import template
from front_end.navigation import navbar
from front_end.pages import style
from .content import content


@template
def index()->rx.Component:
    return rx.box(
        navbar("拧紧机操作日志"),
        rx.box(
            content(),
            margin_top=f"calc(50px + {style.Siderbar.margin_top})",
            padding="2em",
        ),
        font_family="Inter",
        padding_left="250px",        # siderbar的宽度
    )