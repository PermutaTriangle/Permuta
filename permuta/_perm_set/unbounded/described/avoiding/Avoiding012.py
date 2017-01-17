from .Avoiding import *
from permuta import Perm
from .CatalanAvoiding import CatalanAvoidingClass

class Avoiding012(AvoidingGeneric, CatalanAvoidingClass):
    descriptor = Basis(Perm((0, 1, 2)))

    def _ensure_level(self, level_number):
        # Ensure level is available
        patts = self.basis
        while len(self.cache) <= level_number:
            new_level = set()

            for perm in self.cache[-1]:
                first_ascent_location = 0
                while first_ascent_location < level_number - 2 and perm[first_ascent_location] > perm[first_ascent_location+1]:
                    first_ascent_location += 1
                
            self.cache.append(new_level)

    def _ensure_level(self, level_number):
        while len(self.cache) <= level_number:
            new_level = set()



            self.cache.append(new_level)

    def __iter__(self):

        if self.n == 0:
            yield Permutation([])
            return
        elif self.n < 3:
            for p in Permutations(self.n):
                yield p
            return
        elif self.n ==3:
            for p in Permutations(self.n):
                if p!= Permutation([1,2,3]):
                    yield p
            return

        for p in PermutationsAvoiding021(self.n):
            # use simion-schmidt bijection
            m = self.n + 1
            minima = []
            minima_positions = []
            for index, value in enumerate(p):
                if value < m:
                    minima_positions.append(index)
                    minima.append(value)
                    m = value
            new_perm = []
            non_minima = [x for x in range(self.n, 0, -1) if x not in minima]
            a = 0
            b = 0
            for i in range(self.n):
                if i in minima_positions:
                    new_perm.append( minima[a] )
                    a += 1
                else:
                    new_perm.append( non_minima[b] )
                    b += 1
            yield Permutation(new_perm)
