import datetime as dt
from typing import Optional

from pydantic import Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from core.enums import AppointmentStatus

PhoneNumber.phone_format = "INTERNATIONAL"


class Appointment:
    customer_name: str
    customer_phone: PhoneNumber
    timeslot_start: dt.datetime
    timeslot_end: dt.datetime
    status: AppointmentStatus


class AppointmentCreate(Appointment):
    status: AppointmentStatus = Field(default=AppointmentStatus.pending)


class AppointmentPartialUpdate(Appointment):
    status: Optional[AppointmentStatus] = None


class AppointmentRead(Appointment):
    id: int
