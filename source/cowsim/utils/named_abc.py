from abc import ABC

class Named_ABC(ABC):
    @classmethod
    @property
    def name(cls) -> str:
        """Name of entity.

        Parameters
        ----------
        none

        Returns
        -------
        str
            A name identifying this class.
        """
        return cls.__name__