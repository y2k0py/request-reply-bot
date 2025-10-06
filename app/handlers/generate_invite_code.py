from datetime import timedelta, datetime, UTC, timezone

from aiogram import Router
from aiogram.filters import Command

from app.database.crud.invite_code import InviteCodeService
import secrets

from app.database.crud.user import UserService
from app.database.db.session import get_db
from app.database.schemas.invite_code import InviteCodeCreate
from app.handlers.start import hash_secret

invite_code_router = Router()

@invite_code_router.message(Command('generate_invite_code'))
async def generate_invite_code_dev(message):

    async with get_db() as db:
        user_service = UserService(db)
        user = await user_service.get_by_telegram_id(str(message.from_user.id))
        if not user:
            return

        message_to_edit = await message.answer("Generating invite code...")
        code = secrets.token_urlsafe(InviteCodeService.CODE_LENGTH)
        hashed_code = hash_secret(code)
        invite_code_service = InviteCodeService(db)
        await invite_code_service.create(InviteCodeCreate(
            code_hash=hashed_code,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=InviteCodeService.CODE_EXPIRE_AFTER_SECONDS))
        )
        bot = message.bot
        bot_user = await bot.get_me()
        bot_username = bot_user.username

        await message_to_edit.edit_text(f"✅ Generated link: \n"
                                        f"t.me/{bot_username}?start={code}\n"
                                        f"Code expires after {round(InviteCodeService.CODE_EXPIRE_AFTER_SECONDS / 60)} minutes")

