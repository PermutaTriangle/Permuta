# TODO: Module docstring

from permuta import Perm
from permuta import PermSet

from .Descriptor import Descriptor


# TODO: Inherit from PermSetGeneric
class Basis(Descriptor):  # pylint: disable=too-few-public-methods
    """A basis class.

    A PermSet can be built with a Basis instance by using the basis provided
    to it to see if a perm should be in the PermSet or not. Additionally,
    various fast methods exist to build a PermSet defined by a basis.
    """
    def __init__(self, perms):
        # Make sure we're working with a PermSet
        if isinstance(perms, Perm) or not isinstance(perms, PermSet):
            perms = PermSet(perms)

        if len(perms > 1):
            # Remove superfluous elements from basis
            # TODO: This can be smarter, I guess
            not_needed = set()
            for i in range(len(perms)):
                if i in not_needed:
                    continue
                for j in range(i + 1, len(perms)):
                    if perms[i].contained_in(perm[j]):
                        not_needed.add(j)
            if not_needed:
                perms = PermSet(perms[i] for i in range(len(perms)) if i not in not_needed)


        # TODO: Make perms a proper basis
        self.basis = perms
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.basis == other.basis
    def __repr__(self):
        return "<{} {}>".format(self.__class__.__qualname__, self.basis)
