from dataclasses import dataclass
from typing import TYPE_CHECKING

from repos.appointment import AppointmentRepo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class MasterRepo:
    """Repo that contains all repos."""

    session: "AsyncSession"

    def __init__(self, session: "AsyncSession"):
        self.session = session

    @property
    def appointment(self) -> AppointmentRepo:
        return AppointmentRepo(self.session)
