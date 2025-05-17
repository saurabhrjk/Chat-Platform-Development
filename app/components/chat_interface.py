import reflex as rx
from app.states.chat_state import ChatState
from app.states.auth_state import (
    AuthState,
    DEFAULT_PROFILE_PIC,
)


def message_item(
    message: rx.Var[dict],
    current_user_email: rx.Var[str | None],
) -> rx.Component:
    """Displays a single chat message."""
    is_sender = (
        message["sender_email"] == current_user_email
    )
    timestamp = message["timestamp"].to_string()
    display_time = rx.cond(
        timestamp.contains("T"),
        timestamp.split("T")[1]
        .split(".")[0]
        .to_string()[0:5],
        timestamp,
    )
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                message["content"],
                class_name="px-4 py-2 rounded-lg inline-block max-w-xs md:max-w-md lg:max-w-lg break-words",
                background_color=rx.cond(
                    is_sender,
                    rx.color("indigo", 6),
                    rx.color("slate", 2),
                ),
                color=rx.cond(
                    is_sender,
                    "white",
                    rx.color("slate", 12),
                ),
            ),
            rx.el.span(
                display_time,
                class_name="text-xs text-slate-400 ml-2 align-bottom",
            ),
            class_name=rx.cond(
                is_sender,
                "flex items-end justify-end flex-row-reverse",
                "flex items-end justify-start",
            ),
        ),
        class_name="mb-3 w-full",
    )


def chat_area() -> rx.Component:
    """The main chat interface component."""
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=ChatState.current_chat_partner_profile_pic,
                class_name="w-10 h-10 rounded-full mr-3 object-cover border-2 border-slate-300",
            ),
            rx.el.h2(
                ChatState.current_chat_partner_name,
                class_name="text-lg font-semibold text-slate-700",
            ),
            class_name="flex items-center p-3 border-b border-slate-200 bg-slate-50 rounded-t-xl sticky top-0 z-10",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    ChatState.displayed_messages,
                    lambda msg: message_item(
                        msg, AuthState.logged_in_user_email
                    ),
                ),
                id="message-list",
                class_name="flex-grow overflow-y-auto p-4 space-y-2",
            ),
            class_name="h-[calc(100vh-260px)] md:h-[calc(100vh-240px)] flex flex-col bg-white",
        ),
        rx.el.form(
            rx.el.input(
                placeholder="Type your message here...",
                name="chat_message_content",
                default_value=ChatState.current_message_input,
                key=ChatState.current_message_input,
                class_name="flex-grow p-3 border border-slate-300 rounded-l-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors text-slate-700 placeholder-slate-400 focus:outline-none",
            ),
            rx.el.button(
                rx.icon(tag="send", class_name="w-5 h-5"),
                type="submit",
                class_name="bg-indigo-600 hover:bg-indigo-700 text-white p-3.5 rounded-r-lg transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50",
            ),
            on_submit=ChatState.send_message,
            reset_on_submit=False,
            class_name="flex p-3 border-t border-slate-200 bg-slate-50 rounded-b-xl sticky bottom-0 z-10",
        ),
        class_name="flex flex-col w-full h-full bg-white rounded-xl shadow-lg border border-slate-200",
    )


def admin_user_list_item(
    user: rx.Var[dict],
) -> rx.Component:
    """Displays an item in the admin's list of users."""
    return rx.el.div(
        rx.el.img(
            src=user["profile_photo_src"],
            alt=user["name"],
            class_name="w-10 h-10 rounded-full mr-3 object-cover",
        ),
        rx.el.div(
            rx.el.p(
                user["name"],
                class_name="font-semibold text-slate-700 truncate",
            ),
            rx.el.p(
                user["email"],
                class_name="text-sm text-slate-500 truncate",
            ),
            class_name="flex-grow min-w-0",
        ),
        on_click=lambda: ChatState.select_user_to_chat(
            user["email"]
        ),
        class_name="flex items-center p-3 hover:bg-slate-100 cursor-pointer border-b border-slate-200 transition-colors rounded-lg mb-1",
        background_color=rx.cond(
            ChatState.active_chat_user_email
            == user["email"],
            rx.color("slate", 2),
            "transparent",
        ),
        border_left_width=rx.cond(
            ChatState.active_chat_user_email
            == user["email"],
            "4px",
            "0px",
        ),
        border_left_color=rx.cond(
            ChatState.active_chat_user_email
            == user["email"],
            rx.color("indigo", 6),
            "transparent",
        ),
    )


def admin_dashboard_layout() -> rx.Component:
    """Layout for the admin's chat view, including user list and chat area."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Users",
                class_name="text-xl font-semibold p-4 border-b border-slate-200 text-slate-700 sticky top-0 bg-slate-50 z-10",
            ),
            rx.el.div(
                rx.cond(
                    ChatState.get_chat_user_list_for_admin_view.length()
                    > 0,
                    rx.foreach(
                        ChatState.get_chat_user_list_for_admin_view,
                        admin_user_list_item,
                    ),
                    rx.el.p(
                        "No users to display yet.",
                        class_name="p-4 text-slate-500 text-center",
                    ),
                ),
                class_name="overflow-y-auto p-2 flex-grow",
            ),
            class_name="w-full md:w-1/3 lg:w-1/4 bg-slate-50 border-r border-slate-200 flex flex-col rounded-l-xl h-full",
        ),
        rx.el.div(
            rx.cond(
                ChatState.active_chat_user_email,
                chat_area(),
                rx.el.div(
                    rx.icon(
                        tag="message_circle",
                        class_name="w-16 h-16 text-slate-300 mb-4",
                    ),
                    rx.el.p(
                        "Select a user from the list to start chatting.",
                        class_name="text-slate-500 text-lg",
                    ),
                    class_name="flex flex-col items-center justify-center h-full w-full text-center p-8 bg-white rounded-r-xl",
                ),
            ),
            class_name="flex-grow h-full",
        ),
        class_name="flex flex-row h-[calc(100vh-150px)] md:h-[calc(100vh-120px)] w-full max-w-7xl mx-auto bg-white rounded-xl shadow-xl border border-slate-200",
    )