import datetime as dt
import uuid

from pydantic import BaseModel

from schemas.notifications import AppointmentData


class AppointmentCreatedNotification(BaseModel):
    event_id: uuid.UUID
    event_type: str
    occurred_at: dt.datetime
    payload: AppointmentData