import reflex as rx
from app.models import User
import bcrypt
import uuid
import os
from typing import Optional, cast
import random

ADMIN_EMAIL = "saurabh@connectwithsaurabh.com"
ADMIN_NAME = "Saurabh K."
DEFAULT_PROFILE_PICS = [
    "default_avatar.png",
    "minimal_abstract_geometric.png",
    "simple_minimal_abstract.png",
]


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()
    ).decode()


def verify_password(
    plain_password: str, hashed_password: str
) -> bool:
    """Verifies a plain password against a hashed one."""
    return bcrypt.checkpw(
        plain_password.encode(), hashed_password.encode()
    )


class AuthState(rx.State):
    """Manages user authentication, registration, and session state."""

    users: dict[str, User] = {
        ADMIN_EMAIL: User(
            password=hash_password("adminpassword123"),
            name=ADMIN_NAME,
            profile_photo=DEFAULT_PROFILE_PICS[0],
        )
    }
    logged_in_user_email: str | None = None

    @rx.var
    def is_authenticated(self) -> bool:
        """Checks if a user is currently logged in."""
        return self.logged_in_user_email is not None

    @rx.var
    def current_user(self) -> User | None:
        """Returns the User object for the currently logged-in user."""
        if (
            self.logged_in_user_email
            and self.logged_in_user_email in self.users
        ):
            return self.users[self.logged_in_user_email]
        return None

    @rx.var
    def is_admin(self) -> bool:
        """Checks if the logged-in user is the admin."""
        return self.logged_in_user_email == ADMIN_EMAIL

    @rx.var
    def current_user_display_name(self) -> str:
        """Returns the display name of the current user."""
        user = self.current_user
        return user["name"] if user else "Guest"

    @rx.var
    def current_user_profile_photo_src(self) -> str:
        """Returns the URL for the current user's profile photo."""
        user = self.current_user
        if (
            user
            and user["profile_photo"]
            in DEFAULT_PROFILE_PICS
        ):
            return f"/{user['profile_photo']}"
        return f"/{DEFAULT_PROFILE_PICS[0]}"

    @rx.var
    def admin_user_details(self) -> User | None:
        """Returns the admin user details."""
        return self.users.get(ADMIN_EMAIL)

    @rx.var
    def admin_display_name(self) -> str:
        """Returns the admin's display name."""
        admin = self.admin_user_details
        return admin["name"] if admin else "Admin"

    @rx.var
    def admin_profile_photo_src(self) -> str:
        """Returns the URL for the admin's profile photo."""
        admin = self.admin_user_details
        if (
            admin
            and admin["profile_photo"]
            in DEFAULT_PROFILE_PICS
        ):
            return f"/{admin['profile_photo']}"
        return f"/{DEFAULT_PROFILE_PICS[0]}"

    @rx.event
    def sign_up(self, form_data: dict):
        """Registers a new user."""
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "")
        name = form_data.get("name", "").strip()
        if not email or not password or (not name):
            yield rx.toast.error(
                "Name, email, and password are required."
            )
            return
        if email == ADMIN_EMAIL:
            yield rx.toast.error("This email is reserved.")
            return
        if email in self.users:
            yield rx.toast.error(
                "Email already in use. Please log in or use a different email."
            )
            return
        profile_photo_to_save = random.choice(
            DEFAULT_PROFILE_PICS
        )
        hashed_pw = hash_password(password)
        new_user = User(
            password=hashed_pw,
            name=name,
            profile_photo=profile_photo_to_save,
        )
        self.users[email] = new_user
        self.logged_in_user_email = email
        yield rx.toast.success(
            f"Welcome, {name}! Your account has been created with a random avatar."
        )
        return rx.redirect("/chat")

    @rx.event
    def sign_in(self, form_data: dict):
        """Logs in an existing user."""
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "")
        if not email or not password:
            yield rx.toast.error(
                "Email and password are required."
            )
            return
        user_data = self.users.get(email)
        if user_data and verify_password(
            password, user_data["password"]
        ):
            self.logged_in_user_email = email
            yield rx.toast.success(
                f"Welcome back, {user_data['name']}!"
            )
            return rx.redirect("/chat")
        yield rx.toast.error("Invalid email or password.")
        self.logged_in_user_email = None

    @rx.event
    def sign_out(self):
        """Logs out the current user."""
        user_name = (
            self.current_user_display_name
            if self.current_user
            else "User"
        )
        self.logged_in_user_email = None
        yield rx.toast.info(
            f"You have been logged out, {user_name}."
        )
        return rx.redirect("/login")

    @rx.event
    def check_login_status(self):
        """Redirects to login page if the user is not authenticated."""
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    def redirect_if_logged_in(self):
        """Redirects to chat page if the user is already authenticated."""
        if self.is_authenticated:
            return rx.redirect("/chat")