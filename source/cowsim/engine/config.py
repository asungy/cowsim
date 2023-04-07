from cowsim.entity import Entity
from cowsim.environment import Environment
from enum import Enum


class EnvironmentType(Enum):
    """Represents available environment types."""

    COW_PEN = 1


class EntityType(Enum):
    """Represents available entity types."""

    PURPLE_ANGUS = 1


class Config:
    def __init__(self):
        """Constructor for Config class.

        Parameters
        ----------
        none
        """
        self._environment: Environment = None
        self._entities: [Entity] = []

    def set_environment(self, env_type: EnvironmentType) -> None:
        """Set the environment type."""
        pass

    def add_entity(entity_type: EntityType, quantity: int) -> None:
        """Add entity type."""
        pass

    def build(self) -> Environment:
        """Build environment to run simulation."""
        pass
