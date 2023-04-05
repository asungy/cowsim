from .. import Entity
from abc import abstractmethod
from enum import Enum


class Emotion(Enum):
    """Enumeration class for discerning emotional characteristics of cow."""
    CONFUSED    = 0
    CONTENT     = 1
    CURIOUS     = 2
    JOYFUL      = 3
    MELANCHOLIC = 4
    UPSET       = 5


class CauseOfDeath(Enum):
    """Enumeration class for identifying why a cow died."""
    NOT_DEAD = 1
    OLD_AGE = 2
    MALNOURISHED = 3
    OVERWEIGHT = 4


class Cow(Entity):
    @classmethod
    @abstractmethod
    def generate(cls) -> "Cow":
        """Randomly generate an instance of a Cow."""
        ...

    # @abstractmethod
    def milk_production(self) -> float:
        ...

    # @abstractmethod
    def methane_production(self) -> float:
        ...

    # @abstractmethod
    def feed_requirement(self) -> float:
        ...

    # @abstractmethod
    def emotion(self) -> Emotion:
        ...

    # @abstractmethod
    def talk(self) -> str:
        ...
