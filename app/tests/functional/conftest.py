import pytest
from redis import Redis

from app.tests.functional.settings import RedisParams

redis_params = RedisParams()


@pytest.fixture(scope="function", autouse=True)
def delete_trash(redis):
    redis.delete("movies:*")
    redis.delete("persons:*")
    redis.delete("genres:*")


@pytest.fixture(scope="function")
def redis() -> Redis:
    redis = Redis(
        host=redis_params.host,
        port=redis_params.port,
        decode_responses=True,
    )
    yield redis
    redis.close()
