from elasticsearch import exceptions
from fastapi import FastAPI

from app.exceptions.entity import EntityNotExistException
from app.exceptions.handlers import (
    entity_not_exist_exception_handler,
    es_bad_request_error_handler,
    es_not_found_error_handler,
)


def bind_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        exceptions.RequestError,
        es_bad_request_error_handler,
    )
    app.add_exception_handler(
        exceptions.NotFoundError,
        es_not_found_error_handler,
    )
    app.add_exception_handler(
        EntityNotExistException,
        entity_not_exist_exception_handler,
    )
