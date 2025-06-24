"""
Модуль содержит контейнер зависимостей.
"""

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from .providers.admin import AdminProvider
from .providers.auth import AuthProvider
from .providers.cache import RedisMiddlewareProvider, RedisProvider
from .providers.database import DatabaseProvider
from .providers.messaging import RabbitMQProvider
from .providers.storage import S3Provider


container = make_async_container(

    AdminProvider(),
    FastapiProvider(),
    DatabaseProvider(),
    RabbitMQProvider(),
    RedisProvider(),
    RedisMiddlewareProvider(),
    S3Provider(),
    AuthProvider(),
)
