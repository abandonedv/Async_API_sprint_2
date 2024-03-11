from pydantic import Field

from .base import BaseMixin
from .person import Actor, Writer


class Film(BaseMixin):
    imdb_rating: float | None
    title: str
    description: str | None
    genre: list[str] = Field(default_factory=list)
    director: str = Field(default_factory=str)
    actors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)
    actors: list[Actor] = Field(default_factory=list)
    writers: list[Writer] = Field(default_factory=list)
