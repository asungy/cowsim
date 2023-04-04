from abc import ABC, abstractmethod
import uuid


class Entity(ABC):
    @staticmethod
    @abstractmethod
    def key_name() -> str:
        """Key name to be used in environment Entity map."""
        ...

    @classmethod
    @abstractmethod
    def new(cls) -> "Entity":
        """Creates a new instance of an Entity."""
        ...

    @property
    @abstractmethod
    def id(self) -> uuid.UUID:
        """Unique identifier for an Entity instance."""
        ...
