import datetime as dt
from typing import Optional

from sqlalchemy import (
    Unicode,
    Enum,
    String,
    CheckConstraint,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, composite
from sqlalchemy_utils import PhoneNumber

from core.enums import AppointmentStatus
from db.models import Base
from db.models.mixins import IDPKINTMixin, CreatedAtMixin


class Appointment(CreatedAtMixin, IDPKINTMixin, Base):
    # data
    customer_name: Mapped[str] = mapped_column(String(255))
    customer_phone: Mapped[str] = mapped_column(Unicode(17))
    _customer_phone = composite(PhoneNumber, customer_phone)
    # time
    timeslot_start: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    timeslot_end: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    # status
    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.created)
    # additional
    cancel_reason: Mapped[Optional[str]] = mapped_column(String(255))

    __table_args__ = (
        CheckConstraint(
            "timeslot_start < timeslot_end",
            name="check_timeslot",
        ),
    )

    def __str__(self):
        return f"Appointment(id={self.id}, customer_name={self.customer_name}, status={self.status})"
