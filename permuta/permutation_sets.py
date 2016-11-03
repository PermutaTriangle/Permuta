import collections
from .permutation import Permutation
from .permutations import Permutations
from .math import catalan

class PermutationPatternClass(object):
    def __init__(self, n, pattern):
        self.n = n
        self.patt = pattern
        self.pattstr = "".join(map(str,self.patt))

    def __str__(self):
        return "Permutations of length %d avoiding %s" % (self.n, self.pattstr)

    def __repr__(self):
        return "PermutationPatternClass(%d,%s)" % (self.n, self.patt)


class AvoidanceClass(object):
    def __new__(cls, n, avoiding, **kwargs):
        if isinstance(avoiding, Permutation):
            p = avoiding.perm
            if p == [1,2]:
                return PermutationsAvoiding12(n)
            elif p== [2,1]:
                return PermutationsAvoiding21(n)
            elif p == [1,2,3]:
                return PermutationsAvoiding123(n)
            elif p == [1,3,2]:
                return PermutationsAvoiding132(n)
            elif p == [2,1,3]:
                return PermutationsAvoiding213(n)
            elif p == [2,3,1]:
                return PermutationsAvoiding231(n)
            elif p == [3,1,2]:
                return PermutationsAvoiding312(n)
            elif p == [3,2,1]:
                return PermutationsAvoiding321(n)
            else:
                return PermutationsAvoidingGeneric(n,(avoiding,))
        elif (isinstance(avoiding, collections.Iterable) and
                all(isinstance(x, Permutation) for x in avoiding)):
            return PermutationsAvoidingGeneric(n,avoiding, **kwargs)
        else:
            raise RuntimeError("Cannot avoid " + repr(avoiding))


class PermutationsAvoidingGeneric(PermutationPatternClass):
    def __init__(self, n, patterns, upto=False):
        super(PermutationsAvoidingGeneric, self).__init__(n,tuple(patterns))
        self.n = n
        self.pattstr = "("+",".join(["".join(map(str,x)) for x in patterns])+")"
        self.upto = upto

    def __iter__(self):
        # TODO: make this lazy, i.e. use yield inside the generation (if possible)
        cur = set([ Permutation([]) ])
        if self.upto or self.n == 0:
            maybe = Permutation([])
            ok = True
            for p in self.patt:
                if maybe.contains(p):
                    ok = False
                    break
            if ok:
                yield maybe

        for l in range(1,self.n+1):
            nxt = set()
            for prev in cur:
                for i in range(len(prev)+1):
                    maybe = Permutation(prev.perm[:i] + [len(prev)+1] + prev.perm[i:])
                    ok = True
                    for p in self.patt:
                        if maybe.contains(p): # TODO: only check for occurrences that contain the new len(prev)+1 element
                            ok = False
                            break
                    if ok:
                        nxt.add(maybe)
            cur = nxt
            if self.upto or l == self.n:
                for p in cur:
                    yield p

    def is_polynomial(self):
        overallinterset = set([])
        for perm in self.patt:
            overallinterset = overallinterset.union(types(perm))
            if len(overallinterset) == 10:
                return True
        return False

class PermutationsAvoiding12(PermutationPatternClass):
    """Class for iterating through Permutations avoiding 12 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding12, self).__init__(n,[1,2])

    def __iter__(self):
        yield Permutation(range(self.n,0,-1))

    def __len__(self):
        return 1

class PermutationsAvoiding21(PermutationPatternClass):
    """Class for iterating through Permutations avoiding 21 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding21, self).__init__(n,[2,1])

    def __iter__(self):
        yield Permutation(range(1,self.n+1))

    def __len__(self):
        return 1

class CatalanAvoidingClass(PermutationPatternClass):
    def __init__(self, n, pattern):
        super(CatalanAvoidingClass, self).__init__(n,pattern)

    def __len__(self):
        return catalan(self.n)

class PermutationsAvoiding123(CatalanAvoidingClass):
    def __init__(self,n):
        super(PermutationsAvoiding123, self).__init__(n,[1,2,3])

    def __iter__(self):

        if self.n == 0:
            yield Permutation([])
            return
        elif self.n <3:
            for p in Permutations(self.n):
                yield p
            return
        elif self.n ==3:
            for p in Permutations(self.n):
                if p!= Permutation([1,2,3]):
                    yield p
            return

        for p in PermutationsAvoiding132(self.n):
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
        super(PermutationsAvoiding213, self).__init__(n,[2,1,3])

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.reverse().complement()


class PermutationsAvoiding231(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 231 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding231, self).__init__(n,[2,3,1])

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.reverse()


class PermutationsAvoiding312(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 312 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding312, self).__init__(n,[3,1,2])

    def __iter__(self):
        for p in PermutationsAvoiding132(self.n):
            yield p.complement()

class PermutationsAvoiding321(CatalanAvoidingClass):
    def __init__(self,n):
        super(PermutationsAvoiding321, self).__init__(n,[3,2,1])

    def __iter__(self):
        for p in PermutationsAvoiding123(self.n):
            yield p.reverse()

# # Will return the set of polynomial types it intersects with (W_++, W+-, W^-1 ++, L_2, L_2^R etc)
# # 1: W++, 2: W+-, 3: W-+, 4: W--, 5: Winv++, 6: Winv+-, 7: Winv-+, 8: Winv--, 9: L2, 10: L2inv
def types(perm):
    interset = set([])
    for i in range(len(perm)+1):
        part1 = perm[0:i]
        part2 = perm[i:]

        if is_incr(part1):
            if is_incr(part2):
                interset.add(1)
            if is_decr(part2):
                interset.add(2)

        if is_decr(part1):
            if is_incr(part2):
                interset.add(3)
            if is_decr(part2):
                interset.add(4)

        # if is_incr(part1) and is_incr(part2):
        #     interset.add(1)
        # if is_incr(part1) and is_decr(part2):
        #     interset.add(2)
        # if is_decr(part1) and is_incr(part2):
        #     interset.add(3)
        # if is_decr(part1) and is_decr(part2):
        #     interset.add(4)
    flipperm = perm.inverse()
    for i in range(len(perm)+1):
        part1 = flipperm[0:i]
        part2 = flipperm[i:]

        if is_incr(part1):
            if is_incr(part2):
                interset.add(5)
            if is_decr(part2):
                interset.add(6)

        if is_decr(part1):
            if is_incr(part2):
                interset.add(7)
            if is_decr(part2):
                interset.add(8)

        # if is_incr(part1) and is_incr(part2):
        #     interset.add(5)
        # if is_incr(part1) and is_decr(part2):
        #     interset.add(6)
        # if is_decr(part1) and is_incr(part2):
        #     interset.add(7)
        # if is_decr(part1) and is_decr(part2):
        #     interset.add(8)
    if in_L2(perm):
        interset.add(9)
    if in_L2([perm[i] for i in range(len(perm)-1,-1,-1)]):
        interset.add(10)
    return interset

# TODO: When Permutation inherits from tuple, this function should no longer be
# necessary.
def is_decr(L):
    for i in range(len(L) - 1):
        if L[i] < L[i+1]:
            return False
    return True

# TODO: When Permutation inherits from tuple, this function should no longer be
# necessary.
def is_incr(L):
    for i in range(len(L) - 1):
        if L[i] > L[i+1]:
            return False
    return True


# TODO: When Permutation inherits from tuple, move this into Permutation.py?
def in_L2(L):
    n = len(L)
    if n == 0 or n == 1:
        return True
    if L[-1] == n:
        return in_L2(L[0:n-1])
    elif L[-1] == n-1 and L[-2] == n:
        return in_L2(L[0:n-2])
    else:
        return False
