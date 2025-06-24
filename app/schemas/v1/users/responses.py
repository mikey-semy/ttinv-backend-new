"""
Модуль схем пользователя.
"""

from app.schemas.v1.base import BaseResponseSchema
from app.schemas.v1.pagination import Page

from .base import UserDetailDataSchema, UserSchema


class UserResponseSchema(BaseResponseSchema):
    """
    Схема ответа с данными пользователя.

    Attributes:
        message (str): Сообщение о результате операции.
        data (UserDetailDataSchema): Данные пользователя.
    """

    message: str = "Пользователь успешно получен."
    data: UserDetailDataSchema


class UserUpdateResponseSchema(BaseResponseSchema):
    """
    Схема ответа при обновлении данных пользователя.

    Attributes:
        message (str): Сообщение о результате операции.
        data (UserDetailDataSchema): Обновленные данные пользователя.
    """

    message: str = "Данные пользователя успешно обновлены"
    data: UserDetailDataSchema


class UserRoleUpdateResponseSchema(UserUpdateResponseSchema):
    """
    Схема ответа при обновлении роли пользователя.

    Attributes:
        message (str): Сообщение о результате операции.
        data (UserDetailDataSchema): Обновленные данные пользователя.
    """

    message: str = "Роль пользователя успешно обновлена"


class UserActiveUpdateResponseSchema(UserUpdateResponseSchema):
    """
    Схема ответа при обновлении статуса активности пользователя.

    Attributes:
        message (str): Сообщение о результате операции.
        data (UserDetailDataSchema): Обновленные данные пользователя.
    """

    message: str = "Статус активности пользователя успешно обновлен"


class UserDeleteResponseSchema(BaseResponseSchema):
    """
    Схема ответа при удалении пользователя.

    Attributes:
        message (str): Сообщение о результате операции.
    """

    message: str = "Пользователь успешно удален"


class UserListResponseSchema(BaseResponseSchema):
    """
    Схема ответа со списком пользователей.

    Attributes:
        message (str): Сообщение о результате операции
        data (Page[UserSchema]): Список пользователей
    """

    message: str = "Список пользователей успешно получен"
    data: Page[UserSchema]
