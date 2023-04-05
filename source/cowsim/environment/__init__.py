from abc import ABC, abstractmethod
from cowsim.entity import Entity
import uuid


class Environment(ABC):
    @property
    @abstractmethod
    def id(self) -> uuid.UUID:
        """Unique identifier for an Environment instance."""
        ...

    @abstractmethod
    def add_entity(self, entity_class: Entity, count: int) -> None:
        """Initialize Entity class with a given count."""
        ...
