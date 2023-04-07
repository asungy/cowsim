from .. import Entity
from abc import abstractmethod
from enum import Enum


class Emotion(Enum):
    """Enumeration class for discerning emotional characteristics of cow."""

    CONTENT = 0
    HAPPY = 1
    EXCITED = 2
    CURIOUS = 3
    MELANCHOLIC = 4
    NOSTALGIC = 5
    TIRED = 6
    UPSET = 7
    SCARED = 8
    STRESSED = 9

    @classmethod
    def is_positive(cls, emotion: "Emotion") -> bool:
        """Determines if emotion is classfied as positive.

        Parameters
        ----------
        emotion : Emotion
            Emotion in question.

        Returns
        -------
        bool
            True, if the emotion is classified as positive.
        """
        match emotion:
            case cls.CONTENT | cls.HAPPY | cls.EXCITED:
                return True
            case _:
                return False

    @classmethod
    def is_neutral(cls, emotion: "Emotion") -> bool:
        """Determines if emotion is classfied as neutral.

        Parameters
        ----------
        emotion : Emotion
            Emotion in question.

        Returns
        -------
        bool
            True, if the emotion is classified as neutral.
        """
        match emotion:
            case cls.CURIOUS | cls.MELANCHOLIC | cls.NOSTALGIC:
                return True
            case _:
                return False

    @classmethod
    def is_negative(cls, emotion: "Emotion") -> bool:
        """Determines if emotion is classfied as negative.

        Parameters
        ----------
        emotion : Emotion
            Emotion in question.

        Returns
        -------
        bool
            True, if the emotion is classified as negative.
        """
        match emotion:
            case cls.TIRED | cls.UPSET | cls.SCARED | cls.STRESSED:
                return True
            case _:
                return False


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
