"""
Модуль безопасности приложения.

Содержит классы для работы с паролями, секретными ключами и токенами.

Example:
    >>> from app.core.security import PasswordHasher
    >>> hashed_password = PasswordHasher.hash_password("secretpassword")
"""

from .password import PasswordHasher

__all__ = ["PasswordHasher"]
