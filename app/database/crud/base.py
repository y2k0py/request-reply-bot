from typing import TypeVar, Generic, Type, Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession = None):
        self.model = model
        self.session = session

    async def get(self, obj_id: int) -> Optional[ModelType]:
        return await self.session.get(self.model, obj_id)

    async def get_all(self) -> Sequence[ModelType]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, data: CreateSchemaType, flush: bool = False) -> ModelType:
        obj = self.model(**data.model_dump())
        self.session.add(obj)
        if flush:
            await self.session.flush()
            return obj
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj_id: int, data: UpdateSchemaType) -> Optional[ModelType]:
        obj = await self.get(obj_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool:
        obj = await self.get(obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
