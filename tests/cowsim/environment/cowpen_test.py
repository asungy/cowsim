from cowsim.environment.cowpen import Cowpen
from cowsim.entity.cow.purple_angus import PurpleAngus


class CowpenTest:
    def test_constructor(self):
        """Test Cowpen constructor."""
        quantity = 4
        environment = Cowpen([(PurpleAngus, quantity)])
        assert PurpleAngus.name() in environment._entities
        assert len(environment._entities[PurpleAngus.name()]) == quantity

    def test_feeding_phase(self):
        """Test the feeding phase."""
        
