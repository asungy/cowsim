from cowsim.environment.cowpen import CowPen, OrangeGrass
from cowsim.entity.cow.purple_angus import PurpleAngus
from cowsim.entity import Sex
import numpy as np


class CowPenTest:
    """Tests for the CowPen class."""

    def test_constructor(self):
        """Test CowPen constructor."""
        quantity = 4
        environment = CowPen([(PurpleAngus, quantity)])
        assert PurpleAngus.name in environment._entities
        assert len(environment._entities[PurpleAngus.name]) == quantity

    def test_feeding_phase(self):
        """Test the feeding phase."""
        quantity = 4
        environment = CowPen([(PurpleAngus, quantity)])

        # Asserting empty data in the first row.
        for id in environment._feeding_data[PurpleAngus.name]:
            assert environment._feeding_data[PurpleAngus.name][id][0] is np.nan

        environment._feeding_phase()

        # Assert row is propagated.
        for id in environment._feeding_data[PurpleAngus.name]:
            assert environment._feeding_data[PurpleAngus.name][id][0] is not None

    def test_step(self):
        """Test the step method"""
        cowpen = CowPen([(PurpleAngus, 50)])
        cowpen.step()

    def test_run(self):
        """Test the run method"""
        cowpen = CowPen([(PurpleAngus, 50)])
        cowpen.run()


class OrangeGrassTest:
    """Tests for the OrangeGrass class."""

    def test_constructor(self):
        """Tests the OrangeGrass constructor."""
        cow_list_size = 5
        calories_per_cow = 1000
        cow_list = []
        for _ in range(cow_list_size):
            angus = PurpleAngus(
                age=100,
                sex=Sex.MALE,
                calories=calories_per_cow,
                weight=1000,
            )
            cow_list.append(angus)

        servings = 20
        orange_grass = OrangeGrass(servings, cow_list)
        assert orange_grass.initial_serving_total == servings
        assert orange_grass.current_serving_total == servings
        assert orange_grass._total_entity_calories == cow_list_size * calories_per_cow

    def test_feed(self):
        """Tests the OrangeGrass `feed` method."""
        angus1 = PurpleAngus(
            age=100,
            sex=Sex.MALE,
            calories=6000,
            weight=1000,
        )
        angus2 = PurpleAngus(
            age=200,
            sex=Sex.MALE,
            calories=12000,
            weight=2000,
        )
        angus3 = PurpleAngus(
            age=300,
            sex=Sex.MALE,
            calories=15000,
            weight=3000,
        )
        angus4 = PurpleAngus(
            age=400,
            sex=Sex.MALE,
            calories=24000,
            weight=4000,
        )

        servings = 20
        cow_list = [angus1, angus2, angus3, angus4]
        orange_grass = OrangeGrass(servings, cow_list)

        angus1_old_calories = angus1.calories
        servings_for_angus1 = orange_grass.feed(angus1)
        assert servings_for_angus1 == 3
        assert orange_grass.current_serving_total == 17
        assert (
            angus1.calories - angus1_old_calories
            == 3 * OrangeGrass.CALORIES_PER_SERVING
        )

        assert orange_grass.feed(angus2) == 5
        assert orange_grass.feed(angus3) == 6
        assert orange_grass.feed(angus4) == 6
