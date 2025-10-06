from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

class CancelCallback(CallbackData, prefix="cancel"):
    pass

def cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Cancel", callback_data=CancelCallback())
    return builder.as_markup()

def cancel_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="❌ Cancel", callback_data=CancelCallback().pack())