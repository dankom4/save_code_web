from app.models.users import User

from app.repository.database import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
