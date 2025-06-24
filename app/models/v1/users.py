from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.models.v1.base import BaseModel
import enum

class UserRole(str, enum.Enum):
    """
    Роли пользователей.
    """
    USER = "user"
    ADMIN = "admin"

class UserModel(BaseModel):
    """
    Модель пользователя сайта.

    Атрибуты:
        email (str): Электронная почта пользователя.
        username (str): Имя пользователя.
        hashed_password (str): Хэшированный пароль.
        role (UserRole): Роль пользователя (user/admin).
        is_active (bool): Активен ли пользователь.
    """
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False) 