import reflex as rx
from .. import style

# from front_end.components import plotly_component
from front_end.components import custom_button
from front_end.components import dashboard
from front_end.components import torque_chart
from front_end.components import camera

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
            on_click=rx.redirect("/login"),
        ),
        rx.moment(interval=1000, format="YYYY年MM月DD日 HH:mm:ss",position="fixed",top="0.1em",left="2em",font_weight="500"),
        rx.hstack(
            rx.heading("PLC连接: ",size="2"),
            # rx.avatar(fallback=ControlState.plc_ok, color_scheme="grass"),
            rx.cond(
                ControlState.plc_ok,
                rx.avatar(fallback="正常", color_scheme="grass"),
                rx.avatar(fallback="断开", color_scheme="crimson"),
            ),
            # rx.button("change",on_click=ControlState.changeplc_ok),
            on_mount=ControlState.update_heartbeat_value,
            align="center",
        ),
        rx.flex(
            rx.spacer(),
            rx.vstack(
                camera.create(id="0"),
                align="center",
                justify="center",
            ),
            rx.spacer(),
            rx.vstack(
                # rx.box(background="black", width="33%"),
                rx.hstack(
                    dashboard.create(
                        radius=10,
                        border_width=0.7,
                        pin_lenth=6,
                        max_num=ControlDashboardState.scope_max,
                        pin_angle=ControlDashboardState.pin_angle_sytle,
                        color=ControlDashboardState.color,
                        board_num=ControlDashboardState.board_num,
                    ),
                    # rx.button("start", on_click=ControlDashboardState.add_count),
                    # rx.button("stop", on_click=ControlDashboardState.sub_count),
                    id="dashboard-id",
                    # min_height="50vh",
                    width="33%",
                    on_mount=ControlDashboardState.update_torque,
                ),
                # width="100%",
                height="30vh",
                align="center",
                justify="center",
            ),
            rx.spacer(),
            rx.vstack(
                camera.create(id="1"),
                align="center",
                justify="center",
            ),
            rx.spacer(),
            flex_direction="row",
            width="100%",
        ),
        torque_chart.create_torque_chart(data=torque_chart.TorqueChartState.data),
        # rx.hstack(
        #     rx.button(
        #         "曲线测试",
        #         color_scheme="red",
        #         on_click=torque_chart.TorqueChartState.change_data,
        #     ),
        #     rx.button(
        #         "清空数据",
        #         color_scheme="green",
        #         on_click=torque_chart.TorqueChartState.clear_data,
        #     ),
        # ),

        rx.hstack(
            rx.hstack(
                rx.heading(f"设置输出扭矩: ",size="4",width="200px"),
                rx.avatar(fallback=f"{SlidersState.torque}"),
                rx.heading(f"N.m",size="4"),
                rx.slider(
                    default_value=SlidersState.get_aim_torque,
                    # value=SlidersState.get_torque,
                    min=0.0,
                    max=6000.0,
                    on_value_commit=SlidersState.set_aim_torque,
                    # on_change=SlidersState.set_torque.throttle(6000),
                    # on_mount=SlidersState.init_torque,
                ),
                rx.spacer(),
                min_width = "600px",
                align="center",
            ),
            rx.spacer(),
            rx.hstack(
                rx.heading(f"设置最大扭矩: ",size="4",width="200px"),
                rx.avatar(fallback=f"{SlidersState.max_torque}"),
                rx.heading(f"N.m",size="4"),
                rx.slider(
                    default_value=SlidersState.get_max_torque,
                    # value=SlidersState.get_torque,
                    min=0.0,
                    max=6000.0,
                    on_value_commit=SlidersState.set_max_torque,
                    # on_change=SlidersState.set_torque.throttle(6000),
                    # on_mount=SlidersState.init_torque,
                ),
                min_width = "600px",
                align="center",
            ),
            rx.spacer(),
            width = "100vw",
        ),

        rx.spacer(),
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
        rx.spacer(),
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
