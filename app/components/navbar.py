import reflex as rx
from app.states.auth_state import AuthState


def navbar() -> rx.Component:
    """Renders the navigation bar for the application."""
    return rx.el.nav(
        rx.el.div(
            rx.el.a(
                "ConnectWithSaurabh",
                href="/",
                class_name="text-2xl font-bold text-indigo-100 hover:text-white transition-colors duration-150",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.img(
                            src=AuthState.current_user_profile_photo_src,
                            alt=AuthState.current_user_display_name,
                            class_name="h-10 w-10 rounded-full border-2 border-indigo-300 object-cover shadow-md",
                        ),
                        rx.el.p(
                            AuthState.current_user_display_name,
                            class_name="text-indigo-100 hidden md:block ml-3 font-medium",
                        ),
                        rx.el.button(
                            "Sign Out",
                            on_click=AuthState.sign_out,
                            class_name="ml-4 bg-pink-500 hover:bg-pink-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-150 text-sm shadow focus:outline-none focus:ring-2 focus:ring-pink-400 focus:ring-opacity-75",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Login",
                            href="/login",
                            class_name="text-indigo-100 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-150",
                        ),
                        rx.el.a(
                            "Sign Up",
                            href="/signup",
                            class_name="ml-2 bg-teal-500 hover:bg-teal-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-150 text-sm shadow focus:outline-none focus:ring-2 focus:ring-teal-400 focus:ring-opacity-75",
                        ),
                        class_name="flex items-center",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="container mx-auto flex items-center justify-between px-4 py-3 md:px-6",
        ),
        class_name="bg-gradient-to-r from-indigo-600 to-purple-700 shadow-lg sticky top-0 z-50",
    )