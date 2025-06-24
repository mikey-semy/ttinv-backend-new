"""
Модуль инициализации Starlette Admin

"""

from starlette_admin.contrib.sqla import Admin
from app.core.settings import settings
from admin.auth import CustomAuthProvider
from app.core.connections.database import database_client

admin = Admin(
    engine=database_client.get_engine(),
    auth_provider=CustomAuthProvider(),
    **settings.admin_params,
) 