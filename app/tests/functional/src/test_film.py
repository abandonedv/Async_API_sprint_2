import pytest

from app.tests.functional.src.base_classes.test_base import TestApiBase
from app.tests.functional.utils.helpers import prepare_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_data(test_name="test_get_film_all_request"),
)
async def test_get_film_all_request(data_dict: dict, es_write_data):
    await es_write_data(data_type="movies")
    await TestApiBase(**data_dict).perform()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_data(test_name="test_get_film_all_request"),
)
async def test_get_film_all_cache_request(data_dict: dict, es_write_data):
    await es_write_data(data_type="movies")
    await TestApiBase(**data_dict).perform(from_cache=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_data(test_name="test_get_film_all_by_search_request"),
)
async def test_get_film_all_by_search_request(data_dict: dict, es_write_data):
    await es_write_data(data_type="movies")
    await TestApiBase(**data_dict).perform()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_data(test_name="test_get_film_all_by_search_request"),
)
async def test_get_film_all_by_search_cache_request(data_dict: dict, es_write_data):
    await es_write_data(data_type="movies")
    await TestApiBase(**data_dict).perform(from_cache=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_data(test_name="test_get_film_by_id_request"),
)
async def test_get_film_by_id_request(data_dict: dict, es_write_data):
    await es_write_data(data_type="movies")
    await TestApiBase(**data_dict).perform()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_data(test_name="test_get_film_by_id_request"),
)
async def test_get_film_by_id_cache_request(data_dict: dict, es_write_data, redis):
    await es_write_data(data_type="movies")
    await TestApiBase(**data_dict).perform(from_cache=True)
