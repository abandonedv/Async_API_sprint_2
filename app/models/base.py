from pydantic import BaseModel


class BaseMixin(BaseModel):
    id: str
