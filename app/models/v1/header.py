from app.models.v1.base import BaseModel
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

# Логотип сайта
class LogoModel(BaseModel):
    """
    Модель логотипа сайта.

    Атрибуты:
        file_url (str): URL или путь к файлу логотипа.
        alt_text (str): Альтернативный текст для логотипа.
    """
    __tablename__ = "logo"

    file_url: Mapped[str] = mapped_column(String(256), nullable=False)
    alt_text: Mapped[str] = mapped_column(String(128), nullable=True)

# Пункт меню
class MenuItemModel(BaseModel):
    """
    Модель пункта меню с поддержкой вложенности.

    Атрибуты:
        title (str): Название пункта меню.
        url (str): Ссылка.
        order (int): Порядок отображения.
        parent_id (int | None): ID родительского пункта меню (null для корневых).
    """
    __tablename__ = "menu_item"

    title: Mapped[str] = mapped_column(String(64), nullable=False)
    url: Mapped[str] = mapped_column(String(256), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("menu_item.id"), nullable=True)

# Контактная информация
class ContactInfoModel(BaseModel):
    """
    Модель контактной информации.

    Атрибуты:
        type (str): Тип контакта (phone, email и т.д.).
        value (str): Значение контакта.
    """
    __tablename__ = "contact_info"

    type: Mapped[str] = mapped_column(String(32), nullable=False)
    value: Mapped[str] = mapped_column(String(128), nullable=False) 