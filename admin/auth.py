from starlette_admin.auth import AuthProvider, AdminUser, AdminConfig
from starlette_admin.exceptions import LoginFailed
from starlette.requests import Request
from starlette.responses import Response
from app.core.connections.database import get_db_session
from app.core.connections.cache import get_redis_client
from app.core.security.password import PasswordHasher
from app.models.v1.users import UserRole, UserModel
from sqlalchemy import select

class CustomAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response | None:
        session = await anext(get_db_session())
        redis = await get_redis_client()
        stmt = select(UserModel).where((UserModel.email == username) | (UserModel.username == username))
        user = await session.scalar(stmt)
        if not user or not user.hashed_password or not PasswordHasher.verify(user.hashed_password, password):
            raise LoginFailed("Неверные учетные данные")
        if user.role != UserRole.ADMIN:
            raise LoginFailed("Недостаточно прав для доступа к админ-панели")
        request.session.update({
            "username": username,
            "user_id": user.id,
            "is_admin": True
        })
        return response

    async def is_authenticated(self, request: Request) -> bool | None:
        session = await anext(get_db_session())
        username = request.session.get("username")
        if not username:
            return False
        stmt = select(UserModel).where((UserModel.email == username) | (UserModel.username == username))
        user = await session.scalar(stmt)
        if user and user.role == UserRole.ADMIN:
            request.state.user = user
            return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        return AdminConfig(app_title="Админка сайта")

    def get_admin_user(self, request: Request) -> AdminUser:
        user = getattr(request.state, "user", None)
        return AdminUser(
            username=user.username if user else "admin",
            photo_url="/static/logo.png"
        )

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response 