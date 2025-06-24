from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.v1.users import UserModel
from app.services.v1.base import BaseEntityManager
from app.schemas.v1.base import BaseSchema

class AuthDataManager(BaseEntityManager[BaseSchema]):
    """
    Менеджер данных для поиска пользователей по username или email.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, schema=BaseSchema, model=UserModel)

    async def get_user_by_identifier(self, identifier: str) -> Optional[UserModel]:
        """
        Получает пользователя по username или email.
        """
        # Поиск по username
        user = await self.get_model_by_field("username", identifier)
        if user:
            return user

        # Поиск по email (если поле есть)
        user = await self.get_model_by_field("email", identifier)
        if user:
            return user

        return None 