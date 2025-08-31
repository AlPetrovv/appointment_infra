from enum import StrEnum


class AppointmentStatus(StrEnum):
    created = "Created"
    confirmed = "Confirmed"
    canceled = "Canceled"
