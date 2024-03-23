import json
import os

TESTDATA_PATH = "app/tests/functional/testdata"


def read_json(path: str) -> list | dict:
    with open(path) as f:
        return json.loads(f.read())


def prepare_test_data(test_name: str) -> list[dict]:
    dir_name = f"{test_name.split('_')[2]}/{test_name}"
    files_path = [
        os.path.split(x)[-1] for x in os.listdir(path=f"{TESTDATA_PATH}/{dir_name}")
    ]

    return [read_json(path=f"{TESTDATA_PATH}/{dir_name}/{file}") for file in files_path]


def load_data(data_name: str) -> list:
    return read_json(path=f"{TESTDATA_PATH}/{data_name}")
