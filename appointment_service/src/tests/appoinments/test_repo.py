import pytest

from core.enums import AppointmentStatus
from schemas.appointments import AppointmentCreate


@pytest.mark.asyncio
async def test_repo_create(repo):
    appointment_in = AppointmentCreate(**{
        "customer_name": "John Doe",
        "timeslot_start": "2021-01-01T00:00:00+00:00",
        "timeslot_end": "2022-01-01T00:00:00+00:00",
        "customer_phone": "+79999999999",
        "status": "Created",
    })
    appointment = await repo.appointment.create(appointment_in)
    assert appointment.customer_name == appointment_in.customer_name
    assert appointment.timeslot_start == appointment_in.timeslot_start
    assert appointment.timeslot_end == appointment_in.timeslot_end
    assert appointment.customer_phone == appointment_in.customer_phone
    assert appointment.status == appointment_in.status



@pytest.mark.asyncio
async def test_repo_get_by_status(repo):
    await repo.appointment.create(AppointmentCreate(**{
        "customer_name": "John Doe",
        "timeslot_start": "2021-01-01T00:00:00+00:00",
        "timeslot_end": "2022-01-01T00:00:00+00:00",
        "customer_phone": "+79999999999",
        "status": "Created",
    }))
    appointments = await repo.appointment.get_by_status(status=AppointmentStatus.created)
    assert len(appointments) == 1
