from typing import Callable

import reflex as rx

from .navigation import dashboard_sidebar


def template(page: Callable[[], rx.Component]) -> rx.Component:
    return rx.box(
        dashboard_sidebar,
        page(),
        # rx.logo(),
        background_color="var(--accent-2)",
        font_family="Share Tech Mono",
        padding_bottom="4em",
    )
