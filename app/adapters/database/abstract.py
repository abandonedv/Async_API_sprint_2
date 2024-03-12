import abc

from pydantic import BaseModel


class NoSQLDatabaseI(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, index: str, _id: str, model: BaseModel) -> dict | None:
        pass
