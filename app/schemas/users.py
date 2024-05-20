from pydantic import EmailStr, BaseModel, UUID4


class UserFull(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    password: str
    role: str = 'user'
    is_active: bool = True


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    username: str
    email: EmailStr
    items: list = []


class UserOauth2(BaseModel):
    grant_type: str | None = None
    username: str | EmailStr
    password: str
    scopes: list = []
    client_id: str | None = None
    client_secret: str | None = None