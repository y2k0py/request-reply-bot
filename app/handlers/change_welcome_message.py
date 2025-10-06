from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pydantic import HttpUrl, ValidationError

from app.database.crud.settings_data import SettingsDataService
from app.database.db.session import get_db
from app.database.enums import TagsEnums
from app.database.schemas.settings_data import SettingsDataCreate
from app.keyboards.cancel import cancel_keyboard
from app.keyboards.cancel_accept import accept_cancel_keyboard, AcceptActions, AcceptCallback
from app.keyboards.menu import MainMenuActions, MainMenuCallback, main_menu_keyboard
from app.states.change_welcome_message import ChangeWelcomeMessage

welcome_message_router = Router()

@welcome_message_router.callback_query(MainMenuCallback.filter(F.action == MainMenuActions.CHANGE_WELCOME_MESSAGE_AND_BUTTON))
async def change_welcome_message_and_button(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.answer("💬 Send Welcome Message", reply_markup=cancel_keyboard())
    await state.set_state(ChangeWelcomeMessage.change_message)
    await query.answer()

@welcome_message_router.message(ChangeWelcomeMessage.change_message)
async def change_welcome_message(message: Message, state: FSMContext):
    welcome_message = message.text
    print(welcome_message)
    await state.update_data(welcome_message=welcome_message)
    await message.answer("💬 Send Welcome Message Button Text", reply_markup=cancel_keyboard())
    await state.set_state(ChangeWelcomeMessage.change_button_text)

@welcome_message_router.message(ChangeWelcomeMessage.change_button_text)
async def change_welcome_message_button_text(message: Message, state: FSMContext):
    welcome_message_button_text = message.text
    await state.update_data(welcome_message_button_text=welcome_message_button_text)
    await message.answer("💬 Send Welcome Message Button Url", reply_markup=cancel_keyboard())
    await state.set_state(ChangeWelcomeMessage.change_button_url)

@welcome_message_router.message(ChangeWelcomeMessage.change_button_url)
async def change_welcome_message_button_url(message: Message, state: FSMContext):
    button_url = message.text
    if not button_url.startswith(("http://", "https://")):
        button_url = f"https://{button_url}"
    try:
        url = HttpUrl(button_url)
    except ValidationError:
        await message.answer('❌ Invalid URL, please send a valid URL', reply_markup=cancel_keyboard())
        return
    await state.update_data(welcome_message_button_url=str(url))
    data = await state.get_data()
    welcome_message = data.get("welcome_message")
    welcome_message_button_text = data.get("welcome_message_button_text")
    welcome_message_button_url = data.get("welcome_message_button_url")
    await message.answer(f"💬 Welcome Message: {welcome_message}\n"
                         f"💬 Welcome Message Button Text: {welcome_message_button_text}\n"
                         f"💬 Welcome Message Button Url: {welcome_message_button_url}",
                         reply_markup=accept_cancel_keyboard(AcceptActions.CHANGE_WELCOME_MESSAGE))

@welcome_message_router.callback_query(AcceptCallback.filter(F.action == AcceptActions.CHANGE_WELCOME_MESSAGE))
async def accept_change_welcome_message(callback_query: CallbackQuery, state: FSMContext):
    async with get_db() as db:
        service = SettingsDataService(db)
        data = await state.get_data()
        await service.create(SettingsDataCreate(text=data.get('welcome_message'), tag=TagsEnums.WELCOME_MESSAGE))
        await service.create(SettingsDataCreate(text=data.get('welcome_message_button_text'), tag=TagsEnums.WELCOME_MESSAGE_BUTTON))
        await service.create(SettingsDataCreate(text=data.get('welcome_message_button_url'), tag=TagsEnums.WELCOME_BUTTON_URL))
    await state.clear()
    await callback_query.message.edit_text("✅ Saved Successfully, use buttons below", reply_markup=main_menu_keyboard())

