"""
Менеджер данных для работы с пользователями.

Работает только с моделями SQLAlchemy. Преобразование в схемы - задача сервисного слоя.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.v1.users import UserModel
from app.schemas.v1.users import UserSchema
from app.services.v1.base import BaseEntityManager

class UserDataManager(BaseEntityManager[UserSchema]):
    """
    Менеджер данных для композитных операций с пользователями.
    Работает только с моделями SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session,schema=UserSchema, model=UserModel)

