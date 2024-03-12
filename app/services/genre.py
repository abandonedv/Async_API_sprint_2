from functools import lru_cache

from fastapi import Depends

from app.adapters.database.elastic.async_client import ElasticClient
from app.adapters.database.redis.async_client import RedisClient
from app.models.genre import Genre
from app.services.base import BaseService
from app.utils.es import get_offset, get_sort_params


class GenreService(BaseService):
    def __init__(self, cache: RedisClient, elastic: ElasticClient):
        super().__init__(cache, elastic)
        self.index_name = "genres"
        self.model = Genre

    async def get_genres(
        self,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Genre]:
        params = dict(
            sort=sort,
            page_number=page_number,
            page_size=page_size,
        )

        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        genres = await self.cache.get_by_params(
            params=params,
            index=self.index_name,
            model=self.model,
        )
        if not genres:
            # Если жанров нет в кеше, то ищем его в Elasticsearch
            genres = await self._get_genres_from_elastic(**params)
            if not genres:
                # Если он отсутствует в Elasticsearch, значит, жанра вообще нет в базе
                return []
            # Сохраняем жанр  в кеш
            await self.cache.add_many(
                entities=genres,
                params=params,
                index=self.index_name,
            )

        return genres

    async def get_genres_by_search(
        self,
        query: str,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Genre]:
        params = dict(
            query=query,
            sort=sort,
            page_number=page_number,
            page_size=page_size,
        )

        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        genres = await self.cache.get_by_params(
            params=params,
            index=self.index_name,
            model=self.model,
        )
        if not genres:
            # Если жанров нет в кеше, то ищем его в Elasticsearch
            genres = await self._get_genres_from_elastic_match(**params)
            if not genres:
                # Если он отсутствует в Elasticsearch, значит, жанра вообще нет в базе
                return []
            # Сохраняем жанр  в кеш
            await self.cache.add_many(
                entities=genres,
                params=params,
                index=self.index_name,
            )

        return genres

    async def _get_genres_from_elastic(
        self,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Genre]:
        sort_type, field_name = get_sort_params(sort=sort)
        offset = get_offset(page_number=page_number, page_size=page_size)

        if field_name == "name":
            field_name = "name.raw"

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

        return [Genre(**hit["_source"]) for hit in result["hits"]["hits"]]

    async def _get_genres_from_elastic_match(
        self,
        query: str,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Genre]:
        sort_type, field_name = get_sort_params(sort=sort)
        offset = get_offset(page_number=page_number, page_size=page_size)

        if field_name == "name":
            field_name = "name.raw"

        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["name", "description"],
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

        return [Genre(**hit["_source"]) for hit in result["hits"]["hits"]]


@lru_cache()
def get_genre_service(
    redis: RedisClient = Depends(RedisClient),
    elastic: ElasticClient = Depends(ElasticClient),
) -> GenreService:
    return GenreService(redis, elastic)
