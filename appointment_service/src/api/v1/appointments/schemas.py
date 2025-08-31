import datetime as dt
import uuid

from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, Field



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
