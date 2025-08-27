import datetime as dt
from typing import Optional

from sqlalchemy import Unicode, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, composite
from sqlalchemy_utils import PhoneNumber

from core.enums import AppointmentStatus
from db.models import Base
from db.models.mixins import IDPKINTMixin, CreatedAtMixin


class Appointment(CreatedAtMixin, IDPKINTMixin, Base):
    # data
    customer_name: Mapped[str] = mapped_column()
    customer_phone: Mapped[str] = mapped_column(Unicode(17), unique=True)
    _customer_phone = composite(PhoneNumber, customer_phone)
    # time
    timeslot_start: Mapped[dt.datetime]
    timeslot_end: Mapped[dt.datetime]
    # status
    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.pending)
    # additional
    cancel_reason: Mapped[Optional[str]] = mapped_column(String(255))

    def __str__(self):
        return f"Appointment(id={self.id}, customer_name={self.customer_name}, status={self.status})"
