from typing import Annotated

from fastapi import HTTPException, Path
from starlette import status

from api.dependencies.repo import RepoDep


async def get_appointment(appointment_id: Annotated[int, Path(alias="id", gt=0)], repo: RepoDep):
    appointment = await repo.appointment.get(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return appointment
