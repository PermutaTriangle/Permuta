from .Avoiding import *
from permuta import Perm
from .CatalanAvoiding import CatalanAvoidingClass


class Avoiding210(AvoidingGeneric, CatalanAvoidingClass):
    descriptor = Basis(Perm((2, 1, 0)))

    def _ensure_level(self, level_number):
        raise NotImplementedError
