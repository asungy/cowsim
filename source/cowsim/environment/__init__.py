from abc import ABC, abstractmethod
from ..entity import Entity


class Environment(ABC):
    """Represents the environment for the simulation."""

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

    @abstractmethod
    def __init__(self, entities: [(Entity, int)]):
        """Constructor for Environment and derived classes.

        Parameters
        ----------
        entities : [(Entity, int)]
            A list of tuples that describe the entities and quantities that
            will inhabit the environment.
        """
        ...

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

    # @abstractmethod
    def run(self, **kwargs) -> None:
        """Run the entire simulation.

        Parameters
        ----------
        **kwargs
            Necessary arguments for derived classes to initialize simulation.

        """
        ...

    # @abstractmethod
    def report(self, filename: str) -> None:
        """Produce report of simulation execution.

        Parameters
        ----------
        filename : str
            Path to output report.

        Returns
        -------
        None
        """
        ...
