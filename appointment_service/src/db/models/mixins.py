import datetime as dt

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


class IDPKINTMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class CreatedAtMixin:
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=dt.datetime.now,
    )
