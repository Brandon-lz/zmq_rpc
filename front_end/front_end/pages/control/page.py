import reflex as rx
from .. import style

# from ninjinji.components import plotly_component
from front_end.components import custom_button
from front_end.components import dashboard

from .state import (
    ControlState,
    ControlDashboardState,
    SlidersState,
    StartButtonState,
    StopButtonState,
    JogAddButtonState,
    JogSubButtonState,
)


def index() -> rx.Component:
    return rx.vstack(
        # plotly_component.create(),
        # dashboard.create(
        #     pin_angle=dashboard.State.pin_angle_sytle,
        #     color=dashboard.State.color,
        #     # style=dict(position="absolute",bottom="20em")
        # ),
        rx.icon_button(
            rx.icon("home"),
            position="fixed",
            top="0em",
            right="0em",
            on_click=rx.redirect("/"),
        ),
        rx.hstack(
            rx.box(background="black", width="33%"),
            rx.hstack(
                dashboard.create(
                    radius=10,
                    border_width=0.7,
                    pin_lenth=6,
                    pin_angle=ControlDashboardState.pin_angle_sytle,
                    color=ControlDashboardState.color,
                    board_num=ControlDashboardState.board_num,
                ),
                # rx.button("start", on_click=ControlDashboardState.add_count),
                # rx.button("stop", on_click=ControlDashboardState.sub_count),
                id="dashboard-id",
                min_height="50vh",
                width="33%",
                on_mount=ControlDashboardState.update_torque,
            ),
            width="100%",
        ),
        rx.box(
            rx.heading(
                f"plc心跳: {ControlState.value}",
                on_mount=ControlState.update_value,
            ),
            # rx.heading(f"current value: {ControlState.value}",on_mount=ControlState.update_value),
            # rx.button("start",on_click=ControlState.update_value),
            height="5em",
        ),
        rx.vstack(
            rx.heading(f"设置扭矩: {SlidersState.torque} N.m"),
            rx.slider(
                default_value=SlidersState.get_torque,
                # value=SlidersState.get_torque,
                min=0.0,
                max=100.0,
                on_value_commit=SlidersState.set_torque,
                on_mount=SlidersState.init_torque,
            ),
            min_width="30em",
        ),
        rx.center(
            custom_button.create_start_button(
                StartButtonState.pressed,
                StartButtonState.animation_background,
                click_start=StartButtonState.on_click,
                click_finish=StartButtonState.on_click,
                button_text=StartButtonState.start_button_text,
            ),
            rx.spacer(),
            custom_button.create_stop_button(
                on_click=StopButtonState.on_click,
                background=StopButtonState.backgroup_color,
                button_text=StopButtonState.button_text,
            ),
            rx.spacer(),
            custom_button.create_jog_forward_button(
                pressed=JogAddButtonState.on_pressed,
                unpressed=JogAddButtonState.on_unpressed,
                jog_add_press_anima=JogAddButtonState.animation_background,
                button_text=JogAddButtonState.button_text,
            ),
            rx.spacer(),
            custom_button.create_jog_backward_button(
                pressed=JogSubButtonState.on_pressed,
                unpressed=JogSubButtonState.on_unpressed,
                jog_sub_press_anima=JogSubButtonState.animation_background,
                button_text=JogSubButtonState.button_text,
            ),
            flex_direction="row",
            # justify="center",
            width="100%",
        ),
        # rx.box(height="5em"),
        # rx.box("hello", id="text1"),
        # rx.vstack(
        #     rx.script(
        #         """const handle_press = (arg) => {
        #     window.alert("You clicked at " + arg.clientX + ", " + arg.clientY);
        # }"""
        #     ),
        #     rx.button(
        #         "Where Did I Click?",
        #         on_click=rx.client_side("handle_press(args)"),
        #     ),
        # ),
        #         rx.vstack(
        #             rx.script(
        # """function displayResult() {
        #     document.getElementById("text1").innerHTML = "Have a nice day!";
        # }"""
        #             ),
        #             rx.button(
        #                 "Where Did I Click?",
        #                 on_click=rx.client_side("""document.getElementById("text1").innerHTML = "Have a nice day!";"""),
        #             ),
        #         ),
        # on_mount=ControlState.send_heart_beat,
        # rx.box(on_mount=ControlState.send_heart_beat),
        on_mount=ControlState.send_heart_beat,
        on_unmount=ControlState.quit_page,
        style=style.page,
        padding="2em",
    )
