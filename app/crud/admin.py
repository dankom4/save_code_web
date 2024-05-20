from fastapi import APIRouter


from app.services.user import UsersService
from app.services.item import ItemServices


router = APIRouter(prefix='/admin', tags=['ADMIN'])


@router.post('/all_users')
async def all_users():
    res = await UsersService().get_users()
    return res


@router.post('/all_items')
async def all_items():
    res = await ItemServices().get_items()
    return res
