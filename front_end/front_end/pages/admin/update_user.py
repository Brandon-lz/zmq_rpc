import reflex as rx
from front_end.models.user import User
from .state import AdminState
from front_end.state import AppState


def update_User(user: User):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square_pen"),
                # rx.icon("square_pen", width=24, height=24),
                bg="green",
                color="white",
                on_click=lambda: AdminState.set_user_vars(user),      # 带上原本的默认数据
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("修改用户信息"),
            rx.dialog.description(
                size="2",
                mb="4",
                padding_bottom="1em",
            ),
            rx.flex(
                rx.text(
                    "姓名",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    placeholder=user.name,
                    default_value=user.name,
                    on_blur=AdminState.set_name_field,
                    on_change=AdminState.set_name_field,
                ),
                rx.text(
                    "工号",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    placeholder=user.worker_id,
                    default_value=user.worker_id,
                    on_blur=AdminState.set_worker_id_field,
                    on_change=AdminState.set_worker_id_field,
                ),
                rx.text(
                    "班组",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    placeholder=user.class_group,
                    default_value=user.class_group,
                    on_blur=AdminState.set_class_group_field,
                    on_change=AdminState.set_class_group_field,
                ),
                rx.cond(
                    AppState.is_admin,
                    rx.checkbox(
                        "设置为管理员",
                        disabled=(user.name == "admin"),
                        checked=AdminState.is_admin_field,
                        spacing="2",
                        on_change=AdminState.set_is_admin_field,
                    ),
                ),
                direction="column",
                spacing="3",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "取消",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "保存",
                        on_click=AdminState.update_User,
                        variant="solid",
                    ),
                ),
                padding_top="1em",
                spacing="3",
                mt="4",
                justify="end",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1em",
            border_radius="25px",
        ),
    )
