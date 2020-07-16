import multiprocessing
from itertools import islice
from typing import ClassVar, Dict, Iterable, List, Union

from ..patterns import MeshPatt, Perm
from .basis import Basis, MeshBasis


class Av:
    """A permutation class defined by its minimal basis."""

    _CLASS_CACHE: ClassVar[Dict[Union[Basis, MeshBasis], "Av"]] = {}
    _CACHE_LOCK = multiprocessing.Lock()

    def __new__(cls, basis: Union[Basis, MeshBasis]) -> "Av":
        assert len(basis) > 0
        instance = Av._CLASS_CACHE.get(basis)
        if instance is None:
            new_instance: "Av" = object.__new__(cls)
            return new_instance
        return instance

    def __init__(self, basis: Union[Basis, MeshBasis]) -> None:
        self.basis: Union[Basis, MeshBasis] = basis
        self._cache: List[Dict[Perm, List[int]]] = [{Perm(): [0]}]
        Av._CLASS_CACHE[basis] = self

    @classmethod
    def clear_cache(cls) -> None:
        cls._CLASS_CACHE = {}

    @classmethod
    def from_iterable(
        cls, basis: Union[Iterable[Perm], Iterable[Union[Perm, MeshPatt]]]
    ):
        if MeshBasis.is_mesh_basis(basis):
            return cls(MeshBasis(*basis))
        return cls(Basis(*basis))

    def first(self, count: int) -> Iterable[Perm]:
        yield from islice(self._all(), count)

    def of_length(self, length: int) -> Iterable[Perm]:
        return iter(self._get_level(length))

    def up_to_length(self, length: int) -> Iterable[Perm]:
        for n in range(length + 1):
            yield from self.of_length(n)

    def count(self, length: int) -> int:
        return sum(1 for _ in self.of_length(length))

    def enumeration(self, length: int) -> List[int]:
        return [self.count(i) for i in range(length + 1)]

    def __contains__(self, other: object):
        if isinstance(other, Perm):
            return other in self._get_level(len(other))
        return False

    def is_subclass(self, other: "Av"):
        """ Check if the `self` is a subclass of `other`. """
        return all(p1 not in self for p1 in other.basis)

    def _ensure_level(self, level_number: int) -> None:
        if isinstance(self.basis, Basis):
            self._ensure_level_classical_pattern_basis(level_number)
        else:
            self._ensure_level_mesh_pattern_basis(level_number)

    def _ensure_level_classical_pattern_basis(self, level_number: int) -> None:
        # Ensure level is available
        while len(self._cache) <= level_number:
            nplusone = len(self._cache)  # really: len(perm) + 1
            # Smart way when basis consists only of Perms
            # We will build the length n + 1 perms, from the length n perms

            n = nplusone - 1
            new_level: Dict[Perm, List[int]] = dict()
            max_size = max(len(p) for p in self.basis)
            last_level = self._cache[-1]

            # If we are currently building a length for which there is a
            #   basis element of that length, we set this to True
            check_length = nplusone in [len(b) for b in self.basis]
            # and get the basis element of this nplusone
            smaller_elems = [b for b in self.basis if len(b) == nplusone]

            def valid_insertions(perm):
                res = None
                for i in range(max(0, n - max_size), n):
                    val = perm[i]
                    subperm = perm.remove(i)
                    spots = self._cache[n - 1][subperm]
                    acceptable = [k for k in spots if k <= val] + [
                        k + 1 for k in spots if k >= val
                    ]
                    if res is None:
                        res = frozenset(acceptable)
                    res = res.intersection(acceptable)
                    if not res:
                        break
                return res if res is not None else frozenset(range(nplusone))

            for perm in last_level:
                for value in valid_insertions(perm):
                    new_perm = perm.insert(index=nplusone, new_element=value)
                    if not check_length or new_perm not in smaller_elems:
                        new_level[new_perm] = []
                        last_level[perm].append(value)
            self._cache.append(new_level)

    def _ensure_level_mesh_pattern_basis(self, level_number: int) -> None:
        while len(self._cache) <= level_number:
            nplusone = len(self._cache)
            new_level: Dict[Perm, List[int]] = dict()
            for new_perm in Perm.of_length(nplusone):
                if new_perm.avoids(*self.basis):
                    new_level[new_perm] = []
            self._cache.append(new_level)

    def _get_level(self, level_number: int) -> Iterable[Perm]:
        with Av._CACHE_LOCK:
            self._ensure_level(level_number)
        res = self._cache[level_number]
        if isinstance(res, dict):
            return self._cache[level_number]
        return res

    def _all(self) -> Iterable[Perm]:
        length = 0
        while True:
            yield from self.of_length(length)
            length += 1
