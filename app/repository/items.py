from app.models.items import Item

from app.repository.database import SQLAlchemyRepository


class ItemsRepository(SQLAlchemyRepository):
    model = Item
