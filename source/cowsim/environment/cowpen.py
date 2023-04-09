from ..entity.cow import Cow, CauseOfDeath
from ..environment import Environment, Feed
from cowsim.utils import LOG
from typing import Type
import math
import os
import pandas as pd
import pathlib
import random


class CowPen(Environment):
    """CowPen simulation environment to understand milk and emission
    production from cows.

    Attributes
    ----------
    _feeding_data: Dict[str, pd.DataFrame]
        Records the number of servings given to each cow at each simulation step.

    _milk_data : Dict[str, pd.DataFrame]
        Records the milk production at each simulation step.

    _methane_data : Dict[str, pd.DataFrame]
        Records the methane production at each simulation step.

    _population_data : pd.DataFrame
        Records the population at each simulation step.

    _entity : pd.DataFrame
        Records data of the entity at each simulation step. Data is stored in tuple form:
            (age, calories, weight)

    _feed : tuple[Type[Feed], int]
        A tuple containing the type of Feed and the number of servings to
        provide to the cow pen at each simulation step.
    """

    DEFAULT_MAX_CAPACITY = 100
    DEFAULT_STEPS = 365

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
        return "Cow Pen"

    def __init__(
        self,
        entities: [(Type[Cow], int)],
        max_capacity: int = DEFAULT_MAX_CAPACITY,
        max_steps: int = DEFAULT_STEPS,
    ):
        """Constructor for Environment and derived classes.

        Parameters
        ----------
        entities : [(Entity, int)]
            A list of tuples that describe the cows and quantities that
            will inhabit the environment.

        max_capacity : int
            The maximum population capacity of any given entity that the
            environment can hold.

        max_steps : int
            Number of steps to run the simulation.

        Raises
        ------
        RuntimeError
            - If entity is not derived from Cow.
            - If quantity is less than zero.
        """
        super().__init__(max_capacity, max_steps)
        self._feed = (OrangeGrass, max_capacity)

        # Generating cows for the cow pen.
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

        self._feeding_data = {}
        for key in self._entities.keys():
            self._feeding_data[key] = pd.DataFrame(
                columns=[cow.id for cow in self._entities[key]],
                index=[x for x in range(self._max_steps)],
            )

        self._milk_data = {}
        for key in self._entities.keys():
            self._milk_data[key] = pd.DataFrame(
                columns=[cow.id for cow in self._entities[key]],
                index=[x for x in range(self._max_steps)],
            )

        self._methane_data = {}
        for key in self._entities.keys():
            self._methane_data[key] = pd.DataFrame(
                columns=[cow.id for cow in self._entities[key]],
                index=[x for x in range(self._max_steps)],
            )

        self._population_data = pd.DataFrame(
            columns=[key for key in self._entities.keys()],
            index=[x for x in range(self._max_steps)],
        )

        self._entity_data = {}
        for key in self._entities.keys():
            self._entity_data[key] = pd.DataFrame(
                columns=[cow.id for cow in self._entities[key]],
                index=[x for x in range(self._max_steps)],
            )

    def step(self) -> None:
        """Perform simulation step in cowpen.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        # Record population
        for key in self._entities.keys():
            self._population_data[key].iloc[self._steps] = len(self._entities[key])

        # Record entity data
        for key in self._entities.keys():
            for entity in self._entities[key]:
                self._entity_data[key][entity.id].iloc[self._steps] = (
                    entity.age,
                    entity.calories,
                    entity.weight,
                )

        self._feeding_phase()
        self._reproduction_phase()
        self._energy_expenditure_phase()
        self._population_pruning_phase()
        self._milk_production_phase()
        self._methane_production_phase()

        # Age population
        for key in self._entities.keys():
            for entity in self._entities[key]:
                entity.increment_age()

        self._steps += 1

    def run(self) -> None:
        """Run the entire simulation.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        for _ in range(self._max_steps):
            LOG.info(f"Starting iteration {self._steps}")

            for key in self._entities.keys():
                if len(self._entities[key]) == 0:
                    LOG.warning(
                        f"The {key} population is extinct. Stopping simulation at step {self._steps}."
                    )
                    return

            self.step()
            LOG.info(f"Finishing iteration {self._steps}")

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
        dir_path = pathlib.Path(directory)
        dir_path.resolve()
        if not dir_path.is_dir():
            LOG.info(f"Creating directory: {dir_path}")
            os.makedirs(directory)

        for key in self._entities.keys():
            self._population_data[key].to_csv(
                dir_path.joinpath(f"{key}_population.csv")
            )
            self._entity_data[key].to_csv(dir_path.joinpath(f"{key}_entities.csv"))
            self._feeding_data[key].to_csv(dir_path.joinpath(f"{key}_feeding.csv"))
            self._milk_data[key].to_csv(dir_path.joinpath(f"{key}_milk.csv"))
            self._methane_data[key].to_csv(dir_path.joinpath(f"{key}_methane.csv"))

    def set_feed(self, feed: Type[Feed], servings: int) -> None:
        """Set feed for cow pen environment.

        Parameters
        ----------
        feed : Type[Feed]
            The Feed class object to feed the cows.

        servings : int
            The number of servings to provide the pen each simulation step.

        Returns
        -------
        None
        """
        self._feed = (feed, servings)

    def _feeding_phase(self) -> None:
        """Perform the feeding phase of the simulation.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        for key in self._entities.keys():
            entity_list = self._entities[key]
            random.shuffle(entity_list)
            feed = self._feed[0](self._feed[1], entity_list)
            for entity in entity_list:
                servings = feed.feed(entity)
                # Log feeding data
                self._feeding_data[entity.__class__.name()][entity.id].iloc[
                    self._steps
                ] = servings

    def _reproduction_phase(self) -> None:
        """Perform the reproduction phase of the simulation.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        for key in self._entities.keys():
            for entity_a in self._entities[key]:
                for entity_b in self._entities[key]:
                    if entity_a.__class__.should_reproduce(entity_a, entity_b):
                        new_entity = entity_a.__class__.newborn()
                        self._entities[key].append(new_entity)

                        # Add column to feeding dataframe.
                        df = self._feeding_data[new_entity.__class__.name()]
                        new_col = pd.DataFrame(
                            columns=[new_entity.id],
                            index=[x for x in range(self._max_steps)],
                        )
                        self._feeding_data[new_entity.__class__.name()] = pd.concat(
                            (df, new_col),
                            axis=1,
                        )

                        # Add column to milk dataframe
                        df = self._milk_data[new_entity.__class__.name()]
                        new_col = pd.DataFrame(
                            columns=[new_entity.id],
                            index=[x for x in range(self._max_steps)],
                        )
                        self._milk_data[new_entity.__class__.name()] = pd.concat(
                            (df, new_col),
                            axis=1,
                        )

                        # Add column to methane dataframe
                        df = self._methane_data[new_entity.__class__.name()]
                        new_col = pd.DataFrame(
                            columns=[new_entity.id],
                            index=[x for x in range(self._max_steps)],
                        )
                        self._methane_data[new_entity.__class__.name()] = pd.concat(
                            (df, new_col),
                            axis=1,
                        )

                        # Add column to weight dataframe.
                        df = self._entity_data[new_entity.__class__.name()]
                        new_col = pd.DataFrame(
                            columns=[new_entity.id],
                            index=[x for x in range(self._max_steps)],
                        )
                        self._entity_data[new_entity.__class__.name()] = pd.concat(
                            (df, new_col),
                            axis=1,
                        )

                        LOG.info(f"{entity_a} and {entity_b} reproduced {new_entity}")

    def _population_pruning_phase(self) -> None:
        """Perform population pruning phase of the simulation.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        # Check if entities should die from any conditions.
        death_list = []
        for key in self._entities.keys():
            for entity in self._entities[key]:
                match entity.cause_of_death():
                    case CauseOfDeath.OLD_AGE:
                        death_list.append(entity)
                        LOG.info(f"{entity} died from old age.")
                    case CauseOfDeath.OVERWEIGHT:
                        death_list.append(entity)
                        LOG.info(f"{entity} died from being overweight.")
                    case CauseOfDeath.MALNOURISHED:
                        death_list.append(entity)
                        LOG.info(f"{entity} died from being malnourished.")
                    case CauseOfDeath.NOT_DEAD:
                        pass
                    case _:
                        raise RuntimeError(
                            "_population_pruning_phase: Unreachable code."
                        )

        # Filter out dead entities from list
        for key in self._entities.keys():
            self._entities[key] = [
                entity for entity in self._entities[key] if entity not in death_list
            ]

        # Check for overpopulation
        for key in self._entities.keys():
            entity_list = self._entities[key]
            if len(entity_list) > self._max_capacity:
                random.shuffle(entity_list)
                overpopulation_diff = len(entity_list) - self._max_capacity
                LOG.info(
                    (
                        f"The following entities of type {key} will perish due to "
                        f"overpopulation: {entity_list[overpopulation_diff:]}"
                    )
                )
                self._entities[key] = entity_list[:overpopulation_diff]

    def _energy_expenditure_phase(self) -> None:
        """Perform energy expenditure phase of the simulation.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        for key in self._entities.keys():
            for entity in self._entities[key]:
                entity.expend_calories()

    def _milk_production_phase(self) -> None:
        """Perform milk production phase of the simulation.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        for key in self._entities.keys():
            for entity in self._entities[key]:
                milk_produced = entity.milk_production()
                self._milk_data[entity.__class__.name()][entity.id].iloc[
                    self._steps
                ] = milk_produced

    def _methane_production_phase(self) -> None:
        """Perform methane production phase of the simulation.

        Parameters
        ----------
        none

        Returns
        -------
        None
        """
        for key in self._entities.keys():
            for entity in self._entities[key]:
                methane_produced = entity.methane_production()
                self._methane_data[entity.__class__.name()][entity.id].iloc[
                    self._steps
                ] = methane_produced


class OrangeGrass(Feed):
    """Food for Purple Angus.

    Attributes
    ----------
    _initial_servings : int
        Initial servings in this OrangeGrass feed.

    _current_servings : int
        Current servings in this OrangeGrass feed.

    _total_entity_calories : float
        Total number of calories amongst the entities being fed.
    """

    CALORIES_PER_SERVING = 7000
    PRICE_PER_SERVING = 10.00

    def __init__(self, servings: int, cow_list: [Cow]):
        """ """
        self._initial_servings = servings
        self._current_servings = servings
        self._total_entity_calories = 0
        for cow in cow_list:
            self._total_entity_calories += cow.calories

    @staticmethod
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
        return "Orange Grass"

    @property
    def initial_serving_total(self) -> int:
        """Number of original servings when this Feed object was first
        instantiated.

        Parameters
        ----------
        none

        Returns
        -------
        int
            Number of original servings.
        """
        return self._initial_servings

    @property
    def current_serving_total(self) -> int:
        """Number of current servings in this Feed object.

        Parameters
        ----------

        Returns
        -------
        int
            Number of current servings.
        """
        return self._current_servings

    @property
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
        return self.__class__.CALORIES_PER_SERVING * self._initial_servings

    @property
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
        return self.__class__.CALORIES_PER_SERVING * self._current_servings

    @property
    def price(self) -> float:
        """Price of this OrangeGrass object.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Price of this OrangeGrass object.
        """
        return self.__class__.PRICE_PER_SERVING * self._initial_servings

    def feed(self, cow: Cow) -> int:
        """Feeds the provided Cow object.

        OrangeGrass is distributed proportionally to Cows based on caloric
        levels.

        Parameters
        ----------
        entity : Entity
            The entity to feed.

        Returns
        -------
        int
            The number of servings given to the Cow object.
        """
        if self._total_entity_calories == 0:
            return 0

        servings = (cow.calories / self._total_entity_calories) * self._initial_servings
        servings = math.ceil(servings)
        if servings > self._current_servings:
            servings = self._current_servings
            self._current_servings = 0
        else:
            self._current_servings -= servings

        cow.caloric_intake(servings * self.__class__.CALORIES_PER_SERVING)

        return servings
