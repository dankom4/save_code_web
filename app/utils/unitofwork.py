from abc import ABC, abstractmethod
from typing import Type

from app.db.db import async_session
from app.repository.items import ItemsRepository
from app.repository.user import UserRepository


class IUnitOfWork(ABC):
    user: Type[UserRepository]
    item: Type[ItemsRepository]
    
    @abstractmethod
    def __init__(self):
        raise NotImplemented

    @abstractmethod
    async def __aenter__(self):
        raise NotImplemented

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplemented

    @abstractmethod
    async def commit(self):
        raise NotImplemented

    @abstractmethod
    async def rollback(self):
        raise NotImplemented


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UserRepository(self.session)
        self.item = ItemsRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
