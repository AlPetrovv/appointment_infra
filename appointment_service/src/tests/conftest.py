import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from sqlalchemy import text
from pytest import MonkeyPatch

from core.config import settings
from db.manager import db_manager
from db.models import Base
from main import create_app
from sqlalchemy.ext.asyncio import AsyncConnection

from repos import MasterRepo


@pytest_asyncio.fixture(scope="session", autouse=True)
def override_schema(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(settings.db, "schema", "test")
    yield
    monkeypatch.setattr(settings.db, "schema", "public")


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    async with db_manager.connect() as conn:  # type: AsyncConnection
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS test;"))
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.execute(text("DROP SCHEMA IF EXISTS test CASCADE;"))


@pytest_asyncio.fixture
async def api_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()), base_url="http://test/api/v1"
    ) as client:
        yield client

@pytest_asyncio.fixture(scope="function", autouse=True)
async def repo():
    async with db_manager.session() as session:
        yield MasterRepo(session)
