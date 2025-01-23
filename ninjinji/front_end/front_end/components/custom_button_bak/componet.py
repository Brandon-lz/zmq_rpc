import reflex as rx
from .state import BigButtonState
from . import style


def create_start_button() -> rx.Component:
    """
    一个集开始、过程显示、结果确认功能为一体的按钮
    """
    return rx.box(
        rx.box(
            rx.cond(
                BigButtonState.pressed,
                rx.box(
                    rx.box(
                        BigButtonState.start_button_text,
                        element="startbutton",
                        background=BigButtonState.animation_background,
                        class_name=["startbutton"],
                        on_click=BigButtonState.to_start,
                    ),
                    element="div",
                    class_name=["jogwrap"],
                    # height="50px",
                    # position="absolute",
                ),
                rx.box(
                    rx.box(
                        BigButtonState.start_button_text,
                        element="startbuttonlow",
                        class_name=["startbuttonlow"],
                        on_click=BigButtonState.to_start,
                    ),
                    element="div",
                    class_name=["jogwrap"],
                    # height="50px",
                    # position="absolute",
                ),
            ),
        ),
        rx.box(height="6em"),
        id="start-button",
        width="300px",
        height="60px",
        # position="absolute",           # 去除居中排布
    )


def create_jog_forward_button() -> rx.Component:
    return rx.box(
        rx.box(
            "jog+",
            background=BigButtonState.jog_add_press_anima,
            on_mouse_down=BigButtonState.jog_add_pressed,
            on_mouse_up=BigButtonState.jog_add_unpressed,
            on_mouse_out=BigButtonState.jog_add_unpressed,
            class_name=["jogforwardbutton"],
        ),
        element="div",
        class_name=[
            "jogwrap",
        ],
    )


def create_jog_backward_button() -> rx.Component:
    return rx.box(
        rx.box(
            "jog-",
            background=BigButtonState.jog_sub_press_anima,
            on_mouse_down=BigButtonState.jog_sub_pressed,
            on_mouse_up=BigButtonState.jog_sub_unpressed,
            on_mouse_out=BigButtonState.jog_sub_unpressed,
            class_name=["jogbackwardbutton"],
        ),
        element="div",
        class_name=[
            "jogwrap",
        ],
    )


def create_stop_button(on_click=None) -> rx.Component:
    if on_click:
        return rx.box(
            rx.box(
                "stop",
                element="stopbutton",
                class_name=["stopbutton"],
                on_click=on_click,
            ),
            element="div",
            class_name=[
                "wrap",
            ],
        )
    return rx.box(
        rx.box(
            "stop",
            element="stopbutton",
            class_name=["stopbutton"],
        ),
        element="div",
        class_name=[
            "wrap",
        ],
    )
