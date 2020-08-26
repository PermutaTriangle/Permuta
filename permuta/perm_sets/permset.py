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
            new_level: Dict[Perm, Optional[List[int]]] = dict()
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

    def __str__(self) -> str:
        return f"Av({','.join(str(p) for p in self.basis)})"

    def __repr__(self) -> str:
        return f"Av({repr(self.basis)})"
