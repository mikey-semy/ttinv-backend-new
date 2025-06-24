# TASK.md: Реализация backend для header (логотип, меню, контакты)

## 1. Проектирование моделей данных
- [x] 1.1. Создать SQLAlchemy-модели:
  - [x] Logo (путь к файлу/URL, alt-текст)
  - [x] MenuItem (название, ссылка, порядок)
  - [x] ContactInfo (тип, значение: телефон, email и т.д.)

## 2. Pydantic-схемы
- [x] 2.1. Создать Pydantic-схемы для CRUD-операций (разделены на base, requests, responses):
  - [x] LogoBaseSchema, LogoCreateSchema, LogoUpdateSchema, LogoResponseSchema
  - [x] MenuItemBaseSchema, MenuItemCreateSchema, MenuItemUpdateSchema, MenuItemResponseSchema
  - [x] ContactInfoBaseSchema, ContactInfoCreateSchema, ContactInfoUpdateSchema, ContactInfoResponseSchema

## 3. Сервисы и data_manager
- [x] 3.1. Реализовать сервисы для работы с моделями (services/v1/header/)
- [x] 3.2. Реализовать data_manager для абстракции работы с БД

## 4. CRUD-роуты (API)
- [x] 4.1. Создать роуты для управления header (routes/v1/header.py, с наследованием от BaseRouter)
  - [x] CRUD для логотипа
  - [x] CRUD для пунктов меню
  - [x] CRUD для контактной информации

## 5. Интеграция с Starlette Admin
- [ ] 5.1. Добавить модели header в Starlette Admin для управления через UI

## 6. Хранение файлов (логотип)
- [ ] 6.1. Реализовать загрузку и хранение файлов (S3/локально)
- [ ] 6.2. Настроить путь к логотипу в модели и схеме

## 7. Документирование и тестирование
- [ ] 7.1. Добавить Google-style docstrings на русском языке
- [ ] 7.2. Покрыть CRUD-логику unit-тестами

## 8. Примеры и OpenAPI
- [ ] 8.1. Добавить примеры в схемы для автогенерации документации

---

### Пример структуры файлов:

- app/models/v1/header.py
- app/schemas/v1/header/base.py
- app/schemas/v1/header/requests.py
- app/schemas/v1/header/responses.py
- app/services/v1/header/service.py
- app/services/v1/header/data_manager.py
- app/routes/v1/header.py

---

## Примечания:
- Все классы должны наследоваться от базовых (base.py).
- Использовать асинхронные методы.
- Документировать все публичные методы.
- Для хранения логотипа использовать S3/MinIO или локально (на выбор).
- В будущем предусмотреть расширение для других секций сайта. 