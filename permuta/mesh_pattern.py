import bisect
import itertools
import numbers
import collections

from permuta import Permutation, Pattern
from permuta.misc import DIR_EAST, DIR_NORTH, DIR_WEST, DIR_SOUTH, DIR_NONE


class MeshPattern(Pattern):
    """A mesh pattern class."""

    def __init__(self, pattern=(), shading=frozenset(), check=False):
        # TODO: Docstring
        if not isinstance(pattern, Permutation):
            pattern = Permutation(pattern, check=check)
        if check:
            # TODO: Add exception messages
            assert isinstance(collections.Set, shading)
            for coordinate in shading:
                assert isinstance(coordinate, tuple)
                assert len(coordinate) == 2
                x, y = coordinate
                assert isinstance(x, numbers.Integral)
                assert 0 <= x <= len(pattern)
                assert isinstance(y, numbers.Integral)
                assert 0 <= y <= len(pattern)
        self.pattern = pattern
        self.shading = shading

    #
    # Occurrence/Avoidance/Containment methods
    #

    def contained_in(self, perm):
        # TODO: Make occurrence function like for classical patterns
        #       and call that function
        clpatt = self.perm
        R = self.shading
        k = len(clpatt)
        n = len(perm)

        perm_cart = set(_G(perm))

        for H in clpatt.occurrences_in(perm):
            X = dict(_G(sorted(i+1 for i in H)))
            Y = dict(_G(sorted(perm[i] for i in H)))
            X[0], X[k+1] = 0, n+1
            Y[0], Y[k+1] = 0, n+1
            shady = ( X[i] < x < X[i+1] and Y[j] < y < Y[j+1]
                      for (i,j) in R
                      for (x,y) in perm_cart
                      )
            if not any(shady):
                return True
        return False

    def count_occurrences_in(self, perm):
        """Returns the number of occurrences of self in perm"""

        def contains(i, now):
            if len(now) == len(self.perm):
                st = sorted(now)
                x = 0
                for k in perm:
                    if x < len(now) and k == now[x]:
                        x += 1
                    else:
                        y = bisect.bisect_left(st, k)
                        if (x, y) in self.shading:
                            return 0
                return 1

            if i == len(perm):
                return 0

            c = 0
            nxt = now + [perm[i]]
            if (Permutation.to_standard(nxt) ==
                    Permutation.to_standard(self.perm[:len(nxt)])):
                c += contains(i+1, nxt)

            c += contains(i+1, now)
            return c

        return contains(0, [])

    def occurrences_in(self, perm):
        # TODO: Implement all nice
        indices = list(range(len(perm)))
        for candidate_indices in itertools.combinations(indices, len(self)):
            candidate = [perm[i] for i in candidate_indices]
            if Permutation.to_standard(candidate) != self.perm:
                continue
            x = 0
            for i in range(len(perm)):
                e = perm[i]
                if e in candidate:
                    x += 1
                    continue
                y = sum(1 for c in candidate if c < e)
                if (x, y) in self.shading:
                    break
            else:
                # No unused point fell within shading
                yield list(candidate_indices)

    def contained_in(self, perm):
        # TODO: Use occurrences_in
        return self.count_occurrences_in(perm) > 0

    #
    # Methods returning new permutations
    #

    def rotate_right(self):
        return MeshPattern(self.perm.rotate_right(),
                           set([_rot_right(len(self.perm), pos) for pos in
                                self.shading]))

    def shade(self, pos):
        if type(pos) is list:
            pos = set(pos)
        elif type(pos) is not set:
            pos = set([pos])
        return MeshPattern(self.perm, self.shading | pos)

    def sub_mesh(self, positions):
        """
        Returns the mesh pattern given by using only points in positions
        from self.
        positions: 1-based indices of points
        """
        positions = sorted(positions)
        perm = self.perm
        assert(set(positions) <= set(self.perm.perm))

        def is_shaded(left, right, lower, upper):
            for i in range(len(perm)):
                if left < i+1 < right and lower < perm[i] < upper:
                    return False
                if i+1 >= right:
                    break
            for h in range(left, right):
                for v in range(lower, upper):
                    if (h, v) not in self.shading:
                        return False
            return True

            # shades = 0
            # for m in self.shading:
            #     if left <= m[0] < right and lower <= m[1] < upper:
            #         shades += 1
            # return shades == (right - left)*(upper - lower)
            # shades = [m for m in self.shading if left <= m[0] < right and
            #           lower <= m[1] < upper]
            # points = [i for i in range(len(perm)) if left < i+1 < right and
            #           lower < perm[i] < upper]
            # return (len(shades) == (right-left)*(upper-lower) and
            #         points == [])

        nperm = Permutation.to_standard([perm[i-1] for i in positions])
        hor_lines = sorted([0] +
                           [perm[i-1] for i in positions] +
                           [len(perm) + 1])
        ver_lines = sorted([0] + positions + [len(perm) + 1])

        nshading = set()
        for i in range(len(ver_lines)-1):
            for j in range(len(hor_lines)-1):
                if is_shaded(ver_lines[i], ver_lines[i+1],
                             hor_lines[j], hor_lines[j+1]):
                    nshading.add((i, j))

        return MeshPattern(nperm, nshading)

    def add_point(self, pt, shade_dir=DIR_NONE, safe=True):
        """Returns a mesh pattern with a point added in pt.
        If shade_dir is specified adds shading in that direction"""
        x,y = pt
        if safe:
            assert (x, y) not in self.shading

        perm = [v if v < y+1 else v+1 for v in self.perm]
        nperm = perm[:x] + [y+1] + perm[x:]
        nshading = set()
        for (a, b) in self.shading:
            if a < x:
                nx = [a]
            elif a == x:
                nx = [a, a+1]
            else:
                nx = [a+1]

            if b < y:
                ny = [b]
            elif b == y:
                ny = [b, b+1]
            else:
                ny = [b+1]

            for na in nx:
                for nb in ny:
                    nshading.add((na, nb))

        if shade_dir == DIR_EAST:
            nshading.add((x+1, y))
            nshading.add((x+1, y+1))
        elif shade_dir == DIR_NORTH:
            nshading.add((x, y+1))
            nshading.add((x+1, y+1))
        elif shade_dir == DIR_WEST:
            nshading.add((x, y))
            nshading.add((x, y+1))
        elif shade_dir == DIR_SOUTH:
            nshading.add((x, y))
            nshading.add((x+1, y))

        return MeshPattern(Permutation(list(nperm)), nshading)

    def add_increase(self,box):
        x,y = box
        s1 = self.add_point(box)
        return s1.add_point((x+1,y+1))

    def add_decrease(self,box):
        x,y = box
        s1 = self.add_point(box)
        return s1.add_point((x+1,y))

    def complement(self):
        return MeshPattern(self.perm.complement(),
                           [(x, len(self.perm)-y) for (x, y) in self.shading])

    def reverse(self):
        return MeshPattern(self.perm.reverse(),
                           [(len(self.perm)-x, y) for (x, y) in self.shading])

    def inverse(self):
        return MeshPattern(self.perm.flip_diagonal(),
                           [(y, x) for (x, y) in self.shading])

    def flip_horizontal(self):
        """Returns the Mesh Pattern self flipped horizontally"""
        return self.complement()

    def flip_vertical(self):
        """Returns the Mesh Pattern self flipped vertically"""
        return self.reverse()

    def flip_diagonal(self):
        """Returns the Mesh Pattern self flipped along the diagonal, y=x"""
        return self.inverse()

    def flip_antidiagonal(self):
        """Returns the Mesh Pattern self flipped along the
        antidiagonal, y=len(perm)-x"""
        return MeshPattern(self.perm.flip_antidiagonal(),
                           [(len(self.perm)-y, len(self.perm)-x) for (x, y) in
                            self.shading])

    #
    # Other methods
    #

    def non_pointless_boxes(self):
        res = []
        L = self.perm
        for i,v in enumerate(L):
            res.extend([(i+1, v), (i, v), (i, v-1), (i+1, v-1)])
        return set(res)

    def _can_shade(self, pos):
        i, j = pos
        if (i, j) in self.shading:
            return False
        if i-1 < 0 or self.perm[i-1] != j:
            return False
        if (i-1, j-1) in self.shading:
            return False
        c = 0
        if (i, j-1) in self.shading:
            c += 1
        if (i-1, j) in self.shading:
            c += 1
        if c == 2:
            return False
        for l in range(len(self.perm)+1):
            if l == i-1 or l == i:
                continue
            if (l, j-1) in self.shading and (l, j) not in self.shading:
                return False
        for l in range(len(self.perm)+1):
            if l == j-1 or l == j:
                continue
            if (i-1, l) in self.shading and (i, l) not in self.shading:
                return False
        return (i-1, j-1)

    def can_shade(self, pos):
        """Returns whether it is possible to shade the box pos"""
        mp = self
        poss = []
        for i in range(4):
            ans = mp._can_shade(pos)
            if ans:
                for j in range((-i) % 4):
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

        if pos1 in self.shading:
            return False
        if pos2 in self.shading:
            return False
        if (pos1[0]-1, pos1[1]) in self.shading:
            return False
        if (pos2[0]-1, pos2[1]) in self.shading:
            return False
        for y in range(len(self.perm) + 1):
            if y == pos1[1] or y == pos1[1] - 1:
                continue
            if (pos1[0] - 1, y) in self.shading and (pos1[0], y) not in self.shading:
                return False
        for x in range(len(self.perm) + 1):
            if x == pos1[0] or x == pos1[0] - 1:
                continue
            if ((x, pos1[1]) in self.shading) != ((x, pos2[1]) in self.shading):
                return False
        return (pos1[0]-1, pos1[1]-1)

    def can_shade2(self, pos1, pos2):
        """Returns if it is possible to shade pos1 and pos2"""
        mp = self
        poss = []
        for i in range(4):
            ans = mp._can_shade2(pos1, pos2)
            if ans:
                for j in range((-i) % 4):
                    ans = _rot_right(len(self.perm)-1, ans)
                poss.append(ans[1]+1)
            mp = mp.rotate_right()
            pos1 = _rot_right(len(self.perm), pos1)
            pos2 = _rot_right(len(self.perm), pos2)
        return poss

    def rank(self):
        res = 0
        for (x, y) in self.shading:
            res |= 1 << (x * (len(self.perm)+1) + y)
        return res

    def latex(self,scale=0.3):
        """Returns the LaTeX code for the TikZ figure of the mesh pattern. The
        LaTeX code requires the TikZ library 'patterns'.
        """

        return ("\\raisebox{{0.6ex}}{{\n"
        "\\begin{{tikzpicture}}[baseline=(current bounding box.center),scale={0}]\n"
        "\\useasboundingbox (0.0,-0.1) rectangle ({1}+1.4,{1}+1.1);\n"
        "\\foreach \\x/\\y in {{{3}}}\n"
        "  \\fill[pattern color = black!65, pattern=north east lines] (\\x,\\y) rectangle +(1,1);\n"
        "\\draw (0.01,0.01) grid ({1}+0.99,{1}+0.99);\n"
        "\\foreach [count=\\x] \\y in {{{2}}}\n"
        "  \\filldraw (\\x,\\y) circle (6pt);\n"
        "\\end{{tikzpicture}}}}").format(
                scale, len(self.perm), ','.join(map(str, self.perm)),
                ','.join(["{}/{}".format(p[0],p[1]) for p in self.shading]))

    #
    # Static methods
    #

    @staticmethod
    def unrank(perm, x):
        shading = set()
        for i in range(len(perm)+1):
            for j in range(len(perm)+1):
                if (x & (1 << (i*(len(perm)+1)+j))) != 0:
                    shading.add((i, j))
        return MeshPattern(perm, shading)

    #
    # Dunder methods
    #

    def __eq__(self, other):
        if type(other) is not MeshPattern:
            return False
        return self.perm == other.perm and self.shading == other.shading

    def __hash__(self):
        return hash((self.perm, tuple(sorted(self.shading))))

    def __repr__(self):
        representation = ["MeshPattern("]
        representation.append(super(MeshPattern, self).__repr__())
        representation.append(", ")
        representation.append(repr(self.shading))
        representation.append(")")
        return "".join(representation)

    def __str__(self):
        n = len(self.perm)
        arr = [[((str(n-(i-1)//2) if n < 10 else 'o') if self.perm[(j-1)/2] == n-(i-1)//2 else '+') if j % 2 != 0 and i % 2 != 0 else '|' if j % 2 != 0 else '-' if i % 2 != 0 else ('#' if ((j-1)/2+1, n-(i-1)/2-1) in self.shading else ' ') for j in range(2*n+1)] for i in range(2*n+1)]
        return '\n'.join(''.join(line) for line in arr)

#
# Orphan functions
#

def _rot_right(n, pos):
    x, y = pos
    assert 0 <= x < n+1
    assert 0 <= y < n+1
    return (y, n-x)

def _G(seq):
    return zip(range(1, len(seq)+1), seq)

def contained_in_many_shadings(clpatt, Rs, perm):
    k = len(clpatt)
    n = len(perm)

    perm_cart = set(_G(perm))

    for H in clpatt.occurrences_in(perm):
        X = dict(_G(sorted(i+1 for i in H)))
        Y = dict(_G(sorted(perm[i] for i in H)))
        X[0], X[k+1] = 0, n+1
        Y[0], Y[k+1] = 0, n+1
        for R in Rs:
            shady = ( X[i] < x < X[i+1] and Y[j] < y < Y[j+1]
                      for (i,j) in R
                      for (x,y) in perm_cart
                      )
            if not any(shady):
                return True
    return False
