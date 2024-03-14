import logging
import time

from elasticsearch import Elasticsearch

from app.tests.functional.settings import ElasticParams

if __name__ == "__main__":
    params = ElasticParams()
    es_client = Elasticsearch(params.url())
    while True:
        if es_client.ping():
            break
        logging.warning("ES is not available")
        time.sleep(1)
