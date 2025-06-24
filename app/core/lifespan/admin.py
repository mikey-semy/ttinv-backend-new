"""
Модуль инициализации администратора при старте приложения.

Регистрирует обработчик для создания администратора
с указанными в настройках учетными данными.
"""
import logging

from fastapi import FastAPI

from app.core.lifespan.base import register_startup_handler
from app.core.dependencies.container import container
from app.core.settings import settings
from app.services.v1.admin.service import AdminInitService

logger = logging.getLogger("app.lifecycle.admin")


@register_startup_handler
async def initialize_admin(app: FastAPI) -> None:
    """
    Инициализация администратора при старте приложения.
    
    Создает администратора с учетными данными из настроек,
    если он еще не существует в системе.
    
    Args:
        app: Экземпляр FastAPI приложения
    """
    admin_email = settings.ADMIN_EMAIL
    
    if not admin_email:
        logger.info(
            "ADMIN_EMAIL не указан в настройках, пропускаем создание администратора"
        )
        return

    if not settings.ADMIN_PASSWORD:
        logger.error("ADMIN_PASSWORD не указан в настройках")
        return

    async with container() as request_container:
        admin_service = await request_container.get(AdminInitService)
        await admin_service.initialize_admin(
            admin_email=admin_email,
            password=settings.ADMIN_PASSWORD.get_secret_value()
        ) 