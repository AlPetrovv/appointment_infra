from sqlalchemy.orm import Mapped, mapped_column

from .mixins import CreatedAtMixin, IDPKINTMixin
from .base import Base
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB


class Notification(CreatedAtMixin, IDPKINTMixin, Base):
    appointment_data: Mapped[JSON] = mapped_column(JSONB)

    def __str__(self):
        return f"{self.__class__.__name__}#{self.id}"
