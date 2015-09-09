import bisect
from .permutation import Permutation

def _rot_right(n,pos):
    x,y = pos
    assert 0 <= x < n+1
    assert 0 <= y < n+1
    return (y,n-x)

class MeshPattern(object):
    def __init__(self, perm, mesh):
       self.perm = perm
       self.mesh = set(mesh)

    def contained_in(self, perm):

        def contains(i, now):
            if len(now) == len(self.perm):
                st = sorted(now)
                x = 0
                for k in perm:
                    if x < len(now) and k == now[x]:
                        x += 1
                    else:
                        y = bisect.bisect_left(st, k)
                        if (x,y) in self.mesh:
                            return False
                return True

            if i == len(perm):
                return False

            nxt = now + [perm[i]]
            if Permutation.to_standard(nxt) == Permutation.to_standard(self.perm[:len(nxt)]):
                if contains(i+1, nxt):
                    return True

            return contains(i+1, now)

        return contains(0, [])

    def rotate_right(self):
        return MeshPattern(self.perm.rotate_right(), set([ _rot_right(len(self.perm), pos) for pos in self.mesh ]))

    def _can_shade(self, pos):
        i,j = pos
        if (i,j) in self.mesh: return False
        if i-1 < 0 or self.perm[i-1] != j: return False
        if (i-1,j-1) in self.mesh: return False
        c = 0
        if (i,j-1) in self.mesh: c += 1
        if (i-1,j) in self.mesh: c += 1
        if c == 2: return False
        for l in range(len(self.perm)+1):
            if l == i-1 or l == i: continue
            if (l,j-1) in self.mesh and (l,j) not in self.mesh:
                return False
        for l in range(len(self.perm)+1):
            if l == j-1 or l == j: continue
            if (i-1,l) in self.mesh and (i,l) not in self.mesh:
                return False
        return (i-1,j-1)

    def can_shade(self, pos):
        mp = self
        for i in range(4):
            ans = mp._can_shade(pos)
            if ans:
                for j in range((-i)%4):
                    ans = _rot_right(len(self.perm)-1, ans)
                return ans[1]+1
            mp = mp.rotate_right()
            pos = _rot_right(len(self.perm), pos)
        return False

    def _can_shade2(self, pos1, pos2):
        if pos1[1] < pos2[1]:
            pos1, pos2 = pos2, pos1
        if pos1[0] == 0 or self.perm[pos1[0]-1] != pos1[1]:
            return False
        if pos1[0] != pos2[0] or pos1[1]-1 != pos2[1]:
            return False

        if pos1 in self.mesh:
            return False
        if pos2 in self.mesh:
            return False
        if (pos1[0]-1,pos1[1]) in self.mesh:
            return False
        if (pos2[0]-1,pos2[1]) in self.mesh:
            return False
        for y in range(len(self.perm) + 1):
            if y == pos1[1] or y == pos1[1] - 1: continue
            if (pos1[0] - 1, y) in self.mesh and (pos1[0], y) not in self.mesh:
                return False
        for x in range(len(self.perm) + 1):
            if x == pos1[0] or x == pos1[0] - 1: continue
            if ((x,pos1[1]) in self.mesh) != ((x,pos2[1]) in self.mesh):
                return False
        return (pos1[0]-1, pos1[1]-1)

    def can_shade2(self, pos1, pos2):
        mp = self
        for i in range(4):
            ans = mp._can_shade2(pos1, pos2)
            if ans:
                for j in range((-i)%4):
                    ans = _rot_right(len(self.perm)-1, ans)
                return ans[1]+1
            mp = mp.rotate_right()
            pos1 = _rot_right(len(self.perm), pos1)
            pos2 = _rot_right(len(self.perm), pos2)
        return False

    def shade(self, pos):
        if type(pos) is list:
            pos = set(pos)
        elif type(pos) is not set:
            pos = set([pos])
        return MeshPattern(self.perm, self.mesh | pos)

    def __eq__(self, other):
        return self.perm == other.perm and self.mesh == other.mesh

    def __hash__(self):
        return hash((self.perm, tuple(sorted(self.mesh))))

    def __repr__(self):
        return 'MeshPattern(%s, %s)' % (repr(self.perm), repr(self.mesh))

