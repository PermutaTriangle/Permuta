# from .permutation import Permutation
# from .permutations import Permutations
# from .misc import DancingLinks

from permuta.permutation import Permutation
from permuta.permutations import Permutations
from permuta.misc import DancingLinks

class Avoiders(object):
    def __init__(self, patt, n):
        self.patt = patt
        self.n = n

    def __iter__(self):
        left = DancingLinks(range(1,self.n+1))
        cur = [0]*self.n
        def bt(at):
            if not Permutation.to_standard(cur[:at]).avoids(self.patt):
                return
            if at == self.n:
                yield Permutation(cur)
            else:
                nd = left.front
                while nd is not None:
                    cur[at] = nd.value
                    left.erase(nd)
                    for res in bt(at+1):
                        yield res
                    left.restore(nd)
                    nd = nd.next
        return bt(0)

class Avoiders2(object):
    def __init__(self, patt, n):
        self.patt = patt
        self.n = n

    def __iter__(self):
        left = DancingLinks(range(1,self.n+1))
        cur = [0]*self.n

        m = len(self.patt)
        st = [ Permutation.to_standard(self.patt[:i]) for i in range(m+1) ]

        occ = [ [] for i in range(m) ]
        occ[0].append([])

        def bt(at):
            # if not Permutation.to_standard(cur[:at]).avoids(self.patt):
            #     return
            if at == self.n:
                yield Permutation(cur)
            else:
                nd = left.front
                while nd is not None:
                    cur[at] = nd.value
                    left.erase(nd)

                    ok = True
                    for o in occ[m-1]:
                        here = o+[nd.value]
                        if Permutation.to_standard(here) == st[m]:
                            ok = False
                            break
                    if ok:
                        added = [0]*m
                        for l in range(m-2,-1,-1):
                            for o in occ[l]:
                                here = o+[nd.value]
                                if Permutation.to_standard(here) == st[len(here)]:
                                    occ[l+1].append(here)
                                    added[l+1] += 1

                        for res in bt(at+1):
                            yield res

                        for l in range(m):
                            for i in range(added[l]):
                                occ[l].pop()

                    left.restore(nd)
                    nd = nd.next
        return bt(0)

class Avoiders3(object):
    def __init__(self, patt, n):
        self.patt = patt
        self.n = n

    def __iter__(self):
        def bt(cur):
            if not Permutation.to_standard(cur).avoids(self.patt):
                return
            if len(cur) == self.n:
                yield Permutation(cur)
            else:
                for i in range(len(cur)+1):
                    for res in bt(cur[:i] + [len(cur)+1] + cur[i:]):
                        yield res
        return bt([])

class AvoidersMany(object):
    def __init__(self, patts, n):
        self.patts = patts
        self.n = n

    def __iter__(self):
        left = DancingLinks(range(1,self.n+1))
        cur = [0]*self.n
        def bt(at):
            for patt in self.patts:
                if not Permutation.to_standard(cur[:at]).avoids(patt):
                    return
            if at == self.n:
                yield Permutation(cur)
            else:
                nd = left.front
                while nd is not None:
                    cur[at] = nd.value
                    left.erase(nd)
                    for res in bt(at+1):
                        yield res
                    left.restore(nd)
                    nd = nd.next
        return bt(0)

class AvoidersMany2(object):
    def __init__(self, patts, n):
        self.patts = patts
        self.n = n

    def __iter__(self):
        def bt(cur):
            for patt in self.patts:
                if not Permutation.to_standard(cur).avoids(patt):
                    return
            if len(cur) <= self.n:
                yield Permutation(cur)
            if len(cur) < self.n:
                for i in range(len(cur)+1):
                    for res in bt(cur[:i] + [len(cur)+1] + cur[i:]):
                        yield res
        return bt([])

patts = [Permutation([4, 2, 3, 1]), Permutation([1, 2, 4, 3]), Permutation([4, 3, 2, 1]), Permutation([3, 4, 2, 1]), Permutation([4, 3, 1, 2]), Permutation([2, 3, 4, 1]), Permutation([2, 4, 1, 3]), Permutation([2, 3, 1, 4]), Permutation([4, 1, 3, 2]), Permutation([1, 3, 2, 4]), Permutation([3, 2, 1, 4])]
# for l in range(8+1):
#     print(l)
#     for p in AvoidersMany2(patts, l):
#         print(p)
#

patts = [ Permutation([1,2,3]), Permutation([1,4,3,2]) ]
from permuta import AvoidanceClass

for l in range(10):
    cnt = 0
    for p in AvoidanceClass(l, patts):
        cnt += 1
    print(l, cnt)


