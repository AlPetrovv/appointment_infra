from fastapi import APIRouter

from core.config import settings
from .appointments.handlers import router as appointments_router

__all__ = ("router",)

router = APIRouter(prefix=settings.api_v1.prefix)

router.include_router(appointments_router)
