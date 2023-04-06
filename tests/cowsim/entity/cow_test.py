from cowsim.entity.cow.purple_angus import (
    MAX_AGE,
    MAX_CALORIC_BOUND,
    MAX_WEIGHT,
    MIN_AGE,
    MIN_CALORIC_BOUND,
    MIN_WEIGHT,
    PurpleAngus,
)
from cowsim.entity import Sex
from cowsim.entity.cow import CauseOfDeath


class PurpleAngusTest:
    def test_properties(self):
        """Test getters of properties."""
        age = 100
        sex = Sex.FEMALE
        calories = 20500
        weight = 550

        p_angus = PurpleAngus(
            age=age,
            sex=sex,
            calories=calories,
            weight=weight,
        )

        assert p_angus.id is not None
        assert p_angus.age == age
        assert p_angus.sex == sex
        assert p_angus.calories == calories
        assert p_angus.weight == weight

    def test_static_name(self):
        """Test PurpleAngus.name() static method."""
        assert PurpleAngus.name() == "Purple Angus"

    def test_generate(self):
        """Test PurpleAngus.generate() class method."""
        for _ in range(1000):
            p_angus = PurpleAngus.generate()
            assert p_angus.age >= MIN_AGE and p_angus.age <= MAX_AGE
            assert (
                p_angus.calories >= MIN_CALORIC_BOUND
                and p_angus.calories <= MAX_CALORIC_BOUND
            )
            assert p_angus.weight >= MIN_WEIGHT and p_angus.weight <= MAX_WEIGHT

    def test_should_perish(self):
        """Test PurpleAngus.should_perish() method."""
        ok_angus = PurpleAngus(
            age=(MAX_AGE + MIN_AGE) / 2,
            sex=Sex.FEMALE,
            calories=(MAX_CALORIC_BOUND + MIN_CALORIC_BOUND) / 2,
            weight=(MAX_WEIGHT + MIN_WEIGHT) / 2,
        )
        assert ok_angus.cause_of_death() == CauseOfDeath.NOT_DEAD

        old_angus = PurpleAngus(
            age=MAX_AGE + 1,
            sex=Sex.FEMALE,
            calories=(MAX_CALORIC_BOUND + MIN_CALORIC_BOUND) / 2,
            weight=(MAX_WEIGHT + MIN_WEIGHT) / 2,
        )
        assert old_angus.cause_of_death() == CauseOfDeath.OLD_AGE

        overweight_angus = PurpleAngus(
            age=(MAX_AGE + MIN_AGE) / 2,
            sex=Sex.FEMALE,
            calories=(MAX_CALORIC_BOUND + MIN_CALORIC_BOUND) / 2,
            weight=MAX_WEIGHT + 1,
        )
        assert overweight_angus.cause_of_death() == CauseOfDeath.OVERWEIGHT

        underweight_angus = PurpleAngus(
            age=(MAX_AGE + MIN_AGE) / 2,
            sex=Sex.FEMALE,
            calories=(MAX_CALORIC_BOUND + MIN_CALORIC_BOUND) / 2,
            weight=MIN_WEIGHT - 1,
        )
        assert underweight_angus.cause_of_death() == CauseOfDeath.MALNOURISHED

    def test_expend_calories(self):
        """Test PurpleAngus.expend_calories() method."""
        for _ in range(1000):
            angus = PurpleAngus.generate()
            old_weight = angus.weight
            _ = angus.expend_calories()

            if angus.calories > MAX_CALORIC_BOUND:
                assert angus.weight > old_weight
            elif angus.calories < MIN_CALORIC_BOUND:
                assert angus.weight < old_weight
            else:
                assert angus.weight == old_weight
