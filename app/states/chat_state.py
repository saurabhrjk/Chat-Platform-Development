import reflex as rx
from app.models import Message, User
from app.states.auth_state import (
    AuthState,
    ADMIN_EMAIL,
    DEFAULT_PROFILE_PIC,
)
import datetime
from typing import cast


class ChatState(rx.State):
    """Manages chat messages and interactions."""

    messages: list[Message] = []
    current_message_input: str = ""
    active_chat_user_email: str | None = None

    async def _get_user_details_from_auth(
        self, email: str
    ) -> tuple[str, str]:
        """Helper to get user name and profile pic URL from AuthState."""
        auth_s = await self.get_state(AuthState)
        user = auth_s.users.get(email)
        if user:
            name = user["name"]
            profile_photo_filename = user["profile_photo"]
            if (
                profile_photo_filename
                == DEFAULT_PROFILE_PIC
            ):
                pic_src = f"/{DEFAULT_PROFILE_PIC}"
            else:
                pic_src = rx.get_upload_url(
                    profile_photo_filename
                )
            return (name, pic_src)
        return ("Unknown User", f"/{DEFAULT_PROFILE_PIC}")

    @rx.var
    async def current_chat_partner_name(self) -> str:
        """Determines the name of the current chat partner."""
        auth_s = await self.get_state(AuthState)
        if auth_s.is_admin:
            if self.active_chat_user_email:
                user = auth_s.users.get(
                    self.active_chat_user_email
                )
                return (
                    user["name"] if user else "Select User"
                )
            return "Select a User to Chat"
        else:
            return auth_s.admin_display_name

    @rx.var
    async def current_chat_partner_profile_pic(self) -> str:
        """Determines the profile picture of the current chat partner."""
        auth_s = await self.get_state(AuthState)
        if auth_s.is_admin:
            if self.active_chat_user_email:
                user = auth_s.users.get(
                    self.active_chat_user_email
                )
                if user:
                    if (
                        user["profile_photo"]
                        == DEFAULT_PROFILE_PIC
                    ):
                        return f"/{DEFAULT_PROFILE_PIC}"
                    return rx.get_upload_url(
                        user["profile_photo"]
                    )
            return f"/{DEFAULT_PROFILE_PIC}"
        else:
            return auth_s.admin_profile_photo_src

    @rx.var
    async def displayed_messages(self) -> list[Message]:
        """Filters messages for the current active chat."""
        auth_s = await self.get_state(AuthState)
        if (
            not auth_s.is_authenticated
            or not auth_s.logged_in_user_email
        ):
            return []
        logged_in_email = auth_s.logged_in_user_email
        if auth_s.is_admin:
            if not self.active_chat_user_email:
                return []
            return [
                m
                for m in self.messages
                if m["sender_email"] == logged_in_email
                and m["receiver_email"]
                == self.active_chat_user_email
                or (
                    m["sender_email"]
                    == self.active_chat_user_email
                    and m["receiver_email"]
                    == logged_in_email
                )
            ]
        else:
            return [
                m
                for m in self.messages
                if m["sender_email"] == logged_in_email
                and m["receiver_email"] == ADMIN_EMAIL
                or (
                    m["sender_email"] == ADMIN_EMAIL
                    and m["receiver_email"]
                    == logged_in_email
                )
            ]

    @rx.event(background=True)
    async def send_message(self, form_data: dict):
        """Sends a message."""
        auth_s = await self.get_state(AuthState)
        submitted_content = form_data.get(
            "chat_message_content", ""
        ).strip()
        if (
            not auth_s.is_authenticated
            or not auth_s.logged_in_user_email
        ):
            yield rx.toast.error(
                "You must be logged in to send messages."
            )
            return
        if not submitted_content:
            yield rx.toast.warning(
                "Message content cannot be empty."
            )
            return
        sender_email = cast(
            str, auth_s.logged_in_user_email
        )
        receiver_email: str | None
        if auth_s.is_admin:
            if not self.active_chat_user_email:
                yield rx.toast.error(
                    "Admin: Please select a user to send a message to."
                )
                return
            receiver_email = self.active_chat_user_email
        else:
            receiver_email = ADMIN_EMAIL
        if not receiver_email:
            yield rx.toast.error(
                "Error: Could not determine message recipient."
            )
            return
        new_msg = Message(
            sender_email=sender_email,
            receiver_email=receiver_email,
            content=submitted_content,
            timestamp=datetime.datetime.utcnow().isoformat(),
            is_read=False,
            file_url=None,
        )
        async with self:
            self.messages.append(new_msg)
            self.current_message_input = ""
        yield

    @rx.event
    async def select_user_to_chat(self, user_email: str):
        """Allows admin to select a user to chat with."""
        auth_s = await self.get_state(AuthState)
        if auth_s.is_admin:
            self.active_chat_user_email = user_email
            user_details = (
                await self._get_user_details_from_auth(
                    user_email
                )
            )
            yield rx.toast.info(
                f"Opened chat with {user_details[0]}"
            )
        else:
            yield rx.toast.error(
                "This action is available for admins only."
            )

    @rx.var
    async def get_chat_user_list_for_admin_view(
        self,
    ) -> list[dict[str, str]]:
        """
        Provides a list of users the admin has chatted with,
        for display in the admin's user list.
        Each item is a dict: {"email": str, "name": str, "profile_photo_src": str}
        """
        auth_s = await self.get_state(AuthState)
        if not auth_s.is_admin:
            return []
        interacted_user_emails = set()
        for msg in self.messages:
            if (
                msg["sender_email"] == ADMIN_EMAIL
                and msg["receiver_email"] != ADMIN_EMAIL
            ):
                interacted_user_emails.add(
                    msg["receiver_email"]
                )
            elif (
                msg["receiver_email"] == ADMIN_EMAIL
                and msg["sender_email"] != ADMIN_EMAIL
            ):
                interacted_user_emails.add(
                    msg["sender_email"]
                )
        for email in auth_s.users:
            if email != ADMIN_EMAIL:
                interacted_user_emails.add(email)
        user_list_for_view = []
        for email in sorted(list(interacted_user_emails)):
            user = auth_s.users.get(email)
            if user:
                profile_pic_src = f"/{DEFAULT_PROFILE_PIC}"
                if (
                    user["profile_photo"]
                    != DEFAULT_PROFILE_PIC
                ):
                    profile_pic_src = rx.get_upload_url(
                        user["profile_photo"]
                    )
                user_list_for_view.append(
                    {
                        "email": email,
                        "name": user["name"],
                        "profile_photo_src": profile_pic_src,
                    }
                )
        return user_list_for_view