from typing import Iterable, Iterator, Tuple

from permuta.patterns.perm import Perm

__all__ = ("CyclicPerm",)


class CyclicPerm:
    """A cyclic permutation: the equivalence class of all rotations of a
    linear permutation, stored via its unique ``1 ⊕ σ`` representative
    (the rotation that places the smallest element first).
    """

    __slots__ = ("_rep",)

    def __new__(cls, iterable: Iterable[int] = ()) -> "CyclicPerm":
        """Build a ``CyclicPerm`` from any rotation of the underlying class.

        Examples:
            >>> CyclicPerm((3, 1, 2, 4, 0))
            CyclicPerm((0, 3, 1, 2, 4))
            >>> CyclicPerm((0, 3, 1, 2, 4)) == CyclicPerm((4, 0, 3, 1, 2))
            True
            >>> CyclicPerm(())
            CyclicPerm(())
        """
        obj = object.__new__(cls)
        p = iterable if isinstance(iterable, Perm) else Perm(iterable)
        obj._rep = CyclicPerm._canonical(p)
        return obj

    @staticmethod
    def _canonical(p: Perm) -> Perm:
        if len(p) == 0:
            return p
        return p.shift_left(p.index(0))

    @classmethod
    def _from_canonical(cls, p: Perm) -> "CyclicPerm":
        """Fast path when ``p`` already starts with ``0``."""
        obj = object.__new__(cls)
        obj._rep = p
        return obj

    @classmethod
    def from_perm(cls, p: Perm) -> "CyclicPerm":
        """Build the cyclic class of a ``Perm``."""
        return cls(p)

    @classmethod
    def to_standard(cls, iterable: Iterable) -> "CyclicPerm":
        """Build a cyclic permutation by standardizing any iterable of distinct
        comparable elements (1-indexed inputs work fine).

        Examples:
            >>> CyclicPerm.to_standard("42351")
            CyclicPerm((0, 3, 1, 2, 4))
        """
        return cls(Perm.to_standard(iterable))

    @classmethod
    def of_length(cls, n: int) -> Iterator["CyclicPerm"]:
        """Yield every cyclic class of length ``n`` exactly once.

        Examples:
            >>> sorted(str(c) for c in CyclicPerm.of_length(3))
            ['[012]', '[021]']
            >>> sum(1 for _ in CyclicPerm.of_length(5))
            24
        """
        if n == 0:
            yield cls._from_canonical(Perm(()))
            return
        if n == 1:
            yield cls._from_canonical(Perm((0,)))
            return
        for sigma in Perm.of_length(n - 1):
            yield cls._from_canonical(Perm((0,) + tuple(v + 1 for v in sigma)))

    def representative(self) -> Perm:
        """The canonical ``1 ⊕ σ`` linear representative (starts with 0)."""
        return self._rep

    def sigma(self) -> Perm:
        """The ``σ`` in ``1 ⊕ σ`` as a ``Perm`` of length ``n - 1``."""
        if len(self._rep) <= 1:
            return Perm(())
        return Perm(v - 1 for v in self._rep[1:])

    def rotations(self) -> Iterator[Perm]:
        """All ``n`` linear rotations of the representative."""
        rep = self._rep
        n = len(rep)
        for k in range(n):
            yield rep.shift_left(k)

    def reverse(self) -> "CyclicPerm":
        return CyclicPerm(self._rep.reverse())

    def complement(self) -> "CyclicPerm":
        return CyclicPerm(self._rep.complement())

    def reverse_complement(self) -> "CyclicPerm":
        return CyclicPerm(self._rep.reverse_complement())

    def contains(self, *patts: "CyclicPerm") -> bool:
        """Cyclic containment.

        Examples:
            >>> sigma = CyclicPerm((3, 1, 2, 4, 0))
            >>> sigma.contains(CyclicPerm((0, 1, 2, 3)))
            True
            >>> Perm((3, 1, 2, 4, 0)).avoids(Perm((0, 1, 2, 3)))
            True
        """
        return all(self._contains_one(p) for p in patts)

    def avoids(self, *patts: "CyclicPerm") -> bool:
        """Cyclic avoidance. True iff no cyclic pattern in ``patts`` occurs."""
        return all(not self._contains_one(p) for p in patts)

    def avoids_set(self, patts: Iterable["CyclicPerm"]) -> bool:
        return self.avoids(*tuple(patts))

    def _contains_one(self, patt: "CyclicPerm") -> bool:
        rep = self._rep
        if len(patt) > len(rep):
            return False
        if len(patt) == 0:
            return True
        return any(rep.contains(rot) for rot in patt.rotations())

    def occurrences_of(
        self, patt: "CyclicPerm"
    ) -> Iterator[Tuple[int, Tuple[int, ...]]]:
        """Yield ``(rotation_index, positions)`` for each linear copy of a
        rotation of ``patt`` inside the canonical representative.
        """
        rep = self._rep
        if len(patt) > len(rep):
            return
        if len(patt) == 0:
            yield (0, ())
            return
        for k, rot in enumerate(patt.rotations()):
            for positions in rot.occurrences_in(rep):
                yield (k, positions)

    def count_occurrences_of(self, patt: "CyclicPerm") -> int:
        return sum(1 for _ in self.occurrences_of(patt))

    def cyclic_descents(self) -> Iterator[int]:
        """Yield indices ``i`` with ``π_i > π_{i+1 mod n}``."""
        rep = self._rep
        n = len(rep)
        for i in range(n):
            if rep[i] > rep[(i + 1) % n]:
                yield i

    def cdes(self) -> int:
        """The cyclic descent number.

        Examples:
            >>> CyclicPerm.to_standard("23514").cdes()
            2
        """
        return sum(1 for _ in self.cyclic_descents())

    def __len__(self) -> int:
        return len(self._rep)

    def __iter__(self) -> Iterator[int]:
        return iter(self._rep)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CyclicPerm):
            return self._rep == other._rep
        return NotImplemented

    def __hash__(self) -> int:
        return hash(("CyclicPerm", self._rep))

    def __lt__(self, other: "CyclicPerm") -> bool:
        if not isinstance(other, CyclicPerm):
            return NotImplemented
        return (len(self._rep), tuple(self._rep)) < (len(other._rep), tuple(other._rep))

    def __le__(self, other: "CyclicPerm") -> bool:
        if not isinstance(other, CyclicPerm):
            return NotImplemented
        return (len(self._rep), tuple(self._rep)) <= (
            len(other._rep),
            tuple(other._rep),
        )

    def __contains__(self, patt: "CyclicPerm") -> bool:
        return self._contains_one(patt)

    def __repr__(self) -> str:
        return f"CyclicPerm({tuple(self._rep)!r})"

    def __str__(self) -> str:
        if not self._rep:
            return "[ε]"
        if len(self._rep) <= 10:
            return "[" + "".join(str(i) for i in self._rep) + "]"
        return "[" + ",".join(str(i) for i in self._rep) + "]"
