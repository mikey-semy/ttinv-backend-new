from starlette_admin.contrib.sqla import Admin, ModelView
from app.models.v1.header import Logo, MenuItem, ContactInfo
from app.models.v1.base import Base
from app.core.connections.database import database_client
from app.core.settings import settings
from .auth import CustomAuthProvider

engine = database_client.get_engine()
session_factory = database_client.get_session_factory()

admin = Admin(
    engine=engine,
    session_maker=session_factory,
    base_model=Base,
    auth_provider=CustomAuthProvider(),
    **settings.admin_params,
)
admin.add_view(ModelView(Logo))
admin.add_view(ModelView(MenuItem))
admin.add_view(ModelView(ContactInfo)) 