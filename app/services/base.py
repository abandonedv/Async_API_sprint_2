import abc

from app.adapters.database.abstract import CacheDatabaseI, NoSQLDatabaseI
from app.exceptions.entity import EntityNotExistException
from app.models.base import BaseMixin


class ServiceI(abc.ABC):
    def __init__(self, cache: CacheDatabaseI, db: NoSQLDatabaseI):
        self.cache = cache
        self.db = db
        self.index_name = None
        self.model = BaseMixin

    async def get_by_id(self, _id: str) -> BaseMixin:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        entity = await self.cache.get_by_id(
            _id=_id,
            index=self.index_name,
            model=self.model,
        )
        if not entity:
            # Если записи нет в кеше, то ищем ее в Elasticsearch
            entity = await self.db.get_by_id(
                _id=_id,
                index=self.index_name,
                model=self.model,
            )
            if not entity:
                # Если она отсутствует в Elasticsearch, значит, записи вообще нет в базе
                raise EntityNotExistException(
                    detail=f"{self.model.__name__} with id = {_id!r} not found",
                )
            # Сохраняем запись в кеш
            await self.cache.add_one(entity=entity, index=self.index_name)

        return entity

    @abc.abstractmethod
    async def get_many_by_search(
        self,
        query: str,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[BaseMixin]:
        pass

    @abc.abstractmethod
    async def _get_many_from_db_match(
        self,
        query: str,
        sort: str,
        page_number: int,
        page_size: int,
    ) -> list[BaseMixin]:
        pass
