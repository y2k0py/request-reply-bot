import re

from aiogram import Router, F, Bot
from aiogram.enums import ChatType, ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, Chat

from app.database.crud.settings_data import SettingsDataService
from app.database.db.session import get_db
from app.database.enums import TagsEnums
from app.database.schemas.settings_data import SettingsDataCreate
from app.keyboards.cancel import cancel_keyboard
from app.keyboards.cancel_accept import accept_cancel_keyboard, AcceptActions, AcceptCallback
from app.keyboards.menu import MainMenuActions, MainMenuCallback, main_menu_keyboard
from app.states.add_channel import AddChannelState
from app.states.change_welcome_message import ChangeWelcomeMessage

add_channel_router = Router()

@add_channel_router.callback_query(MainMenuCallback.filter(F.action == MainMenuActions.ADD_CHANNEL))
async def add_channel_handler(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.answer("🔁 Forward any message from your channel", reply_markup=cancel_keyboard())
    await state.set_state(AddChannelState.waiting_for_channel)
    await query.answer()

async def _extract_channel_chat(message: Message, bot: Bot) -> Chat | None:
    if message.forward_origin and getattr(message.forward_origin, "type", None) == "channel":
        return message.forward_origin.chat
    if message.forward_from_chat and message.forward_from_chat.type == ChatType.CHANNEL:
        return message.forward_from_chat
    text = (message.text or "").strip()
    if not text:
        return None
    if "t.me/+" in text or "joinchat" in text:
        return None
    m = re.search(r"(?:https?://)?t\.me/c/(\d+)(?:/\d+)?", text)
    if m:
        chat_id = int("-100" + m.group(1))
        return await bot.get_chat(chat_id)
    m = re.search(r"(?:https?://)?t\.me/(@?[A-Za-z0-9_]{5,})/?", text)
    if m:
        username = m.group(1)
        if not username.startswith("@"):
            username = "@" + username
        chat = await bot.get_chat(username)
        if chat.type == ChatType.CHANNEL:
            return chat
        return None
    if text.startswith("@") and len(text) > 5:
        chat = await bot.get_chat(text)
        if chat.type == ChatType.CHANNEL:
            return chat
    return None

@add_channel_router.message(AddChannelState.waiting_for_channel)
async def process_channel_message_or_url(message: Message, state: FSMContext, bot: Bot):
    chat = await _extract_channel_chat(message, bot)
    if not chat or chat.type != ChatType.CHANNEL:
        await message.answer(
            "❌ Unable to detect a channel.\n"
            "Forward a post from the channel or send https://t.me/<channel_name> or @<channel_name>",
            reply_markup=cancel_keyboard()
        )
        return

    me = await bot.get_me()
    try:
        member = await bot.get_chat_member(chat.id, me.id)
        if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
            await message.answer(
                "❌ I must be an administrator in this channel. "
                "Add the bot as an admin and try again.",
                reply_markup=cancel_keyboard()
            )
            return
    except Exception:
        await message.answer(
            "❌ Failed to verify my permissions in the channel. "
            "Make sure the bot is added as an administrator and try again.",
            reply_markup=cancel_keyboard()
        )
        return

    members_count = None
    try:
        members_count = await bot.get_chat_member_count(chat.id)
    except Exception:
        pass

    await state.update_data(channel_title=chat.title)
    await state.update_data(channel_id=chat.id)

    await message.answer(
        f"🔗 Channel found: {chat.title}\n"
        f"👤 Members: {members_count}\n"
        f"Save it?",
        reply_markup=accept_cancel_keyboard(AcceptActions.ADD_CHANNEL)
    )
    await state.set_state(ChangeWelcomeMessage.change_message)

@add_channel_router.callback_query(AcceptCallback.filter(F.action == AcceptActions.ADD_CHANNEL))
async def save_channel_callback(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel_id = data.get('channel_id')
    async with get_db() as db:
        service = SettingsDataService(db)
        await service.create(SettingsDataCreate(text=str(channel_id), tag=TagsEnums.CHANNEL_ID))
    await query.message.answer("✅ Saved Successfully, use buttons below", reply_markup=main_menu_keyboard())
    await state.clear()
    await query.answer()



