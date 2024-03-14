import pytest_asyncio  # noqa
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from redis.asyncio import Redis

from app.tests.functional.settings import ElasticParams, RedisParams
from app.tests.functional.testdata import es_mapping
from app.tests.functional.utils.helpers import read_json

redis_params = RedisParams()
es_params = ElasticParams()

indexes_mapping = {
    "movies": es_mapping.movies_mapping,
    "persons": es_mapping.persons_mapping,
    "genres": es_mapping.genres_mapping,
}


@pytest_asyncio.fixture(scope="function", autouse=True)
async def delete_trash(redis):
    await redis.flushall()


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


@pytest_asyncio.fixture(name="es_write_data")
def es_write_data():
    async def inner(data_type: str):
        es_client = AsyncElasticsearch(es_params.url())

        if await es_client.indices.exists(index=data_type):
            await es_client.indices.delete(index=data_type)
        await es_client.indices.create(index=data_type, **indexes_mapping[data_type])

        data = read_json(path=f"{data_type}.json")

        updated, errors = await async_bulk(client=es_client, actions=data, refresh=True)

        await es_client.close()

        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner
