import datetime as dt
import uuid

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


class IDPKINTMixin:
    id: Mapped[int] = mapped_column(primary_key=True)

class UUIDPKMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class CreatedAtMixin:
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=dt.datetime.now,
    )