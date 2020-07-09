from collections import deque
from typing import Iterable

from ..patterns import Perm


def dihedral_group(n: int) -> Iterable[Perm]:
    """Generate dihedral group of length n.

    Examples:
        >>> sorted(dihedral_group(4))
        [Perm((0, 1, 2, 3)), Perm((0, 3, 2, 1)), Perm((1, 0, 3, 2)), Perm((1, 2, 3, 0))\
, Perm((2, 1, 0, 3)), Perm((2, 3, 0, 1)), Perm((3, 0, 1, 2)), Perm((3, 2, 1, 0))]
    """
    if n <= 2:
        return
    increasing, decreasing = deque(range(n)), deque(range(n - 1, -1, -1))
    yield Perm(increasing)
    yield Perm(decreasing)
    for _ in range(n - 1):
        increasing.appendleft(increasing.pop())
        decreasing.appendleft(decreasing.pop())
        yield Perm(increasing)
        yield Perm(decreasing)
