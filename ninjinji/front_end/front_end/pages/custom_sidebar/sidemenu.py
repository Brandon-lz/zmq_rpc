import reflex as rx

def row() -> rx.Component:
    return rx.flex(
        # rx.section(rx.button(width="100%", radius="none"), width="70%"),
        rx.section(rx.button(width="100%", radius="none"), width="70%"),
        rx.section(rx.icon(tag="chevron-down")),
        # background="gray",
        # direction="row",
        width="100%",
        height="25px",
    )

def create() -> rx.Component:
    return rx.vstack(
        row(),
        # row(),
        width="100%",
    )
