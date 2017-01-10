from .Permutations import Permutations
from .MeshPattern import MeshPattern
import random


class MeshPatterns(object):
    """Class to allow for collections of MeshPatterns"""
    def __init__(self, n, patt=None):
        """Returns the MeshPatterns object for mesh patterns of length n
        If patt is specified only generates patterns with
        underlying pattern patt"""
        self.n = n
        self.patt = patt
        if patt is not None:
            assert len(patt) == n

    def __iter__(self):
        def gen(p, x, y, s):
            if x == self.n+1:
                for r in gen(p, 0, y+1, s):
                    yield r
            elif y == self.n+1:
                yield MeshPattern(p, s)
            else:
                for r in gen(p, x+1, y, s):
                    yield r
                for r in gen(p, x+1, y, s + [(x, y)]):
                    yield r

        if self.patt is None:
            for p in Permutations(self.n):
                for r in gen(p, 0, 0, []):
                    yield r
        else:
            for r in gen(self.patt, 0, 0, []):
                yield r

    def random_element(self):
        """Returns a random MeshPattern of length n
        if patt with underlying pattern patt """
        perm = (Permutations(self.n).random_element() if
                self.patt is None else self.patt)
        mesh = set()
        for i in range(self.n+1):
            for j in range(self.n+1):
                if random.randint(0, 1):
                    mesh.add((i, j))
        return MeshPattern(perm, mesh)

    def __str__(self):
        if self.patt is not None:
            return ('The set of MeshPatterns with underlying classical pattern \
                    %s' % self.patt)
        else:
            return 'The set of MeshPatterns of length %d' % self.n

    def __repr__(self):
        return 'MeshPatterns(%d%s)' % (self.n,
                                       ', %s' % self.patt if
                                       self.patt is not None else '')
