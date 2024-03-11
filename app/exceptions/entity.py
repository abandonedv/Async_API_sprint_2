from dataclasses import dataclass


@dataclass
class EntityException(Exception):
    detail: str


@dataclass
class EntityNotExistException(EntityException):
    pass
