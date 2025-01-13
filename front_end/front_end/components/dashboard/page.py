# """Welcome to Reflex! This file outlines the steps to create a basic app."""
from .state import DashboardState
import reflex as rx
from .componet import create


def index()->rx.Component:
    return rx.vstack(
        create(
            radius=10,
            border_width=0.7,
            pin_lenth=6,
            pin_angle=DashboardState.pin_angle_sytle,
            color=DashboardState.color,
            board_num=DashboardState.board_num,
            style=dict(position="absolute",bottom="20em")
            # style=dict(position="static")
        ),
        rx.hstack(
            rx.button(
                "Decrement",
                color_scheme="red",
                border_radius="1em",
                on_mouse_down=DashboardState.add_count,on_mouse_up=DashboardState.stop_add_count,on_mouse_leave=DashboardState.stop_add_count,
                position="relative",left="1em"

            ),
            rx.text(DashboardState.count, font_size="2em",text_align="center",width="5em"),
            rx.button(
                "Increment",
                color_scheme="green",
                border_radius="1em",
                on_mouse_down=DashboardState.sub_count,on_mouse_up=DashboardState.stop_add_count,on_mouse_leave=DashboardState.stop_add_count,
            ),
            style=dict(position="absolute",bottom="14em")
        ),
        style=dict(
            position="fixed",
            width="100vw",
            height="100vh"
        )
    )
        
