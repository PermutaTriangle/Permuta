# TODO: Module docstring

from .Descriptor import Descriptor


class Basis(Descriptor):  # pylint: disable=too-few-public-methods
    """A basis class.

    A PermSet can be built with a Basis instance by using the basis provided
    to it to see if a perm should be in the PermSet or not. Additionally,
    various fast methods exist to build a PermSet defined by a basis.
    """
    def __init__(self, perms):
        # TODO: Make perms a proper basis
        self.basis = perms
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.basis == other.basis
