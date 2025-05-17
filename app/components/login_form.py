import reflex as rx
from app.states.auth_state import AuthState


def login_form() -> rx.Component:
    """Renders the user login form."""
    return rx.el.div(
        rx.el.h2(
            "Welcome Back!",
            class_name="text-3xl font-bold text-center text-slate-800 mb-2",
        ),
        rx.el.p(
            "Log in to continue your conversation with Saurabh.",
            class_name="text-center text-slate-600 mb-8",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    html_for="email",
                    class_name="block text-sm font-medium text-slate-700 mb-1",
                ),
                rx.el.input(
                    type="email",
                    id="email",
                    name="email",
                    placeholder="you@example.com",
                    required=True,
                    class_name="w-full px-4 py-3 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors text-slate-700 placeholder-slate-400",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    html_for="password",
                    class_name="block text-sm font-medium text-slate-700 mb-1",
                ),
                rx.el.input(
                    type="password",
                    id="password",
                    name="password",
                    placeholder="Enter your password",
                    required=True,
                    class_name="w-full px-4 py-3 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors text-slate-700 placeholder-slate-400",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Log In",
                type="submit",
                class_name="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50",
            ),
            on_submit=AuthState.sign_in,
            reset_on_submit=True,
            class_name="space-y-4",
        ),
        rx.el.p(
            "Don't have an account? ",
            rx.el.a(
                "Sign Up",
                href="/signup",
                class_name="font-medium text-indigo-600 hover:text-indigo-500",
            ),
            class_name="mt-8 text-center text-sm text-slate-600",
        ),
        class_name="max-w-md w-full bg-white p-8 md:p-10 rounded-xl shadow-2xl border border-slate-200",
    )