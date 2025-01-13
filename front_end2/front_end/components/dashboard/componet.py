import reflex as rx


# def semicircle(
#     radius: int = 10, color: str = "orange", style={}, id=""
# ) -> rx.Component:
#     """
#     半圆形组件
#     """
#     return rx.vstack(
#             rx.center(
#                 style=dict(
#                     bg=color,
#                     width=f"{radius*2}em",
#                     height=f"{radius*2}em",
#                     # clip_path=f'''ellipse({radius}em {radius}em at 50% 100%)''',
#                     clip_path=f"""polygon(50% 0, 100% 0, 100% 100%, 50% 100%);""",
#                 )
#             ),
#             align="center",
#             # width=f"{radius*2}em",
#             # height=f"{radius}em",
#             style=dict(
#                 clip_path="circle(50%);",
#                 transform=f"rotate(-90deg)",
#                 transform_origin="center",
#                 position="absolute",
#                 bottom=f"-{radius}em",
#             ) | style,
#     )


def semicircle(
    radius: int = 10, color: str = "orange", style={}, id=""
) -> rx.Component:
    """
    半圆形组件
    """
    return rx.center(
        rx.center(
            style=dict(
                border_radius="50%",
                width=f"{radius*2}em",
                height=f"{radius*2}em",
                bg=color,
                radius=radius,
                # color=color,
                position="absolute",
                bottom=-radius,
                clip_path=f"""polygon(50% 0, 100% 0, 100% 100%, 50% 100%);""",
                transform=f"rotate(-90deg)",
                transform_origin="center",
            ),
        ),
        id=id,
        # height=f"{radius}em",
        # width=f"{radius*2}em",
        style=style,
        position="absolute",
    )


def huxing(inner_radius: float = 10, width=1, color="#87CEEB", style=dict()):
    """
    圆弧
    """
    color_inner = "radial-gradient(#5d6d8d, var(--chakra-colors-chakra-body-bg));"
    return rx.container(
        rx.vstack(
            semicircle(
                radius=inner_radius + width,
                color=color,
                style=dict(position="absolute", bottom="0em"),
                id="huxing-inner",
            ),
            semicircle(
                radius=inner_radius,
                # color=color_inner,
                color="#fff",
                style=dict(
                    position="absolute",
                    bottom=f"{width-0.1}em",
                ),
                id="huxing-outer",
            ),
            height=f"{inner_radius+width}em",
            width=f"2*{inner_radius+width}em",
            align="center",
            style=dict() | style,
        )
    )


def clock_hand(
    length: float = 20,
    radius: float = 1,
    color="orange",
    transform="rotate(90deg)",
    style=dict(),
) -> rx.Component:
    """
    指针
    """
    return rx.vstack(
        rx.box(
            style=dict(
                width=f"{radius*2}em",
                height=f"{length}em",
                bg=color,
                clip_path="polygon(50% 0, 100% 100%, 50% 100%, 0 100%)",
                position="absolute",
                bottom=0,
            )
        ),
        rx.box(
            width=f"{radius*2}em",
            height=f"{radius*2}em",
            border_radius="50%",
            bg=color,
            position="absolute",
            bottom=f"-{radius}em",
        ),
        color=color,
        align="center",
        height=f"{length}em",
        width=f"{radius*2}em",
        style=dict(
            transform=transform,
            transform_origin="bottom center",
            position="absolute",
            # bottom="20em",
        )
        | style,
    )


def circle(radius: float = 10, color: str = "orange", style={}) -> rx.Component:
    """
    圆形组件
    """
    return rx.container(
        style=dict(
            border_radius="50%",
            width=f"{radius*2}em",
            height=f"{radius*2}em",
            bg=color,
        )
        | style,
    )

# 组件的创建api
def create(
    radius: float = 10,
    border_width=0.6,
    pin_lenth: float = 8.5,
    pin_angle: str = "",
    color="",
    board_num: str = "0.0%",
    min_num=0.0,
    max_num=100.0,
    style={},
) -> rx.Component:
    return rx.vstack(
        huxing(
            inner_radius=radius,
            width=border_width,
            color=color,
            style=dict(position="absolute", bottom=0),
        ),
        clock_hand(
            radius=0.5,
            length=pin_lenth,
            transform=pin_angle,
            style=dict(position="absolute", bottom=f"{radius+radius*0.3}em"),
        ),
        rx.vstack(
            rx.heading(board_num, size="3", color="gray"),
            z_index=100,
            align="center",
            style=dict(
                position="absolute",
                bottom=f"{radius}em",
            ),
        ),
        rx.hstack(
            rx.heading(
                min_num, size="1", color="gray", position="absolute", left=f"1em"
            ),
            # rx.spacer(width=f"{radius*2-2}em"),
            rx.heading(max_num, size="1", color="gray", position="absolute", right=0),
            width=f"{2*(radius+border_width+1.25)}em",
            z_index=100,
            style=dict(
                position="absolute",
                bottom=f"{radius}em",
            ),
        ),
        align="center",
        width=f"{2*(radius+border_width)}em",
        height=f"{radius+border_width}em",
        position="absolute",
        id="dashboard-root",
        transform=f"translate(0,{radius}em);",
        style=style,
    )
