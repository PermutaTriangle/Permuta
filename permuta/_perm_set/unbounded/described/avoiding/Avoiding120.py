from .Avoiding import *
from permuta import Perm
from .CatalanAvoiding import CatalanAvoidingClass


class Avoiding120(AvoidingGeneric, CatalanAvoidingClass):
    descriptor = Basis(Perm((1, 2, 0)))

    def _ensure_level(self, level_number):
        while len(self.cache) <= level_number:
            new_level = set()
            current_level_number = len(self.cache)
            frame = Perm((0,2,1))
            for left_length in range(current_level_number):
                right_length = current_level_number - left_length - 1
                for left_perm in self.cache[left_length]:
                    for right_perm in self.cache[right_length]:
                        new_perm = frame.inflate([left_perm, None, right_perm])
                        new_level.add(new_perm)
            self.cache.append(new_level)
