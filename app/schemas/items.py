from pydantic import BaseModel, UUID4


class ItemsFull(BaseModel):
    id: UUID4
    title: str
    price: float
    picture: str
    specifications: str
    user_id: UUID4


class ItemsIn(BaseModel):
    title: str
    price: float
    picture: str
    specifications: str


class ItemsOut(BaseModel):
    title: str
    price: float
    picture: str
    specifications: str
