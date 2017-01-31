from .Avoiding import AvoidingGeneric
from .CatalanAvoidingSpecificLength import CatalanAvoidingSpecificLength

from permuta import Perm


class Avoiding012(AvoidingGeneric):
    descriptor = Basis(Perm((0, 1, 2)))

    def _ensure_level(self, level_number):
        while len(self.cache) <= level_number:
            new_level = set()
            current_level_number = len(self.cache)
            for perm in self.cache[-1]:
                first_ascent_location = next(perm.ascents(), current_level_number - 2)
                for index in range(first_ascent_location+2):
                    new_perm = perm.insert(index, current_level_number - 1)
                    new_level.add(new_perm)
            self.cache.append(new_level)
