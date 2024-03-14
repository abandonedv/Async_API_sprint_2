import asyncio

import pytest_asyncio # noqa
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch

from app.tests.functional.settings import RedisParams, ElasticParams
from app.tests.functional.testdata import es_mapping

redis_params = RedisParams()
es_params = ElasticParams()

indexes_mapping = {
    "movies": es_mapping.movies_mapping,
    "persons": es_mapping.persons_mapping,
    "genres": es_mapping.genres_mapping,
}


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def delete_trash(redis):
    await redis.flushall()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def es_create_index(es_client: AsyncElasticsearch):
    for index, mapping in indexes_mapping.items():
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)
        await es_client.indices.create(index=index, **mapping)


@pytest_asyncio.fixture(scope="function")
async def redis() -> Redis:
    redis = Redis(
        host=redis_params.host,
        port=redis_params.port,
        decode_responses=True,
    )
    yield redis
    await redis.aclose()


@pytest_asyncio.fixture(scope="function")
async def es_client():
    es_client = AsyncElasticsearch(es_params.url())
    yield es_client
    await es_client.close()
