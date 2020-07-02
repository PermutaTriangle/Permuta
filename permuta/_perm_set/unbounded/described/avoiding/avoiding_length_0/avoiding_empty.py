from typing import Any

from ......descriptors.basis import Basis
from ......perm import Perm
from .....finite.permset_static import PermSetStatic
from ..avoiding import Avoiding


class AvoidingEmpty(Avoiding):
    """The empty perm set class."""

    DESCRIPTOR: Any = Basis(Perm())
    __CLASS_CACHE = None

    def __new__(cls, basis):
        if AvoidingEmpty.__CLASS_CACHE is None:
            instance = super(AvoidingEmpty, cls).__new__(cls)
            AvoidingEmpty.__CLASS_CACHE = instance
            return instance
        else:
            return AvoidingEmpty.__CLASS_CACHE

    def of_length(self, _length):
        return PermSetStatic()

    def __contains__(self, _object):
        return False

    def __getitem__(self, _key):
        raise IndexError

    def __len__(self):
        return 0
