import pytest

from core.enums import AppointmentStatus
from schemas.appointments import AppointmentPartialUpdate

pytestmark = pytest.mark.anyio


@pytestmark
async def test_get_by_status(master_repo, mock_appointment):
    await mock_appointment(master_repo)
    appointments = await master_repo.appointment.get_by_status(status=AppointmentStatus.created)
    assert len(appointments) == 1


@pytestmark
async def test_create(master_repo, mock_appointment_in):
    appointment_in = mock_appointment_in()
    appointment = await master_repo.appointment.create(appointment_in)
    assert appointment.customer_name == appointment_in.customer_name
    assert appointment.timeslot_start == appointment_in.timeslot_start
    assert appointment.timeslot_end == appointment_in.timeslot_end
    assert appointment.customer_phone == appointment_in.customer_phone
    assert appointment.status == AppointmentStatus.created


@pytestmark
async def test_update_partial(master_repo, mock_appointment):
    appointment = await mock_appointment(master_repo)
    appointment_in = AppointmentPartialUpdate(
        status=AppointmentStatus.canceled,
        cancel_reason="Test reason",
    )
    updated_appointment = await master_repo.appointment.update_partial(appointment_in, appointment)
    assert updated_appointment.status == AppointmentStatus.canceled
    assert updated_appointment.cancel_reason == "Test reason"
