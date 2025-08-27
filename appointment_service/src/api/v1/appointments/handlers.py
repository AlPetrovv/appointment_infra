from typing import Annotated

from fastapi import APIRouter, Header

from .schemas import IdempotencyHeaders
from schemas.appointments import AppointmentCreate, AppointmentRead
from redis_tools.client import redis_client
from api.dependencies.repo import RepoDep

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=AppointmentRead)
async def create_appointment(
        repo: RepoDep,
        appointment_in: AppointmentCreate,
        headers: Annotated[IdempotencyHeaders, Header()]
):
    appointment_key = await redis_client.get(headers.idempotency_key)
    if appointment_key:
        return await repo.appointment.get()
    else:
        return await repo.appointment.create(appointment_in)


