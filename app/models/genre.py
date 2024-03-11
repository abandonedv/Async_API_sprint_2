from .base import BaseMixin


class Genre(BaseMixin):
    name: str
    description: str | None
