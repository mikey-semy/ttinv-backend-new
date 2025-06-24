
from typing import TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .users import UserModel
    from .header import Logo, MenuItem, ContactInfo

__all__ = ["BaseModel"]