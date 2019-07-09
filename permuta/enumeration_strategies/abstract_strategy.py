from abc import ABC, abstractmethod

class EnumerationStrategy(ABC):

    """Abstract class for a strategy to enumerate a permutation classes"""

    def __init__(self, basis):
        ABC.__init__(self)
        self._basis = basis

    @property
    def basis(self):
        return self._basis

    @property
    @staticmethod
    def reference():
        """A reference for the strategy."""
        raise NotImplementedError

    @abstractmethod
    def applies(self):
        """
        Return True if the strategy can be used for the basis
        """
        pass
