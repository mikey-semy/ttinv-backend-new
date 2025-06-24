from sqlalchemy.ext.asyncio import AsyncSession
from app.services.v1.auth.data_manager import AuthDataManager
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """
    Сервис для аутентификации админки.
    """
    def __init__(self, session: AsyncSession, redis):
        self.session = session
        self.redis = redis
        self.data_manager = AuthDataManager(session)