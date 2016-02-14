from .misc import DancingLinks
from .permutation import Permutation
import random


class Permutations(object):
    """Class for iterating through all Permutations of length n"""

    def __init__(self, n):
        """Returns an object giving all permutations of length n"""
        assert 0 <= n
        self.n = n

    def __iter__(self):
        """Iterates through permutations of length n in lexical order"""
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

    def random_element(self):
        """Returns a random permutation of length n"""
        p = [i+1 for i in range(self.n)]
        for i in range(self.n-1, -1, -1):
            j = random.randint(0, i)
            p[i], p[j] = p[j], p[i]
        return Permutation(p)

    def __str__(self):
        return 'The set of Permutations of length %d' % self.n

    def __repr__(self):
        return 'Permutations(%d)' % self.n
