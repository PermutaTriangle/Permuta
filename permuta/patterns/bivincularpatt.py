from random import randint
from typing import Iterable, Iterator, List, Optional, Tuple

from .meshpatt import MeshPatt
from .patt import Patt
from .perm import Perm


class BivincularPatt(MeshPatt):
    """A bivincular pattern class."""

    @staticmethod
    def _to_shading(
        n: int, adjacent_indices: Iterable[int], adjacent_values: Iterable[int]
    ) -> Iterator[Tuple[int, int]]:
        """Convert adjacent requirements into shading."""
        for idx in adjacent_indices:
            assert 0 <= idx <= n
            yield from ((idx, val) for val in range(n + 1))
        for val in adjacent_values:
            assert 0 <= val <= n
            yield from ((idx, val) for idx in range(n + 1))

    def __init__(
        self,
        perm: Perm,
        adjacent_indices: Iterable[int],
        adjacent_values: Iterable[int],
    ) -> None:
        super().__init__(
            perm,
            BivincularPatt._to_shading(len(perm), adjacent_indices, adjacent_values),
        )

    @classmethod
    def unrank(cls, pattern: Perm, number: int) -> MeshPatt:
        """Not implemented, inherited from MeshPatt."""
        raise NotImplementedError

    @classmethod
    def of_length(
        cls, length: int, patt: Optional[Perm] = None
    ) -> Iterator["MeshPatt"]:
        """Not implemented, inherited from MeshPatt."""
        raise NotImplementedError

    @classmethod
    def random(cls, length: int) -> "BivincularPatt":
        """Return a random Bivincular pattern of a given length."""
        return cls(
            Perm.random(length),
            (
                i
                for i, keep in enumerate(randint(0, 1) for _ in range(length + 1))
                if keep
            ),
            (
                i
                for i, keep in enumerate(randint(0, 1) for _ in range(length + 1))
                if keep
            ),
        )

    def get_adjacent_requirements(self) -> Tuple[List[int], List[int]]:
        """Convert shading into the bivincular requirements. Returned as a tuple of
        adjacent indices and adjacent values, both in order.

        Examples:
            >>> BivincularPatt(Perm((0, 3, 1, 2)), (0, 1, 2),
            ... (0, 2, 4)).get_adjacent_requirements()
            ([0, 1, 2], [0, 2, 4])
        """
        n, adj_idx, adj_val = len(self), set(), set()
        for x, y in self.shading:
            if all((x, i) in self.shading for i in range(n + 1)):
                adj_idx.add(x)
            if all((i, y) in self.shading for i in range(n + 1)):
                adj_val.add(y)
        return sorted(adj_idx), sorted(adj_val)

    def occurrences_in(self, patt: Patt, *args, **kwargs) -> Iterator[Tuple[int, ...]]:
        """Find all indices of self in patt. Each yielded element is a tuple of integer
        indices of the pattern such that

            Classical pattern:
                Occurrence of instance's perm in patt if no elements land
                in shaded region.

            Mesh pattern (including Bivincular):
                Occurrences of instances's perm in the pattern's perm is found, and if
                the sub mesh pattern formed by the occurrence indices is a superset of
                the instance shading, they are included.
        """
        if isinstance(patt, Perm):
            # TODO: Optimize me for Bivincular patterns
            pass
        return super().occurrences_in(patt, args, kwargs)

    def __repr__(self) -> str:
        adj_idx, adj_val = self.get_adjacent_requirements()
        return f"BivincularPatt({repr(self.pattern)}, {adj_idx}, {adj_val})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MeshPatt):
            return self.pattern == other.pattern and self.shading == other.shading
        return False

    def __hash__(self) -> int:
        return hash(super())


class VincularPatt(BivincularPatt):
    """A vincular pattern class."""

    def __init__(self, perm: Perm, adjacent_indices: Iterable[int]) -> None:
        super().__init__(perm, adjacent_indices, ())

    @classmethod
    def random(cls, length: int) -> "VincularPatt":
        """Return a random Vincular pattern of a given length."""
        return cls(
            Perm.random(length),
            (
                i
                for i, keep in enumerate(randint(0, 1) for _ in range(length + 1))
                if keep
            ),
        )

    def __repr__(self) -> str:
        adj_idx, _ = self.get_adjacent_requirements()
        return f"VincularPatt({repr(self.pattern)}, {adj_idx})"


class CovincularPatt(BivincularPatt):
    """A covincular pattern class."""

    def __init__(self, perm: Perm, adjacent_values: Iterable[int]) -> None:
        super().__init__(perm, (), adjacent_values)

    @classmethod
    def random(cls, length: int) -> "CovincularPatt":
        """Return a random Covincular pattern of a given length."""
        return cls(
            Perm.random(length),
            (
                i
                for i, keep in enumerate(randint(0, 1) for _ in range(length + 1))
                if keep
            ),
        )

    def __repr__(self) -> str:
        _, adj_val = self.get_adjacent_requirements()
        return f"CovincularPatt({repr(self.pattern)}, {adj_val})"
