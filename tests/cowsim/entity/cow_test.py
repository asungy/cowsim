from cowsim.entity.cow.purple_angus import PurpleAngus
from cowsim.entity import Sex
from cowsim.entity.cow import CauseOfDeath, Emotion
import random


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
            assert (
                p_angus.age >= PurpleAngus.MIN_AGE
                and p_angus.age <= PurpleAngus.MAX_AGE
            )
            assert (
                p_angus.calories >= PurpleAngus.MIN_CALORIC_BOUND
                and p_angus.calories <= PurpleAngus.MAX_CALORIC_BOUND
            )
            assert (
                p_angus.weight >= PurpleAngus.MIN_WEIGHT
                and p_angus.weight <= PurpleAngus.MAX_WEIGHT
            )

    def test_should_perish(self):
        """Test PurpleAngus.should_perish() method."""
        ok_angus = PurpleAngus(
            age=(PurpleAngus.MAX_AGE + PurpleAngus.MIN_AGE) / 2,
            sex=Sex.FEMALE,
            calories=(PurpleAngus.MAX_CALORIC_BOUND + PurpleAngus.MIN_CALORIC_BOUND)
            / 2,
            weight=(PurpleAngus.MAX_WEIGHT + PurpleAngus.MIN_WEIGHT) / 2,
        )
        assert ok_angus.cause_of_death() == CauseOfDeath.NOT_DEAD

        old_angus = PurpleAngus(
            age=PurpleAngus.MAX_AGE + 1,
            sex=Sex.FEMALE,
            calories=(PurpleAngus.MAX_CALORIC_BOUND + PurpleAngus.MIN_CALORIC_BOUND)
            / 2,
            weight=(PurpleAngus.MAX_WEIGHT + PurpleAngus.MIN_WEIGHT) / 2,
        )
        assert old_angus.cause_of_death() == CauseOfDeath.OLD_AGE

        overweight_angus = PurpleAngus(
            age=(PurpleAngus.MAX_AGE + PurpleAngus.MIN_AGE) / 2,
            sex=Sex.FEMALE,
            calories=(PurpleAngus.MAX_CALORIC_BOUND + PurpleAngus.MIN_CALORIC_BOUND)
            / 2,
            weight=PurpleAngus.MAX_WEIGHT + 1,
        )
        assert overweight_angus.cause_of_death() == CauseOfDeath.OVERWEIGHT

        underweight_angus = PurpleAngus(
            age=(PurpleAngus.MAX_AGE + PurpleAngus.MIN_AGE) / 2,
            sex=Sex.FEMALE,
            calories=(PurpleAngus.MAX_CALORIC_BOUND + PurpleAngus.MIN_CALORIC_BOUND)
            / 2,
            weight=PurpleAngus.MIN_WEIGHT - 1,
        )
        assert underweight_angus.cause_of_death() == CauseOfDeath.MALNOURISHED

    def test_expend_calories(self):
        """Test PurpleAngus.expend_calories() method."""
        for _ in range(1000):
            angus = PurpleAngus.generate()
            old_weight = angus.weight
            _ = angus.expend_calories()

            if angus.calories < PurpleAngus.MIN_CALORIC_BOUND:
                assert angus.weight < old_weight
            else:
                assert angus.weight == old_weight

    def test_caloric_intake(self):
        """Test PurpleAngus.caloric_intake() method."""
        # Testing case where angus ingests calories but does not gain weight.
        no_gaingus = PurpleAngus(
            age=(PurpleAngus.MAX_AGE + PurpleAngus.MIN_AGE) / 2,
            sex=Sex.MALE,
            calories=PurpleAngus.MIN_CALORIC_BOUND,
            weight=(PurpleAngus.MAX_WEIGHT + PurpleAngus.MIN_WEIGHT) / 2,
        )
        kcal = (PurpleAngus.MAX_CALORIC_BOUND - PurpleAngus.MIN_CALORIC_BOUND) / 2
        old_weight = no_gaingus.weight
        old_calories = no_gaingus.calories
        no_gaingus.caloric_intake(kcal)
        assert no_gaingus.weight == old_weight
        assert no_gaingus.calories > old_calories

        # Testing case where angus ingests calories and gains weight.
        gaingus = PurpleAngus(
            age=(PurpleAngus.MAX_AGE + PurpleAngus.MIN_AGE) / 2,
            sex=Sex.MALE,
            calories=PurpleAngus.MAX_CALORIC_BOUND,
            weight=(PurpleAngus.MAX_WEIGHT + PurpleAngus.MIN_WEIGHT) / 2,
        )
        old_weight = gaingus.weight
        old_calories = gaingus.calories
        gaingus.caloric_intake(random.randint(1, 100))
        assert gaingus.weight > old_weight
        assert gaingus.calories == PurpleAngus.MAX_CALORIC_BOUND

    def test_emotion(self):
        angus = PurpleAngus.generate()
        assert isinstance(angus.emotion, Emotion)
