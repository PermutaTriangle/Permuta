import abc
from typing import TYPE_CHECKING, Iterator, Tuple

if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from .perm import Perm


class Patt(abc.ABC):
    """A permutation pattern, e.g. classical, bivincular and mesh patterns."""

    def avoided_by(self, *patts: "Patt") -> bool:
        """Check if self is avoided by all the provided patterns."""
        return all(not patt.contains(self) for patt in patts)

    def contained_in(self, *patts: "Patt") -> bool:
        """Check if self is a pattern of all the provided patterns."""
        return all(patt.contains(self) for patt in patts)

    def count_occurrences_in(self, patt: "Patt") -> int:
        """Count the number of occurrences of self in the pattern."""
        return sum(1 for _ in self.occurrences_in(patt))

    @abc.abstractmethod
    def occurrences_in(
        self, patt: "Patt", *args, **kwargs
    ) -> Iterator[Tuple[int, ...]]:
        """Find all indices of occurrences of self in pattern."""

    @abc.abstractmethod
    def __len__(self) -> int:
        """The length of the pattern."""

    @abc.abstractmethod
    def get_perm(self) -> "Perm":
        """Get the permutation part of the pattern"""

    @abc.abstractmethod
    def _contains(self, patt: "Patt") -> bool:
        """Does pattern contains another?"""

    contains = _contains

    def __contains__(self, patt: "Patt") -> bool:
        return self._contains(patt)
