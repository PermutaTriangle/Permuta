from permutations import Permutations
from mesh_pattern import MeshPattern

class MeshPatterns(object):
    def __init__(self, n):
        self.n = n

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
                for r in gen(p, x+1, y, s + [(x,y)]):
                    yield r

        for p in Permutations(self.n):
            for r in gen(p, 0, 0, []):
                yield r

    def __str__(self):
        return 'The set of MeshPatterns of length %d' % self.n

    def __repr__(self):
        return 'MeshPatterns(%d)' % self.n

