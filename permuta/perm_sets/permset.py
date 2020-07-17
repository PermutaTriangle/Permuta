import multiprocessing
from itertools import islice
from typing import ClassVar, Dict, Iterable, List, NamedTuple, Optional, Union

from ..patterns import MeshPatt, Perm
from ..permutils import is_finite, is_insertion_encodable, is_polynomial
from .basis import Basis, MeshBasis


class AvBase(NamedTuple):
    """A base class for Av to define instance variables without having to use
    __init__ in Av.
    """

    basis: Union[Basis, MeshBasis]
    cache: List[Dict[Perm, List[int]]]


class Av(AvBase):
    """A permutation class defined by its minimal basis."""

    _CLASS_CACHE: ClassVar[Dict[Union[Basis, MeshBasis], "Av"]] = {}
    _CACHE_LOCK = multiprocessing.Lock()

    def __new__(cls, basis: Union[Basis, MeshBasis]) -> "Av":
        assert len(basis) > 0 and basis != Basis(Perm())
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
    def from_iterable(
        cls, basis: Union[Iterable[Perm], Iterable[Union[Perm, MeshPatt]]]
    ):
        """Create a permutation class from a basis defined by an iterable of patterns.
        """
        if MeshBasis.is_mesh_basis(basis):
            return cls(MeshBasis(*basis))
        return cls(Basis(*basis))

    def is_finite(self) -> bool:
        """Check if the perm class is finite."""
        return is_finite(self.basis)

    def is_polynomial(self) -> bool:
        """Check if the perm class has polynomial growth."""
        return is_polynomial(self.basis)

    def is_insertion_encodable(self) -> bool:
        """Check if the perm class is insertion encodable."""
        return is_insertion_encodable(self.basis)

    def first(self, count: int) -> Iterable[Perm]:
        """Generate the first `count` permutation in this permutation class given
        that it has that many, if not all are generated.
        """
        yield from islice(self._all(), count)

    def of_length(self, length: int) -> Iterable[Perm]:
        """Generate all perms of a given length that belong to this permutation class.
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
        return sum(1 for _ in self.of_length(length))

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
        if isinstance(self.basis, Basis):
            self._ensure_level_classical_pattern_basis(level_number)
        else:
            self._ensure_level_mesh_pattern_basis(level_number)

    def _ensure_level_classical_pattern_basis(self, level_number: int) -> None:
        # We build new elements from existing ones
        lengths = {len(b) for b in self.basis}
        max_size = max(lengths)
        for nplusone in range(len(self.cache), level_number + 1):
            n = nplusone - 1
            new_level: Dict[Perm, List[int]] = dict()
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
                    acceptable = [k for k in spots if k <= val]
                    acceptable.extend(k + 1 for k in spots if k >= val)
                    if res is None:
                        res = frozenset(acceptable)
                    res = res.intersection(acceptable)
                    if not res:
                        break
                return res if res is not None else range(nplusone)

            for perm in last_level:
                for value in valid_insertions(perm):
                    new_perm = perm.insert(index=nplusone, new_element=value)
                    if not check_length or new_perm not in smaller_elems:
                        new_level[new_perm] = []
                        last_level[perm].append(value)
            self.cache.append(new_level)

    def _ensure_level_mesh_pattern_basis(self, level_number: int) -> None:
        self.cache.extend(
            {p: [] for p in Perm.of_length(i) if p.avoids(*self.basis)}
            for i in range(len(self.cache), level_number + 1)
        )

    def _get_level(self, level_number: int) -> Iterable[Perm]:
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

    def __str__(self) -> str:
        return f"Av({','.join(str(p) for p in self.basis)})"

    def __repr__(self) -> str:
        return f"Av({repr(self.basis)})"
