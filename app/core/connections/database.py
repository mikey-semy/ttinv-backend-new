"""
Модуль для работы с базой данных.

Предоставляет классы для управления подключением к PostgreSQL через SQLAlchemy:
- DatabaseClient: Клиент для установки и управления подключением к базе данных
- DatabaseContextManager: Контекстный менеджер для автоматического управления сессиями БД
- AsyncSessionFactory: Фабрика для создания асинхронных сессий

Модуль использует настройки подключения из конфигурации приложения и реализует
базовые интерфейсы из модуля base.py.
"""

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from typing import cast, Optional
import asyncio

from app.core.settings import Config, settings

from .base import BaseClient, BaseContextManager


class DatabaseClient(BaseClient):
    """
    Singleton клиент для работы с базой данных.

    Реализует паттерн Singleton для обеспечения единого глобального подключения
    к PostgreSQL через SQLAlchemy. Управляет жизненным циклом engine и session factory.

    Attributes:
        _instance (Optional[DatabaseClient]): Единственный экземпляр класса
        _initialized (bool): Флаг инициализации
        _settings (Config): Конфигурация с параметрами подключения к БД
        _engine (Optional[AsyncEngine]): Глобальный асинхронный движок SQLAlchemy
        _session_factory (Optional[async_sessionmaker]): Глобальная фабрика сессий
        _lock (asyncio.Lock): Блокировка для thread-safe инициализации
        logger (logging.Logger): Логгер для записи событий
    """

    _instance: Optional['DatabaseClient'] = None
    _initialized: bool = False
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs) -> 'DatabaseClient':
        """Реализация паттерна Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, _settings: Config = settings) -> None:
        if self._initialized:
            return
        super().__init__()
        self._settings = _settings
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None
        self._initialized = True

    async def connect(self) -> async_sessionmaker:
        if self._session_factory is not None:
            return self._session_factory
        async with self._lock:
            if self._session_factory is not None:
                return self._session_factory
            self.logger.debug("Инициализация глобального подключения к базе данных...")
            self._engine = create_async_engine(
                url=self._settings.database_url,
                **self._settings.engine_params
            )
            self._session_factory = async_sessionmaker(
                bind=self._engine,
                **self._settings.session_params
            )
            self.logger.info("Глобальное подключение к базе данных установлено")
        return self._session_factory

    async def close(self) -> None:
        async with self._lock:
            if self._engine:
                self.logger.debug("Закрытие глобального подключения к базе данных...")
                await self._engine.dispose()
                self._engine = None
                self._session_factory = None
                self.logger.info("Глобальное подключение к базе данных закрыто")
                DatabaseClient._instance = None
                DatabaseClient._initialized = False

    def get_session_factory(self) -> async_sessionmaker:
        """
        Получение фабрики сессий.
        Returns:
            async_sessionmaker: Фабрика для создания сессий
        Raises:
            RuntimeError: Если база данных не была инициализирована
        """
        if self._session_factory is None:
            raise RuntimeError(
                "База данных не инициализирована. "
                "Вызовите connect() перед использованием."
            )
        return self._session_factory

    def get_engine(self) -> AsyncEngine:
        """
        Получение текущего движка базы данных.
        Returns:
            AsyncEngine: асинхронный движок SQLAlchemy
        Raises:
            RuntimeError: если движок еще не инициализирован (connect не вызывался)
        """
        if self._engine is None:
            raise RuntimeError(
                "База данных не инициализирована. "
                "Вызовите connect() перед использованием."
            )
        return self._engine

    @property
    def is_connected(self) -> bool:
        return self._engine is not None

# Глобальный экземпляр клиента базы данных

database_client = DatabaseClient()


class DatabaseContextManager(BaseContextManager):
    """
    Контекстный менеджер для сессий базы данных.

    Упрощает работу с сессиями SQLAlchemy, автоматически управляя
    жизненным циклом сессии и подключения к базе данных.

    Attributes:
        db_client (DatabaseClient): Клиент базы данных для управления подключением.
        session (AsyncSession | None): Текущая активная сессия SQLAlchemy.
        logger (logging.Logger): Логгер для записи событий
    """

    def __init__(self) -> None:
        """
        Инициализирует контекстный менеджер базы данных.

        Создает экземпляр DatabaseClient для управления подключением.
        """
        super().__init__()
        self.db_client = DatabaseClient()
        self.session: AsyncSession | None = None

    async def connect(self) -> AsyncSession:
        """
        Устанавливает подключение к базе данных и создает сессию.

        Returns:
            AsyncSession: Асинхронная сессия SQLAlchemy для работы с базой данных.
        """
        session_factory = await self.db_client.connect()
        session = cast(AsyncSession, session_factory())
        if session is None:
            raise RuntimeError("Не удалось создать сессию базы данных.")
        self.session = session
        return self.session

    async def close(self, do_rollback: bool = False) -> None:
        """
        Закрывает сессию и подключение к базе данных.

        Args:
            do_rollback (bool, optional): Флаг, указывающий, нужно ли выполнить
                откат транзакции перед закрытием сессии. По умолчанию False.

        Note:
            Если do_rollback=True, все незафиксированные изменения будут отменены.
            Если do_rollback=False, незафиксированные изменения останутся в сессии,
            но не будут применены к базе данных.

        Usage:
            ```python
            # Закрытие сессии без отката транзакции
            await db_manager.close()

            # Закрытие сессии с откатом транзакции
            await db_manager.close(do_rollback=True)
            ```
        """
        if self.session:
            if do_rollback:
                await self.session.rollback()
            await self.session.close()
            self.session = None
        await self.db_client.close()

    async def commit(self) -> None:
        """
        Фиксирует изменения в базе данных.

        Применяет все изменения, сделанные в текущей транзакции.

        Raises:
            RuntimeError: Если сессия не была инициализирована.

        Usage:
            ```python
            # Создание новой записи
            new_user = User(username="john_doe")
            session.add(new_user)

            # Фиксация изменений
            await db_manager.commit()
            ```
        """
        if self.session:
            await self.session.commit()
