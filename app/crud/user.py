from typing import Annotated

from fastapi import APIRouter, Response, Depends

from app.models.users import User
from app.schemas.items import ItemsIn
from app.schemas.users import UserIn, UserOauth2

from app.services.user import UsersService


router = APIRouter(prefix='/user', tags=['USER'])


@router.post('/create_user')
async def create_user(users: UserIn):
    user = await UsersService().add_user(users)
    return user


@router.post('/login')
async def login(users: UserIn, response: Response):
    await UsersService().login_for_access_token(form_data=UserOauth2(username=users.email, password=users.password),
                                                response=response)
    return f'USER: {users.username} LOGIN'


@router.post('/sing_in')
async def sing_in(users: UserIn, response: Response):
    await UsersService().sing_in(users=users, response=response)
    return f'USER: {users.username} CREATED AND LOGIN'


@router.get('/read_me')
async def read_user(current_user: Annotated[User, Depends(UsersService().get_current_user)]):
    return current_user


@router.post('/logout')
async def logout(current_user: Annotated[User, Depends(UsersService().get_current_user)], response: Response):
    res = await UsersService().logout(current_user=current_user, response=response)
    return res


@router.post('/add_item')
async def add_item(item: ItemsIn, current_user: Annotated[User, Depends(UsersService().get_current_user)]):
    user = await UsersService().add_items(item=item, current_user=current_user)
    return user


@router.get('/get_all_my_items')
async def get_all_my_items(current_user: Annotated[User, Depends(UsersService().get_current_user)]):
    res = await UsersService().get_items(current_user.id)
    return res
