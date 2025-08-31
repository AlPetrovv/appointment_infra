import datetime as dt
from typing import Optional, Self

from pydantic import Field, BaseModel, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from core.enums import AppointmentStatus

PhoneNumber.phone_format = "INTERNATIONAL"


class Appointment(BaseModel):
    customer_name: str
    customer_phone: PhoneNumber = Field(examples=["+79999999999"])
    timeslot_start: dt.datetime
    timeslot_end: dt.datetime
    status: AppointmentStatus
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)


class AppointmentCreate(Appointment):
    status: AppointmentStatus = Field(default=AppointmentStatus.created)

    @model_validator(mode="after")
    def check_timeslot(cls, instance: Self):
        if instance.timeslot_start >= instance.timeslot_end:
            raise ValueError("Timeslot start must be less than timeslot end")
        return instance


class AppointmentPartialUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    cancel_reason: Optional[str] = None


class AppointmentRead(Appointment):
    id: int
