import abc

from pydantic import BaseModel


class BaseMixin(BaseModel, abc.ABC):
    id: str
