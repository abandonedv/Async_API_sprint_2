from .base import BaseMixin


class Actor(BaseMixin):
    name: str


class Writer(BaseMixin):
    name: str


class Person(BaseMixin):
    full_name: str
