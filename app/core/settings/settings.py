import logging
from typing import Any, Dict, List

from pydantic import AmqpDsn, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.lifespan import lifespan
from app.core.settings.logging import LoggingSettings
from app.core.settings.paths import PathSettings

env_file_path, app_env = PathSettings.get_env_file_and_type()

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Настройки приложения

    """

    # Виртуальное окружение приложения
    app_env: str = app_env

    logging: LoggingSettings = LoggingSettings()
    paths: PathSettings = PathSettings()

    # Настройки приложения
    TITLE: str = "TechTransInvest"
    DESCRIPTION: str = ""
    VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    @property
    def app_params(self) -> dict:
        """
        Параметры для инициализации FastAPI приложения.

        Returns:
            Dict с настройками FastAPI
        """
        return {
            "title": self.TITLE,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "swagger_ui_parameters": {"defaultModelsExpandDepth": -1},
            "root_path": "",
            "lifespan": lifespan,
        }

    @property
    def uvicorn_params(self) -> dict:
        """
        Параметры для запуска uvicorn сервера.

        Returns:
            Dict с настройками uvicorn
        """
        return {
            "host": self.HOST,
            "port": self.PORT,
            "proxy_headers": True,
            "log_level": "debug",
        }

    # Настройки админа
    ADMIN_EMAIL: str = ""
    ADMIN_IDS: List[str] = []
    ADMIN_PASSWORD: SecretStr
    ADMIN_TITLE: str = "TechTransInvest Admin"
    ADMIN_LOGIN_LOGO_URL: str = "https://storage.yandexcloud.net/ttinv/admin_logo.png"
    ADMIN_DEBUG: bool = True

    @property
    def admin_params(self) -> dict:
        """
        Параметры для инициализации Starlette Admin.
        
        Returns:
            Dict с настройками админ-панели:
                title: Заголовок админ-панели
                login_logo_url: URL логотипа на странице входа
                debug: Режим отладки
        """
        return {
            "title": self.ADMIN_TITLE,
            "login_logo_url": self.ADMIN_LOGIN_LOGO_URL,
            "debug": self.ADMIN_DEBUG,
        }

    # Настройки аутентификации
    AUTH_URL: str = "api/v1/auth"
    TOKEN_TYPE: str = "Bearer"
    TOKEN_EXPIRE_MINUTES: int = 30  # 30 минут
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30 # 30 дней
    VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 часа
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_SECRET_KEY: SecretStr
    USER_INACTIVE_TIMEOUT: int = 900  # 15 минут

    # Настройки почты
    VERIFICATION_URL: str = "https://api.ttinv.ru/api/v1/register/verify-email/"
    PASSWORD_RESET_URL: str = "https://api.ttinv.ru/api/v1/auth/reset-password/"
    # PASSWORD_RESET_URL: str = "https://ttinv.ru/reset-password?token="
    LOGIN_URL: str = "https://api.ttinv.ru/api/v1/auth"
    SMTP_SERVER: str = "smtp.ttinv.ru"
    SMTP_PORT: int = 587
    SENDER_EMAIL: str = "noreply@ttinv.ru"
    SMTP_USERNAME: str = "admin"
    SMTP_PASSWORD: SecretStr

    # Настройки доступа в docs/redoc
    DOCS_ACCESS: bool = True
    DOCS_USERNAME: str = "admin"
    DOCS_PASSWORD: SecretStr

    # Настройки Redis
    REDIS_USER: str = "default"
    REDIS_PASSWORD: SecretStr
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_POOL_SIZE: int = 10

    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USER,
            password=self.REDIS_PASSWORD.get_secret_value(),
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=f"/{self.REDIS_DB}",
        )

    @property
    def redis_url(self) -> str:
        return str(self.redis_dsn)

    @property
    def redis_params(self) -> Dict[str, Any]:
        return {"url": self.redis_url, "max_connections": self.REDIS_POOL_SIZE}

    # Настройки базы данных
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @property
    def database_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @property
    def database_url(self) -> str:
        """
        Для alembic нужно строку с подключением к БД
        """
        database_dsn = str(self.database_dsn)
        return database_dsn

    @property
    def engine_params(self) -> Dict[str, Any]:
        """
        Формирует параметры для создания SQLAlchemy engine
        """
        return {
            "echo": True,
        }

    @property
    def session_params(self) -> Dict[str, Any]:
        """
        Формирует параметры для создания SQLAlchemy session
        """
        return {
            "autocommit": False,
            "autoflush": False,
            "expire_on_commit": False,
            "class_": AsyncSession,
        }

    # Настройки RabbitMQ
    RABBITMQ_CONNECTION_TIMEOUT: int = 30
    RABBITMQ_EXCHANGE: str = "ttinv"
    RABBITMQ_USER: str
    RABBITMQ_PASS: SecretStr
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672

    @property
    def rabbitmq_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.RABBITMQ_USER,
            password=self.RABBITMQ_PASS.get_secret_value(),
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT,
        )

    @property
    def rabbitmq_url(self) -> str:
        """
        Для pika нужно строку с подключением к RabbitMQ
        """
        return str(self.rabbitmq_dsn)

    @property
    def rabbitmq_params(self) -> Dict[str, Any]:
        """
        Формирует параметры подключения к RabbitMQ.

        Returns:
            Dict с параметрами подключения к RabbitMQ
        """
        return {
            "url": self.rabbitmq_url,
            "connection_timeout": self.RABBITMQ_CONNECTION_TIMEOUT,
            "exchange": self.RABBITMQ_EXCHANGE,
        }

    # Настройки AWS
    AWS_SERVICE_NAME: str = "s3"
    AWS_REGION: str = "ru-central1"
    AWS_ENDPOINT: str = "https://storage.yandexcloud.net"
    AWS_BUCKET_NAME: str = "ttinv.data"
    AWS_ACCESS_KEY_ID: SecretStr
    AWS_SECRET_ACCESS_KEY: SecretStr

    @property
    def s3_params(self) -> Dict[str, Any]:
        """
        Формирует информацию о конфигурации S3.
        """
        return {
            "service_name": self.AWS_SERVICE_NAME,
            "aws_region": self.AWS_REGION,
            "aws_endpoint": self.AWS_ENDPOINT,
            "aws_bucket_name": self.AWS_BUCKET_NAME,
            "aws_access_key_id": self.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": self.AWS_SECRET_ACCESS_KEY,
        }

    # Настройки Yandex GPT
    REDIS_CHAT_HISTORY_TTL: int = 86400 # 24 часа
    AI_STORAGE_TYPE: str = "redis"
    YANDEX_PRE_INSTRUCTIONS: str = "Ты ассистент, помогающий пользователю."
    YANDEX_TEMPERATURE: float = 0.6
    YANDEX_MAX_TOKENS: int = 2000
    YANDEX_MODEL_NAME: str = "llama"
    YANDEX_MODEL_VERSION: str = "rc"
    YANDEX_API_URL: str = (
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    )
    YANDEX_API_KEY: SecretStr
    YANDEX_FOLDER_ID: SecretStr

    @property
    def yandex_model_uri(self) -> str:
        """
        Формирует URI модели Yandex GPT.

        Returns:
            str: URI в формате gpt://{folder_id}/{model_name}/{model_version}
        """
        return f"gpt://{self.YANDEX_FOLDER_ID.get_secret_value()}/{self.YANDEX_MODEL_NAME}/{self.YANDEX_MODEL_VERSION}"

    # Настройки CORS
    ALLOW_ORIGINS: List[str] = []
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]

    @property
    def cors_params(self) -> Dict[str, Any]:
        """
        Формирует параметры CORS для FastAPI.

        Returns:
            Dict с настройками CORS middleware
        """
        return {
            "allow_origins": self.ALLOW_ORIGINS,
            "allow_credentials": self.ALLOW_CREDENTIALS,
            "allow_methods": self.ALLOW_METHODS,
            "allow_headers": self.ALLOW_HEADERS,
        }

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="allow",
    )
