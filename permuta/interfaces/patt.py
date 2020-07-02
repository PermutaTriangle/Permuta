import abc
from typing import Iterator, List, Tuple, Union


class Patt(abc.ABC):
    def avoided_by(self, *perms):
        """Check if self is avoided by perms.

        Args:
            self:
                A classical/mesh pattern.
            perms: [permuta.Permutation]
                A list of permutations.

        Returns: bool
            True if and only if every permutation in perms avoids self.
        """
        return all(self not in perm for perm in perms)

    def contained_in(self, *perms):
        """Check if self is a pattern of perms.

        Args:
            self:
                A classical/mesh pattern.
            perms: [permuta.Permutation]
                A list of permutations.

        Returns: bool
            True if and only if self is a pattern of all permutations in perms.
        """
        return all(self in perm for perm in perms)

    def count_occurrences_in(self, perm) -> int:
        """Count the number of occurrences of self in perm.

        Args:
            self:
                A classical/mesh pattern.
            perm: permuta.Permutation
                A permutation.

        Returns: int
            The number of times self occurs in perm.
        """
        return sum(1 for _ in self.occurrences_in(perm))

    @abc.abstractmethod
    def occurrences_in(
        self, perm
    ) -> Union[Iterator[List[Tuple[int, ...]]], Iterator[Tuple[()]]]:
        """Find all indices of occurrences of self in perm."""
        pass

    @abc.abstractmethod
    def __len__(self):
        pass

    @property
    def pattern(self):
        return self
