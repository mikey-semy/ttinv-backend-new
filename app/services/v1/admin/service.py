"""
Сервис для управления администраторами системы.

Предоставляет функционал для:
- Инициализации администратора при старте приложения
- Управления правами администраторов
- Создания и обновления учетных записей администраторов
"""
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.v1.base import BaseService
from app.services.v1.users.data_manager import UserDataManager
from app.models.v1.users import UserModel, UserRole
from app.core.security.password import PasswordHasher
from app.core.settings import settings
logger = logging.getLogger(__name__)

class AdminInitService(BaseService):
    """
    Сервис для инициализации и управления администраторами.
    
    Attributes:
        session (AsyncSession): Сессия базы данных
        data_manager (UserDataManager): Менеджер данных пользователей
    """
    def __init__(self, session: AsyncSession):
        """
        Инициализирует сервис.
        
        Args:
            session (AsyncSession): Сессия базы данных
        """
        self.session = session
        self.data_manager = UserDataManager(session)

    async def initialize_admin(self, admin_email: str, password: Optional[str] = None, username: str = "admin") -> None:
        """
        Инициализирует администратора системы.

        Если администратор уже существует — пропускает создание.
        Если пользователь с email существует — назначает ему роль админа.
        Если не существует — создает нового пользователя-админа.

        Args:
            admin_email (str): Email администратора
            password (str, optional): Пароль администратора. Если не указан, 
                                   берется из настроек приложения
            username (str, optional): Имя пользователя. По умолчанию "admin"
            
        Returns:
            None
        """

        if not password:
            if not settings.ADMIN_PASSWORD:
                logger.error("Пароль администратора не указан в настройках")
                return
            password = settings.ADMIN_PASSWORD.get_secret_value()

        # Проверяем, есть ли уже администраторы
        admins = await self.data_manager.filter_by(role=UserRole.ADMIN)
        if admins:
            logger.info("Администратор уже существует: %s", [a.email for a in admins])
            return
        
        # Ищем пользователя с указанным email
        user = await self.data_manager.get_model_by_field("email", admin_email)
        if user:
            # Назначаем роль администратора
            user.role = UserRole.ADMIN
            user.hashed_password = PasswordHasher.hash_password(password)
            await self.session.commit()
            logger.info("Пользователь %s назначен администратором", admin_email)
        else:
            # Создаём нового пользователя-админа
            new_user = UserModel(
                email=admin_email,
                username=username,
                hashed_password=PasswordHasher.hash_password(password),
                role=UserRole.ADMIN,
                is_active=True,
            )
            await self.data_manager.add_one(new_user)
            logger.info("Создан новый администратор: %s", admin_email)