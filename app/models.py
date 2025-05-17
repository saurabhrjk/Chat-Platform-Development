from typing import TypedDict, List


class User(TypedDict):
    password: str
    name: str
    profile_photo: str


class Message(TypedDict):
    sender_email: str
    receiver_email: str
    content: str
    timestamp: str
    is_read: bool
    file_url: str | None