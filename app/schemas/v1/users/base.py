"""
Модуль схем пользователя.
"""

from typing import Optional

from pydantic import EmailStr

from app.models.v1.users import UserRole
from app.schemas.v1.base import BaseSchema, CommonBaseSchema


class UserSchema(BaseSchema):
    """
    Схема пользователя.

    Attributes:
        username (str): Имя пользователя.
        role (UserRole): Роль пользователя.
        email (EmailStr): Email пользователя.
        is_active (bool): Флаг активности пользователя.
    """

    username: str
    role: UserRole
    email: EmailStr
    is_active: bool = True


class CurrentUserSchema(CommonBaseSchema):
    """
    Схема текущего аутентифицированного пользователя без чувствительных данных.

    Attributes:
        id (int): ID пользователя
        username (str): Имя пользователя (логин)
        email (EmailStr): Email пользователя
        role (UserRole): Роль пользователя
        is_active (bool): Активен ли пользователь
    """

    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool = True
    is_verified: bool = False


class UserDetailDataSchema(BaseSchema):
    """
    Схема детальной информации о пользователе.

    Attributes:
        id (int): Идентификатор пользователя.
        username (str): Имя пользователя.
        email (str): Email пользователя.
        role (UserRole): Роль пользователя.
        is_active (bool): Активен ли пользователь.
    """

    username: str
    email: str
    role: UserRole
    is_active: bool = True
