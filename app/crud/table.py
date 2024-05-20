from fastapi import APIRouter

from app.db.db import engine, Base, engine_docker


router = APIRouter(prefix='/tables')


@router.post('/create_table', tags=['TABLE'])
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.post('/drop_table', tags=['TABLE'])
async def drop_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@router.post('/create_docker_table', tags=['DOCKER'])
async def create_docker_table():
    async with engine_docker.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.post('/drop_docker_table', tags=['DOCKER'])
async def drop_docker_table():
    async with engine_docker.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)