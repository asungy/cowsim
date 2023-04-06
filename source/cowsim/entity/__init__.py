from abc import ABC, abstractmethod
from enum import Enum
import uuid


class Sex(Enum):
    """Enumeration class for discerning sex of entity."""

    MALE = 1
    FEMALE = 2


class Entity(ABC):
    """Represents a general, living entity.

    Attributes
    ----------
    age : int
        Current age of the entity (in days).

    sex : Sex
        Sex of the entity (expected to be constant for lifetime duration).

    calories : float
        The current caloric levels of the entity (in kilocalorie).

    weight : float
        The current weight of the entity (in kilograms).
    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """Name of entity.

        Returns
        -------
        str
            A name identifying this class.
        """
        ...

    # @classmethod
    # @abstractmethod
    def should_reproduce(cls, entity1: "Entity", entity2: "Entity") -> bool:
        """Determines if two entities should reproduce.

        Parameters
        ----------
        entity1 : Entity
            An arbitrary Entity instance

        entity2 : Entity
            An arbitrary Entity instance

        Returns
        -------
        bool
            True, if entities should reproduce.

        Notes
        -----
        `entity1` and `entity2` cannot be identical.
        """
        ...

    @abstractmethod
    def cause_of_death(self) -> Enum:
        """Determines the reason an entity has perished (if applicable).

        Returns
        -------
        Enum
            An enumeration class denoting cause of death (if any).
        """
        ...

    @abstractmethod
    def expend_calories(self) -> float:
        """Calculates and expends entity's calories.

        Returns
        -------
        float
            Caloric expenditure (in kcal).

        Notes
        -----
        This method mutates self.
        """
        ...

    # @abstractmethod
    def caloric_intake(self, kcal: float) -> float:
        ...

    # @abstractmethod
    def tick(self) -> None:
        ...

    def __init__(self, age: int, sex: Sex, calories: int, weight: int):
        """Organism class constructor."""
        assert age is not None
        assert sex is not None
        assert calories is not None
        assert weight is not None

        self._id = uuid.uuid4()

        self._age = age
        self._sex = sex
        self._calories = calories
        self._weight = weight

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def age(self) -> int:
        return self._age

    @property
    def sex(self) -> Sex:
        return self._sex

    @property
    def calories(self) -> float:
        return self._calories

    @property
    def weight(self) -> float:
        return self._weight
