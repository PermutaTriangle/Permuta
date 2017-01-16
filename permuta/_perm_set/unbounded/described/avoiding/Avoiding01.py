from .Avoiding import *
from permuta import Perm


class Avoiding01(Avoiding):
    descriptor = Basis(Perm((0, 1)))
    def contains(self, perm):
        return perm.is_decreasing()
    def __getitem__(self, perm):
        raise NotImplementedError
