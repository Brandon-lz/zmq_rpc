import reflex as rx
from ..style import page as pagestyle
from .sidemenu import create


def siderbar() -> rx.Component:
    return rx.vstack(
        rx.heading("header"),
        create(),
        position="fixed",
        height="100%",
        # left="0px",
        # top="0px",
        z_index="5",
        # padding_x="1.5em",
        padding_y="1em",
        background_color="lightgray",
        align_items="left",
        width="20vw",
    )


def content():
    return rx.container(
        rx.heading("abc", id="12345345", size="4"),
        max_width="60em",
        margin_left="20vw",
        # padding="2em",
        align_items="start",
    )


def index():
    # return rx.fragment(
    #     siderbar(),
    #     content(),
    #     # style=pagestyle,
    # )
    return rx.menu.root(
    rx.menu.trigger(
        rx.button("Options", variant="soft"),
    ),
    rx.menu.content(
        rx.menu.item("Edit", shortcut="⌘ E"),
        rx.menu.item("Duplicate", shortcut="⌘ D"),
        rx.menu.separator(),
        rx.menu.item("Archive", shortcut="⌘ N"),
        rx.menu.sub(
            rx.menu.sub_trigger("More"),
            rx.menu.sub_content(
                rx.menu.item("Move to project…"),
                rx.menu.item("Move to folder…"),
                rx.menu.separator(),
                rx.menu.item("Advanced options…"),
            ),
        ),
        rx.menu.separator(),
        rx.menu.item("Share"),
        rx.menu.item("Add to favorites"),
        rx.menu.separator(),
        rx.menu.item("Delete", shortcut="⌘ ⌫", color="red"),
    ),
)

