from hashlib import md5
from logging import getLogger

import orjson
from pydantic import BaseModel
from redis.asyncio import Redis

from app.adapters.database.abstract import NoSQLDatabaseI
from app.core.config import RedisParams


class RedisClient(NoSQLDatabaseI):
    def __init__(self):
        self.config = RedisParams()
        self.redis = Redis(**self.config.model_dump())
        self.cache_timeout = 60 * 5  # 5 минут
        self.log = getLogger(self.__class__.__name__)

    async def get_by_id(
        self, _id: str, index: str, model: BaseModel
    ) -> BaseModel | None:
        data = await self.redis.get(f"{index}:{_id}")
        if not data:
            return None

        return model.model_validate_json(json_data=data)

    async def get_by_params(
        self,
        params: dict,
        index: str,
        model: BaseModel,
    ) -> list[BaseModel]:
        params = md5(orjson.dumps(params)).hexdigest()
        data = await self.redis.get(f"{index}:{params}")
        if not data:
            return []

        data = orjson.loads(data)
        return [model(**orjson.loads(entity)) for entity in data]

    async def add_one(self, entity: BaseModel, index: str):
        await self.redis.set(
            f"{index}:{entity.id}",
            entity.model_dump_json(),
            self.cache_timeout,
        )

    async def add_many(
        self,
        entities: list[BaseModel],
        params: dict,
        index: str,
    ):
        entities = [entity.model_dump_json() for entity in entities]
        data = orjson.dumps(entities)
        params = md5(orjson.dumps(params)).hexdigest()
        await self.redis.set(
            f"{index}:{params}",
            data,
            self.cache_timeout,
        )
