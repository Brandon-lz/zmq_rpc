import reflex as rx
from .state import RegisterState


def index() -> rx.Component:
    return rx.center(
        # *deploy_dialogs(),
        rx.vstack(
            rx.heading(
                "拧紧机控制系统",
                font_size="1.5em",
                letter_spacing="1px",
                color="#3b94fd",
                align="center",
            ),
            rx.vstack(
                rx.vstack(
                    rx.input(
                        id="name",
                        placeholder="输入用户名",
                        on_change=RegisterState.set_name_field,
                        on_blur=RegisterState.set_name_field,
                        min_width="13em",
                    ),
                    rx.spacer(height="1em"),
                    rx.input(
                        id="password",
                        placeholder="输入密码",
                        on_change=RegisterState.set_password_field,
                        on_blur=RegisterState.set_password_field,
                        type="password",
                        min_width="13em",
                    ),
                    rx.spacer(height="2em"),
                    rx.hstack(
                        # rx.button(
                        #     "登陆",
                        #     on_click=LoginState.log_in,
                        #     width="45%",
                        # ),
                        # rx.spacer(width="10%"),
                        rx.button(
                            "注册",
                            on_click=RegisterState.sign_up,
                            width="45%",
                        ),
                        width="100%",
                        justify="center",
                    ),
                    # rx.text(LoginState.name_field),
                    # rx.text(LoginState.password_field)
                ),
            ),
            align="center",
            spacing="4",
            min_height="40vh",
            min_width="50vh",
            # rx.divider(),
            # rx.cond(
            #     LoginState.image_processing,
            #     rx.circular_progress(is_indeterminate=True),
            #     rx.cond(
            #         LoginState.image_made,
            #         rx.image(
            #             src=LoginState.image_url,
            #             height="25em",
            #             width="25em",
            #         ),
            #     ),
            # ),
            bg="white",
            padding="2em",
            shadow="lg",
            border_radius="lg",
        ),
        width="100vw",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )
