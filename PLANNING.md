# FastAPI Project Planning
## High-Level Vision
Создание масштабируемого веб-приложения на FastAPI с использованием современных практик разработки, включая асинхронное программирование, микросервисную архитектуру и интеграцию с внешними сервисами.
## Architecture Overview
- **Layered Architecture**: Строгое разделение слоев (routes → services → data_managers → models)
- **Domain-Driven Design**: Организация кода по предметным областям
- **Dependency Injection**: Централизованное управление зависимостями
- **API Versioning**: Поддержка версионирования API (v1, v2, etc.)
## Project Structure
```
app/
├── core/                    # Инфраструктурные компоненты
│   ├── settings/           # Конфигурация приложения
│   │   ├── __init__.py
│   │   ├── settings.py     # Основные настройки
│   │   ├── logging.py      # Настройки логирования
│   │   └── paths.py        # Пути файловой системы
│   ├── security/           # Аутентификация и авторизация
│   │   ├── __init__.py
│   │   ├── auth.py         # Аутентификация
│   │   ├── password.py     # Хеширование паролей
│   │   ├── token.py        # JWT токены
│   │   └── cookies.py      # Secure cookies
│   ├── middlewares/        # Промежуточное ПО
│   │   ├── __init__.py
│   │   ├── logging.py      # Логирование запросов
│   │   ├── auth_cookie.py  # Cookie аутентификация
│   │   ├── rate_limit.py   # Ограничение частоты
│   │   ├── verification.py # Верификация запросов
│   │   └── activity.py     # Отслеживание активности
│   ├── dependencies/       # Внедрение зависимостей
│   │   ├── __init__.py
│   │   ├── base.py         # Базовые зависимости
│   │   ├── database.py     # БД зависимости
│   │   ├── cache.py        # Кэш зависимости
│   │   └── storage.py      # Хранилище зависимости
│   ├── exceptions/         # Обработка исключений
│   │   ├── __init__.py
│   │   ├── base.py         # Базовые исключения
│   │   ├── handlers.py     # Обработчики исключений
│   │   ├── auth.py         # Исключения аутентификации
│   │   ├── users.py        # Пользовательские исключения
│   │   ├── profile.py      # Исключения профиля
│   │   └── rate_limit.py   # Исключения лимитов
│   ├── integrations/       # Внешние сервисы
│   │   ├── __init__.py
│   │   ├── cache/          # Кэш интеграции
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── auth.py
│   │   ├── mail/           # Email сервисы
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── auth.py
│   │   ├── storage/        # Файловое хранилище
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   └── messaging/      # Сообщения
│   │       ├── __init__.py
│   │       ├── setup.py
│   │       ├── broker.py
│   │       ├── api.py
│   │       ├── producers.py
│   │       ├── consumers.py
│   │       └── hooks.py
│   ├── connections/        # Подключения к БД, кэшу
│   │   ├── __init__.py
│   │   ├── base.py         # Базовые подключения
│   │   ├── database.py     # PostgreSQL
│   │   ├── cache.py        # Redis
│   │   ├── storage.py      # S3/MinIO
│   │   └── messaging.py    # RabbitMQ
│   ├── lifespan/          # Жизненный цикл приложения
│   │   ├── __init__.py
│   │   ├── base.py         # Базовый жизненный цикл
│   │   ├── database.py     # БД инициализация
│   │   └── clients.py      # Клиенты сервисов
│   └── logging/           # Система логирования
│       ├── __init__.py
│       ├── setup.py        # Настройка логирования
│       └── formatters.py   # Форматтеры логов
├── models/v1/              # SQLAlchemy модели
│   ├── __init__.py
│   ├── base.py             # Базовая модель
│   ├── users.py            # Пользователи
│   ├── addresses.py        # Адреса
│   └── payments.py         # Платежи
├── schemas/v1/             # Pydantic схемы
│   ├── __init__.py
│   ├── base.py             # Базовые схемы
│   ├── errors.py           # Схемы ошибок
│   ├── pagination.py       # Пагинация
│   ├── auth/               # Аутентификация
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── request.py
│   │   ├── response.py
│   │   └── exception.py
│   ├── registration/       # Регистрация
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── request.py
│   │   ├── response.py
│   │   └── exception.py
│   ├── profile/            # Профиль
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── request.py
│   │   ├── response.py
│   │   └── exception.py
│   ├── users/              # Пользователи
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── response.py
│   └── mail/               # Почта
│       ├── __init__.py
│       └── base.py
├── services/v1/            # Бизнес-логика
│   ├── __init__.py
│   ├── base.py             # Базовый сервис
│   ├── auth/               # Аутентификация
│   │   ├── __init__.py
│   │   ├── service.py
│   │   └── data_manager.py
│   ├── registration/       # Регистрация
│   │   ├── __init__.py
│   │   ├── service.py
│   │   └── data_manager.py
│   ├── profile/            # Профиль
│   │   ├── service.py
│   │   └── data_manager.py
│   └── users/              # Пользователи
│       ├── __init__.py
│       ├── service.py
│       └── data_manager.py
├── routes/v1/              # API эндпоинты
│   ├── __init__.py
│   ├── auth.py             # Аутентификация
│   ├── registration.py     # Регистрация
│   ├── verification.py     # Верификация
│   ├── users.py            # Пользователи
│   └── profile.py          # Профиль
├── routes/                 # Основные роуты
│   ├── __init__.py
│   ├── base.py             # Базовый роутер
│   └── main.py             # Главный роутер
└── main.py                 # Точка входа
```
## Technology Stack
- **Framework**: FastAPI 0.104+
- **ASGI Server**: Uvicorn
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0+ (async)
- **Migrations**: Alembic
- **Cache**: Redis 7+
- **Message Broker**: RabbitMQ + FastStream
- **Validation**: Pydantic v2
- **Package Manager**: uv
- **Testing**: pytest + pytest-asyncio
- **Documentation**: Automatic OpenAPI/Swagger
## Development Tools
- **Package Management**: uv для управления зависимостями
- **Code Quality**: ruff для линтинга и форматирования
- **Type Checking**: mypy для статической типизации
- **Pre-commit**: Автоматические проверки перед коммитом
- **Docker**: Контейнеризация для разработки и продакшена
## Coding Standards
- **Language**: Все ответы и комментарии на русском языке
- **Documentation**: Google-style docstrings на русском
- **Type Hints**: Обязательные аннотации типов
- **OOP**: Объектно-ориентированный подход
- **Base Classes**: Наследование от базовых классов в base.py
- **Error Handling**: Централизованная обработка ошибок
- **Async/Await**: Асинхронное программирование везде где возможно
## Security Requirements
- **Authentication**: JWT токены + secure cookies
- **Authorization**: Role-based access control
- **Password Security**: Bcrypt хеширование
- **Rate Limiting**: Защита от DDoS и брутфорса
- **CORS**: Настройка для фронтенда
- **HTTPS**: Обязательно в продакшене
## Performance Considerations
- **Database**: Connection pooling, индексы, оптимизация запросов
- **Caching**: Redis для кеширования частых запросов
- **Background Tasks**: Celery/FastStream для тяжелых операций
- **Monitoring**: Логирование производительности
- **Pagination**: Для больших наборов данных
## Integration Patterns
- **External APIs**: HTTP клиенты с retry логикой
- **Message Queues**: Асинхронная обработка сообщений
- **File Storage**: S3-совместимые хранилища
- **Email**: SMTP интеграция для уведомлений
- **Monitoring**: Prometheus + Grafana метрики
## Deployment Strategy
- **Containerization**: Docker + docker-compose
- **Environment**: Разделение dev/staging/prod
- **CI/CD**: GitHub Actions или GitLab CI
- **Database Migrations**: Автоматические миграции
- **Health Checks**: Эндпоинты для мониторинга
## Constraints
- **Python Version**: 3.11+
- **Database**: Только PostgreSQL
- **Cache**: Только Redis
- **Message Broker**: RabbitMQ предпочтительно
- **Documentation**: Обязательная для всех публичных методов
- **Testing**: Минимум 80% покрытие кода
## Code Generation Rules
- **Inheritance**: Все классы наследуются от базовых в base.py
- **Naming Convention**: snake_case для файлов и функций, PascalCase для классов
- **Import Organization**: Стандартные → сторонние → локальные импорты
- **Error Messages**: Детальные сообщения об ошибках на русском языке
- **Logging**: Структурированное логирование с контекстом
- **Configuration**: Все настройки через environment variables
- **Validation**: Pydantic модели для всех входных/выходных данных
- **Database**: Async SQLAlchemy с proper session management
- **Testing**: Comprehensive unit и integration тесты
- **Documentation**: Автоматическая генерация API документации
