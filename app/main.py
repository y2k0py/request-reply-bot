import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.handlers.add_channel import add_channel_router
from app.handlers.cancel import cancel_router
from app.handlers.change_welcome_message import welcome_message_router
from app.handlers.generate_invite_code import invite_code_router
from app.handlers.generate_message_with_button import create_message_with_button_router
from app.handlers.request_to_channel import request_to_channel_router
from app.handlers.start import start_router

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)


    dp.include_routers(start_router)
    dp.include_router(invite_code_router)
    dp.include_router(welcome_message_router)
    dp.include_router(request_to_channel_router)
    dp.include_router(add_channel_router)
    dp.include_router(create_message_with_button_router)
    dp.include_router(cancel_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    print('project starts')
    asyncio.run(main())