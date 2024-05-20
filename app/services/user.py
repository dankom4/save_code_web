from typing import Annotated

import fastapi
import jwt
from fastapi import Depends, HTTPException, status, Response, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from passlib.context import CryptContext

from app.schemas.ouath2 import OAuth2PasswordBearerWithCookieOnly, Token
from app.schemas.users import UserIn
from app.utils.unitofwork import UnitOfWork
from app.schemas.items import ItemsIn

router = APIRouter(prefix='/auth')
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearerWithCookieOnly(tokenUrl='/auth/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def __verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    async def __get_password_hash(self, password):
        return pwd_context.hash(password)

    async def __get_user(self, email: str):
        async with self.uow:
            res = await self.uow.user.find_one(email=email)
            return res

    async def __create_token(self, data: dict):
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    async def __authenticate_user(self, email: str, password: str):
        user = await self.__get_user(email)
        if not user:
            return False
        if not await self.__verify_password(password, user.password):
            return False
        return user

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            email = payload.get('email')
            if email is None:
                raise HTTPException(status_code=401)
        except JWTError:
            raise HTTPException(status_code=401)
        user = await self.__get_user(email)
        if user is None:
            raise HTTPException(status_code=401)
        return user

    @router.post("/token")
    async def login_for_access_token(self,
                                     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                     response: Response
                                     ):
        user = await self.__authenticate_user(email=form_data.username, password=form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = await self.__create_token({'email': form_data.username})
        response.set_cookie(key="Authorization",
                            value="Bearer {}".format(fastapi.encoders.jsonable_encoder(access_token)),
                            httponly=True, )
        return Token(access_token=access_token, token_type='bearer')

    async def add_user(self, users: UserIn):
        user_dict = users.model_dump()
        async with self.uow:
            user_dict['password'] = pwd_context.hash(user_dict['password'])
            user = await self.uow.user.add_one(user_dict)
            await self.uow.commit()
            return user

    async def get_users(self):
        async with self.uow:
            users = await self.uow.user.find_all()
            return users

    @staticmethod
    async def logout(current_user, response: Response):
        response.delete_cookie(key='Authorization')
        return F"USER: {current_user.username} LOGOUT"

    async def add_items(self, item: ItemsIn, current_user):
        item_dict = item.model_dump()
        item_dict['user_id'] = current_user.id
        async with self.uow:
            item = await self.uow.item.add_one(item_dict)
            await self.uow.commit()
            return item

    async def get_items(self, user_id: str):
        async with self.uow:
            res = await self.uow.item.find_all_filter(user_id=user_id)
            return res

    async def sing_in(self, users: UserIn, response: Response):
        user_dict = users.model_dump()
        async with self.uow:
            user_dict['password'] = pwd_context.hash(user_dict['password'])
            await self.uow.user.add_one(user_dict)
            access_token = await self.__create_token({'email': users.email})
            response.set_cookie(key="Authorization",
                                value="Bearer {}".format(fastapi.encoders.jsonable_encoder(access_token)),
                                httponly=True, )
            await self.uow.commit()
