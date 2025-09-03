from typing import Optional, Sequence

from sqlalchemy import desc

from core.enums import AppointmentStatus
from repos import BaseRepo
from db.models import Appointment
from schemas.appointments import AppointmentPartialUpdate, AppointmentCreate


class AppointmentRepo(BaseRepo):
    model = Appointment

    async def get(self, appointment_id: int | str) -> Optional[Appointment]:
        if isinstance(appointment_id, str):
            appointment_id = int(appointment_id)
        return await self._get_model(conditions=[self.model.id == appointment_id])

    async def create(self, model_in: AppointmentCreate) -> Appointment:
        return await self._create_model(model_in)

    async def get_by_status(self, status: AppointmentStatus) -> Sequence[Appointment]:
        return await self._get_model_all(
            conditions=[self.model.status == status.name],
            order_by=[desc(self.model.created_at)],
        )

    async def update_partial(self, model_in: AppointmentPartialUpdate, instance: Appointment) -> "Appointment":
        return await self._update_partial_model(model_in, instance)
