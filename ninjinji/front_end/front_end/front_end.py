"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from front_end.models import init_db

init_db()

from rxconfig import config
from .state import AppState
from front_end.pages import (
    index,
    login,
    # register,
    admin,
    operate_log,
    control,
    # control_test,
    dashboard,
    test,
    sidebar_example,
    system,
    custom_sidebar,
)



app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="blue"
    ),
    stylesheets=[
        "custom_button2_fast.css",
        "custom_button2_low.css",
        "custom_jog_forward_button.css",
        "custom_jog_backward_button.css",
        "custom_button2_stop.css",
        "googlefont.css",
    ],
)


app.add_page(index.index)
app.add_page(login.index, route="/login")
# app.add_page(register.index,route="/register")
app.add_page(admin.index, route="/admin", on_load=AppState.require_admin)
app.add_page(system.index, route="/system", on_load=AppState.require_admin)
app.add_page(operate_log.index, route="/oplogs", on_load=AppState.require_admin)
app.add_page(control.index, route="/control", on_load=AppState.require_login)
# app.add_page(control_test.index, route="/control-test", on_load=AppState.require_login)
app.add_page(dashboard.index, route="/dashboard", on_load=AppState.require_login)
app.add_page(sidebar_example.index, route="/siderbar")
app.add_page(test.index, route="/test")
app.add_page(custom_sidebar.index, route="/custom_siderbar")

from front_end.components.dashboard.page import index as dash

app.add_page(dash, route="/dashboard/dash")

# abc