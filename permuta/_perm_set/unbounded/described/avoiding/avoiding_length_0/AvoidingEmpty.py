from permuta import Perm
from permuta.descriptors import Basis
from permuta._perm_set.finite import PermSetStatic

from ..Avoiding import Avoiding


class AvoidingEmpty(Avoiding):
    """The empty perm set class."""
    DESCRIPTOR = Basis(Perm())

    def of_length(self, _length):
        return PermSetStatic()

    def __contains__(self, _object):
        return False

    def __getitem__(self, _key):
        raise IndexError

    def __len__(self):
        return 0
