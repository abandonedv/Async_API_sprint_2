import pytest

from tests.api_tests.base_classes.test_base import TestApiBase
from tests.api_tests.test_utils import prepare_test_dir


@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_person_all_request"),
)
def test_get_person_all_request(data_dict: dict):
    TestApiBase(**data_dict).perform()


@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_person_all_by_search_request"),
)
def test_get_person_all_by_search_request(data_dict: dict):
    TestApiBase(**data_dict).perform()


@pytest.mark.parametrize(
    "data_dict",
    prepare_test_dir(test_name="test_get_person_by_id_request"),
)
def test_get_person_by_id_request(data_dict: dict):
    TestApiBase(**data_dict).perform()
