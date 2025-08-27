from typing import Optional

from repos import BaseRepo
from db.models import Appointment
from schemas.appointments import AppointmentPartialUpdate, AppointmentCreate


class AppointmentRepo(BaseRepo):
    model = Appointment

    async def get(self, appointment_id) -> Optional[Appointment]:
        return await self._get_model(conditions=[self.model.id == appointment_id])

    async def update_partial(self, model_in: AppointmentPartialUpdate) -> Appointment:
        return await self._update_partial_model(model_in)

    async def create(self, model_in: AppointmentCreate) -> Appointment:
        return await self._create_model(model_in)
