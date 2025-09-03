import secrets
import datetime as dt
from typing import TYPE_CHECKING

import pytest
from pydantic import ValidationError

from core.enums import AppointmentStatus

pytestmark = pytest.mark.anyio

if TYPE_CHECKING:
    from repos import MasterRepo


def get_idempotency_key():
    return secrets.token_hex(32)


@pytestmark
async def test_create_appointment(api_client, master_repo, mock_appointment_in):
    appointment_in = mock_appointment_in()
    response = await api_client.post(
        "/appointments/",
        json=appointment_in.model_dump(mode="json"),
        headers={"Idempotency-Key": get_idempotency_key()},
    )
    assert response.status_code == 201


@pytestmark
async def test_confirm_appointment(api_client, master_repo, mock_appointment):
    appointment = await mock_appointment(master_repo)
    response = await api_client.patch(
        f"/appointments/{appointment.id}/confirm",
    )
    assert response.status_code == 200


@pytestmark
async def test_cancel_appointment(api_client, master_repo, mock_appointment):
    appointment = await mock_appointment(master_repo)
    response = await api_client.patch(
        f"/appointments/{appointment.id}/cancel",
        json={"cancel_reason": "Test reason"},
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "timeslot_start, timeslot_end",
    [
        (dt.datetime.now(tz=dt.timezone.utc), dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(hours=1)),
        (dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(hours=1), dt.datetime.now(tz=dt.timezone.utc)),
    ],
)
async def test_create_invalid_timeslot(
    api_client,
    mock_appointment_in,
    timeslot_start: dt.datetime,
    timeslot_end: dt.datetime,
):
    with pytest.raises(ValueError):
        mock_appointment_in({"timeslot_start": timeslot_start, "timeslot_end": timeslot_end})


@pytest.mark.parametrize(
    "timeslot_start, timeslot_end",
    [
        (dt.datetime.now(tz=dt.timezone.utc), dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(hours=1)),
        (dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(hours=1), dt.datetime.now(tz=dt.timezone.utc)),
    ],
)
async def test_create_valid_timeslot(
    api_client,
    mock_appointment_in,
    timeslot_start: dt.datetime,
    timeslot_end: dt.datetime,
):
    appointment_in = mock_appointment_in({"timeslot_start": timeslot_start, "timeslot_end": timeslot_end})
    response = await api_client.post(
        "/appointments/",
        json=appointment_in.model_dump(mode="json"),
        headers={"Idempotency-Key": get_idempotency_key()},
    )
    assert response.status_code == 201


@pytest.mark.parametrize(
    "phone_number",
    [
        ("+7999999999",),
        ("7999999999",),
        ("+799999999999",),
        ("+799999999999999",),
    ],
)
async def test_invalid_phone_number(api_client, mock_appointment_in, phone_number: str):
    with pytest.raises(ValidationError):
        mock_appointment_in({"customer_phone": phone_number})


@pytest.mark.parametrize(
    "phone_number, status_code",
    [
        ("+79999999999", 201),
        ("+7 999 999 99 99", 201),
        ("+7-999-999-99-99", 201),
        ("+7(999)999-99-99", 201),
        ("+79111111111", 201),
    ],
)
async def test_valid_phone_number(api_client, mock_appointment_in, phone_number: str, status_code: int):
    appointment_in = mock_appointment_in({"customer_phone": phone_number})
    response = await api_client.post(
        "/appointments/",
        json=appointment_in.model_dump(mode="json"),
        headers={
            "Idempotency-Key": get_idempotency_key(),
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "status", [AppointmentStatus.created, AppointmentStatus.confirmed, AppointmentStatus.canceled]
)
async def test_get_by_status(api_client, master_repo: "MasterRepo", status: AppointmentStatus, mock_appointment):
    await mock_appointment(master_repo, data={"status": status})
    response = await api_client.get(f"/appointments/?status={status}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


@pytest.mark.parametrize(
    "status, cancel_reason, status_code",
    [
        (AppointmentStatus.created, "Test reason", 200),
        (AppointmentStatus.created, None, 200),
        (AppointmentStatus.confirmed, "Test reason", 200),
        (AppointmentStatus.confirmed, None, 409),
    ],
)
async def test_cancel_appointment_detail(
    api_client,
    master_repo: "MasterRepo",
    mock_appointment,
    status: AppointmentStatus,
    cancel_reason: str,
    status_code: int,
):
    appointment = await mock_appointment(master_repo, {"status": status})
    response = await api_client.patch(
        f"/appointments/{appointment.id}/cancel",
        json={"reason": cancel_reason},
        headers={"Idempotency-Key": get_idempotency_key()},
    )
    assert response.status_code == status_code


@pytest.mark.parametrize("idempotency_key", [get_idempotency_key() for _ in range(10)])
async def test_idempotency_key(api_client, mock_appointment_in, idempotency_key: str):
    appointment_in = mock_appointment_in()
    response = await api_client.post(
        "/appointments/",
        json=appointment_in.model_dump(mode="json"),
        headers={"Idempotency-Key": idempotency_key},
    )
    assert response.status_code == 201
    response = await api_client.post(
        "/appointments/",
        json=appointment_in.model_dump(mode="json"),
        headers={"Idempotency-Key": idempotency_key},
    )
    assert response.status_code == 200
