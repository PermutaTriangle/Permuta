import bisect
import itertools
import numbers
import collections
import sys

from permuta import Permutation, Pattern, Rotatable, Shiftable, Flippable
from permuta.misc import DIR_EAST, DIR_NORTH, DIR_WEST, DIR_SOUTH, DIR_NONE

if sys.version_info.major == 2:
    range = xrange


MeshPatternBase = collections.namedtuple("MeshPatternBase",
                                         ["pattern", "shading"])


class MeshPattern(MeshPatternBase, Pattern, Rotatable, Shiftable, Flippable):
    """A mesh pattern class."""

    def __new__(cls, pattern=Permutation(), shading=frozenset(), check=False):
        # TODO: Tests, took into having shading be a sorted tuple of coordinates
        if not isinstance(pattern, Permutation):
            pattern = Permutation(pattern, check=check)
        if not isinstance(shading, frozenset):
            shading = frozenset(shading)
        return super(MeshPattern, cls).__new__(cls, pattern, shading)

    def __init__(self, pattern=None, shading=None, check=False):
        # TODO: Docstring, tests
        if check:
            # TODO: Add exception messages
            assert isinstance(self.shading, collections.Set)
            for coordinate in self.shading:
                assert isinstance(coordinate, tuple)
                assert len(coordinate) == 2
                x, y = coordinate
                assert isinstance(x, numbers.Integral)
                assert 0 <= x <= len(self.pattern)
                assert isinstance(y, numbers.Integral)
                assert 0 <= y <= len(self.pattern)

    #
    # Methods returning new permutations
    #

    def complement(self):
        # TODO: Docstring, tests
        return MeshPattern(self.pattern.complement(),
                           [(x, len(self.pattern)-y) for (x, y) in self.shading])

    def reverse(self):
        # TODO: Docstring, tests
        return MeshPattern(self.pattern.reverse(),
                           [(len(self.pattern)-x, y) for (x, y) in self.shading])

    def inverse(self):
        # TODO: Docstring, tests
        return MeshPattern(self.pattern.inverse(),
                           [(y, x) for (x, y) in self.shading])

    def sub_mesh_pattern(self, indices):
        """Return the mesh pattern induced by indices.

        Args:
            self:
                A mesh pattern.
            indices: <collections.Iterable> of <numbers.Integral>
                A list of unique indices of elements in self.

        Returns: permuta.MeshPattern
            A mesh pattern where the pattern is the permutation induced by the
            indices and a region is shaded if and only if the corresponding
            region of self is fully shaded.
        """
        indices = sorted(indices)
        if not indices:
            return MeshPattern()
        pattern = Permutation.to_standard(self.pattern[index] for index in indices)
        vertical = [0]
        vertical.extend(index + 1 for index in indices)
        vertical.append(len(self) + 1)
        horizontal = [0]
        horizontal.extend(sorted(self.pattern[index] for index in indices))
        horizontal.append(len(self) + 1)
        shading = frozenset((x, y)
                            for x in range(len(pattern) + 1)
                            for y in range(len(pattern) + 1)
                            if self.is_shaded((vertical[x],
                                               horizontal[y]),
                                              (vertical[x+1] - 1,
                                               horizontal[y+1] - 1)))
        return MeshPattern(pattern, shading)

    def _rotate_right(self):
        """Return self rotated 90 degrees to the right."""
        return MeshPattern(self.pattern.rotate(),
                           set([_rotate_right(len(self.pattern), coordinate)
                                for coordinate in self.shading]))

    def _rotate_left(self):
        """Return self rotated 90 degrees to the left."""
        return MeshPattern(self.pattern.rotate(3),
                           set([_rotate_left(len(self.pattern), coordinate)
                                for coordinate in self.shading]))

    def _rotate_180(self):
        """Return self rotated 180 degrees."""
        return MeshPattern(self.pattern.rotate(2),
                           set([_rotate_180(len(self.pattern), coordinate)
                                for coordinate in self.shading]))

    def flip_horizontal(self):
        """Return self flipped horizontally."""
        # TODO: Tests
        return self.complement()

    def flip_vertical(self):
        """Return self flipped vertically."""
        # TODO: Tests
        return self.reverse()

    def flip_diagonal(self):
        """Return self flipped along the diagonal."""
        # TODO: Tests
        return self.inverse()

    def flip_antidiagonal(self):
        """Return self flipped along the antidiagonal."""
        # TODO: Tests
        return MeshPattern(self.pattern.flip_antidiagonal(),
                           [(len(self.pattern)-y, len(self.pattern)-x)
                            for (x, y) in self.shading])

    def shade(self, pos):
        # TODO: Review, tests
        if type(pos) is list:
            pos = set(pos)
        elif type(pos) is not set:
            pos = set([pos])
        return MeshPattern(self.pattern, self.shading | pos)

    def add_point(self, pt, shade_dir=DIR_NONE, safe=True):
        # TODO: Review, tests
        """Returns a mesh pattern with a point added in pt.
        If shade_dir is specified adds shading in that direction"""
        x,y = pt
        if safe:
            assert (x, y) not in self.shading

        perm = [v if v < y+1 else v+1 for v in self.pattern]
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
        # TODO: Review, tests
        x,y = box
        s1 = self.add_point(box)
        return s1.add_point((x+1,y+1))

    def add_decrease(self,box):
        # TODO: Review, tests
        x,y = box
        s1 = self.add_point(box)
        return s1.add_point((x+1,y))

    #
    # Occurrence/Avoidance/Containment methods
    #

    def occurrences_in(self, perm):
        """Find all indices of occurrences of self in perm.

        Args:
            self:
                The mesh pattern whose occurrences are to be found.
            perm: permuta.Permutation
                The permutation to search for occurrences in.

        Yields: [int]
            The indices of the occurrences of self in perm. Each yielded element
            l is a list of integer indices of the permutation perm such that
            self.pattern == permuta.Permutation.to_standard([perm[i] for i in l])
            and that no element not in the occurrence falls within self.shading.
        """
        # TODO: Implement all nice
        indices = list(range(len(perm)))
        for candidate_indices in itertools.combinations(indices, len(self)):
            candidate = [perm[index] for index in candidate_indices]
            if Permutation.to_standard(candidate) != self.pattern:
                continue
            x = 0
            for element in perm:
                if element in candidate:
                    x += 1
                    continue
                y = sum(1 for candidate_element in candidate
                        if candidate_element < element)
                if (x, y) in self.shading:
                    break
            else:
                # No unused point fell within shading
                yield list(candidate_indices)

    #
    # Other methods
    #

    def is_shaded(self, lower_left, upper_right=None):
        """Check if a region of the grid is shaded.

        Args:
            self:
                A mesh pattern.
            lower_left: (int, int)
                A shading coordinate of self.
            upper_right: (int, int)
                A shading coordinate of self.

        Returns: bool
            If upper_right is None, then True if and only if lower_left is
            shaded; otherwise, True if and only if all regions (x, y)
            for x in the range lower_left[0] to upper_right[0] (inclusive) and
            for y in the range lower_left[1] to upper_right[1] (inclusive) are
            shaded.
        """
        if upper_right is None:
            return lower_left in self.shading
        else:
            left, lower = lower_left
            right, upper = upper_right
            for x in range(left, right+1):
                for y in range(lower, upper+1):
                    if (x, y) not in self.shading:
                        return False
            return True

    def non_pointless_boxes(self):
        # TODO: Review, tests
        res = []
        L = self.pattern
        for i,v in enumerate(L):
            res.extend([(i+1, v), (i, v), (i, v-1), (i+1, v-1)])
        return set(res)

    def _can_shade(self, pos):
        # TODO: Review, tests?
        i, j = pos
        if (i, j) in self.shading:
            return False
        if i-1 < 0 or self.pattern[i-1] != j:
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
        for l in range(len(self.pattern)+1):
            if l == i-1 or l == i:
                continue
            if (l, j-1) in self.shading and (l, j) not in self.shading:
                return False
        for l in range(len(self.pattern)+1):
            if l == j-1 or l == j:
                continue
            if (i-1, l) in self.shading and (i, l) not in self.shading:
                return False
        return (i-1, j-1)

    def can_shade(self, pos):
        """Returns whether it is possible to shade the box pos"""
        # TODO: Review, tests?
        mp = self
        poss = []
        for i in range(4):
            ans = mp._can_shade(pos)
            if ans:
                for j in range((-i) % 4):
                    ans = _rot_right(len(self.pattern)-1, ans)
                poss.append(ans[1]+1)
            mp = mp.rotate_right()
            pos = _rot_right(len(self.pattern), pos)
        return poss

    def _can_shade2(self, pos1, pos2):
        # TODO: Review, tests?
        if pos1[1] < pos2[1]:
            pos1, pos2 = pos2, pos1
        if pos1[0] == 0 or self.pattern[pos1[0]-1] != pos1[1]:
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
        for y in range(len(self.pattern) + 1):
            if y == pos1[1] or y == pos1[1] - 1:
                continue
            if (pos1[0] - 1, y) in self.shading and (pos1[0], y) not in self.shading:
                return False
        for x in range(len(self.pattern) + 1):
            if x == pos1[0] or x == pos1[0] - 1:
                continue
            if ((x, pos1[1]) in self.shading) != ((x, pos2[1]) in self.shading):
                return False
        return (pos1[0]-1, pos1[1]-1)

    def can_shade2(self, pos1, pos2):
        """Returns if it is possible to shade pos1 and pos2"""
        # TODO: Review, tests?
        mp = self
        poss = []
        for i in range(4):
            ans = mp._can_shade2(pos1, pos2)
            if ans:
                for j in range((-i) % 4):
                    ans = _rot_right(len(self.pattern)-1, ans)
                poss.append(ans[1]+1)
            mp = mp.rotate_right()
            pos1 = _rot_right(len(self.pattern), pos1)
            pos2 = _rot_right(len(self.pattern), pos2)
        return poss

    def rank(self):
        # TODO: Review, tests
        res = 0
        for (x, y) in self.shading:
            res |= 1 << (x * (len(self.pattern)+1) + y)
        return res

    def latex(self,scale=0.3):
        """Returns the LaTeX code for the TikZ figure of the mesh pattern. The
        LaTeX code requires the TikZ library 'patterns'.
        """
        # TODO: Review
        return ("\\raisebox{{0.6ex}}{{\n"
        "\\begin{{tikzpicture}}[baseline=(current bounding box.center),scale={0}]\n"
        "\\useasboundingbox (0.0,-0.1) rectangle ({1}+1.4,{1}+1.1);\n"
        "\\foreach \\x/\\y in {{{3}}}\n"
        "  \\fill[pattern color = black!65, pattern=north east lines] (\\x,\\y) rectangle +(1,1);\n"
        "\\draw (0.01,0.01) grid ({1}+0.99,{1}+0.99);\n"
        "\\foreach [count=\\x] \\y in {{{2}}}\n"
        "  \\filldraw (\\x,\\y) circle (6pt);\n"
        "\\end{{tikzpicture}}}}").format(scale,
                                         len(self.pattern),
                                         ','.join(map(str, self.pattern)),
                                         ','.join(["{}/{}".format(p[0],p[1])
                                                   for p in self.shading]))

    #
    # Static methods
    #

    @staticmethod
    def unrank(pattern, number):
        """Return the number-th shading of pattern."""
        assert isinstance(pattern, Permutation)
        assert isinstance(number, numbers.Integral)
        assert 0 <= number < 2**((len(pattern) + 1)**2)
        bound = len(pattern)
        x = 0
        y = 0
        shading = set()
        while number != 0:
            if number % 2 == 1:
                shading.add((x, y))
            number //= 2
            if y == bound:
                x += 1
                y = 0
            else:
                y += 1
        return MeshPattern(pattern, shading)

    #
    # Dunder methods
    #

    def __repr__(self):
        return "MeshPattern({self.pattern}, {self.shading})".format(self=self)

    def __str__(self):
        result = []
        for line_number in range(2*len(self), -1, -1):
            if line_number % 2 == 0:
                # The regions defined by, and the columns of, the mesh grid
                y = line_number//2
                for x in range(len(self) + 1):
                    if (x, y) in self.shading:
                        result.append("#")
                    else:
                        result.append(" ")
                    result.append("|")
                else:
                    # Remove extra "|"
                    result.pop()
            else:
                # The rows of the mesh grid
                row_index = line_number//2
                for column_index in range(0, len(self)):
                    if self.pattern[column_index] == row_index+1:
                        result.append("-")
                        if len(self) > 9:
                            result.append("o")
                        else:
                            result.append(str(self.pattern[column_index]))
                    else:
                        result.append("-+")
                else:
                    result.append("-")
            result.append("\n")
        else:
            # Remove extra "\n"
            result.pop()
        return "".join(result)

    def __len__(self):
        return len(self.pattern)

    def __bool__(self):
        return (bool(self.pattern) or bool(self.shading))

    if sys.version_info.major == 2:
        __nonzero__ = __bool__

    def __contains__(self, other):
        # TODO: Review, tests
        # TODO: is subshading of mesh pattern?
        # other in self
        raise NotImplementedError

#
# Private helper functions
#

def _rotate_right(length, element):
    """Rotate an element of the Cartesian product of {0,...,length} right."""
    x, y = element
    return (y, length - x)

def _rotate_left(length, element):
    """Rotate an element of the Cartesian product of {0,...,length} left."""
    x, y = element
    return (length - y, x)

def _rotate_180(length, element):
    """Rotate an element of the Cartesian product of {0,...,length} 180 degrees."""
    x, y = element
    return (length - x, length - y)

def _G(seq):
    # TODO: Review
    return zip(range(1, len(seq)+1), seq)

def contained_in_many_shadings(clpatt, Rs, perm):
    # TODO: Review
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
