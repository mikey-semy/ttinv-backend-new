from starlette_admin.contrib.sqla import ModelView
from app.models.v1.header import LogoModel, MenuItemModel, ContactInfoModel
from .base import admin

admin.add_view(ModelView(LogoModel))
admin.add_view(ModelView(MenuItemModel))
admin.add_view(ModelView(ContactInfoModel)) 