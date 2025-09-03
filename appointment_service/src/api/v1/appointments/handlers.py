from typing import Annotated

from fastapi import APIRouter, Header, Response
from fastapi.params import Depends, Query
from fastapi_pagination import paginate

from starlette import status

from core.enums import AppointmentStatus
from db.models import Appointment

from schemas.appointments import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentPartialUpdate,
)
from redis_tools.client import redis_client
from api.dependencies.repo import RepoDep
from .schemas import CancelAppointmentBody
from .services import process_appointment_create
from api.v1.pagination import CustomPage
from api.dependencies.appointment import get_appointment

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get("/", response_model=CustomPage[AppointmentRead])
async def get_appointments(
    repo: RepoDep,
    appointment_status: Annotated[AppointmentStatus, Query(alias="status")] = AppointmentStatus.created,
):
    appointments = await repo.appointment.get_by_status(status=appointment_status)
    return paginate(appointments)


@router.post(
    "/",
    response_model=AppointmentRead,
    responses={
        status.HTTP_200_OK: {"model": AppointmentRead},
        status.HTTP_201_CREATED: {"model": AppointmentRead},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    repo: RepoDep,
    appointment_in: AppointmentCreate,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    response: Response,
):
    appointment_id = await redis_client.get(idempotency_key)
    if appointment_id:
        response.status_code = status.HTTP_200_OK
        appointment = await repo.appointment.get(int(appointment_id))
        return appointment
    else:
        appointment = await process_appointment_create(
            repo=repo, appointment_in=appointment_in, idempotency_key=idempotency_key
        )
        return appointment


@router.patch(
    "/{id}/cancel",
    responses={
        status.HTTP_200_OK: {
            "description": "OK",
            "content": {"application/json": {"example": "OK"}},
        },
        status.HTTP_409_CONFLICT: {
            "description": "Operation not allowed",
            "value": "Operation not allowed",
            "content": {"application/json": {"example": "Operation not allowed"}},
        },
    },
    status_code=status.HTTP_200_OK,
)
async def cancel_appointment(
    repo: RepoDep,
    appointment: Annotated[Appointment, Depends(get_appointment)],
    response: Response,
    body: CancelAppointmentBody,
):
    if appointment.status == AppointmentStatus.confirmed and body.reason is None:
        response.status_code = status.HTTP_409_CONFLICT
        return "Operation not allowed"
    model_in = AppointmentPartialUpdate(status=AppointmentStatus.canceled, cancel_reason=body.reason)
    await repo.appointment.update_partial(model_in, instance=appointment)
    return "OK"


@router.patch(
    "/{id}/confirm",
    responses={
        status.HTTP_200_OK: {
            "description": "OK",
            "value": "OK",
            "content": {"application/json": {"example": "OK"}},
        },
        status.HTTP_409_CONFLICT: {
            "description": "Operation not allowed",
            "value": "Operation not allowed",
            "content": {"application/json": {"example": "Operation not allowed"}},
        },
    },
)
async def confirm_appointment(
    repo: RepoDep, appointment: Annotated[Appointment, Depends(get_appointment)], response: Response
):
    if appointment.status != AppointmentStatus.created:
        response.status_code = status.HTTP_409_CONFLICT
        return "Operation not allowed"
    model_in = AppointmentPartialUpdate(status=AppointmentStatus.confirmed)
    await repo.appointment.update_partial(model_in, instance=appointment)
    return "OK"
