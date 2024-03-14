import pytest

from app.tests.functional.base_classes.test_base import TestApiBase
from app.tests.functional.utils.helpers import prepare_test_dir


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_person_all_request"),
)
async def test_get_person_all_request(data_dict: dict):
    await TestApiBase(**data_dict).perform()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_person_all_by_search_request"),
)
async def test_get_person_all_by_search_request(data_dict: dict):
    await TestApiBase(**data_dict).perform()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_person_by_id_request"),
)
async def test_get_person_by_id_request(data_dict: dict):
    await TestApiBase(**data_dict).perform()
