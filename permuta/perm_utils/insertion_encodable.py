from itertools import islice
from typing import ClassVar, Dict, Iterable, Tuple

from permuta.patterns.perm import Perm


class InsertionEncodablePerms:
    """A static container of functions fortesting
    if a basis has a regular insertion encoding.
    """

    _ALL_PROPERTIES: ClassVar[int] = 15
    _CACHE: ClassVar[Dict[Tuple, int]] = dict()

    @staticmethod
    def _is_incr_next_incr(perm: Perm) -> bool:
        n = len(perm)
        return not any(
            curr < prev and any(perm[j + 1] < perm[j] for j in range(i + 1, n - 1))
            for i, (prev, curr) in enumerate(zip(perm, islice(perm, 1, None)))
        )

    @staticmethod
    def _is_incr_next_decr(perm: Perm) -> bool:
        n = len(perm)
        return not any(
            curr < prev and any(perm[j + 1] > perm[j] for j in range(i + 1, n - 1))
            for i, (prev, curr) in enumerate(zip(perm, islice(perm, 1, None)))
        )

    @staticmethod
    def _is_decr_next_incr(perm: Perm) -> bool:
        n = len(perm)
        return not any(
            curr > prev and any(perm[j + 1] < perm[j] for j in range(i + 1, n - 1))
            for i, (prev, curr) in enumerate(zip(perm, islice(perm, 1, None)))
        )

    @staticmethod
    def _is_decr_next_decr(perm: Perm) -> bool:
        n = len(perm)
        return not any(
            curr > prev and any(perm[j + 1] > perm[j] for j in range(i + 1, n - 1))
            for i, (prev, curr) in enumerate(zip(perm, islice(perm, 1, None)))
        )

    @staticmethod
    def _insertion_encodable_properties(perm: Perm) -> int:
        properties = InsertionEncodablePerms._CACHE.get(perm, -1)
        if properties < 0:
            properties = sum(
                val << shift
                for shift, val in enumerate(
                    (
                        InsertionEncodablePerms._is_incr_next_decr(perm),
                        InsertionEncodablePerms._is_incr_next_incr(perm),
                        InsertionEncodablePerms._is_decr_next_decr(perm),
                        InsertionEncodablePerms._is_decr_next_incr(perm),
                    )
                )
            )
            InsertionEncodablePerms._CACHE[perm] = properties
        return properties

    @staticmethod
    def is_insertion_encodable_rightmost(basis: Iterable[Perm]) -> bool:
        """Check if basis is insertion encodable by rightmost."""
        curr = 0
        for perm in basis:
            curr = curr | InsertionEncodablePerms._insertion_encodable_properties(perm)
            if curr == InsertionEncodablePerms._ALL_PROPERTIES:
                return True
        return False

    @staticmethod
    def is_insertion_encodable_maximum(basis: Iterable[Perm]) -> bool:
        """Check if basis is insertion encodable by maximum."""
        curr = 0
        for perm in basis:
            curr = curr | InsertionEncodablePerms._insertion_encodable_properties(
                perm.rotate()
            )
            if curr == InsertionEncodablePerms._ALL_PROPERTIES:
                return True
        return False

    @staticmethod
    def is_insertion_encodable(basis: Iterable[Perm]) -> bool:
        """Check if basis is insertion encodable."""
        return InsertionEncodablePerms.is_insertion_encodable_rightmost(
            basis
        ) or InsertionEncodablePerms.is_insertion_encodable_maximum(basis)
