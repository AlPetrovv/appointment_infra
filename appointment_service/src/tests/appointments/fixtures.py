import datetime as dt
import random
import string
from typing import Optional

import faker
import pytest
import pytest_asyncio

from core.enums import AppointmentStatus
from schemas.appointments import AppointmentCreate, Appointment

fake = faker.Faker()

__all__ = ("appointment_data_default", "mock_appointment_in", "mock_appointment")


@pytest.fixture
def appointment_data_default():
    start = fake.date_time_between(start_date="+1d", end_date="+2m", tzinfo=dt.timezone.utc)
    end = start + dt.timedelta(hours=1)
    yield {
        "customer_name": fake.first_name(),
        "customer_phone": f"+79{''.join(random.choices(string.digits, k=9))}",
        "timeslot_start": start,
        "timeslot_end": end,
        "status": AppointmentStatus.created,
    }


@pytest.fixture
def mock_appointment_in(appointment_data_default):
    def _mock_appointment_in(data: Optional[dict] = None) -> AppointmentCreate:
        if data is None:
            data = {}
        return AppointmentCreate(**(appointment_data_default | data))

    return _mock_appointment_in


@pytest_asyncio.fixture()
async def mock_appointment(appointment_data_default):
    async def _mock_appointment(master_repo, data: Optional[dict] = None):
        if data is None:
            data = {}
        appointment_data = appointment_data_default | data
        appointment_in = Appointment(**appointment_data)
        return await master_repo.appointment.create(appointment_in)

    return _mock_appointment
