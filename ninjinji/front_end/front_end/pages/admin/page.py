import reflex as rx
from front_end.models.user import User
import reflex as rx
from .state import AdminState
from .update_user import update_User
from .add_user import add_customer
from .delete_user import delete_user


def show_users(user: User):
    """Show a customer in a table row."""
    return rx.table.row(
        rx.table.cell(rx.avatar(fallback="DA")),
        rx.table.cell(
            user.name,
        ),
        rx.table.cell(user.worker_id),
        rx.table.cell(user.class_group),
        rx.table.cell(
            update_User(user),
        ),
        rx.table.cell(
            delete_user(user),
        ),
    )


def content():
    return rx.fragment(
        rx.vstack(
            # rx.divider(),
            rx.hstack(
                rx.heading(
                    f"总计: {AdminState.num_Users} 用户",
                    size="5",
                    font_family="Inter",
                ),
                rx.spacer(),
                add_customer(),
                rx.select(
                    ["姓名", "工号", "班组"],
                    placeholder="排序: 姓名",
                    size="3",
                    on_change=lambda sort_value: AdminState.sort_values(sort_value),
                    font_family="Inter",
                ),
                width="100%",
                padding_x="1em",
                padding_top="2em",
                padding_bottom="1em",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("头像"),
                        rx.table.column_header_cell("姓名"),
                        rx.table.column_header_cell("工号"),
                        rx.table.column_header_cell("班组"),
                        rx.table.column_header_cell("编辑"),
                        rx.table.column_header_cell("删除"),
                    ),
                ),
                rx.table.body(rx.foreach(AdminState.users, show_users)),
                # variant="surface",
                size="3",
                width="100%",
            ),
        ),
    )


from front_end.template import template
from front_end.navigation import navbar
from .. import style


@template
def index() -> rx.Component:
    return rx.box(
        navbar("拧紧机用户管理"),
        rx.box(
            content(),
            margin_top=f"calc(50px + {style.Siderbar.margin_top})",
            padding="2em",
        ),
        font_family="Inter",
        padding_left="250px",  # siderbar的宽度
        on_mount=AdminState.on_load,
    )
