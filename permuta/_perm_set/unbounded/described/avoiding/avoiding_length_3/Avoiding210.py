from .Avoiding import *
from permuta import Perm
from .CatalanAvoiding import CatalanAvoidingClass


class Avoiding210(AvoidingGeneric, CatalanAvoidingClass):
    descriptor = Basis(Perm((2, 1, 0)))

    def _ensure_level(self, level_number):
        while len(self.cache) <= level_number:
            new_level = set()
            current_level_number = len(self.cache)
            for perm in self.cache[-1]:
                first_descent_location = next(perm.descents(), current_level_number-2)
                for index in range(first_descent_location+2):
                    new_perm = perm.insert(index, 0)
                    new_level.add(new_perm)
            self.cache.append(new_level)
