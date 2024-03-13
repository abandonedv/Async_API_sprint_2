import time
import logging

from redis import Redis

from app.tests.functional.settings import RedisParams

if __name__ == '__main__':
    params = RedisParams()
    redis_client = Redis(**params.model_dump())
    while True:
        if redis_client.ping():
            break
        logging.warning("Redis is not available")
        time.sleep(1)
