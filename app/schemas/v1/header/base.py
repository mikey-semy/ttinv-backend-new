from app.schemas.v1.base import BaseSchema, BaseRequestSchema
from typing import Optional

class LogoBaseSchema(BaseSchema):
    """
    Базовая схема логотипа.

    Атрибуты:
        file_url (str): URL или путь к файлу логотипа.
        alt_text (str | None): Альтернативный текст.
    """
    file_url: str
    alt_text: Optional[str] = None

class MenuItemBaseSchema(BaseSchema):
    """
    Базовая схема пункта меню.

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

class ContactInfoBaseSchema(BaseSchema):
    """
    Базовая схема контактной информации.

    Атрибуты:
        type (str): Тип контакта (phone, email и т.д.).
        value (str): Значение контакта.
    """
    type: str
    value: str 