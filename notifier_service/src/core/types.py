from typing import TypeVar, Type

from db.models import Base

MODEL = TypeVar("MODEL", bound=Base)
TYPE_MODEL = Type[MODEL]
