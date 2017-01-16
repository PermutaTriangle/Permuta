# TODO: Module docstring

from permuta import Perm

from .Descriptor import Descriptor


class Basis(Descriptor):  # pylint: disable=too-few-public-methods
    """A basis class.

    A PermSet can be built with a Basis instance by using the basis provided
    to it to see if a perm should be in the PermSet or not. Additionally,
    various fast methods exist to build a PermSet defined by a basis.
    """
    def __init__(self, perms):
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

        self._perms = perms

    @property
    def perms(self):
        return self._perms

    def is_polynomial(self):
        return True  # TODO

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.perms == other.perms

    def __hash__(self):
        return hash(self.perms)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__qualname__, self.perms)
