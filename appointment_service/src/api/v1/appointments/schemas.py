import datetime as dt
import uuid
from typing import Optional

from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, Field


class CancelAppointmentBody(BaseModel):
    reason: Optional[str] = None


class AppointmentPayload(BaseModel):
    appointment_id: int = Field(alias="id")
    customer_phone: PhoneNumber
    timeslot_start: dt.datetime
    timeslot_end: dt.datetime


class AppointmentNotificationPub(BaseModel):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    event_type: str
    occurred_at: dt.datetime
    payload: AppointmentPayload
