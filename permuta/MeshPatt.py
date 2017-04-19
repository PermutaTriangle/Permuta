import collections
import itertools
import numbers
import random
import sys

from permuta import Perm, PermSet
from permuta.interfaces import Patt, Rotatable, Shiftable, Flippable
from permuta.misc import DIR_EAST, DIR_NORTH, DIR_WEST, DIR_SOUTH, DIR_NONE

MeshPatternBase = collections.namedtuple("MeshPatternBase",
                                         ["pattern", "shading"])

class MeshPatt(MeshPatternBase, Patt, Rotatable, Shiftable, Flippable):
    """A mesh pattern class.

    Attributes:
        pattern: <permuta.Perm>
            The underlying classical pattern.
        shading: frozenset
            The shading as a immutable set of coordinates, with lower-left as
            origin.
    """

    def __new__(cls, pattern=Perm(), shading=frozenset()):
        """Return a MeshPatt instance.

        Args:
            cls:
                The class of which an instance is requested.
            pattern: <permuta.Perm> or <collections.Iterable>
                An perm or an iterable corresponding to a legal perm.
            shading: <collections.Iterable>
                An iterable of 2-tuples.
        Raises:
            TypeError:
                Bad argument type.
            ValueError:
                Bad argument, but correct type.
        """
        if not isinstance(pattern, Perm):
            pattern = Perm(pattern)
        if not isinstance(shading, frozenset):
            shading = frozenset(shading)
        return super(MeshPatt, cls).__new__(cls, pattern, shading)

    def __init__(self, pattern=Perm(), shading=frozenset()):
        for coordinate in self.shading:
            if not isinstance(coordinate, tuple):
                message = "'{}' object is not a tuple".format(repr(coordinate))
                raise TypeError(message)
            if len(coordinate) != 2:
                message = "Element is not a shading coordinate: '{}'".format(repr(coordinate))
                raise ValueError(message)
            x, y = coordinate
            if not isinstance(x, numbers.Integral):
                message = "'{}' object is not an integer".format(repr(x))
                raise TypeError(message)
            if not isinstance(y, numbers.Integral):
                message = "'{}' object is not an integer".format(repr(y))
                raise TypeError(message)
            if (not 0 <= x <= len(self.pattern)) or (not 0 <= y <= len(self.pattern)):
                message = "Element out of range: '{}'".format(coordinate)
                raise ValueError(message)

    #
    # Methods returning new permutations
    #

    def complement(self):
        """Returns the complement of the mesh pattern, which has the complement
        of the underlying pattern and every shading flipped across the
        horizontal axis.

        Returns: <permuta.MeshPatt>
            The complement of the meshpatt.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).complement()
            MeshPatt(Perm((0,)), frozenset({(0, 0)}))
            >>> MeshPatt(Perm((0, 2, 1)), frozenset({(0, 1), (0, 0), (1, 0), (0, 2), (0, 3)})).complement()
            MeshPatt(Perm((2, 0, 1)), frozenset({(0, 1), (1, 3), (0, 0), (0, 3), (0, 2)}))
        """
        return MeshPatt(self.pattern.complement(),
                           [(x, len(self)-y) for (x, y) in self.shading])

    def reverse(self):
        """Returns the reversed mesh patterns, which has the underlying pattern
        reversed and every shading flipped across the vertical axis.

        Returns: <permuta.MeshPatt>
            The meshpatt reversed.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).reverse()
            MeshPatt(Perm((0,)), frozenset({(1, 1)}))
            >>> MeshPatt(Perm((2, 1, 0)), frozenset({(3, 2), (3, 3), (0, 2), (2, 2), (1, 1)})).reverse()
            MeshPatt(Perm((0, 1, 2)), frozenset({(1, 2), (3, 2), (2, 1), (0, 3), (0, 2)}))
        """
        return MeshPatt(self.pattern.reverse(),
                           [(len(self)-x, y) for (x, y) in self.shading])


    def inverse(self):
        """Returns the inverse of the meshpatt, that is the meshpatt with the
        underlying classical pattern as the inverse and the shadings hold the
        same relation between the points. This is equivalent to flipping the
        pattern over the diagonal.

        Returns: <permuta.MeshPatt>
            The 'inverse' of the meshpatt.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).inverse()
            MeshPatt(Perm((0,)), frozenset({(1, 0)}))
        """
        return MeshPatt(self.pattern.inverse(),
                           [(y, x) for (x, y) in self.shading])

    def sub_mesh_pattern(self, indices):
        """Return the mesh pattern induced by indices.

        Args:
            indices: <collections.Iterable> of <numbers.Integral>
                A list of unique indices of elements in self.

        Returns: <permuta.MeshPattern>
            A mesh pattern where the pattern is the permutation induced by the
            indices and a region is shaded if and only if the corresponding
            region of self is fully shaded.

        Exampes:
            >>> shading = frozenset({(3, 2), (1, 3), (4, 2), (0, 3), (1, 2), (4, 3), (3, 4), (4, 1)})
            >>> MeshPatt(Perm((3, 2, 1, 0)), shading).sub_mesh_pattern((0, 1, 3))
            MeshPatt(Perm((2, 1, 0)), frozenset({(1, 2), (3, 2), (3, 1), (0, 2)}))
            >>> MeshPatt(Perm((2, 3, 1, 0)), shading).sub_mesh_pattern((1, 2, 3))
            MeshPatt(Perm((2, 1, 0)), frozenset({(3, 2), (3, 1), (2, 3)}))
        """
        indices = sorted(indices)
        if not indices:
            return MeshPatt()
        pattern = Perm.to_standard(self.pattern[index] for index in indices)
        vertical = [0]
        vertical.extend(index + 1 for index in indices)
        vertical.append(len(self) + 1)
        horizontal = [0]
        horizontal.extend(sorted(self.pattern[index] + 1 for index in indices))
        horizontal.append(len(self) + 1)
        shading = frozenset((x, y)
                            for x in range(len(pattern) + 1)
                            for y in range(len(pattern) + 1)
                            if self.is_shaded((vertical[x],
                                               horizontal[y]),
                                              (vertical[x + 1] - 1,
                                               horizontal[y + 1] - 1))
                            and self.is_pointfree((vertical[x],
                                               horizontal[y]),
                                              (vertical[x + 1] - 1,
                                               horizontal[y + 1] - 1)))
        return MeshPatt(pattern, shading)

    def flip_horizontal(self):
        """Return self flipped horizontally which is equivalent to the
        complement.

        Returns: <permuta.MeshPatt>
            The complement of the meshpatt.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).flip_horizontal()
            MeshPatt(Perm((0,)), frozenset({(0, 0)}))
            >>> MeshPatt(Perm((0, 2, 1)), frozenset({(0, 1), (0, 0), (1, 0), (0, 2), (0, 3)})).flip_horizontal()
            MeshPatt(Perm((2, 0, 1)), frozenset({(0, 1), (1, 3), (0, 0), (0, 3), (0, 2)}))
        """
        return self.complement()

    def flip_vertical(self):
        """Return self flipped vertically which is equivalent to the
        meshpatt reversed.

        Returns: <permuta.MeshPatt>
            The meshpatt reversed.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).flip_vertical()
            MeshPatt(Perm((0,)), frozenset({(1, 1)}))
            >>> MeshPatt(Perm((2, 1, 0)), frozenset({(3, 2), (3, 3), (0, 2), (2, 2), (1, 1)})).flip_vertical()
            MeshPatt(Perm((0, 1, 2)), frozenset({(1, 2), (3, 2), (2, 1), (0, 3), (0, 2)}))
        """
        return self.reverse()

    def flip_diagonal(self):
        """Return self flipped along the diagonal which is equivalent to the
        'inverse' of the pattern.

        Returns: <permuta.MeshPatt>
            The 'inverse' of the meshpatt.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).inverse()
            MeshPatt(Perm((0,)), frozenset({(1, 0)}))
        """
        return self.inverse()

    def _rotate_right(self):
        """Return the pattern rotated 90 degrees to the right.

        Returns: <permuta.MeshPatt>
            The meshpatt rotated 90 degrees to the right.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1), (1, 1)}))._rotate_right()
            MeshPatt(Perm((0,)), frozenset({(1, 0), (1, 1)}))
        """
        return MeshPatt(self.pattern.rotate(),
                           set([_rotate_right(len(self.pattern), coordinate)
                                for coordinate in self.shading]))

    def _rotate_left(self):
        """Return the pattern rotated 90 degrees to the left.

        Returns: <permuta.MeshPatt>
            The meshpatt rotated 90 degrees to the left.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1), (1, 1)}))._rotate_left()
            MeshPatt(Perm((0,)), frozenset({(0, 1), (0, 0)}))
        """
        return MeshPatt(self.pattern.rotate(3),
                           set([_rotate_left(len(self.pattern), coordinate)
                                for coordinate in self.shading]))

    def _rotate_180(self):
        """Return the pattern rotated 180 degrees.

        Returns: <permuta.MeshPatt>
            The meshpatt rotated 180 degrees.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1), (1, 1)}))._rotate_180()
            MeshPatt(Perm((0,)), frozenset({(1, 0), (0, 0)}))
        """
        return MeshPatt(self.pattern.rotate(2),
                           set([_rotate_180(len(self.pattern), coordinate)
                                for coordinate in self.shading]))

    def all_symmetries(self):
        """Return the set of all symmetries of the mesh pattern.

        Returns: <set>
            All the symmetries of a mesh pattern.
        """
        symmetries = set()
        current = self
        symmetries.add(current)
        symmetries.add(current.inverse())
        for i in range(3):
            current = current._rotate_left()
            symmetries.add(current)
            symmetries.add(current.inverse())
        return symmetries


    def shade(self, positions):
        """Returns the mesh pattern with the added shadings given by positions.

        Args:
            positions: tuple or <collections.Iterable>
                The shading given as a single coordinate or as an iterable of
                coordinates.

        Raises:
            ValueError:
                Bad argument, but correct type.

        Returns: <permuta.MeshPatt>
            The new meshpatt with the added shadings.
        """
        if isinstance(positions, tuple):
            if len(positions) == 0:
                message = "Element is not a valid shading coordinate: '{}'".format(positions)
                raise ValueError(message)
            if isinstance(positions[0], numbers.Integral):
                positions = set([positions])
        positions = set(positions)

        return MeshPatt(self.pattern, self.shading | positions)

    def add_point(self, pos, shade_dir=DIR_NONE, safe=True):
        """Returns a mesh pattern with a point added in the box at position pos.  If shade_dir is
        specified adds shading in that direction.

        Args:
            pos: tuple
                Coordinates corresponding to a box in the pattern.
            shade_dir: int
                The direction which to shade within the box.
            safe: bool, optional
                True to check if box must not be shaded.

        Raises:
            ValueError:
                Bad box argument, if it is already shaded.
            TypeError:
                Bad argument type.

        Returns: <permuta.MeshPatt>
            The mesh pattern with a point added in pos.
        """
        x,y = pos
        if not isinstance(x, numbers.Integral) or not isinstance(y, numbers.Integral):
            message = "Element is not a tuple of integers: '{}'".format(pos)
            raise TypeError(message)
        if safe and (x, y) in self.shading:
            message = "Can not add point to shaded pos: '{}'"
            raise ValueError(message)

        perm = [v if v < y else (v + 1) for v in self.pattern]
        nperm = perm[:x] + [y] + perm[x:]
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

        return MeshPatt(Perm(nperm), nshading)

    def add_increase(self, pos):
        """Adds an increasing pattern (0, 1) into the given coordinate.

        Args:
            pos: tuple
                The coordinate of the position to insert (0, 1) into.

        Returns: <permuta.MeshPatt>
            The new pattern with the increased pattern inserted into pos.

        Examples:
            >>> MeshPatt((0,)).add_increase((0, 0))
            MeshPatt(Perm((0, 1, 2)), frozenset())
            >>> MeshPatt((0, 1, 2), [(1, 0), (2, 1), (3, 2)]).add_increase((2, 0))
            MeshPatt(Perm((2, 3, 0, 1, 4)), frozenset({(1, 2), (5, 4), (3, 3), (2, 3), (4, 3), (1, 0), (1, 1)}))
        """
        x, y = pos
        return self.add_point((x, y)).add_point((x + 1,y + 1))

    def add_decrease(self, pos):
        """Adds an decreasing pattern (1, 0) into the given coordinate.

        Args:
            pos: tuple
                The coordinate of the position to insert (1, 0) into.

        Returns: <permuta.MeshPatt>
            The new pattern with the decreasing pattern inserted into pos.

        Examples:
            >>> MeshPatt((0,)).add_decrease((0, 0))
            MeshPatt(Perm((1, 0, 2)), frozenset())
            >>> MeshPatt((0, 1, 2), [(1, 0), (2, 1), (3, 2)]).add_decrease((2, 0))
            MeshPatt(Perm((2, 3, 1, 0, 4)), frozenset({(1, 2), (5, 4), (3, 3), (2, 3), (4, 3), (1, 0), (1, 1)}))
        """
        x, y = pos
        return self.add_point((x, y)).add_point((x + 1, y))

    #
    # Occurrence/Avoidance/Containment methods
    #

    def occurrences_in(self, perm):
        """Find all indices of occurrences of self in perm.

        Args:
            self:
                The mesh pattern whose occurrences are to be found.
            perm: <permuta.Perm>
                The permutation to search for occurrences in.

        Yields: numbers.Integral
            The indices of the occurrences of self in perm. Each yielded
            element l is a list of integer indices of the permutation perm such
            that self.pattern == permuta.Perm.to_standard([perm[i] for i in l])
            and that no element not in the occurrence falls within
            self.shading.
        """
        # TODO: Implement all nice
        indices = list(range(len(perm)))
        for candidate_indices in self.pattern.occurrences_in(perm):
            candidate = [perm[index] for index in candidate_indices]
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

        Raises:
            ValueError:
                Bad argument, but correct type.

        Returns: bool
            If upper_right is None, then True if and only if lower_left is
            shaded; otherwise, True if and only if all regions (x, y) for x in
            the range lower_left[0] to upper_right[0] (inclusive) and for y in
            the range lower_left[1] to upper_right[1] (inclusive) are shaded.
        """
        if ((lower_left[0] < 0 or lower_left[1] < 0)
                or (lower_left[0] > len(self) or lower_left[1] > len(self))):
            message = "Element out of range: '{}'".format(lower_left)
            raise ValueError(message)
        elif upper_right is None:
            return lower_left in self.shading
        elif ((upper_right[0] < 0 or upper_right[1] < 0)
                or (upper_right[0] > len(self) or upper_right[1] > len(self))):
            message = "Element out of range: '{}'".format(upper_right)
            raise ValueError(message)
        elif lower_left[0] > upper_right[0] or lower_left[1] > upper_right[1]:
            message = "Elements do not correspond to lower left and upper right of a non-empty rectangle: '{}' '{}'".format(lower_left, upper_right)
            raise ValueError(message)
        else:
            left, lower = lower_left
            right, upper = upper_right
            for x in range(left, right + 1):
                for y in range(lower, upper + 1):
                    if (x, y) not in self.shading:
                        return False
            return True

    def is_pointfree(self, lower_left, upper_right):
        """Check if a region in the grid has no points.

        Args:
            self:
                A mesh pattern.
            lower_left: (int, int)
                A point coordinate of self.
            upper_right: (int, int)
                A point coordinate of self.

        Raises:
            ValueError:
                Bad argument, but correct type.

        Returns: bool
            True if and only if all points self[x] for x in the range
            lower_left[0] + 1 to upper_right[0] - 1 (inclusive) have values
            less than lower_left[1] or greater than or equal to upper_right[1].
        """
        if ((lower_left[0] < 0 or lower_left[1] < 0)
                or (lower_left[0] > len(self) or lower_left[1] > len(self))):
            message = "Element out of range: '{}'".format(lower_left)
            raise ValueError(message)
        elif ((upper_right[0] < 0 or upper_right[1] < 0)
                or (upper_right[0] > len(self) or upper_right[1] > len(self))):
            message = "Element out of range: '{}'".format(upper_right)
            raise ValueError(message)
        elif lower_left[0] > upper_right[0] or lower_left[1] > upper_right[1]:
            message = "Elements do not correspond to lower left and upper right of a non-empty rectangle: '{}' '{}'".format(lower_left, upper_right)
            raise ValueError(message)
        else:
            left, lower = lower_left
            right, upper = upper_right
            for x in range(left, right):
                if lower <= self.pattern[x] < upper:
                    return False
        return True


    def _can_shade(self, pos):
        """Checks if the box at pos can be shaded according to the Shading
        Lemma(northeast).

        Args:
            pos: tuple
                The coordinates of the box to check.

        Returns: tuple
            The point that is 'moved' to shade the box at pos.
        """
        i, j = pos
        # if pos is shaded
        if (i, j) in self.shading:
            return False
        # if pos does not have point in lower-left
        if i - 1 < 0 or self.pattern[i - 1] != j - 1:
            return False
        # if box in south-west direction is shaded
        if (i - 1, j - 1) in self.shading:
            return False
        c = 0
        # only one of the boxes to the left and down can be shaded
        if (i, j-1) in self.shading:
            c += 1
        if (i-1, j) in self.shading:
            c += 1
        if c == 2:
            return False

        # if the box on the lower side of the horizontal line is shaded then
        # the upper one must be shaded
        for l in range(len(self.pattern)+1):
            if l == i - 1 or l == i:
                continue
            if (l, j - 1) in self.shading and (l, j) not in self.shading:
                return False
        # if the box on the left side of the vertical line is shaded then the
        # right one must be shaded
        for l in range(len(self.pattern)+1):
            if l == j-1 or l == j:
                continue
            if (i-1, l) in self.shading and (i, l) not in self.shading:
                return False
        return (i-1, j-1)

    def can_shade(self, pos):
        """Returns whether it is possible to shade the box at position pos
        according to the Shading Lemma. Every direction is checked and the list
        of the values of the adjacent points to the box that can be used is
        returned.

        Args:
            pos: tuple
                The position of the box to check.

        Returns: list
            The values of the points in the permutation adjacent to the box at
            pos that can be used to shade the box.

        Examples:
            >>> MeshPatt((0,),[(0, 0)]).can_shade((1, 1))
            []
            >>> MeshPatt((1, 2, 0), [(2,2),(3,0),(3,2),(3,3)]).can_shade((1, 2))
            [1, 2]
        """
        mp = self
        poss = []
        for i in range(4):
            ans = mp._can_shade(pos)
            if ans:
                for j in range((-i) % 4):
                    ans = _rotate_right(len(self.pattern)-1, ans)
                poss.append(ans[1])
            mp = mp.rotate_right()
            pos = _rotate_right(len(self.pattern), pos)
        return poss

    def _can_simul_shade(self, pos1, pos2):
        if pos1[1] < pos2[1]:
            pos1, pos2 = pos2, pos1
        # There must be a point at (pos1[0]-1, pos1[1]-1)
        if pos1[0] == 0 or self.pattern[pos1[0] - 1] != pos1[1] - 1:
            return False
        if pos1[0] != pos2[0] or pos1[1] - 1 != pos2[1]:
            # the pos1 must be directly above pos2
            return False

        if pos1 in self.shading:
            return False
        if pos2 in self.shading:
            return False
        # The boxes surrounding the point (pos1[0]-1, pos1[1] - 1) must be
        # empty
        if (pos1[0]-1, pos1[1]) in self.shading:
            return False
        if (pos2[0]-1, pos2[1]) in self.shading:
            return False

        # Check the boxes on each side of the vertical line of pos1[0], if the
        # box on the left side is shaded then the box on the right side must be
        # shaded.
        for y in range(len(self.pattern) + 1):
            if y == pos1[1] or y == pos1[1] - 1:
                continue
            if (pos1[0] - 1, y) in self.shading and (pos1[0], y) not in self.shading:
                return False

        # Check the boxes on each side of the horizontal line of pos1[1]-1,
        # they must match.
        for x in range(len(self.pattern) + 1):
            if x == pos1[0] or x == pos1[0] - 1:
                continue
            if ((x, pos1[1]) in self.shading) != ((x, pos2[1]) in self.shading):
                return False
        return (pos1[0] - 1, pos1[1] - 1)

    def can_simul_shade(self, pos1, pos2):
        """Returns whether it is possible to shade the boxes at positions pos1,
        pos2 according to the Shading Lemma. Every direction is checked and the
        list of the values of the adjacent points to the box that can be used
        is returned.

        Args:
            pos1: tuple
                The position of the first box to check.
            pos2: tuple
                The position of the second box to check.

        Returns: list
            The values of the points in the permutation adjacent to the boxes at
            pos1 and pos2 that can be used to shade the box.

        Examples:

        """
        mp = self
        poss = []
        for i in range(4):
            ans = mp._can_simul_shade(pos1, pos2)
            if ans:
                for j in range((-i) % 4):
                    ans = _rotate_right(len(self.pattern) - 1, ans)
                poss.append(ans[1])
            mp = mp.rotate_right()
            pos1 = _rotate_right(len(self.pattern), pos1)
            pos2 = _rotate_right(len(self.pattern), pos2)
        return poss

    can_shade2 = can_simul_shade

    def shadable_boxes(self):
        """Returns a dictionary of all tuples of shadable boxes with the
        shading lemma, with the keys as the points used to shade the tuples of
        boxes.

        Returns: dict
            Dictionary with keys as points and values as tuples of boxes.

        Examples:
        >>> dict(MeshPatt(Perm((0, 3, 1, 2)), frozenset({(3, 2), (3, 0), (4, 2), (1, 0), (0, 3), (1, 2), (2, 0), (0, 4), (0, 2)})).shadable_boxes())
        {0: [((0, 0),)], 3: [((1, 3),), ((1, 3), (1, 4)), ((1, 4),)], 1: [((2, 2),)]}

        """
        shadable = collections.defaultdict(list)
        for i in range(len(self) + 1):
            for j in range(len(self) + 1):
                points = self.can_shade((i,j))
                for p in points:
                    shadable[p].append(((i,j),))
                if i < len(self):
                    points = self.can_simul_shade((i,j), (i+1,j))
                    for p in points:
                        shadable[p].append(((i,j), (i+1,j)))
                if j < len(self):
                    points = self.can_simul_shade((i,j), (i, j+1))
                    for p in points:
                        shadable[p].append(((i,j), (i,j+1)))
        return shadable

    def non_pointless_boxes(self):
        """ Returns the coordinates of the boxes that have a point on their
        boundaries in one of their four corners.

        Returns: set
            The set of boxes with points in one of the corners.

        Examples:
            >>> MeshPatt(Perm((0, 1)), frozenset({(0, 1), (2, 0), (0, 2)})).non_pointless_boxes()
            {(0, 1), (1, 2), (0, 0), (2, 1), (2, 2), (1, 0), (1, 1)}
            >>> MeshPatt(Perm((1, 0, 2)), frozenset({(1, 3), (3, 0), (0, 3), (0, 1), (1, 2), (3, 1), (2, 0), (1, 1)})).non_pointless_boxes()
            {(1, 2), (0, 1), (3, 2), (3, 3), (0, 2), (2, 1), (2, 0), (2, 3), (2, 2), (1, 0), (1, 1)}
        """
        res = []
        for i,v in enumerate(self.pattern):
            res.extend([(i + 1, v + 1), (i, v + 1), (i, v), (i + 1, v)])
        return set(res)

    def has_anchored_point(self):
        """Checks if the mesh pattern has any point anchored to the boundary.
        Returns a tuple (right, top, left, bottom) where each value represent
        whether the point is anchored to the corresponding direction.

        Returns: tuple
            Each boolean in the tuple tells whether the mesh pattern is anchored to the corresponding direction.

        Examples:
            >>> MeshPatt(Perm((0, 1)), frozenset({(0, 0), (1, 0), (2, 0), (1, 1)})).has_anchored_point()
            (False, False, False, True)
        """


        right = all((len(self),i) in self.shading for i in range(len(self) + 1))
        top = all((i,len(self)) in self.shading for i in range(len(self) + 1))
        left = all((0,i) in self.shading for i in range(len(self) + 1))
        bottom = all((i,0) in self.shading for i in range(len(self) + 1))
        return (right, top, left, bottom)

    def rank(self):
        """Computes the rank of the mesh pattern, the bit string of the
        shadings interpreted as an integer.

        Returns: numbers.Integral
            The rank of the mesh pattern.

        Examples:
            >>> rank = MeshPatt(Perm((1, 0, 2)), frozenset({(0, 0), (3, 0), (0, 2), (2, 1), (2, 3), (1, 2), (3, 3), (3, 1), (1, 1)})).rank()
            >>> rank
            47717
            >>> bin(rank)
            '0b1011101001100101'
        """
        res = 0
        for (x, y) in self.shading:
            res |= 1 << (x * (len(self.pattern)+1) + y)
        return res

    def latex(self,scale=0.3): # pragma: no cover
        """Returns the LaTeX code for the TikZ figure of the mesh pattern. The
        LaTeX code requires the TikZ library 'patterns'.

        Args:
            scale: <numbers.Real>
                The scale of the image.

        Returns: str
            The LaTeX code for the TikZ figure of the pattern.
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
        """Return the number-th shading of pattern.

        Args:
            pattern: <permuta.Perm> or <collections.Iterable>
                An perm or an iterable corresponding to a legal perm.
            number: <numbers.Integral>
                An integer of which binary representation corresponds to a
                legal shading.
        Raises:
            TypeError:
                Bad argument type.
            ValueError:
                Bad argument, but correct type.
        Examples:
            >>> bin(22563)
            '0b101100000100011'
            >>> MeshPatt.unrank((0, 1, 2), 22563)
            MeshPatt(Perm((0, 1, 2)), frozenset({(0, 1), (3, 2), (0, 0), (3, 0), (2, 3), (1, 1)}))
        """
        if not isinstance(number, numbers.Integral):
            message = "'{}' object is not an integer".format(repr(number))
            raise TypeError(message)
        if not (0 <= number < 2**((len(pattern) + 1)**2)):
            message = "Element out of range: '{}'".format(number)
            raise ValueError(message)
        bound = len(pattern) + 1
        shading = set((index // bound, index % bound)
                for index, bit in enumerate(reversed(bin(number)[2:])) if bit == '1')
        return MeshPatt(pattern, shading)

    @staticmethod
    def random(length):
        """Return a random mesh pattern of the specified length.

        Args:
            length: <numbers.Integral>
                The length of the random pattern.

        Examples:
            >>> MeshPatt.random(1) in set(MeshPatt.unrank(Perm((0)), i) for i in range(0, 16))
            True
            >>> len(MeshPatt.random(4))
            4
        """
        return MeshPatt.unrank(Perm.random(length),
                random.randint(0, 2**((length + 1)**2) - 1))

    #
    # Dunder methods
    #

    def __repr__(self): # pragma: no cover
        return "MeshPatt({self.pattern}, {self.shading})".format(self=self)

    def __str__(self): # pragma: no cover
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
                    if self.pattern[column_index] == row_index:
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
        return bool(self.pattern) or bool(self.shading)

def _rotate_right(length, element):
    """Rotate an element of the Cartesian product of {0,...,length} clockwise.

    Args:
        length: <numbers.Integral>
            The size of the area(of mesh).
        element: tuple
            A cartesiean coordinate within [0,...,length]x[0,...,length]

    Returns: tuple
        The input point rotated within the box of size length x length.
    """
    x, y = element
    return (y, length - x)

def _rotate_left(length, element):
    """Rotate an element of the Cartesian product of {0,...,length}
    counterclockwise.

    Args:
        length: <numbers.Integral>
            The size of the area(of mesh).
        element: tuple
            A cartesiean coordinate within [0,...,length]x[0,...,length]

    Returns: tuple
        The input point rotated within the box of size length x length.
    """
    x, y = element
    return (length - y, x)

def _rotate_180(length, element):
    """Rotate an element of the Cartesian product of {0,...,length}
    180-degrees.

    Args:
        length: <numbers.Integral>
            The size of the area(of mesh).
        element: tuple
            A cartesiean coordinate within [0,...,length]x[0,...,length]

    Returns: tuple
        The input point rotated within the box of size length x length.
    """
    x, y = element
    return (length - x, length - y)

def gen_meshpatts(length, patt = None):
    """Generates all mesh patterns of length n. If the classical pattern is
    specified then only the mesh patterns with the classical pattern as the
    underlying pattern are generated.

    Args:
        length: <numbers.Integral>
            The length(size) of the mesh pattern.
        patt: <permutation.Permutation>, <numbers.Integral> or <collections.Iterable>

    Yields: <permuta.MeshPatt>
        Every permutation of the specified length with the specified classical
        pattern or each of them if the pattern is not specified.

    Examples:
        >>> list(gen_meshpatts(0))
        [MeshPatt(Perm(()), frozenset()), MeshPatt(Perm(()), frozenset({(0, 0)}))]
        >>> len(list(gen_meshpatts(2, (1, 2))))
        512
    """
    if patt is None:
        for p in PermSet(length):
            for i in range(2**((length + 1)**2)):
                yield MeshPatt.unrank(p, i)
    else:
        if not isinstance(patt, Perm):
            patt = Perm(patt)
        for i in range(2**((length + 1)**2)):
            yield MeshPatt.unrank(patt, i)
