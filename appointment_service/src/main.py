import contextlib

from fastapi import FastAPI

from core.config import settings
from db.manager import db_manager


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await db_manager.dispose()


app = FastAPI(title="Appointment Service",description="Welcome to the Appointment Service API", lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.uvicorn.host, port=settings.uvicorn.port, reload=True)
