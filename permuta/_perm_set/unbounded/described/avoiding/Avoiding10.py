from .Avoiding import *


class Avoiding10(Avoiding):
    descriptor = Basis(Perm((1, 0)))
    def contains(self, perm):
        return perm.is_increasing()
    def __getitem__(self, perm):
        raise NotImplementedError
