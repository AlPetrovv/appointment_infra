import datetime as dt
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.models import Base
from db.models.mixins import UUIDPKMixin


class ProcessedEvent(UUIDPKMixin, Base):
    type: Mapped[str] = mapped_column(String(255))
    occurred_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))


    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, event_type={self.event_type})"
