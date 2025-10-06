from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.cancel import CancelCallback
from app.keyboards.menu import main_menu_keyboard

cancel_router = Router()

@cancel_router.callback_query(CancelCallback.filter())
async def cancel_handler(query: CallbackQuery):
    await query.message.edit_text('🗃 Main Menu', reply_markup=main_menu_keyboard())
    await query.answer()