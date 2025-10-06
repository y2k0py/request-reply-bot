from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.cancel import CancelCallback


class AcceptActions(str, Enum):
    CHANGE_WELCOME_MESSAGE = "change_welcome_message"
    ADD_CHANNEL = "add_channel"
    SEND_MESSAGE_WITH_BUTTON = "send_message_with_button"

class AcceptCallback(CallbackData, prefix="accept"):
    action: str

def accept_cancel_keyboard(action: AcceptActions) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Accept", callback_data=AcceptCallback(action=action).pack())
    builder.button(text="❌ Cancel", callback_data=CancelCallback().pack())
    builder.adjust(2)
    return builder.as_markup()
