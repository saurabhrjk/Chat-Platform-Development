import reflex as rx
from app.components.navbar import navbar
from app.components.login_form import login_form
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    """The user login page."""
    return rx.el.div(
        navbar(),
        rx.el.main(
            login_form(),
            class_name="flex flex-col items-center justify-center min-h-[calc(100vh-72px)] bg-gradient-to-br from-slate-100 to-sky-100 p-4",
        ),
        class_name="min-h-screen bg-slate-100 font-sans",
    )