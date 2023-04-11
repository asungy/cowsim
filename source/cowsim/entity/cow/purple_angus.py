from ..cow import Cow, CauseOfDeath, Emotion
from cowsim.entity import Sex
from enum import Enum
import numpy as np
import random


class PurpleAngus(Cow):
    # Age range (in days)
    MIN_AGE = 1
    MAX_AGE = 25 * 365

    # Adult age (in days)
    ADULT_AGE = 5 * 365

    # Caloric bounds considered "normal" (in kcal)
    MIN_CALORIC_BOUND = 5000
    MAX_CALORIC_BOUND = 30000

    # Weight range (in kilograms)
    MIN_WEIGHT = 65 * 2.2
    MAX_WEIGHT = 3000 * 2.2

    # Minimum healthy weight for adult (in kilograms)
    MIN_ADULT_WEIGHT = 800 * 2.2

    # Average milk production (in liters)
    AVERAGE_MILK_PRODUCTION = 60

    # Max bound on methane production (in kilograms)
    MAX_METHANE_PRODUCTION_BOUND = 300 * 2.2

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
        return "PurpleAngus"

    @classmethod
    def should_reproduce(cls, cow_a: Cow, cow_b: Cow) -> bool:
        """Determines if two cows should reproduce.

        The probability of two cows reproducing (given that certain conditions
        are met) is based on both of the cows' emotional states.

        Parameters
        ----------
        cow_a : Cow
            An arbitrary Cow instance

        cow_b : Cow
            An arbitrary Cow instance

        Returns
        -------
        bool
            True, if entities should reproduce.

        Notes
        -----
        - `cow_a` and `cow_b` cannot be identical.
        - Both cows must be over the adult age.
        - Cows must be over the opposite sex to reproduce.
        """
        if type(cow_a) != type(cow_b):
            return False

        if cow_a.age < cls.ADULT_AGE or cow_b.age < cls.ADULT_AGE:
            return False

        if cow_a.id == cow_b.id:
            return False

        if cow_a.sex == cow_b.sex:
            return False

        prob_a = None
        if Emotion.is_positive(cow_a.emotion):
            prob_a = 1.0
        elif Emotion.is_neutral(cow_a.emotion):
            prob_a = 0.66
        else:
            prob_a = 0.33

        prob_b = None
        if Emotion.is_positive(cow_b.emotion):
            prob_b = 1.0
        elif Emotion.is_neutral(cow_b.emotion):
            prob_b = 0.66
        else:
            prob_b = 0.33

        prob = prob_a * prob_b

        return random.uniform(0, 1) <= prob

    @classmethod
    def newborn(cls) -> "PurpleAngus":
        """Generates a newborn purple angus (when two purple angus reproduce).

        Parameters
        ----------
        none

        Returns
        -------
        PurpleAngus
            A newborn purple angus.
        """
        age = 0
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

    def cause_of_death(self) -> Enum:
        """Returns an enumerated class indicating the cause of death of a
        purple angus (if applicable).

        Parameters
        ----------
        none

        Returns
        -------
        Enum
            Instance of enumerated class.
        """
        if self.age > PurpleAngus.MAX_AGE:
            return CauseOfDeath.OLD_AGE

        if self.weight > PurpleAngus.MAX_WEIGHT:
            return CauseOfDeath.OVERWEIGHT

        if (
            self.weight < PurpleAngus.MIN_ADULT_WEIGHT
            and self.age >= PurpleAngus.ADULT_AGE
        ):
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
        expended_kcal += max(normal[self.age - 1], 0)

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

    def milk_production(self) -> float:
        """Calculates milk produced from cow.

        Milk production is calculated based on sex, age, and weight.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Milk produced (in liters).

        Notes
        -----
        - Milk production follows a normal distribution in regards to age.
        - Milk production is proportionally related to weight.
        """
        # Males do not produce milk.
        if self.sex is Sex.MALE:
            return 0

        # Younger angus do not produce milk.
        if self.age < PurpleAngus.ADULT_AGE:
            return 0

        # Milk production follows a normal distribution in regards to age.
        mu = PurpleAngus.AVERAGE_MILK_PRODUCTION
        sigma = mu / 3
        normal = np.random.normal(mu, sigma, PurpleAngus.MAX_AGE)
        milk_production = max(normal[self.age - 1], 0)

        # Milk production is proportionally related to weight.
        milk_production *= 1 + (self.weight / PurpleAngus.MAX_WEIGHT)

        return max(milk_production, 0)

    def methane_production(self) -> float:
        """Calculate methane production from cow.

        Methane production is calculated based on calories.

        Parameters
        ----------
        none

        Returns
        -------
        float
            Methane produced (in kilograms).

        Notes
        -----
        - Methane production is proportional to calories.
        """
        return PurpleAngus.MAX_METHANE_PRODUCTION_BOUND * (
            self.calories / PurpleAngus.MAX_CALORIC_BOUND
        )

    @property
    def emotion(self) -> Emotion:
        """The current emotional state of the cow. This is randomly generated
        at each call.

        Returns
        -------
        Emotion
            The emotion of the cow.
        """
        i = random.randint(0, len(list(Emotion)) - 1)
        return list(Emotion)[i]
