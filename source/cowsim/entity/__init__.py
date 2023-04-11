from abc import abstractmethod
from enum import Enum
import uuid

from cowsim.utils.named_abc import Named_ABC


class Sex(Enum):
    """Enumeration class for discerning sex of entity."""

    MALE = 1
    FEMALE = 2


class Entity(Named_ABC):
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

    @classmethod
    @abstractmethod
    def generate(cls) -> "Entity":
        """Randomly generate an instance of a entity.

        Parameters
        ----------
        none

        Returns
        -------
        Entity
            A randomly generated Entity.
        """
        ...

    @classmethod
    @abstractmethod
    def newborn(cls) -> "Entity":
        """Generates a newborn entity (when two entities reproduce).

        Parameters
        ----------
        none

        Returns
        -------
        Entity
            A newborn entity.
        """
        ...


    @classmethod
    @abstractmethod
    def should_reproduce(cls, entity_a: "Entity", entity_b: "Entity") -> bool:
        """Determines if two entities should reproduce.

        Parameters
        ----------
        entity_a : Entity
            An arbitrary Entity instance

        entity_b : Entity
            An arbitrary Entity instance

        Returns
        -------
        bool
            True, if entities should reproduce.

        Notes
        -----
        `entity_a` and `entity_b` cannot be identical.
        """
        ...

    @abstractmethod
    def cause_of_death(self) -> Enum:
        """Returns an enumerated class indicating the cause of death of an
        entity (if applicable).

        Parameters
        ----------
        none

        Returns
        -------
        Enum
            Instance of enumerated class.
        """
        ...

    @abstractmethod
    def expend_calories(self) -> float:
        """Calculates and expends entity's calories.

        If the calculated caloric expenditure falls below some minimum caloric
        bound, then it will cause the entity to lose weight.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Caloric expenditure (in kcal).

        Notes
        -----
        This method mutates self.
        """
        ...

    @abstractmethod
    def caloric_intake(self, kcal: float) -> float:
        """Causes entity to ingest specified calorie.

        If the specified caloric intake is above some maximum caloric bound,
        then it will cause the entity to gain weight.

        Parameters
        ----------
        kcal : float
            Calories to be ingested

        Returns
        -------
        float
            Caloric increase of entity
        """
        ...

    def __init__(self, age: int, sex: Sex, calories: float, weight: float):
        """Entity class constructor.

        Parameters
        ----------
        age : int
            The age of the entity.

        sex : Sex
            The sex of the entity.

        calories : float
            The initial caloric levels of the entity.

        weight : float
            The initial weight of the entity.

        Raises
        ------
        AssertionError
            If any of the arguments are None.
        """
        assert age is not None
        assert sex is not None
        assert calories is not None
        assert weight is not None

        self._id = uuid.uuid4()

        self._age = age
        self._sex = sex
        self._calories = calories
        self._weight = weight

    def __str__(self):
        return f"{self.__class__.name} [{str(self._id)[:8]}]"

    @property
    def id(self) -> uuid.UUID:
        """Unique identifier for entity."""
        return self._id

    @property
    def age(self) -> int:
        """Age of entity."""
        return self._age

    @property
    def sex(self) -> Sex:
        """Sex of entity."""
        return self._sex

    @property
    def calories(self) -> float:
        """Caloric levels of entity."""
        return self._calories

    @property
    def weight(self) -> float:
        """Weight of entity."""
        return self._weight

    def increment_age(self) -> None:
        """Increment age.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        self._age += 1
