from ..entity.cow import Cow
from ..environment import Environment


class Cowpen(Environment):
    """Cowpen simulation environment to understand milk and emission
    production from cows.

    Attributes
    ----------
    _entities : Dict[Entity, int]
        A dictionary where the key is the name of a class dervied from Cow and
        the value is an array of instances of that class.

    _max_size : int
        The maximum population size that the environment can hold.
    """

    @staticmethod
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
        return "Cowpen"

    def __init__(self, entities: [(Cow, int)], max_size: int):
        """Constructor for Environment and derived classes.

        Parameters
        ----------
        entities : [(Entity, int)]
            A list of tuples that describe the cows and quantities that
            will inhabit the environment.

        Raises
        ------
        RuntimeError
            - If entity is not derived from Cow.
            - If quantity is less than zero.
        """
        self._entities = {}
        for tup in entities:
            if not issubclass(tup[0], Cow):
                raise RuntimeError("Entity provided in not cow.")

            if tup[1] <= 0:
                raise RuntimeError("Quantity provided is non-positive.")

            entity = tup[0]
            quantity = tup[1]
            entity_list = [entity.generate() for _ in range(quantity)]
            if entity.name() not in self._entities:
                self._entities[entity.name()] = []

            self._entities[entity.name()] += entity_list

    def step(self) -> None:
        """Perform simulation step in cowpen.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        pass

    def _reproduction_phase(self) -> None:
        """ """
        pass

    def _feeding_phase(self) -> None:
        """ """
        pass

    def _population_pruning_phase(self) -> None:
        """ """
        pass

    def _energy_expenditure_phase(self) -> None:
        """ """
        pass

    def _milk_production_phase(self) -> None:
        """ """
        pass

    def _methane_production_phase(self) -> None:
        """ """
        pass
