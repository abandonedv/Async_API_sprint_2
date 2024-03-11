from elasticsearch import AsyncElasticsearch

from app.core.config import ElasticParams


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return AsyncElasticsearch(ElasticParams().url())
