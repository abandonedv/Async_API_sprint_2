import json
import os

TEST_DATA_DIR_PATH = "tests/api_tests/test_data/"
TEST_FILES_DIR_PATH = "tests/api_tests/test_files/"
TEST_SQL_DIR_PATH = "tests/api_tests/test_sql/"


def read_json(path: str):
    with open(TEST_DATA_DIR_PATH + path) as f:
        return json.loads(f.read())


def prepare_test_dir(test_name: str):
    dir_name = f"{test_name.split('_')[2]}/{test_name}"
    files_path = [
        os.path.split(x)[-1] for x in os.listdir(path=TEST_DATA_DIR_PATH + dir_name)
    ]

    return [read_json(path=f"{dir_name}/{file}") for file in files_path]
