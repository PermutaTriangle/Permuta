from itertools import tee
from typing import Iterable

from permuta.patterns.perm import Perm


def is_finite(basis: Iterable[Perm]) -> bool:
    """Check if a basis is finite, i.e. it contains decreasing and increasing
    permutations.
    """
    it1, it2 = tee(basis, 2)
    return any(perm.is_decreasing() for perm in it1) and any(
        perm.is_increasing() for perm in it2
    )
