from app.services.v1.base import BaseService
from app.services.v1.users.data_manager import UserDataManager
from app.models.v1.users import UserModel, UserRole
from app.core.security.password import PasswordHasher

class AdminInitService(BaseService):
    """
    Сервис для инициализации администратора системы.
    Использует только универсальные методы базового менеджера данных.
    """
    def __init__(self, session):
        super().__init__(session)
        self.data_manager = UserDataManager(session)

    async def initialize_admin(self, admin_email: str, password: str, username: str = "admin") -> None:
        """
        Инициализирует администратора системы.
        Если администратор уже существует — пропускает создание.
        Если пользователь с email существует — назначает ему роль админа.
        Если не существует — создает нового пользователя-админа.
        """
        # Проверяем, есть ли уже администраторы
        admins = await self.data_manager.filter_by(role=UserRole.ADMIN)
        if admins:
            return
        # Ищем пользователя с указанным email
        user = await self.data_manager.get_model_by_field("email", admin_email)
        if user:
            user.role = UserRole.ADMIN
            user.hashed_password = PasswordHasher.hash_password(password)
            await self.session.commit()
        else:
            new_user = UserModel(
                email=admin_email,
                username=username,
                hashed_password=PasswordHasher.hash_password(password),
                role=UserRole.ADMIN,
                is_active=True,
            )
            await self.data_manager.add_one(new_user) 