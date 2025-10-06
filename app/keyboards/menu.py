from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MainMenuActions(str, Enum):
    CRATE_MESSAGE_WITH_BUTTON = "create_message_with_button"
    CHANGE_WELCOME_MESSAGE_AND_BUTTON = 'change_welcome_message_and_button'
    ADD_CHANNEL = 'add_channel'

class MainMenuCallback(CallbackData, prefix="main_menu"):
    action: str

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Change Welcome Message and Button",
                   callback_data=MainMenuCallback(action=MainMenuActions.CHANGE_WELCOME_MESSAGE_AND_BUTTON).pack())
    builder.button(text="🔘 Create Message With Button", callback_data=MainMenuCallback(action=MainMenuActions.CRATE_MESSAGE_WITH_BUTTON).pack())
    builder.button(text="➕ Add Channel", callback_data=MainMenuCallback(action=MainMenuActions.ADD_CHANNEL).pack())
    builder.adjust(1)
    return builder.as_markup()
