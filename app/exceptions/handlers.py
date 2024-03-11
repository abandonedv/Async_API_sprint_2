from elasticsearch import exceptions
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions.entity import EntityNotExistException


async def es_bad_request_error_handler(
    request: Request,
    exc: exceptions.RequestError,
):
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def es_not_found_error_handler(
    request: Request,
    exc: exceptions.NotFoundError,
):
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def entity_not_exist_exception_handler(
    request: Request,
    exc: EntityNotExistException,
):
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=status.HTTP_404_NOT_FOUND,
    )
