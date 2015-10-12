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
        poss = []
        for i in range(4):
            ans = mp._can_shade(pos)
            if ans:
                for j in range((-i)%4):
                    ans = _rot_right(len(self.perm)-1, ans)
                poss.append(ans[1]+1)
            mp = mp.rotate_right()
            pos = _rot_right(len(self.perm), pos)
        return poss

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
        poss = []
        for i in range(4):
            ans = mp._can_shade2(pos1, pos2)
            if ans:
                for j in range((-i)%4):
                    ans = _rot_right(len(self.perm)-1, ans)
                poss.append(ans[1]+1)
            mp = mp.rotate_right()
            pos1 = _rot_right(len(self.perm), pos1)
            pos2 = _rot_right(len(self.perm), pos2)
        return poss

    def shade(self, pos):
        if type(pos) is list:
            pos = set(pos)
        elif type(pos) is not set:
            pos = set([pos])
        return MeshPattern(self.perm, self.mesh | pos)

    def sub_mesh(self, positions):
        """
            positions: 1-based indices of points
        """
        positions = sorted(positions)
        perm = self.perm
        assert(set(positions) <= set(self.perm.perm))
        def is_shaded(left, right, lower, upper):
            shades = [ m for m in self.mesh if left <= m[0] < right and lower <= m[1] < upper ]
            points = [ i for i in range(len(perm)) if left < i+1 < right and lower < perm[i] < upper]
            return len(shades) == (right-left)*(upper-lower) and points == []
        nperm = Permutation.to_standard([perm[i-1] for i in positions])
        hor_lines = sorted([0] + [ perm[i-1] for i in positions ] + [len(perm) + 1])
        ver_lines = sorted([0] + positions + [len(perm) + 1])

        nmesh = set()
        for i in range(len(ver_lines)-1):
            for j in range(len(hor_lines)-1):
                if is_shaded(ver_lines[i], ver_lines[i+1], hor_lines[j], hor_lines[j+1]):
                    nmesh.add((i,j))

        return MeshPattern(nperm, nmesh)

    def add_point(self, (x, y), shade_dir=-1, safe=True):
        """
            shade_dir:
                -1: don't shade
                0: shade east
                1: shade north
                2: shade west
                3: shade south
        """

        if safe:
            assert (x,y) not in self.mesh

        perm = [ v if v < y+1 else v+1 for v in self.perm ]
        nperm = perm[:x] + [y+1] + perm[x:]
        nmesh = set()
        for (a,b) in self.mesh:
            if a < x:
                nx = [a]
            elif a == x:
                nx = [a,a+1]
            else:
                nx = [a+1]

            if b < y:
                ny = [b]
            elif b == y:
                ny = [b,b+1]
            else:
                ny = [b+1]

            for na in nx:
                for nb in ny:
                    nmesh.add((na,nb))

        if shade_dir == 0:
            nmesh.add((x+1,y))
            nmesh.add((x+1,y+1))
        elif shade_dir == 1:
            nmesh.add((x,y+1))
            nmesh.add((x+1,y+1))
        elif shade_dir == 2:
            nmesh.add((x,y))
            nmesh.add((x,y+1))
        elif shade_dir == 3:
            nmesh.add((x,y))
            nmesh.add((x+1,y))

        return MeshPattern(Permutation(list(nperm)), nmesh)

    def __len__(self):
        return len(self.perm)

    def __eq__(self, other):
        return self.perm == other.perm and self.mesh == other.mesh

    def __hash__(self):
        return hash((self.perm, tuple(sorted(self.mesh))))

    def __repr__(self):
        return 'MeshPattern(%s, %s)' % (repr(self.perm), repr(self.mesh))

    def __str__(self):
        n = len(self.perm)
        arr = [ [ ((str(n-(i-1)//2) if n < 10 else 'o') if self.perm[(j-1)/2] == n-(i-1)//2 else '+') if j % 2 != 0 and i % 2 != 0 else '|' if j % 2 != 0 else '-' if i % 2 != 0 else ('#' if ((j-1)/2+1, n-(i-1)/2-1) in self.mesh else ' ') for j in range(2*n+1) ] for i in range(2*n+1) ]
        return '\n'.join( ''.join(line) for line in arr )

