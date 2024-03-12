from hashlib import md5

import orjson
from redis.asyncio import Redis

from app.adapters.database.elastic.async_client import ElasticClient
from app.exceptions.entity import EntityNotExistException
from app.models.base import BaseMixin


class BaseService:
    def __init__(self, redis: Redis, elastic: ElasticClient):
        self.redis = redis
        self.elastic = elastic
        self.index_name = None
        self.cache_timeout = 60 * 5  # 5 минут
        self.model = BaseMixin

    async def get_by_id(self, _id: str) -> BaseMixin | None:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        entity = await self._entity_from_cache(_id=_id)
        if not entity:
            # Если записи нет в кеше, то ищем ее в Elasticsearch
            entity = await self.elastic.get_by_id(
                _id=_id, index=self.index_name, model=self.model
            )
            if not entity:
                # Если она отсутствует в Elasticsearch, значит, записи вообще нет в базе
                raise EntityNotExistException(
                    detail=f"{self.model.__name__} with id = {_id!r} not found",
                )
            # Сохраняем запись в кеш
            await self._put_entity_to_cache(entity=entity)

        return entity

    async def _entity_from_cache(self, _id: str) -> BaseMixin | None:
        data = await self.redis.get(f"{self.index_name}:{_id}")
        if not data:
            return None

        return self.model.model_validate_json(json_data=data)

    async def _entities_from_cache(
        self,
        params: dict,
    ) -> list[BaseMixin]:
        params = md5(orjson.dumps(params)).hexdigest()
        data = await self.redis.get(f"{self.index_name}:{params}")
        if not data:
            return []

        data = orjson.loads(data)
        return [self.model(**orjson.loads(entity)) for entity in data]

    async def _put_entity_to_cache(self, entity: BaseMixin):
        await self.redis.set(
            f"{self.index_name}:{entity.id}",
            entity.model_dump_json(),
            self.cache_timeout,
        )

    async def _put_entities_to_cache(
        self,
        entities: list[BaseMixin],
        params: dict,
    ):
        entities = [entity.model_dump_json() for entity in entities]
        data = orjson.dumps(entities)
        params = md5(orjson.dumps(params)).hexdigest()
        await self.redis.set(
            f"{self.index_name}:{params}",
            data,
            self.cache_timeout,
        )
