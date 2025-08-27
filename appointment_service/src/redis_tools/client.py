from redis.asyncio import from_url

from core.config import settings


class RedisClient:

    def __init__(self):
        self.connection = from_url(settings.redis.url)

    async def close(self):
        await self.connection.close()

    async def get(self, key):
        return await self.connection.get(key)

    async def set(self, key, value):
        return await self.connection.set(key, value, ex=settings.redis.ttl, keepttl=True)



redis_client = RedisClient()
