from ..entity import Entity
import uuid


class Cow(Entity):
    def __init__(self, age):
        self._age = age
        self._id = uuid.uuid4()

    @property
    def id(self):
        return self._id

    @property
    def age(self):
        return self._age
