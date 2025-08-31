from typing import Optional, Sequence


from db.models import Notification
from repos import BaseRepo
from schemas.notifications import NotificationCreate


class NotificationRepo(BaseRepo):
    model = Notification

    async def get(self, appointment_id) -> Optional[Notification]:
        return await self._get_model(conditions=[self.model.id == appointment_id])

    async def get_by_customer_phone(self, customer_phone: str) -> Sequence["Notification"]:
        return await self._get_model_all(
            conditions=[
                self.model.appointment_data.has_key("customer_phone"),
                self.model.appointment_data["customer_phone"].astext == customer_phone
            ],
        )

    async def create(self, model_in: NotificationCreate) -> Notification:
        return await self._create_model(model_in)
