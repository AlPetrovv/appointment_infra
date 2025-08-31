from dataclasses import dataclass
from typing import TYPE_CHECKING

from db.manager import db_manager
from .notifications import NotificationRepo
from .events import ProcessedEventRepo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

@dataclass
class MasterRepo:
    """Repo that contains all repos."""

    session: "AsyncSession"

    def __init__(self, session: "AsyncSession"):
        self.session = session

    @property
    def notification(self) -> NotificationRepo:
        return NotificationRepo(self.session)

    @property
    def processed_event(self) -> ProcessedEventRepo:
        return ProcessedEventRepo(self.session)


async def get_repo() -> MasterRepo:
    async with db_manager.session() as session:
        return MasterRepo(session)