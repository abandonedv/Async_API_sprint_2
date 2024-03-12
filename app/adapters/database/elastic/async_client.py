from logging import getLogger

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from pydantic import BaseModel

from app.core.config import ElasticParams
from app.adapters.database.abstract import NoSQLDatabaseI


class ElasticClient(NoSQLDatabaseI):
    def __init__(self):
        self.config = ElasticParams()
        self.elastic = AsyncElasticsearch(self.config.url())
        self.log = getLogger(self.__class__.__name__)

    async def get_by_id(self, index: str, _id: str, model: BaseModel) -> dict | None:
        try:
            doc = await self.elastic.get(index=index, id=_id)
        except NotFoundError:
            return None
        return model(**doc["_source"])  # noqa

    async def search(self, index: str, body: dict) -> dict:
        result = await self.elastic.search(
            index=index,
            body=body,
        )
        return result
