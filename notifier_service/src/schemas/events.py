import datetime as dt

from pydantic import BaseModel


class ProcessedEvent(BaseModel):
    type: str
    occurred_at: dt.datetime


class ProcessedEventCreate(ProcessedEvent):
    pass
