from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database.enums import TagsEnums
from app.database.models import Base


class SettingsData(Base):
    __tablename__ = "settings_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(nullable=False)
    tag: Mapped[TagsEnums] = mapped_column(Enum(TagsEnums), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))



