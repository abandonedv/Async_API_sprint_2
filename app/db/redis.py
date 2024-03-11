from redis.asyncio import Redis

from app.core.config import RedisParams


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return Redis(**RedisParams().model_dump())
