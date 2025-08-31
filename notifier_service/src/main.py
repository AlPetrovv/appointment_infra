import contextlib

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from core.config import settings
from db.manager import db_manager
from api.v1.notifications.handlers import fs_router
from routers import main_router


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await db_manager.dispose()


app = FastAPI(title="Notifier Service", description="Welcome to the Notifier Service API", lifespan=lifespan)
add_pagination(app)

app.include_router(main_router)
app.include_router(fs_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.uvicorn.host, port=settings.uvicorn.port, reload=True)
