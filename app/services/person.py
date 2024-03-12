from functools import lru_cache

from fastapi import Depends

from app.adapters.database.abstract import CacheDatabaseI, NoSQLDatabaseI
from app.adapters.database.elastic.async_client import ElasticClient
from app.adapters.database.redis.async_client import RedisClient
from app.models.person import Person
from app.services.base import BaseService
from app.utils.es import get_offset, get_sort_params


class PersonService(BaseService):
    def __init__(self, cache: CacheDatabaseI, db: NoSQLDatabaseI):
        super().__init__(cache, db)
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
        persons = await self.cache.get_by_params(
            params=params,
            index=self.index_name,
            model=self.model,
        )
        if not persons:
            # Если персон нет в кеше, то ищем его в Elasticsearch
            persons = await self._get_persons_from_elastic(**params)
            if not persons:
                # Если он отсутствует в Elasticsearch, значит, персоны вообще нет в базе
                return []
            # Сохраняем персону  в кеш
            await self.cache.add_many(
                entities=persons,
                params=params,
                index=self.index_name,
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
        persons = await self.cache.get_by_params(
            params=params,
            index=self.index_name,
            model=self.model,
        )
        if not persons:
            # Если персон нет в кеше, то ищем его в Elasticsearch
            persons = await self._get_persons_from_elastic_match(**params)
            if not persons:
                # Если он отсутствует в Elasticsearch, значит, персоны вообще нет в базе
                return []
            # Сохраняем персону  в кеш
            await self.cache.add_many(
                entities=persons,
                params=params,
                index=self.index_name,
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

        result = await self.db.search(
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

        result = await self.db.search(
            index=self.index_name,
            body=body,
        )

        return [Person(**hit["_source"]) for hit in result["hits"]["hits"]]


@lru_cache()
def get_person_service(
    redis: CacheDatabaseI = Depends(RedisClient),
    elastic: NoSQLDatabaseI = Depends(ElasticClient),
) -> PersonService:
    return PersonService(redis, elastic)
