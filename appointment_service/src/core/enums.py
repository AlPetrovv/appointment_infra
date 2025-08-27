from enum import StrEnum


class AppointmentStatus(StrEnum):
   pending = "Pending"
   approved = "Approved"
   canceled = "Canceled"