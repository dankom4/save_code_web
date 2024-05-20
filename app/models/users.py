from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.models.items import Item

from app.schemas.users import UserFull


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str]
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default='user')
    is_active: Mapped[bool] = mapped_column(default=True)
    items: Mapped[list['Item']] = relationship(backref='items', passive_deletes=True, lazy="selectin")

    def to_read_model(self):
        return UserFull(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            role=self.role,
            is_active=self.is_active,
            items=self.items
        )
