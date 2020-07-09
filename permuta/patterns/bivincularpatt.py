from typing import Iterable


"""from .meshpatt import MeshPatt
from .perm import Perm


class BivincularPatt(MeshPatt):
    @staticmethod
    def _to_shading(
        n: int, adjacent_indices: Iterable[int], adjacent_values: Iterable[int]
    ):
        for idx in adjacent_indices:
            yield from ((idx, val) for val in range(n + 1))
        for val in adjacent_values:
            yield from ((idx, val) for idx in range(n + 1))

    def __init__(
        self,
        perm: Perm,
        adjacent_indices: Iterable[int],
        adjacent_values: Iterable[int],
    ):
        super().__init__(
            perm,
            BivincularPatt._to_shading(len(perm), adjacent_indices, adjacent_values),
        )
"""


class VincularPatt(BivincularPatt):
    def __init__(self, perm: Perm, adjacent_indices: Iterable[int]) -> None:
        super().__init__(perm, adjacent_indices, ())


class CovincularPatt(BivincularPatt):
    def __init__(self, perm: Perm, adjacent_values: Iterable[int]) -> None:
        super().__init__(perm, (), adjacent_values)
