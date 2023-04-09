from abc import ABC, abstractmethod
from ..entity import Entity


class Environment(ABC):
    """Represents the environment for the simulation.

    Attributes
    ----------
    _entities : Dict[str, [Entity]]
        A dictionary where the key is the name of a class dervied from Cow and
        the value is an array of instances of that class.

    _max_capacity : int
        The maximum population size of any given entity that the environment
        can hold.

    _max_steps : int
        Number of steps to run the simulation.

    _steps : int
        Number of steps that have elapsed.
    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """Name of environment.

        Parameters
        ----------
        none

        Returns
        -------
        str
            A name identifying this class.
        """
        ...

    def __init__(
        self,
        max_capacity: int,
        max_steps: int,
    ):
        """Constructor for Environment and derived classes.

        Parameters
        ----------
        max_capacity : int
            The maximum population size of any given entity that the
            environment can hold.

        max_steps : int
            Number of steps to run the simulation.
        """
        self._max_capacity = max_capacity
        self._max_steps = max_steps
        self._steps = 0
        self._entities = {}

    @abstractmethod
    def step(self) -> None:
        """Perform simulation step in environment.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        ...

    @abstractmethod
    def run(self, **kwargs) -> None:
        """Run the entire simulation.

        Parameters
        ----------
        **kwargs
            Necessary arguments for derived classes to initialize simulation.

        """
        ...

    @abstractmethod
    def report(self, directory: str) -> None:
        """Produce report of simulation execution.

        Parameters
        ----------
        directory : str
            Path to output report.

        Returns
        -------
        None
        """
        ...


class Feed(ABC):
    """Abstract class for entity feed.

    Derived classes of Feed should be expected to be provided to a derived
    class of Environment. A single Feed object is expected to provide for
    the entire population in the environment for a single day and the Feed
    class is expected to know how much food to provide to each entity.

    Attributes
    ----------

    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """Name of feed.

        Parameters
        ----------
        none

        Returns
        -------
        str
            A name identifying this class.
        """
        ...

    @property
    @abstractmethod
    def initial_serving_total(self) -> int:
        """Number of original servings when this Feed object was first instantiated.

        Parameters
        ----------
        none

        Returns
        -------
        int
            Number of original servings.
        """
        ...

    @property
    @abstractmethod
    def current_serving_total(self) -> int:
        """Number of current servings in this Feed object.

        Parameters
        ----------

        Returns
        -------
        int
            Number of current servings.
        """
        ...

    @property
    @abstractmethod
    def initial_total_calories(self) -> float:
        """Number of original calories (kcal) contained in this Feed object.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Number of (kilo)calories.
        """
        ...

    @property
    @abstractmethod
    def current_total_calories(self) -> float:
        """Number of current calories (kcal) contained in this Feed object.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Number of (kilo)calories.
        """
        ...

    @property
    @abstractmethod
    def price(self) -> float:
        """Total price of this Feed object.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Price of this Feed object.
        """
        ...

    @abstractmethod
    def feed(self, entity: Entity) -> int:
        """Feeds the provided Entity object.

        Parameters
        ----------
        entity : Entity
            The entity to feed.

        Returns
        -------
        int
            The number of servings given to the entity.
        """
        ...
