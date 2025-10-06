from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.database.enums import TagsEnums


class SettingsDataCreate(BaseModel):
    text: str
    tag: TagsEnums
    created_at: datetime | None = None

class SettingsDataUpdate(BaseModel):
    text: str | None = None
    tag: TagsEnums | None = None


class SettingsDataRead(SettingsDataCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
