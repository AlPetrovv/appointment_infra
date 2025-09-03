from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi_pagination.utils import disable_installed_extensions_check
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from fs.appointments.brokers import rabbit_broker, rabbit_exchange
from main import create_app
from repos import MasterRepo, get_repo

from db.manager import db_manager
from tests.appointments.fixtures import *  # noqa


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db_manager():
    disable_installed_extensions_check()
    db_manager.init()
    yield
    await db_manager.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def broker_connect():
    await rabbit_broker.start()
    await rabbit_broker.declare_exchange(rabbit_exchange)
    yield
    await rabbit_broker.stop()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_connection(init_db_manager):
    async with db_manager.connect() as connection:
        yield connection


@pytest_asyncio.fixture()
async def transaction(db_connection):
    async with db_connection.begin() as transaction:
        yield transaction
        await transaction.rollback()


@pytest_asyncio.fixture()
async def session(transaction, db_connection):
    async_session = AsyncSession(
        bind=db_connection,
        join_transaction_mode="create_savepoint",
    )
    yield async_session


# Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture
async def api_client(db_connection, transaction) -> AsyncClient:
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=db_connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield MasterRepo(async_session)

    app = create_app()
    app.dependency_overrides[get_repo] = override_get_async_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1") as client:
        yield client
    del app.dependency_overrides[get_repo]


@pytest_asyncio.fixture
async def master_repo(session):
    yield MasterRepo(session)
