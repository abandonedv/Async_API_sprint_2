import json
import os

TESTDATA_PATH = "app/tests/functional/testdata/"


def read_json(path: str):
    with open(TESTDATA_PATH + path) as f:
        return json.loads(f.read())


def prepare_test_dir(test_name: str):
    dir_name = f"{test_name.split('_')[2]}/{test_name}"
    files_path = [
        os.path.split(x)[-1] for x in os.listdir(path=TESTDATA_PATH + dir_name)
    ]

    return [read_json(path=f"{dir_name}/{file}") for file in files_path]
