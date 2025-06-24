from app.schemas.v1.base import BaseResponseSchema, ItemResponseSchema, ListResponseSchema
from app.schemas.v1.header.base import LogoBaseSchema, MenuItemBaseSchema, ContactInfoBaseSchema
from typing import List, Optional

class LogoResponseSchema(ItemResponseSchema[LogoBaseSchema]):
    """
    Ответ на запрос логотипа.

    Атрибуты:
        success (bool): Успешность операции.
        message (str): Сообщение.
        item (LogoBaseSchema): Данные логотипа.
    """
    pass

class LogoListResponseSchema(ListResponseSchema[LogoBaseSchema]):
    """
    Ответ на запрос списка логотипов.

    Атрибуты:
        success (bool): Успешность операции.
        message (str): Сообщение.
        items (List[LogoBaseSchema]): Список логотипов.
    """
    pass

class MenuItemResponseSchema(ItemResponseSchema[MenuItemBaseSchema]):
    """
    Ответ на запрос пункта меню.

    Атрибуты:
        success (bool): Успешность операции.
        message (str): Сообщение.
        item (MenuItemBaseSchema): Данные пункта меню.
    """
    pass

class MenuItemListResponseSchema(ListResponseSchema[MenuItemBaseSchema]):
    """
    Ответ на запрос списка пунктов меню.

    Атрибуты:
        success (bool): Успешность операции.
        message (str): Сообщение.
        items (List[MenuItemBaseSchema]): Список пунктов меню.
    """
    pass

class ContactInfoResponseSchema(ItemResponseSchema[ContactInfoBaseSchema]):
    """
    Ответ на запрос контактной информации.

    Атрибуты:
        success (bool): Успешность операции.
        message (str): Сообщение.
        item (ContactInfoBaseSchema): Данные контакта.
    """
    pass

class ContactInfoListResponseSchema(ListResponseSchema[ContactInfoBaseSchema]):
    """
    Ответ на запрос списка контактной информации.

    Атрибуты:
        success (bool): Успешность операции.
        message (str): Сообщение.
        items (List[ContactInfoBaseSchema]): Список контактов.
    """
    pass 