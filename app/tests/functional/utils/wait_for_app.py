import logging
import time

import requests

from app.tests.functional.settings import ServiceParams

if __name__ == "__main__":
    with requests.session() as session:
        while True:
            response = session.get(f"{ServiceParams().url()}/api/openapi")
            if response.status_code == 200:
                break
            logging.warning("App is not available")
            time.sleep(1)
