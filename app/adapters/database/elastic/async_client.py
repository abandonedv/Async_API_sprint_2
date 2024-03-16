from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
from pydantic import BaseModel

from app.adapters.database.abstract import NoSQLDatabaseI
from app.core.config import ElasticParams
from app.utils.backoff import backoff


class ElasticClient(NoSQLDatabaseI):
    def __init__(self):
        super().__init__()
        self.config = ElasticParams()
        self.elastic = AsyncElasticsearch(self.config.url())

    @backoff(exceptions=(ConnectionError,))
    async def get_by_id(self, index: str, _id: str, model: BaseModel) -> dict | None:
        try:
            doc = await self.elastic.get(index=index, id=_id)
        except NotFoundError:
            return None
        return model(**doc["_source"])  # noqa

    @backoff(exceptions=(ConnectionError,))
    async def search(self, index: str, body: dict) -> dict:
        result = await self.elastic.search(
            index=index,
            body=body,
        )
        return result
