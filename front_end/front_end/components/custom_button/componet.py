import reflex as rx


def create_start_button(
    pressed,
    animation_background,
    click_start=None,
    click_finish=None,
    button_text="开始",
) -> rx.Component:
    """
    一个集开始、过程显示、结果确认功能为一体的按钮
    """
    return rx.box(
        rx.box(
            rx.cond(
                pressed,
                rx.box(
                    rx.box(
                        button_text,
                        # element="startbutton",
                        background=animation_background,
                        class_name=["startbutton"],
                        # on_click=click_start,
                        on_mouse_up=click_start,
                    ),
                    id="123456789",
                    element="div",
                    class_name=["jogwrap"],
                    # height="50px",
                    # position="absolute",
                ),
                rx.box(
                    rx.box(
                        button_text,
                        # element="startbuttonlow",
                        class_name=["startbuttonlow"],
                        on_click=click_finish,
                    ),
                    id="1234567890",
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


def create_jog_forward_button(
    pressed=None, unpressed=None, jog_add_press_anima=None,button_text="jog+"
) -> rx.Component:
    return rx.box(
        rx.box(
            button_text,
            background=jog_add_press_anima,
            on_mouse_down=pressed,
            on_mouse_up=unpressed,
            on_mouse_out=unpressed,
            class_name=["jogforwardbutton"],
        ),
        element="div",
        class_name=[
            "jogwrap",
        ],
    )


def create_jog_backward_button(
    pressed=None, unpressed=None, jog_sub_press_anima=None,button_text="jog-"
) -> rx.Component:
    return rx.box(
        rx.box(
            button_text,
            background=jog_sub_press_anima,
            on_mouse_down=pressed,
            on_mouse_up=unpressed,
            on_mouse_out=unpressed,
            class_name=["jogbackwardbutton"],
        ),
        element="div",
        class_name=[
            "jogwrap",
        ],
    )


def create_stop_button(on_click=None, background="red",button_text="停止") -> rx.Component:
    # if on_click:
    return rx.box(
        rx.box(
            button_text,
            background=background,
            element="stopbutton",
            class_name=["stopbutton"],
            on_click=on_click,
        ),
        element="div",
        class_name=[
            "wrap",
        ],
    )
    # return rx.box(
    #     rx.box(
    #         "stop",
    #         element="stopbutton",
    #         class_name=["stopbutton"],
    #     ),
    #     element="div",
    #     class_name=[
    #         "wrap",
    #     ],
    # )
