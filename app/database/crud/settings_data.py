from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.enums import TagsEnums
from app.database.models.settings_data import SettingsData
from app.database.schemas.settings_data import SettingsDataCreate, SettingsDataUpdate


class SettingsDataService(BaseService[SettingsData, SettingsDataCreate, SettingsDataUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(SettingsData, session)

    async def get_last_data_by_tag(self, tag: TagsEnums)-> SettingsData | None:
        result = await self.session.execute(
            select(SettingsData).where(SettingsData.tag == tag).order_by(SettingsData.created_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

