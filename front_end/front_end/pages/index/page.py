import reflex as rx
from .state import IndexState,ProgressState
from .. import style


def index() -> rx.Component:
    return rx.vstack(
        rx.image(src="/wl.jpg", style=dict(width="100vw", height="100vh")),
        rx.progress(
            value=ProgressState.value,
            # is_indeterminate=True,
            high_contrast=True,
            color_scheme="blue",
            
            style=dict(
                width="70%",
                height="18px",
                position="fixed",
                bottom="10%",
                z_index=101,
                # transform="rotate(270deg)",
                # transform_origin="left center",
                # position="absolute",
            ),
            on_mount=ProgressState.start_progress
        ),
        rx.text(
            IndexState.load_str,
            style=dict(
                font_size="13px",
                color="#FFFFFF",
                position="fixed",
                bottom="10%",
                z_index=102,
            ),
        ),
        rx.text(
            "Copyright © 2003-2021 银川威力传动技术股份有限公司  版权所有",
            style=dict(
                font_size="xs",
                color="#FFFFFF",
                z_index=103,
                position="fixed",
                bottom="5%",
            ),
        ),
        align="center",
        style=style.page,
    )
