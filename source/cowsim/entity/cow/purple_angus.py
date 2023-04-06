from ..cow import Cow, CauseOfDeath
from cowsim.entity import Sex
import numpy as np
import random


class PurpleAngus(Cow):
    # Age range (in days)
    MIN_AGE = 0
    MAX_AGE = 25 * 365

    # Caloric bounds considered "normal" (in kcal)
    MIN_CALORIC_BOUND = 5000
    MAX_CALORIC_BOUND = 30000

    # Weight range (in kilograms)
    MIN_WEIGHT = 25 * 2.2
    MAX_WEIGHT = 1200 * 2.2

    @staticmethod
    def name() -> str:
        """String name of PurpleAngus class.

        Parameters
        ----------
        none

        Returns
        -------
        str
            Name identifying class.
        """
        return "Purple Angus"

    @classmethod
    def generate(cls) -> "PurpleAngus":
        """Randomly generate an instance of a PurpleAngus.

        Parameters
        ----------
        none

        Returns
        -------
        PurpleAngus
            A randomly generated PurpleAngus.
        """
        age = random.randint(cls.MIN_AGE, cls.MAX_AGE)
        sex = Sex.FEMALE
        if random.randint(0, 1) == 0:
            sex = Sex.MALE
        calories = random.uniform(cls.MIN_CALORIC_BOUND, cls.MAX_CALORIC_BOUND)
        weight = random.uniform(cls.MIN_WEIGHT, cls.MAX_WEIGHT)

        return cls(
            age=age,
            sex=sex,
            calories=calories,
            weight=weight,
        )

    def __init__(self, age: int, sex: Sex, calories: float, weight: float):
        super().__init__(
            age=age,
            sex=sex,
            calories=calories,
            weight=weight,
        )

    def cause_of_death(self) -> bool:
        """Determines if this PurpleAngus should perish (hopefully not!).

        Parameters
        ----------
        none

        Returns
        -------
        bool
            True, if conditions are such that life of Purple Angus is no longer feasible.
        """
        if self.age > PurpleAngus.MAX_AGE:
            return CauseOfDeath.OLD_AGE

        if self.weight > PurpleAngus.MAX_WEIGHT:
            return CauseOfDeath.OVERWEIGHT

        if self.weight < PurpleAngus.MIN_WEIGHT:
            return CauseOfDeath.MALNOURISHED

        return CauseOfDeath.NOT_DEAD

    def expend_calories(self) -> float:
        """Calculates and expends entity's calories.

        If the calculated caloric expenditure falls below MIN_CALORIC_BOUND,
        then it will cause the angus to lose weight.

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

        The following factors affect caloric expenditure:
            - Males (on average) expend more calories than females.
            - Caloric expenditure follows a normal distribution in regards to age.
        """
        expended_kcal = random.uniform(
            PurpleAngus.MIN_CALORIC_BOUND, PurpleAngus.MAX_CALORIC_BOUND
        )

        # Males expend more calories than females.
        if self.sex == Sex.MALE:
            expended_kcal += expended_kcal * 0.15

        # Caloric expenditure follows a normal distribution in regards to age.
        mu = (PurpleAngus.MIN_CALORIC_BOUND + PurpleAngus.MAX_CALORIC_BOUND) / 2
        mu = mu * 0.2
        sigma = mu / 3
        normal = np.random.normal(mu, sigma, PurpleAngus.MAX_AGE)
        expended_kcal += max(normal[self.age], 0)

        # Ensure that self.calories is not negative.
        self._calories = max(0, self.calories - expended_kcal)

        # Weight loss is proportional to caloric difference from bounds.
        if self.calories < PurpleAngus.MIN_CALORIC_BOUND:
            self._weight -= (
                self.weight
                * (PurpleAngus.MIN_CALORIC_BOUND - self.calories)
                / PurpleAngus.MIN_CALORIC_BOUND
            )

        return expended_kcal

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
            Caloric increase of purple angus
        """
        old_calories = self.calories
        self._calories += kcal

        # Weight gain is proportional to caloric difference from bounds.
        if self.calories > PurpleAngus.MAX_CALORIC_BOUND:
            self._weight += (
                self.weight
                * (self.calories - PurpleAngus.MAX_CALORIC_BOUND)
                / PurpleAngus.MAX_CALORIC_BOUND
            )
            # Excess calories are stored as fat, so current calories fall to
            # MAX_CALORIC_BOUND.
            self._calories = PurpleAngus.MAX_CALORIC_BOUND

        return self.calories - old_calories
