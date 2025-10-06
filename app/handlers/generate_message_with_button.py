from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pydantic import HttpUrl, ValidationError

from app.database.crud.settings_data import SettingsDataService
from app.database.db.session import get_db
from app.database.enums import TagsEnums
from app.keyboards.cancel import cancel_keyboard
from app.keyboards.cancel_accept import accept_cancel_keyboard, AcceptActions, AcceptCallback
from app.keyboards.menu import MainMenuActions, MainMenuCallback, main_menu_keyboard
from app.keyboards.request_to_channel import request_to_channel_keyboard

from app.states.send_message_with_button import CrateMessageWithButtonState

create_message_with_button_router = Router()

@create_message_with_button_router.callback_query(MainMenuCallback.filter(F.action == MainMenuActions.CRATE_MESSAGE_WITH_BUTTON))
async def create_message_with_button_handler(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.answer("💬 Send Message Text", reply_markup=cancel_keyboard())
    await state.set_state(CrateMessageWithButtonState.set_message)
    await query.answer()

@create_message_with_button_router.message(CrateMessageWithButtonState.set_message)
async def process_message_text(message: Message, state: FSMContext):
    message_text = message.text
    print(message_text)
    await state.update_data(message_text=message_text)
    await message.answer("💬 Send Message Button Text", reply_markup=cancel_keyboard())
    await state.set_state(CrateMessageWithButtonState.set_button_text)

@create_message_with_button_router.message(CrateMessageWithButtonState.set_button_text)
async def process_button_text(message: Message, state: FSMContext):
    button_text = message.text
    await state.update_data(message_button_text=button_text)
    await message.answer("💬 Send Message Button Url", reply_markup=cancel_keyboard())
    await state.set_state(CrateMessageWithButtonState.set_button_url)

@create_message_with_button_router.message(CrateMessageWithButtonState.set_button_url)
async def process_button_url(message: Message, state: FSMContext):
    button_url = message.text
    if not button_url.startswith(("http://", "https://")):
        button_url = f"https://{button_url}"
    try:
        url = HttpUrl(button_url)
    except ValidationError:
        await message.answer('❌ Invalid URL, please send a valid URL', reply_markup=cancel_keyboard())
        return
    await state.update_data(message_button_url=str(url))
    data = await state.get_data()
    welcome_message = data.get("message_text")
    welcome_message_button_text = data.get("message_button_text")
    welcome_message_button_url = data.get("message_button_url")
    await message.answer(
        f"💬 Message: {welcome_message}\n"
        f"💬 Message Button Text: {welcome_message_button_text}\n"
        f"💬 Message Button Url: {welcome_message_button_url}",
        reply_markup=accept_cancel_keyboard(AcceptActions.SEND_MESSAGE_WITH_BUTTON)
    )

@create_message_with_button_router.callback_query(AcceptCallback.filter(F.action == AcceptActions.SEND_MESSAGE_WITH_BUTTON))
async def accept_change_welcome_message(callback_query: CallbackQuery, state: FSMContext):
    async with get_db() as db:
        service = SettingsDataService(db)
        data = await state.get_data()
        channel_id = await service.get_last_data_by_tag(TagsEnums.CHANNEL_ID)
    await callback_query.bot.send_message(
        chat_id=channel_id.text,
        text=data.get('message_text'),
        reply_markup=request_to_channel_keyboard(text=data.get('message_button_text'), url=data.get('message_button_url'))
    )

    await state.clear()
    await callback_query.answer()
    await callback_query.message.edit_text("✅ Sent to channel Successfully, use buttons below", reply_markup=main_menu_keyboard())

