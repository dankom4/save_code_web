from uuid import UUID,  uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from app.schemas.items import ItemsFull


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    picture: Mapped[str]
    specifications: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    def to_read_model(self):
        return ItemsFull(
            id=self.id,
            title=self.title,
            price=self.price,
            picture=self.picture,
            specifications=self.specifications,
            user_id=self.user_id,
        )