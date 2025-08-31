from typing import Optional

from db.models import Notification, ProcessedEvent
from schemas.events import ProcessedEventCreate
from repos import BaseRepo


class ProcessedEventRepo(BaseRepo):
    model = ProcessedEvent

    async def get(self, pe_id) -> Optional[Notification]:
        return await self._get_model(conditions=[self.model.id == pe_id])

    async def create(self, model_in: ProcessedEventCreate) -> ProcessedEvent:
        return await self._create_model(model_in)