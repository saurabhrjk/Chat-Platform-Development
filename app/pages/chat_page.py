import reflex as rx
from app.states.auth_state import AuthState
from app.states.chat_state import ChatState
from app.components.navbar import navbar
from app.components.chat_interface import (
    chat_area,
    admin_dashboard_layout,
)


def chat_page() -> rx.Component:
    """The main chat page, view depends on whether user is admin or regular user."""
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.cond(
                AuthState.is_authenticated,
                rx.el.div(
                    rx.cond(
                        AuthState.is_admin,
                        admin_dashboard_layout(),
                        rx.el.div(
                            chat_area(),
                            class_name="w-full max-w-3xl mx-auto h-[calc(100vh-150px)] md:h-[calc(100vh-120px)]",
                        ),
                    ),
                    class_name="container mx-auto p-4 md:p-6",
                ),
                rx.el.div(
                    rx.el.p(
                        "Loading chat or redirecting...",
                        class_name="text-xl text-slate-600",
                    ),
                    rx.el.div(
                        class_name="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"
                    ),
                    class_name="container mx-auto p-8 text-center flex flex-col items-center justify-center h-[calc(100vh-72px)]",
                ),
            ),
            class_name="flex-grow bg-slate-100 py-6 md:py-8",
        ),
        class_name="flex flex-col min-h-screen font-sans",
    )