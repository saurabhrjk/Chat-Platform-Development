import reflex as rx
from app.pages.login_page import login_page
from app.pages.signup_page import signup_page
from app.pages.chat_page import chat_page
from app.states.auth_state import AuthState

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
)
app.style = {
    "font_family": "Inter, sans-serif",
    "background_color": rx.color("slate", 1),
}
app.add_page(
    login_page,
    route="/",
    on_load=AuthState.redirect_if_logged_in,
)
app.add_page(
    login_page,
    route="/login",
    on_load=AuthState.redirect_if_logged_in,
)
app.add_page(
    signup_page,
    route="/signup",
    on_load=AuthState.redirect_if_logged_in,
)
app.add_page(
    chat_page,
    route="/chat",
    on_load=AuthState.check_login_status,
)