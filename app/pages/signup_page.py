import reflex as rx
from app.components.navbar import navbar
from app.components.signup_form import signup_form
from app.states.auth_state import AuthState


def signup_page() -> rx.Component:
    """The user registration page."""
    return rx.el.div(
        navbar(),
        rx.el.main(
            signup_form(),
            class_name="flex flex-col items-center justify-center min-h-[calc(100vh-72px)] bg-gradient-to-br from-slate-100 to-sky-100 p-4 py-12",
        ),
        class_name="min-h-screen bg-slate-100 font-sans",
    )