import reflex as rx
from .state import DashboardPageState, BarChartState, PieChartState


def content():
    return rx.box(
        rx.box(
            rx.hstack(
                rx.heading("今日加工数据", size="6", color_scheme="blue"),
                justify="center",
            ),
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=PieChartState.data,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    fill="#6890db",
                    label=True,
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.legend(),
                stack_offset="silhouette",
                margin={
                    "left": 10,
                    "right": 0,
                    "top": 20,
                    "bottom": 20,
                },
                min_height=300,
            ),
            padding="2em",
        ),
        rx.box(
            rx.hstack(
                rx.heading("月度加工数据", size="6", color_scheme="blue"),
                justify="center",
            ),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    rx.recharts.label_list(data_key="uv", position="top",fill="#6890db",stroke="#6890db"),
                    data_key="uv",
                    stroke="#6890db",
                    fill="#6890db",
                ),
                rx.recharts.x_axis(data_key="month",type_="category"),
                rx.recharts.y_axis(unit="件"),
                data=BarChartState.data,
                margin={
                    "left": 10,
                    "right": 0,
                    "top": 20,
                    "bottom": 10,
                },
                # position = "relative",
                # buttom = 0,
                width="100%",
                min_height=300,
            ),
            padding="2em",
        ),
        rx.box(
            rx.recharts.area_chart(
                rx.recharts.area(
                    data_key="uv",
                    stroke="#6890db",
                    fill="#6890db",
                    type_="natural",
                ),
                rx.recharts.area(
                    data_key="pv",
                    stroke="#82ca9d",
                    fill="#82ca9d",
                    type_="natural",
                ),
                rx.recharts.x_axis(data_key="time"),
                rx.recharts.y_axis(),
                rx.recharts.legend(),
                data=DashboardPageState.data,
                width="100%",
                min_height=300,
            ),
            padding="2em",
        ),
        rx.button("Refresh", on_click=DashboardPageState.add_data),
    )
