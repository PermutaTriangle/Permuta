from .Avoiding import *
from permuta import Perm
from .CatalanAvoiding import CatalanAvoidingClass

class Avoiding102(AvoidingGeneric, CatalanAvoidingClass):
    descriptor = Basis(Perm((1, 0, 2)))

    def _ensure_level(self, level_number):
        while len(self.cache) <= level_number:
            new_level = set()
            current_level_number = len(self.cache)
            frame = Perm((1,2,0))
            for lower_length in range(current_level_number):
                upper_length = current_level_number - lower_length - 1
                for lower_perm in self.cache[lower_length]:
                    for upper_perm in self.cache[upper_length]:
                        new_perm = frame.inflate([None, upper_perm, lower_perm])
                        new_level.add(new_perm)
            self.cache.append(new_level)
