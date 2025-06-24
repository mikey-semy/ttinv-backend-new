from app.schemas.v1.base import BaseRequestSchema
from app.schemas.v1.header.base import LogoBaseSchema, MenuItemBaseSchema, ContactInfoBaseSchema
from typing import Optional

class LogoCreateSchema(BaseRequestSchema):
    """
    Схема для создания логотипа.

    Атрибуты:
        file_url (str): URL или путь к файлу логотипа.
        alt_text (str | None): Альтернативный текст.
    """
    file_url: str
    alt_text: Optional[str] = None

class LogoUpdateSchema(BaseRequestSchema):
    """
    Схема для обновления логотипа.

    Атрибуты:
        file_url (str): URL или путь к файлу логотипа.
        alt_text (str | None): Альтернативный текст.
    """
    file_url: Optional[str] = None
    alt_text: Optional[str] = None

class MenuItemCreateSchema(BaseRequestSchema):
    """
    Схема для создания пункта меню.

    Атрибуты:
        title (str): Название пункта меню.
        url (str): Ссылка.
        order (int): Порядок отображения.
        parent_id (int | None): ID родительского пункта меню.
    """
    title: str
    url: str
    order: int
    parent_id: Optional[int] = None

class MenuItemUpdateSchema(BaseRequestSchema):
    """
    Схема для обновления пункта меню.

    Атрибуты:
        title (str): Название пункта меню.
        url (str): Ссылка.
        order (int): Порядок отображения.
        parent_id (int | None): ID родительского пункта меню.
    """
    title: Optional[str] = None
    url: Optional[str] = None
    order: Optional[int] = None
    parent_id: Optional[int] = None

class ContactInfoCreateSchema(BaseRequestSchema):
    """
    Схема для создания контактной информации.

    Атрибуты:
        type (str): Тип контакта (phone, email и т.д.).
        value (str): Значение контакта.
    """
    type: str
    value: str

class ContactInfoUpdateSchema(BaseRequestSchema):
    """
    Схема для обновления контактной информации.

    Атрибуты:
        type (str): Тип контакта (phone, email и т.д.).
        value (str): Значение контакта.
    """
    type: Optional[str] = None
    value: Optional[str] = None 