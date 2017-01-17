from .Avoiding import *
from permuta import Perm
from .CatalanAvoiding import CatalanAvoidingClass

class Avoiding021(AvoidingGeneric, CatalanAvoidingClass):
    descriptor = Basis(Perm((0, 2, 1)))

    def _ensure_level(self, level_number):
        while len(self.cache) <= level_number:
            new_level = set()
            frame = Perm((1,2,0))
            for left_length in range(level_number):
                right_length = level_number - left_length - 1
                for left_perm in self.cache[left_length]:
                    for right_perm in self.cache[right_length]:
                        new_perm = frame.inflate([left_perm, None, right_perm])
                        new_level.add(new_perm)
            self.cache.append(new_level)
