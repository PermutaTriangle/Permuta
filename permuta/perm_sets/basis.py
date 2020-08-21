import re
from typing import Iterable, List, Union

from ..patterns import MeshPatt, Patt, Perm


class Basis(tuple):
    """A set of classical patterns such that none is
    contained in another within the basis.
    """

    def __new__(cls, *patts: Perm) -> "Basis":
        if not patts:
            return tuple.__new__(cls, ())
        return cls._pruner(sorted(patts))

    @classmethod
    def from_string(cls, patts: str) -> "Basis":
        """Construct a Basis from a string. It can be either 0 or 1 based and
        seperated by anything."""
        return cls(*map(Perm.to_standard, re.findall(r"\d+", patts)))

    @classmethod
    def from_iterable(cls, patts: Iterable[Perm]) -> "Basis":
        """Construct a Basis from an iterable."""
        return cls(*patts)

    @classmethod
    def _pruner(cls, patts: List[Perm]) -> "Basis":
        if len(patts[0]) == 0:
            return tuple.__new__(cls, (patts[0],))
        new_basis: List[Perm] = []
        for patt in patts:
            if patt.avoids(*new_basis):
                new_basis.append(patt)
        return tuple.__new__(cls, new_basis)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and tuple.__eq__(self, other)

    def __hash__(self) -> int:
        return tuple.__hash__(self)

    def __repr__(self) -> str:
        return f"Basis({tuple.__repr__(self)})"

    def __str__(self) -> str:
        return f'{{{", ".join(str(p) for p in self)}}}'


class MeshBasis(tuple):
    """A set of patterns such that none is
    contained in another within the basis.
    """

    @staticmethod
    def is_mesh_basis(basis: Iterable[Patt]) -> bool:
        """Checks if a collection of patterns contains any non-classical ones."""
        return not (
            isinstance(basis, Perm) or all(isinstance(patt, Perm) for patt in basis)
        )

    def __new__(cls, *patts: Union[Perm, MeshPatt]) -> "MeshBasis":
        if not patts:
            return tuple.__new__(cls, ())
        return cls._pruner(
            sorted(
                patt if isinstance(patt, MeshPatt) else MeshPatt(patt, [])
                for patt in patts
            )
        )

    @classmethod
    def from_iterable(cls, patts: Iterable[Union[Perm, MeshPatt]]) -> "MeshBasis":
        """Construct a MeshBasis from an iterable."""
        return cls(*patts)

    @classmethod
    def _pruner(cls, patts: List[MeshPatt]) -> "MeshBasis":
        if len(patts[0]) == 0:
            return tuple.__new__(cls, (patts[0],))
        new_basis: List[MeshPatt] = []
        for patt in patts:
            if patt.avoids(*new_basis):
                new_basis.append(patt)
        return tuple.__new__(cls, new_basis)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and tuple.__eq__(self, other)

    def __hash__(self) -> int:
        return tuple.__hash__(self)

    def __repr__(self) -> str:
        return f"{MeshBasis}({tuple.__repr__(self)})"

    def __str__(self) -> str:
        return f'{{{", ".join(str(p) for p in self)}}}'
