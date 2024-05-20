from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(url='postgresql+asyncpg://postgres:postgresql@localhost/postgres')
engine_docker = create_async_engine(url='postgresql+asyncpg://username:password@db/dan')

async_session = async_sessionmaker(engine_docker, expire_on_commit=False)


class Base(DeclarativeBase):
    def __repr__(self):
        cols = []
        for col in self.__table__.columns.key():
            cols.append(f'\n{col}={getattr(self, col)}')
        return f'\n<{self.__class__.__name__}> {",".join(cols)}\n'
