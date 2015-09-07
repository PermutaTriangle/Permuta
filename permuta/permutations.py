from .misc import DancingLinks
from .permutation import Permutation

class Permutations(object):
    def __init__(self, n):
        assert 0 <= n
        self.n = n

    def __iter__(self):

        left = DancingLinks(range(1, self.n+1))
        res = []
        def gen():
            if len(left) == 0:
                yield Permutation(list(res))
            else:
                cur = left.front
                while cur is not None:
                    left.erase(cur)
                    res.append(cur.value)
                    for p in gen():
                        yield p
                    res.pop()
                    left.restore(cur)
                    cur = cur.next

        return gen()

    def __str__(self):
        return 'The set of Permutations of length %d' % self.n

    def __repr__(self):
        return 'Permutations(%d)' % self.n

