import pytest

from app.tests.functional.base_classes.test_base import TestApiBase
from app.tests.functional.utils.helpers import prepare_test_dir


@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_film_all_request"),
)
def test_get_film_all_request(data_dict: dict):
    TestApiBase(**data_dict).perform()


@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_film_all_by_search_request"),
)
def test_get_film_all_by_search_request(data_dict: dict):
    TestApiBase(**data_dict).perform()


@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_film_by_id_request"),
)
def test_get_film_by_id_request(data_dict: dict):
    TestApiBase(**data_dict).perform()
