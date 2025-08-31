import contextlib

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from core.config import settings
from db.manager import db_manager
from fs.appointments.brokers import rabbit_broker, rabbit_exchange
from redis_tools.client import redis_client
from routers import main_router


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_broker.start()
    await rabbit_broker.declare_exchange(rabbit_exchange)
    yield
    await redis_client.close()
    await rabbit_broker.stop()
    await db_manager.dispose()


def create_app():
    app = FastAPI(
        title="Appointment Service",
        description="Welcome to the Appointment Service API",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    return app


main_app = create_app()
add_pagination(main_app)

main_app.include_router(main_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:main_app",
        host=settings.uvicorn.host,
        port=settings.uvicorn.port,
        reload=True,
    )
