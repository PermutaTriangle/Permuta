# TODO: Module docstring

import time

from collections import Iterable
from permuta import Perm

from .Descriptor import Descriptor


class Basis(Descriptor, tuple):  # pylint: disable=too-few-public-methods
    """A basis class.

    A PermSet can be built with a Basis instance by using the basis provided
    to it to see if a perm should be in the PermSet or not. Additionally,
    various fast methods exist to build a PermSet defined by a basis.
    """
    def __new__(cls, perms):
        return tuple.__new__(cls).union(perms)

    @classmethod
    def old_new(cls, perms):
        # Make sure we're working with a sorted list of perms
        if isinstance(perms, Perm):
            perms = (perms,)
        else:
            perms = tuple(sorted(perms))

        if len(perms) > 1:
            # Remove superfluous elements from basis
            # TODO: This can be smarter, I guess
            not_needed = set()
            for i in range(len(perms)):
                if i in not_needed:
                    continue
                for j in range(i + 1, len(perms)):
                    if j in not_needed:
                        continue
                    if perms[i].contained_in(perms[j]):
                        not_needed.add(j)
            if not_needed:
                perms = tuple(perms[i] for i in range(len(perms)) if i not in not_needed)
        return tuple.__new__(cls, perms)

    def union(self, perms):
        if not isinstance(perms, Iterable):
            raise TypeError("Non-iterable argument cannot be unified with basis")

        # Input cleaning
        perms = set([perms] if isinstance(perms, Perm) else perms)

        if not perms:
            # Empty set of perms added to basis
            return self

        # Make sure the elements are permutations
        for perm in perms:
            if not isinstance(perm, Perm):
                raise TypeError("Elements of a basis should all be perms")

        # Add basis perms and sort
        perms.update(self)
        perms = sorted(perms)  # Necessarily non-empty


        # The new basis
        new_basis = []

        # The list of basis perms used for the new basis
        basis_perms_used = []

        # The list of new perms used for the new basis
        new_perms_used = []

        empty_perm = Perm()  # Just for checking if it is in the basis

        if perms[0] == empty_perm:
            # If empty perm is in there, then no other element is viable
            new_basis.append(empty_perm)
            new_perms_used.append(empty_perm)
        else:
            perms_iter = iter(perms)
            basis_iter = iter(self)
            for basis_perm in basis_iter:
                # Add perms up to and including this basis perm to the basis
                while True:
                    perm = next(perms_iter)
                    if perm == basis_perm:
                        # Add if it avoids the new perms used
                        if perm.avoids(*new_perms_used):
                            new_basis.append(perm)
                            basis_perms_used.append(perm)
                        break
                    elif perm.avoids(*new_basis):
                        # Add it if it avoids the new basis perms
                        new_basis.append(perm)
                        new_perms_used.append(perm)
            for perm in perms_iter:
                # All perms left over weren't in the basis before
                if perm.avoids(*new_basis):
                    new_basis.append(perm)
                    new_perms_used.append(perm)

        # Return either the unmodified basis or a new basis
        if new_perms_used:
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
