from typing import Any, Sequence, TYPE_CHECKING, Optional

from sqlalchemy import ScalarResult, select, inspect
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from core.types import MODEL, TYPE_MODEL


class BaseRepo:
    model: "TYPE_MODEL"

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_model(self, conditions: list[Any]) -> Optional["MODEL"]:
        smtp = select(self.model).where(*conditions)
        return await self.session.scalar(smtp)

    async def _get_model_all(self, conditions: list[Any] = None) -> Sequence["MODEL"]:
        smtp = select(self.model)
        if conditions is not None:
            smtp = smtp.where(*conditions)
        result: ScalarResult["MODEL"] = await self.session.scalars(smtp)
        return result.all()

    async def _create_model(self, model_in) -> "MODEL":
        instance = self.model(**model_in.model_dump(exclude_unset=True))
        self.session.add(instance)
        pk = inspect(self.model).primary_key
        if getattr(instance, pk[0].name) is None:
            await self.session.commit()
            await self.session.refresh(instance)
        await self.session.commit()
        return instance

    async def _update_partial_model(self, model_in) -> "MODEL":
        instance = await self._get_model(conditions=[self.model.id == model_in.id])
        for field, value in model_in.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

