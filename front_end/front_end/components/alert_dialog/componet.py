import reflex as rx
from .state import AlertDialogState
from typing import List


def create(
        show:bool=AlertDialogState.show,
        header: str = "Confirm",
        body: str = "Do you want to confirm example?",
           check_it: List[rx.Component] = [
               rx.button(
                   "确认",
                   on_click=AlertDialogState.change,
               ),
           ],
    ):
    return rx.alert_dialog(
        rx.alert_dialog_overlay(
            rx.alert_dialog_content(
                rx.alert_dialog_header(header),
                rx.alert_dialog_body(
                    body
                ),
                rx.alert_dialog_footer(
                    *check_it
                ),
            )
        ),
        is_open=show,
    )
