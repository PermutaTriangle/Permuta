# TODO: Module docstring

import abc
from collections.abc import Iterable

from ..patterns.meshpatt import MeshPatt
from ..patterns.perm import Perm
from .descriptor import Descriptor


class AbstractBasis(Descriptor, tuple, abc.ABC):
    @property
    @abc.abstractmethod
    def ALLOWED_BASIS_ELEMENT_TYPES(self):
        raise NotImplementedError

    def __new__(cls, patts):
        return tuple.__new__(cls).union(patts, cls.ALLOWED_BASIS_ELEMENT_TYPES)

    def union(self, patts, patt_types):
        if not isinstance(patts, Iterable):
            raise TypeError("Non-iterable argument cannot be unified with basis")

        # Input cleaning
        patts = set([patts] if isinstance(patts, patt_types) else patts)

        if not patts:
            # Empty set of patts added to basis
            return self

        # Make sure the elements are patterns
        for patt in patts:
            if not isinstance(patt, patt_types):
                raise TypeError(
                    "Elements of a basis should all be of type(s) {}".format(patt_types)
                )

        # Add basis patts and sort
        patts.update(self)
        patts = sorted(patts)  # Necessarily non-empty

        # The new basis
        new_basis = []

        # The list of basis patts used for the new basis
        basis_patts_used = []

        # The list of new patts used for the new basis
        new_patts_used = []

        if patts[0] in [c() for c in patt_types]:
            new_basis.append(patts[0])
            new_patts_used.append(patts[0])
        else:
            patts_iter = iter(patts)
            basis_iter = iter(self)
            for basis_perm in basis_iter:
                # Add perms up to and including this basis perm to the basis
                while True:
                    patt = next(patts_iter)
                    if patt == basis_perm:
                        # Add if it avoids the new perms used
                        if patt.avoids(*new_patts_used):
                            new_basis.append(patt)
                            basis_patts_used.append(patt)
                        break
                    elif patt.avoids(*new_basis):
                        # Add it if it avoids the new basis perms
                        new_basis.append(patt)
                        new_patts_used.append(patt)
            for patt in patts_iter:
                # All perms left over weren't in the basis before
                if patt.avoids(*new_basis):
                    new_basis.append(patt)
                    new_patts_used.append(patt)

        # Return either the unmodified basis or a new basis
        if new_patts_used:
            return tuple.__new__(self.__class__, new_basis)
        else:
            return self

    def is_polynomial(self):
        return True  # TODO

    def __eq__(self, other):
        return isinstance(other, self.__class__) and tuple.__eq__(self, other)

    def __hash__(self):
        return tuple.__hash__(self)

    def __repr__(self):
        return "{}({})".format(self.__class__.__qualname__, tuple.__repr__(self))

    def __str__(self):
        return "{{{}}}".format(", ".join(str(p) for p in self))


class Basis(AbstractBasis):
    """A basis class.

    A PermSet can be built with a Basis instance by using the basis provided
    to it to see if a perm should be in the PermSet or not. Additionally,
    various fast methods exist to build a PermSet defined by a basis.
    """

    ALLOWED_BASIS_ELEMENT_TYPES = (Perm,)


class MeshBasis(AbstractBasis):
    ALLOWED_BASIS_ELEMENT_TYPES = (MeshPatt,)

    def __new__(cls, patts):
        return super().__new__(
            cls,
            {
                patt if isinstance(patt, MeshPatt) else MeshPatt(Perm(patt), [])
                for patt in patts
            },
        )


def detect_basis_cls(basis):
    # Argument can be the actual basis class
    if basis in AbstractBasis.__subclasses__():
        return basis

    # Argument can be an instance of the basis classes
    for BasisCls in AbstractBasis.__subclasses__():
        if isinstance(basis, BasisCls):
            return BasisCls

    # Argument can be an object or an iterable of objects that makes up a basis
    if isinstance(basis, Perm) or all(isinstance(patt, Perm) for patt in basis):
        return Basis
    elif isinstance(basis, MeshPatt) or all(
        isinstance(patt, (Perm, MeshPatt)) for patt in basis
    ):
        return MeshBasis
    else:
        raise ValueError("A basis can only contain Perms and MeshPatts.")
