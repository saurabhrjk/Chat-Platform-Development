import reflex as rx
from app.states.auth_state import (
    AuthState,
    DEFAULT_PROFILE_PIC,
)


def signup_form() -> rx.Component:
    """Renders the user registration form."""
    return rx.el.div(
        rx.el.h2(
            "Create Your Account",
            class_name="text-3xl font-bold text-center text-slate-800 mb-2",
        ),
        rx.el.p(
            "Connect with Saurabh by creating an account.",
            class_name="text-center text-slate-600 mb-8",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Full Name",
                    html_for="name",
                    class_name="block text-sm font-medium text-slate-700 mb-1",
                ),
                rx.el.input(
                    type="text",
                    id="name",
                    name="name",
                    placeholder="e.g., John Doe",
                    required=True,
                    class_name="w-full px-4 py-3 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors text-slate-700 placeholder-slate-400",
                ),
                class_name="mb-4",
            ),
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
                    placeholder="Create a strong password",
                    required=True,
                    class_name="w-full px-4 py-3 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors text-slate-700 placeholder-slate-400",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Profile Photo (Optional)",
                    class_name="block text-sm font-medium text-slate-700 mb-2",
                ),
                rx.upload.root(
                    rx.el.div(
                        rx.icon(
                            tag="cloud_upload",
                            class_name="w-10 h-10 mb-3 text-slate-400 group-hover:text-indigo-600 transition-colors",
                        ),
                        rx.el.p(
                            rx.el.span(
                                "Click to upload",
                                class_name="font-semibold text-indigo-600",
                            ),
                            " or drag and drop",
                            class_name="text-sm text-slate-500",
                        ),
                        rx.el.p(
                            "PNG, JPG, GIF up to 1MB",
                            class_name="text-xs text-slate-400",
                        ),
                        class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed border-slate-300 rounded-lg group hover:border-indigo-500 transition-colors bg-slate-50 hover:bg-slate-100 cursor-pointer",
                    ),
                    id="profile_photo_upload",
                    on_drop=AuthState.handle_profile_photo_upload(
                        rx.upload_files(
                            upload_id="profile_photo_upload"
                        )
                    ),
                    accept={
                        "image/png": [".png"],
                        "image/jpeg": [".jpg", ".jpeg"],
                        "image/gif": [".gif"],
                    },
                    max_files=1,
                    max_size=1 * 1024 * 1024,
                    border="1px dashed #d1d5db",
                    padding="1rem",
                ),
                rx.cond(
                    AuthState.registration_profile_photo_filename,
                    rx.el.div(
                        rx.el.p(
                            "Selected:",
                            class_name="text-xs text-slate-600 mt-2 mb-1",
                        ),
                        rx.el.div(
                            rx.el.img(
                                src=rx.get_upload_url(
                                    AuthState.registration_profile_photo_filename
                                ),
                                class_name="h-16 w-16 rounded-md object-cover border border-slate-300 mr-2",
                            ),
                            rx.el.p(
                                AuthState.registration_profile_photo_filename,
                                class_name="text-sm text-slate-700 truncate",
                            ),
                            class_name="flex items-center p-2 bg-slate-100 rounded-md",
                        ),
                        class_name="mt-2",
                    ),
                    rx.el.p(
                        f"No photo selected. Default avatar ({DEFAULT_PROFILE_PIC.split('.')[0]}) will be used.",
                        class_name="text-xs text-slate-500 mt-2",
                    ),
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Sign Up",
                type="submit",
                class_name="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50",
            ),
            on_submit=AuthState.sign_up,
            reset_on_submit=False,
            class_name="space-y-4",
        ),
        rx.el.p(
            "Already have an account? ",
            rx.el.a(
                "Log In",
                href="/login",
                class_name="font-medium text-indigo-600 hover:text-indigo-500",
            ),
            class_name="mt-8 text-center text-sm text-slate-600",
        ),
        class_name="max-w-lg w-full bg-white p-8 md:p-10 rounded-xl shadow-2xl border border-slate-200",
    )