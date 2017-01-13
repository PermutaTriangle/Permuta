from .Avoiding import *


class Avoiding10(Avoiding):
    descriptor = Basis(1)
    def contains(self, perm):
        raise NotImplementedError
    def __getitem__(self, perm):
        raise NotImplementedError
