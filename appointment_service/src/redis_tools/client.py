from typing import Optional

from redis.asyncio import from_url

from core.config import settings


class RedisClient:
    def __init__(self):
        self.__connection = from_url(str(settings.redis.url))

    async def close(self):
        await self.__connection.close()

    async def get(self, key) -> Optional[int]:
        key = await self.__connection.get(key)
        if isinstance(key, bytes):
            key = key.decode("utf-8")
        return key

    async def set(self, key, value):
        return await self.__connection.set(key, value, ex=settings.redis.ttl)


redis_client = RedisClient()
