from .. import Entity
from abc import abstractmethod
from enum import Enum


class Emotion(Enum):
    """Enumeration class for discerning emotional characteristics of cow."""

    CONFUSED = 0
    CONTENT = 1
    CURIOUS = 2
    HAPPY = 3
    JOYFUL = 4
    MELANCHOLIC = 5
    UPSET = 6


class CauseOfDeath(Enum):
    """Enumeration class for identifying why a cow died."""

    NOT_DEAD = 1
    OLD_AGE = 2
    MALNOURISHED = 3
    OVERWEIGHT = 4


class Cow(Entity):
    @abstractmethod
    def milk_production(self) -> float:
        """Calculates milk produced from cow.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Milk produced (in liters).
        """
        ...

    @abstractmethod
    def methane_production(self) -> float:
        """Calculate methane production from cow.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Methane produced (in kilograms).
        """
        ...

    @property
    @abstractmethod
    def emotion(self) -> Emotion:
        """Returns the current emotion of cow.

        Parameters
        ----------

        Returns
        -------
        Emotion
            The emotion describing the cow's internal state.
        """
        ...
