import multiprocessing
from itertools import combinations, islice
from typing import ClassVar, Dict, Iterable, Iterator, List, NamedTuple, Optional, Union

from ..patterns import MeshPatt, Perm
from ..permutils import is_finite, is_insertion_encodable, is_polynomial
from ..permutils.pin_words import PinWords
from .basis import Basis, MeshBasis


class AvBase(NamedTuple):
    """A base class for Av to define instance variables without having to use
    __init__ in Av.
    """

    basis: Union[Basis, MeshBasis]
    cache: List[Dict[Perm, Optional[List[int]]]]


class Av(AvBase):
    """A permutation class defined by its minimal basis."""

    _FORBIDDEN_BASIS = Basis(Perm())
    _VALUE_ERROR_MSG = "Basis should be non-empty without the empty perm!"
    _BASIS_ONLY_MSG = "Only supported for Basis!"
    _CLASS_CACHE: ClassVar[Dict[Union[Basis, MeshBasis], "Av"]] = {}
    _CACHE_LOCK = multiprocessing.Lock()

    def __new__(
        cls,
        basis: Union[
            Basis,
            MeshBasis,
            Iterable[Perm],
            Iterable[Union[Perm, MeshPatt]],
        ],
    ) -> "Av":
        if not isinstance(basis, (Basis, MeshBasis)):
            return Av.from_iterable(basis)
        if len(basis) == 0 or basis == Av._FORBIDDEN_BASIS:
            raise ValueError(Av._VALUE_ERROR_MSG)
        instance = Av._CLASS_CACHE.get(basis)
        if instance is None:
            new_instance: "Av" = AvBase.__new__(cls, basis, [{Perm(): [0]}])
            Av._CLASS_CACHE[basis] = new_instance
            return new_instance
        return instance

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the instance cache."""
        cls._CLASS_CACHE = {}

    @classmethod
    def from_string(cls, basis) -> "Av":
        """Create a permutation class from a string. Basis can be either zero or one
        based and seperated by anything. MeshBasis is not supported.
        """
        return cls(Basis.from_string(basis))

    @classmethod
    def from_iterable(
        cls, basis: Union[Iterable[Perm], Iterable[Union[Perm, MeshPatt]]]
    ) -> "Av":
        """
        Create a permutation class from a basis defined by an iterable of patterns.
        """
        if MeshBasis.is_mesh_basis(basis):
            return cls(MeshBasis(*basis))
        return cls(Basis(*basis))

    def is_finite(self) -> bool:
        """Check if the perm class is finite."""
        if isinstance(self.basis, MeshBasis):
            raise NotImplementedError(Av._BASIS_ONLY_MSG)
        return is_finite(self.basis)

    def is_polynomial(self) -> bool:
        """Check if the perm class has polynomial growth."""
        if isinstance(self.basis, MeshBasis):
            raise NotImplementedError(Av._BASIS_ONLY_MSG)
        return is_polynomial(self.basis)

    def is_insertion_encodable(self) -> bool:
        """Check if the perm class is insertion encodable."""
        if isinstance(self.basis, MeshBasis):
            raise NotImplementedError(Av._BASIS_ONLY_MSG)
        return is_insertion_encodable(self.basis)

    def has_finitely_many_simples(self) -> bool:
        """Check if the perm class has finitely many simples."""
        if isinstance(self.basis, MeshBasis):
            raise NotImplementedError(Av._BASIS_ONLY_MSG)
        return (
            self.is_finite()
            or self.is_polynomial()
            or PinWords.has_finite_simples(self.basis)
        )

    def first(self, count: int) -> Iterable[Perm]:
        """Generate the first `count` permutation in this permutation class given
        that it has that many, if not all are generated.
        """
        yield from islice(self._all(), count)

    def of_length(self, length: int) -> Iterable[Perm]:
        """
        Generate all perms of a given length that belong to this permutation class.
        """
        return iter(self._get_level(length))

    def up_to_length(self, length: int) -> Iterable[Perm]:
        """Generate all perms up to and including a given length that
        belong to this permutation class.
        """
        for n in range(length + 1):
            yield from self.of_length(n)

    def count(self, length: int) -> int:
        """Return the nubmber of permutations of a given length."""
        return len(self._get_level(length))

    def enumeration(self, length: int) -> List[int]:
        """Return the enumeration of this permutation class up and including a given
        length."""
        return [self.count(i) for i in range(length + 1)]

    def __contains__(self, other: object):
        if isinstance(other, Perm):
            return other in self._get_level(len(other))
        return False

    def is_subclass(self, other: "Av"):
        """Check if a sublcass of another permutation class."""
        return all(p1 not in self for p1 in other.basis)

    def _ensure_level(self, level_number: int) -> None:
        start = max(0, len(self.cache) - 2)
        if isinstance(self.basis, Basis):
            self._ensure_level_classical_pattern_basis(level_number)
        else:
            self._ensure_level_mesh_pattern_basis(level_number)
        for i in range(start, level_number - 1):
            self.cache[i] = {perm: None for perm in self.cache[i]}

    def _ensure_level_classical_pattern_basis(self, level_number: int) -> None:
        # We build new elements from existing ones
        lengths = {len(b) for b in self.basis}
        max_size = max(lengths)
        for nplusone in range(len(self.cache), level_number + 1):
            n = nplusone - 1
            new_level: Dict[Perm, Optional[List[int]]] = {}
            last_level = self.cache[-1]
            check_length = nplusone in lengths
            smaller_elems = {b for b in self.basis if len(b) == nplusone}

            def valid_insertions(perm):
                # pylint: disable=cell-var-from-loop
                res = None
                for i in range(max(0, n - max_size), n):
                    val = perm[i]
                    subperm = perm.remove(i)
                    spots = self.cache[n - 1][subperm]
                    assert spots is not None
                    acceptable = [k for k in spots if k <= val]
                    acceptable.extend(k + 1 for k in spots if k >= val)
                    if res is None:
                        res = frozenset(acceptable)
                    res = res.intersection(acceptable)
                    if not res:
                        break
                return res if res is not None else range(nplusone)

            for perm, lis in last_level.items():
                for value in valid_insertions(perm):
                    new_perm = perm.insert(index=nplusone, new_element=value)
                    if not check_length or new_perm not in smaller_elems:
                        new_level[new_perm] = []
                        assert lis is not None
                        lis.append(value)
            self.cache.append(new_level)

    def _ensure_level_mesh_pattern_basis(self, level_number: int) -> None:
        self.cache.extend(
            {p: None for p in Perm.of_length(i) if p.avoids(*self.basis)}
            for i in range(len(self.cache), level_number + 1)
        )

    def _get_level(self, level_number: int) -> Dict[Perm, Optional[List[int]]]:
        with Av._CACHE_LOCK:
            self._ensure_level(level_number)
        return self.cache[level_number]

    def _all(self) -> Iterable[Perm]:
        length = 0
        while True:
            gen = (p for p in self.of_length(length))
            first: Optional[Perm] = next(gen, None)
            if first is None:
                break
            yield first
            yield from gen
            length += 1

    def right_juxtaposition(self, other: "Av") -> "Av":
        """Compute the basis of the juxtaposition of two permutation classes.

        Given self = Av(B1) and other = Av(B2), returns the permutation class
        E = Av(B) where E consists of all permutations that can be written as
        the juxtaposition of a permutation from self on the left and a
        permutation from other on the right.

        Raises NotImplementedError: If either basis is a MeshBasis.
        """
        if not isinstance(self.basis, Basis) or not isinstance(other.basis, Basis):
            raise NotImplementedError(Av._BASIS_ONLY_MSG)

        candidates: List[Perm] = []

        for b1 in self.basis:
            for b2 in other.basis:
                # |σ| = 0 case: no overlap
                candidates.extend(self._sigma_0_candidates(b1, b2))
                # |σ| = 1 case: one element overlap
                candidates.extend(self._sigma_1_candidates(b1, b2))

        # Basis constructor automatically minimizes
        return Av(Basis(*candidates))

    def above_juxtaposition(self, other: "Av") -> "Av":
        """Compute the basis of the above juxtaposition of two permutation classes.

        Given self = Av(B1) and other = Av(B2), returns the permutation class
        where self is on the bottom and other is on top.

        This is computed by taking inverses, computing right_juxtaposition,
        then inverting the result.

        Raises NotImplementedError: If either basis is a MeshBasis.
        """
        if not isinstance(self.basis, Basis) or not isinstance(other.basis, Basis):
            raise NotImplementedError(Av._BASIS_ONLY_MSG)

        # Compute inverse classes
        self_inverse = Av(Basis(*[p.inverse() for p in self.basis]))
        other_inverse = Av(Basis(*[p.inverse() for p in other.basis]))

        # Compute right juxtaposition of inverses
        result_inverse = self_inverse.right_juxtaposition(other_inverse)

        # Return inverse of result
        return Av(Basis(*[p.inverse() for p in result_inverse.basis]))

    @staticmethod
    def _sigma_0_candidates(b1: Perm, b2: Perm) -> Iterator[Perm]:
        """Generate candidates where left and right patterns don't overlap.

        Generates all permutations of length |b1| + |b2| where the first |b1|
        positions have pattern b1 and the last |b2| positions have pattern b2.
        """
        n1, n2 = len(b1), len(b2)
        total = n1 + n2

        # Choose which values go to the left block
        for left_values in combinations(range(total), n1):
            right_values = [v for v in range(total) if v not in left_values]

            # Build the permutation
            result = [0] * total
            # Left positions get values according to pattern b1
            for pos in range(n1):
                result[pos] = left_values[b1[pos]]
            # Right positions get values according to pattern b2
            for pos in range(n2):
                result[n1 + pos] = right_values[b2[pos]]

            yield Perm(result)

    @staticmethod
    def _sigma_1_candidates(
        b1: Perm, b2: Perm
    ) -> Iterator[Perm]:  # pylint: disable=R0914
        """Generate candidates where left and right patterns overlap by one element.

        Generates all permutations of length |b1| + |b2| - 1 where the first |b1|
        positions have pattern b1 and the last |b2| positions have pattern b2,
        with position |b1| - 1 shared between both patterns.
        """
        n1, n2 = len(b1), len(b2)
        total = n1 + n2 - 1

        # The shared position is at index n1 - 1
        # Its value v must satisfy: v = b1[-1] + b2[0]
        # (it must be at rank b1[-1] among left and rank b2[0] among right values)
        v = b1[-1] + b2[0]

        # Values less than v: {0, ..., v-1}
        # Values greater than v: {v+1, ..., total-1}
        values_below = list(range(v))
        values_above = list(range(v + 1, total))

        # Left block needs b1[-1] values below v, right block gets the rest
        k1 = b1[-1]  # number of values < v in left block

        # Iterate over all ways to partition values below v
        for left_below in combinations(values_below, k1):
            right_below = [x for x in values_below if x not in left_below]

            # Iterate over all ways to partition values above v
            for left_above in combinations(values_above, n1 - 1 - k1):
                right_above = [x for x in values_above if x not in left_above]

                # Build the left and right value sets
                left_values = sorted(list(left_below) + [v] + list(left_above))
                right_values = sorted(right_below + [v] + right_above)

                # Build the permutation
                result = [0] * total

                # Left positions (0 to n1-1) get values according to pattern b1
                for pos in range(n1):
                    result[pos] = left_values[b1[pos]]

                # Right positions (n1-1 to total-1) get values according to pattern b2
                # But position n1-1 is already set, so we only set n1 to total-1
                for pos in range(1, n2):
                    result[n1 - 1 + pos] = right_values[b2[pos]]

                yield Perm(result)

    def __str__(self) -> str:
        return f"Av({','.join(str(p) for p in self.basis)})"

    def __repr__(self) -> str:
        return f"Av({repr(self.basis)})"
