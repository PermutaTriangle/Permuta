from .permutation import Permutation
from .permutations import Permutations
from .math import catalan

class PermutationPatternClass(Permutations):
    def __init__(self, n, pattern):
        super(PermutationPatternClass,self).__init__(n)
        self.patt = pattern
        self.pattstr = "".join(map(str,self.patt))

    def __str__(self):
        return "Permutations of length %d avoiding %s" % (self.n, self.pattstr)

    def __repr__(self):
        return "PermutationPatternClass(%d,%s)" % (self.n, self.patt)

    def __len__(self):
        return 1
        
class PermutationsAvoiding12(PermutationPatternClass):
    """Class for iterating through Permutations avoiding 12 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding12, self).__init__(n,[1,2])

    def __iter__(self):
        yield Permutation(range(self.n,0,-1))

class PermutationsAvoiding21(PermutationPatternClass):
    """Class for iterating through Permutations avoiding 21 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding12, self).__init__(n,[2,1])

    def __iter__(self):
        yield Permutation(range(1,n+1))

    def __len__(self):
        return 1

class CatalanAvoidingClass(PermutationPatternClass):
    def __init__(self, n, pattern):
        super(PermutationPatternClass, self).__init__(n,pattern)

    def __len__(self):
        return catalan(n)

class PermutationsAvoiding132(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 132 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding132, self).__init__(n,[1,3,2])

    def __iter__(self):

        if self.n == 0:
            yield Permutation([])
            return
        elif self.n < 3:
            for p in Permutations(self.n):
                yield p
            return
        elif self.n == 3:
            for p in Permutations(self.n):
                if p != Permutation([1,3,2]):
                    yield p
            return

        for left_length in range(0,self.n):
            right_length = self.n - 1 - left_length
            for left in PermutationsAvoiding132(left_length):
                for right in PermutationsAvoiding132(right_length):

                    yield Permutation([x + right_length for x in left]
                                         + [self.n]
                                         + list(right))
        return


class PermutationsAvoiding213(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 213 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding213, self).__init__(n)

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.reverse().complement()


class PermutationsAvoiding231(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 231 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding231, self).__init__(n)

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.reverse()


class PermutationsAvoiding312(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 312 of length n"""
    def __init__(self, n):
        assert 0 <= n
        super(PermutationsAvoiding312, self).__init__(n)

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.complement()
