from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import async_session


class DatabaseAbstract(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplemented

    @abstractmethod
    async def find_one(self, **filters):
        raise NotImplemented

    @abstractmethod
    async def update_one_by_id(self, data_id: UUID, **data):
        raise NotImplemented

    @abstractmethod
    async def delete_one(self, **filters):
        raise NotImplemented

    @abstractmethod
    async def find_all(self):
        raise NotImplemented


class SQLAlchemyRepository(DatabaseAbstract):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data)
        await self.session.execute(stmt)
        return 'ok'

    async def find_one(self, **filters):
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.execute(stmt)
        result = res.scalars().first()
        if result:
            return result.to_read_model()

    async def update_one_by_id(self, data_id: UUID, **data):
        stmt = update(self.model).values(**data).where(self.model.id == data_id)
        await self.session.execute(stmt)
        return 'ok'

    async def delete_one(self, **filters):
        await self.session.execute(delete(self.model).where(**filters))
        return 'ok'

    async def find_all(self):
        res = await self.session.execute(select(self.model))
        result = [i.to_read_model() for i in res.scalars().all()]
        return result

    async def find_all_filter(self, **filters):
        res = await self.session.execute(select(self.model).filter_by(**filters))
        result = [i.to_read_model() for i in res.scalars().all()]
        return result
