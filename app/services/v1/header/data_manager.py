from app.services.v1.base import BaseEntityManager
from app.models.v1.header import LogoModel, MenuItemModel, ContactInfoModel
from app.schemas.v1.header.base import LogoBaseSchema, MenuItemBaseSchema, ContactInfoBaseSchema
from sqlalchemy.ext.asyncio import AsyncSession

class LogoDataManager(BaseEntityManager[LogoBaseSchema]):
    """
    Менеджер данных для логотипа сайта.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, LogoBaseSchema, LogoModel)

class MenuItemDataManager(BaseEntityManager[MenuItemBaseSchema]):
    """
    Менеджер данных для пунктов меню.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, MenuItemBaseSchema, MenuItemModel)

class ContactInfoDataManager(BaseEntityManager[ContactInfoBaseSchema]):
    """
    Менеджер данных для контактной информации.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, ContactInfoBaseSchema, ContactInfoModel) 