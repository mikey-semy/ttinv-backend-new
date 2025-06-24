"""
Инициализация моделей SQLAlchemy.

Этот модуль импортирует все модели данных для их регистрации
в системе миграций и обеспечения доступа к ним из других частей приложения.
"""
from app.models.v1.base import BaseModel
from app.models.v1.users import UserModel
from app.models.v1.header import LogoModel, MenuItemModel, ContactInfoModel

# Список всех моделей для использования в миграциях
__all__ = [
    "BaseModel",
    "UserModel",
    "LogoModel",
    "MenuItemModel",
    "ContactInfoModel"

]
