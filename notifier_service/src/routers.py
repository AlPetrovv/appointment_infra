from fastapi import APIRouter

from api.v1.notifications.handlers import router as notifications_router
from api.v1.notifications.handlers import fs_router

main_router = APIRouter(prefix="/api")

main_router.include_router(notifications_router)
main_router.include_router(fs_router)