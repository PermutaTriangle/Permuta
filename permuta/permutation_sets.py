from .permutation import Permutation
from .permutations import Permutations

class PermutationsAvoiding12(Permutations):
    """Class for iterating through Permutations avoiding 12 of length n"""
    def __init__(self, n):
        assert 0 <= n
        super(PermutationsAvoiding12, self).__init__(n)

    def __iter__(self):
        yield Permutation(range(self.n,0,-1))

    def __str__(self):
        mod = ' avoiding 12'
        return super(PermutationsAvoiding12,self).__str__() + mod

    def __repr__(self):
        return 'PermutationsAvoiding12(%d)' % self.n


class PermutationsAvoiding21(Permutations):
    """Class for iterating through Permutations avoiding 21 of length n"""
    def __init__(self, n):
        assert 0 <= n
        super(PermutationsAvoiding12, self).__init__(n)

    def __iter__(self):
        yield Permutation(range(1,n+1))

    def __str__(self):
        mod = ' avoiding 12'
        return super(PermutationsAvoiding12,self).__str__() + mod

    def __repr__(self):
        return 'PermutationsAvoiding12(%d)' % self.n


class PermutationsAvoiding132(Permutations):
    """Class for iterating through Permutations avoiding 132 of length n"""
    def __init__(self, n):
        assert 0 <= n
        super(PermutationsAvoiding132, self).__init__(n)

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

                    yield Permutation([x + right_length for x in left] + [self.n] + list(right))
        return

    def __str__(self):
        mod = ' avoiding 132'
        return super(PermutationsAvoiding132,self).__str__() + mod

    def __repr__(self):
        return 'PermutationsAvoiding132(%d)' % self.n


class PermutationsAvoiding213(Permutations):
    """Class for iterating through Permutations avoiding 213 of length n"""
    def __init__(self, n):
        assert 0 <= n
        super(PermutationsAvoiding213, self).__init__(n)

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.reverse().complement()

    def __str__(self):
        mod = ' avoiding 213'
        return super(PermutationsAvoiding213,self).__str__() + mod

    def __repr__(self):
        return 'PermutationsAvoiding213(%d)' % self.n


class PermutationsAvoiding231(Permutations):
    """Class for iterating through Permutations avoiding 231 of length n"""
    def __init__(self, n):
        assert 0 <= n
        super(PermutationsAvoiding231, self).__init__(n)

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.reverse()

    def __str__(self):
        mod = ' avoiding 231'
        return super(PermutationsAvoiding231,self).__str__() + mod

    def __repr__(self):
        return 'PermutationsAvoiding231(%d)' % self.n


class PermutationsAvoiding312(Permutations):
    """Class for iterating through Permutations avoiding 312 of length n"""
    def __init__(self, n):
        assert 0 <= n
        super(PermutationsAvoiding312, self).__init__(n)

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.complement()

    def __str__(self):
        mod = ' avoiding 312'
        return super(PermutationsAvoiding312,self).__str__() + mod

    def __repr__(self):
        return 'PermutationsAvoiding312(%d)' % self.n
