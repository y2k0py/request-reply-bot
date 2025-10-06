from aiogram import Router, Bot
from aiogram.types import ChatJoinRequest

from app.database.crud.settings_data import SettingsDataService
from app.database.db.session import get_db
from app.database.enums import TagsEnums
from app.keyboards.request_to_channel import request_to_channel_keyboard

request_to_channel_router = Router()

@request_to_channel_router.chat_join_request()
async def request_to_channel(event: ChatJoinRequest, bot: Bot):
    async with get_db() as db:
        service = SettingsDataService(db)
        welcome_message = await service.get_last_data_by_tag(TagsEnums.WELCOME_MESSAGE)
        welcome_message_button_text = await service.get_last_data_by_tag(TagsEnums.WELCOME_MESSAGE_BUTTON)
        welcome_message_button_url = await service.get_last_data_by_tag(TagsEnums.WELCOME_BUTTON_URL)

    try:
        await bot.send_message(
            chat_id=event.from_user.id,
            text=welcome_message.text,
            reply_markup=request_to_channel_keyboard(
                welcome_message_button_text.text,
                welcome_message_button_url.text
            )
        )
    except Exception as e:
        print(f"Failed to send message: {e}")