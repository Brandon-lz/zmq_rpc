import reflex as rx

def create_torque_chart(data,style: dict={}) -> rx.Component:
    return rx.recharts.area_chart(
        rx.recharts.area(
            data_key="目标扭矩",
            stroke="#8884d8",
            fill="#8884d8",
            y_axis_id="left",
        ),
        rx.recharts.area(
            data_key="实际扭矩",
            y_axis_id="right",
            type_="monotone",
            stroke="#82ca9d",
            fill="#82ca9d",
        ),
        rx.recharts.x_axis(data_key="timestamp"),
        rx.recharts.y_axis(data_key="目标扭矩", y_axis_id="left"),
        rx.recharts.y_axis(
            data_key="实际扭矩",
            y_axis_id="right",
            orientation="right",
        ),
        rx.recharts.graphing_tooltip(),
        rx.recharts.legend(),
        data=data,
        width="100%",
        height=300,
        style=style,
    )