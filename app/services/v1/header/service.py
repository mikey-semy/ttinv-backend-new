from app.services.v1.base import BaseService
from app.services.v1.header.data_manager import LogoDataManager, MenuItemDataManager, ContactInfoDataManager
from sqlalchemy.ext.asyncio import AsyncSession

class LogoService(BaseService):
    """
    Сервис для работы с логотипом сайта.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.data_manager = LogoDataManager(session)

class MenuItemService(BaseService):
    """
    Сервис для работы с пунктами меню.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.data_manager = MenuItemDataManager(session)

class ContactInfoService(BaseService):
    """
    Сервис для работы с контактной информацией.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.data_manager = ContactInfoDataManager(session) 