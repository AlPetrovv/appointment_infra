from fastapi import APIRouter

from api.v1 import router as api_v1_router

__all__ = ("main_router",)

main_router = APIRouter(prefix="/api")

main_router.include_router(api_v1_router)
