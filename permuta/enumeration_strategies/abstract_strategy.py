from abc import ABC, abstractmethod
from typing import FrozenSet, Iterable, Iterator

from permuta import Perm
from permuta.permutils.symmetry import all_symmetry_sets


class EnumerationStrategy(ABC):
    """Abstract class for a strategy to enumerate a permutation classes."""

    def __init__(self, basis: Iterable[Perm]) -> None:
        self._basis = frozenset(basis)

    @property
    def basis(self) -> FrozenSet[Perm]:
        """Getter for basis."""
        return self._basis

    @classmethod
    def reference(cls) -> str:
        """A reference for the strategy."""
        raise NotImplementedError

    @abstractmethod
    def applies(self) -> bool:
        """Return True if the strategy can be used for the basis."""


class EnumerationStrategyWithSymmetry(EnumerationStrategy):
    """Abstract class for a strategy to enumerate a permutation classes.
    Each symmetry of the inputed basis is tested against the strategy.
    """

    def applies(self) -> bool:
        """Check if the strategy applies to any symmetry."""
        syms: Iterator[FrozenSet[Perm]] = map(frozenset, all_symmetry_sets(self._basis))
        return next((True for b in syms if self._applies_to_symmetry(b)), False)

    @abstractmethod
    def _applies_to_symmetry(self, basis: FrozenSet[Perm]) -> bool:
        """Check if the strategy applies to this particular symmetry."""
