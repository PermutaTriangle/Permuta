from .Avoiding import *


class Avoiding01(Avoiding):
    descriptor = Basis(1)
    def contains(self, perm):
        raise NotImplementedError
    def __getitem__(self, perm):
        raise NotImplementedError
