from abc import ABC, abstractmethod

from permuta.permutils.symmetry import all_symmetry_sets


class EnumerationStrategy(ABC):
    """Abstract class for a strategy to enumerate a permutation classes"""

    def __init__(self, basis):
        ABC.__init__(self)
        self._basis = frozenset(basis)

    @property
    def basis(self):
        return self._basis

    @classmethod
    def reference(cls):
        """A reference for the strategy."""
        raise NotImplementedError

    @abstractmethod
    def applies(self):
        """
        Return True if the strategy can be used for the basis
        """
        pass


class EnumerationStrategyWithSymmetry(EnumerationStrategy):
    """
    Abstract class for a strategy to enumerate a permutation classes.

    Each symmetry of the inputed basis is tested against the strategy.
    """

    def __init__(self, basis):
        super().__init__(basis)
        self._apply_basis = None

    @property
    def basis(self):
        """
        The symmetry of the inputed basis to which the strategy applies to.
        """
        if self._basis is None:
            self.applies()
        return self._basis

    def applies(self):
        """
        Check if the strategy applies to any symmetry.
        """
        for b in map(frozenset, all_symmetry_sets(self._basis)):
            if self._applies_to_symmetry(b):
                self._apply_basis = b
                return True
        return False

    @abstractmethod
    def _applies_to_symmetry(self, b):
        """
        Check if the strategy applies to this particular symmetry.
        """
        pass
