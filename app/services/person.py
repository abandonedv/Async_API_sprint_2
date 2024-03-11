from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from app.db.elastic import get_elastic
from app.db.redis import get_redis
from app.models.person import Person
from app.services.base import BaseService
from app.utils.es import get_offset, get_sort_params


class PersonService(BaseService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.index_name = "persons"
        self.model = Person

    async def get_persons(
        self,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Person]:
        params = dict(
            sort=sort,
            page_number=page_number,
            page_size=page_size,
        )

        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        persons = await self._entities_from_cache(params=params)
        if not persons:
            # Если персон нет в кеше, то ищем его в Elasticsearch
            persons = await self._get_persons_from_elastic(**params)
            if not persons:
                # Если он отсутствует в Elasticsearch, значит, персоны вообще нет в базе
                return []
            # Сохраняем персону  в кеш
            await self._put_entities_to_cache(
                entities=persons,
                params=params,
            )

        return persons

    async def get_persons_by_search(
        self,
        query: str,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Person]:
        params = dict(
            query=query,
            sort=sort,
            page_number=page_number,
            page_size=page_size,
        )

        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        persons = await self._entities_from_cache(params=params)
        if not persons:
            # Если персон нет в кеше, то ищем его в Elasticsearch
            persons = await self._get_persons_from_elastic_match(**params)
            if not persons:
                # Если он отсутствует в Elasticsearch, значит, персоны вообще нет в базе
                return []
            # Сохраняем персону  в кеш
            await self._put_entities_to_cache(
                entities=persons,
                params=params,
            )

        return persons

    async def _get_persons_from_elastic(
        self,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Person]:
        sort_type, field_name = get_sort_params(sort=sort)
        offset = get_offset(page_number=page_number, page_size=page_size)

        if field_name == "full_name":
            field_name = "full_name.raw"

        body = {
            "from": offset,
            "size": page_size,
            "sort": [
                {field_name: sort_type},
            ],
        }

        result = await self.elastic.search(
            index=self.index_name,
            body=body,
        )

        return [Person(**hit["_source"]) for hit in result["hits"]["hits"]]

    async def _get_persons_from_elastic_match(
        self,
        query: str,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Person]:
        sort_type, field_name = get_sort_params(sort=sort)
        offset = get_offset(page_number=page_number, page_size=page_size)

        if field_name == "full_name":
            field_name = "full_name.raw"

        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["full_name"],
                },
            },
            "from": offset,
            "size": page_size,
            "sort": [
                {field_name: sort_type},
            ],
        }

        result = await self.elastic.search(
            index=self.index_name,
            body=body,
        )

        return [Person(**hit["_source"]) for hit in result["hits"]["hits"]]


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
