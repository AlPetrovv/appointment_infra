import contextlib
from typing import AsyncIterator, Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncConnection,
)

from core.config import settings


class DatabaseSessionManager:
    def __init__(self, db_url: str, engine_kwargs: dict[str, Any]):
        self._engine = create_async_engine(db_url, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def dispose(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()


db_manager = DatabaseSessionManager(
    db_url=str(settings.db.url), engine_kwargs=settings.db.engine_kwargs
)
