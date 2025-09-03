import contextlib
from typing import AsyncIterator, Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncConnection, AsyncEngine

from core.config import settings


class DatabaseSessionManager:
    def __init__(self, db_url: str, engine_kwargs: dict[str, Any]):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None
        self._db_url = db_url
        self._engine_kwargs = engine_kwargs

    def init(self):
        if self._engine is None:
            self._engine = create_async_engine(self._db_url, **self._engine_kwargs)
            self._sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.connect() as connection:  # type: AsyncConnection
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise
            finally:
                await connection.close()

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self.connect() as connection:
            async with self._sessionmaker(bind=connection) as session:
                yield session

    async def dispose(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()


db_manager = DatabaseSessionManager(
    db_url=str(settings.db.url),
    engine_kwargs=settings.db.engine_kwargs,
)
