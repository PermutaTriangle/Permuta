from .Avoiding import *
from permuta import Perm


class AvoidingEmpty(Avoiding):
    descriptor = Basis(Perm())
    def contains(self, _object):
        return False
    def __getitem__(self, perm):
        raise IndexError
