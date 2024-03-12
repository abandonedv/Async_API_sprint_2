import abc
from typing import Type

from pydantic import BaseModel


class NoSQLDatabaseI(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(
        self,
        index: str,
        _id: str,
        model: Type[BaseModel],
    ) -> BaseModel | None:
        pass


class CacheDatabaseI(NoSQLDatabaseI):
    @abc.abstractmethod
    async def get_by_params(
        self,
        params: dict,
        index: str,
        model: Type[BaseModel],
    ) -> list[BaseModel]:
        pass

    @abc.abstractmethod
    async def add_one(self, entity: BaseModel, index: str):
        pass

    @abc.abstractmethod
    async def add_many(
        self,
        entities: list[BaseModel],
        params: dict,
        index: str,
    ):
        pass
