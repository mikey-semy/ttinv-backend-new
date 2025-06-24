"""
Провайдер аутентификации для админ-панели.

Обеспечивает безопасный доступ к админ-панели через проверку
учетных данных администраторов в базе данных.

Поддерживает:
- Аутентификацию по email/username и паролю
- Сессии для запоминания входа
- Проверку прав доступа
- Безопасный выход из системы
"""
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed

from app.core.connections.database import get_db_session
from app.core.connections.cache import get_redis_client
from app.core.security.password import PasswordHasher
from app.services.v1.auth.service import AuthService
from app.models.v1.users import UserRole


class CustomAuthProvider(AuthProvider):
    """
    Кастомный провайдер аутентификации для админ-панели.

    Использует существующую систему аутентификации приложения
    для проверки прав доступа администраторов.
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response | None:
        """
        Обрабатывает вход администратора в систему.

        Args:
            username (str): Имя пользователя или email
            password (str): Пароль
            remember_me (bool): Запомнить вход
            request (Request): HTTP запрос
            response (Response): HTTP ответ

        Returns:
            Response: HTTP ответ с результатом аутентификации

        Raises:
            LoginFailed: При неверных учетных данных или отсутствии прав админа
        """
        redis = await get_redis_client()
        async for session in get_db_session():
            try:
                service = AuthService(session, redis)

                # Получаем пользователя по логину
                user = await service.data_manager.get_user_by_identifier(username)

                if not user:
                    raise LoginFailed("Пользователь не найден")

                # Проверяем пароль
                if not user.hashed_password or not PasswordHasher.verify(user.hashed_password, password): 
                    raise LoginFailed("Неверный пароль")

                # Проверяем права администратора
                if not user.role == UserRole.ADMIN:
                    raise LoginFailed("Недостаточно прав для доступа к админ-панели")

                # Сохраняем данные в сессии
                request.session.update({
                    "username": username,
                    "user_id": user.id,
                    "is_admin": True
                })

                return response

            except Exception as e:
                raise LoginFailed(f"Ошибка аутентификации: {str(e)}")

    async def is_authenticated(
        self,
        request: Request,
    ) -> bool | None:
        """
        Проверяет, аутентифицирован ли пользователь.

        Args:
            request (Request): HTTP запрос

        Returns:
            bool: True если пользователь аутентифицирован и имеет права админа
        """
        redis = await get_redis_client()
        async for session in get_db_session():
            try:
                username = request.session.get("username")
                if not username:
                    return False

                service = AuthService(session, redis)
                user = await service.data_manager.get_user_by_identifier(username)

                if user and user.role == UserRole.ADMIN:
                    # Сохраняем пользователя в состоянии запроса
                    request.state.user = user
                    return True

                return False

            except Exception:
                return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        """
        Возвращает конфигурацию админ-панели.

        Args:
            request (Request): HTTP запрос

        Returns:
            AdminConfig: Конфигурация с настройками интерфейса
        """
        return AdminConfig(
            app_title="Tarot Bot Admin Panel",
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        """
        Возвращает информацию о текущем администраторе.

        Args:
            request (Request): HTTP запрос

        Returns:
            AdminUser: Информация об администраторе для отображения в интерфейсе
        """
        user = request.state.user
        photo_url = (
            "https://static.vecteezy.com/system/resources/previews/009/292/244/"
            "non_2x/default-avatar-icon-of-social-media-user-vector.jpg"
        )

        return AdminUser(
            username=user.username or user.email,
            photo_url=photo_url
        )

    async def logout(self, request: Request, response: Response) -> Response:
        """
        Обрабатывает выход администратора из системы.

        Args:
            request (Request): HTTP запрос
            response (Response): HTTP ответ

        Returns:
            Response: HTTP ответ с очищенной сессией
        """
        request.session.clear()
        return response
