import reflex as rx
from .state import AdminState
from front_end.models import User


def delete_user(user: User):
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.icon_button(rx.icon("trash"), color_scheme="red")
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("删除用户"),
            rx.alert_dialog.description(
                f"确认删除用户:{user.name} ?",
                size="2",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "取消",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "确认",
                        on_click=lambda: AdminState.delete_User(user.worker_id),
                        color_scheme="red",
                        variant="solid",
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )
