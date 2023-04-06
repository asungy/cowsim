from ..cow import Cow, CauseOfDeath
from cowsim.entity import Sex
import numpy as np
import random

# Age range (in days)
MIN_AGE = 0
MAX_AGE = 25 * 365

# Caloric bounds considered "normal" (in kcal)
MIN_CALORIC_BOUND = 5000
MAX_CALORIC_BOUND = 30000

# Weight range (in kilograms)
MIN_WEIGHT = 25 * 2.2
MAX_WEIGHT = 1200 * 2.2


class PurpleAngus(Cow):
    @staticmethod
    def name() -> str:
        """String name of PurpleAngus class.

        Returns
        -------
        str
            Name identifying class.
        """
        return "Purple Angus"

    @classmethod
    def generate(cls) -> "PurpleAngus":
        """Randomly generate an instance of a PurpleAngus.

        Returns
        -------
        PurpleAngus
            A randomly generated PurpleAngus.
        """
        age = random.randint(MIN_AGE, MAX_AGE)
        sex = Sex.FEMALE
        if random.randint(0, 1) == 0:
            sex = Sex.MALE
        calories = random.uniform(MIN_CALORIC_BOUND, MAX_CALORIC_BOUND)
        weight = random.uniform(MIN_WEIGHT, MAX_WEIGHT)

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

        Returns
        -------
        bool
            True, if conditions are such that life of Purple Angus is no longer feasible.
        """
        if self.age > MAX_AGE:
            return CauseOfDeath.OLD_AGE

        if self.weight > MAX_WEIGHT:
            return CauseOfDeath.OVERWEIGHT

        if self.weight < MIN_WEIGHT:
            return CauseOfDeath.MALNOURISHED

        return CauseOfDeath.NOT_DEAD

    def expend_calories(self) -> float:
        """Calculates and expends entity's calories.

        If the calculated caloric expenditure falls out of bounds as defined by
        MIN_CALORIC_BOUND and MAX_CALORIC_BOUND, then it should cause
        the angus to lose or gain weight, respectfully.

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
        expended_kcal = random.uniform(MIN_CALORIC_BOUND, MAX_CALORIC_BOUND)

        # Males expend more calories than females.
        if self.sex == Sex.MALE:
            expended_kcal += expended_kcal * 0.15

        # Caloric expenditure follows a normal distribution in regards to age, (but is capped at)
        mu = (MIN_CALORIC_BOUND + MAX_CALORIC_BOUND) / 2
        mu = mu * 0.2
        sigma = mu / 3
        normal = np.random.normal(mu, sigma, MAX_AGE)
        expended_kcal += max(normal[self.age], 0)
        expended_kcal = min(expended_kcal, MAX_CALORIC_BOUND)

        # Ensure that self.calories is not negative.
        self._calories = max(0, self.calories - expended_kcal)

        # Modify weight proportional to caloric difference from bounds.
        if self.calories < MIN_CALORIC_BOUND:
            self._weight -= (
                self.weight * (MIN_CALORIC_BOUND - self.calories) / MIN_CALORIC_BOUND
            )
        elif self.calories > MAX_CALORIC_BOUND:
            self._weight += (
                self.weight * (self.calories - MAX_CALORIC_BOUND) / MAX_CALORIC_BOUND
            )

        return expended_kcal
