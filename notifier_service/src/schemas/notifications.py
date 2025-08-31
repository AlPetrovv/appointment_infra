import datetime as dt

from pydantic import BaseModel, Field, field_serializer
from pydantic_extra_types.phone_numbers import PhoneNumber


class AppointmentData(BaseModel):
    appointment_id: int
    customer_phone: PhoneNumber
    timeslot_start: dt.datetime
    timeslot_end: dt.datetime

    @field_serializer("customer_phone")
    def serialize_phone(self, value: str, _info):
        if isinstance(value, str):
            return value.replace("tel:", "")
        return value


class Notification(BaseModel):
    appointment_data: AppointmentData
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)


class NotificationRead(Notification):
    id: int


class NotificationCreate(Notification):
    @field_serializer("appointment_data")
    def serialize_payload(self, value: AppointmentData, _info):
        return value.model_dump(mode="json")
