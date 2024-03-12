from functools import lru_cache

from fastapi import Depends

from app.adapters.database.abstract import CacheDatabaseI, NoSQLDatabaseI
from app.adapters.database.elastic.async_client import ElasticClient
from app.adapters.database.redis.async_client import RedisClient
from app.models.film import Film
from app.services.base import BaseService
from app.utils.es import get_offset, get_sort_params


class FilmService(BaseService):
    def __init__(self, cache: CacheDatabaseI, db: NoSQLDatabaseI):
        super().__init__(cache, db)
        self.index_name = "movies"
        self.model = Film

    async def get_films(
        self,
        sort: str,
        genre: str | None,
        actor: str | None,
        writer: str | None,
        page_number: int,
        page_size: int,
    ) -> list[Film]:
        params = dict(
            sort=sort,
            genre=genre,
            actor=actor,
            writer=writer,
            page_number=page_number,
            page_size=page_size,
        )

        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        films = await self.cache.get_by_params(
            params=params,
            index=self.index_name,
            model=self.model,
        )
        if not films:
            # Если фильмов нет в кеше, то ищем его в Elasticsearch
            films = await self._get_films_from_elastic_term(**params)
            if not films:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return []
            # Сохраняем фильм  в кеш
            await self.cache.add_many(
                entities=films,
                params=params,
                index=self.index_name,
            )

        return films

    async def get_films_by_search(
        self,
        query: str,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Film]:
        params = dict(
            query=query,
            sort=sort,
            page_number=page_number,
            page_size=page_size,
        )

        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        films = await self.cache.get_by_params(
            params=params,
            index=self.index_name,
            model=self.model,
        )
        if not films:
            # Если фильмов нет в кеше, то ищем его в Elasticsearch
            films = await self._get_films_from_elastic_match(**params)
            if not films:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return []
            # Сохраняем фильм  в кеш
            await self.cache.add_many(
                entities=films,
                params=params,
                index=self.index_name,
            )

        return films

    async def _get_films_from_elastic_term(
        self,
        sort: str,
        genre: str | None,
        actor: str | None,
        writer: str | None,
        page_number: int,
        page_size: int,
    ) -> list[Film]:
        sort_type, field_name = get_sort_params(sort=sort)
        offset = get_offset(page_number=page_number, page_size=page_size)

        if field_name == "title":
            field_name = "title.raw"

        body = {
            "from": offset,
            "size": page_size,
            "sort": [
                {field_name: sort_type},
            ],
        }

        if genre or actor or writer:
            body["query"] = {"bool": {"must": []}}
            if genre:
                body["query"]["bool"]["must"].append({"term": {"genre": genre}})
            if actor:
                body["query"]["bool"]["must"].append(
                    {"term": {"actors_names.raw": actor}},
                )
            if writer:
                body["query"]["bool"]["must"].append(
                    {"term": {"writers_names.raw": writer}},
                )

        result = await self.db.search(
            index=self.index_name,
            body=body,
        )

        return [Film(**hit["_source"]) for hit in result["hits"]["hits"]]

    async def _get_films_from_elastic_match(
        self,
        query: str,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[Film]:
        sort_type, field_name = get_sort_params(sort=sort)
        offset = get_offset(page_number=page_number, page_size=page_size)

        if field_name == "title":
            field_name = "title.raw"

        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description"],
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

        return [Film(**hit["_source"]) for hit in result["hits"]["hits"]]


@lru_cache()
def get_film_service(
    redis: CacheDatabaseI = Depends(RedisClient),
    elastic: NoSQLDatabaseI = Depends(ElasticClient),
) -> FilmService:
    return FilmService(redis, elastic)
