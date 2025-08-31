from fastapi import APIRouter

from core.config import settings
from .notifications.handlers import router as notifications_router

__all__ = ("router",)

router = APIRouter(prefix=settings.api_v1.prefix)

router.include_router(notifications_router)

