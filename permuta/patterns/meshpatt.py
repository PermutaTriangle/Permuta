# pylint: disable=too-many-public-methods

import collections
import random
from itertools import chain, cycle, islice
from typing import (
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

from ..misc import DIR_EAST, DIR_NONE, DIR_NORTH, DIR_SOUTH, DIR_WEST, HTMLViewer
from .patt import Patt
from .perm import Perm


class MeshPatt(Patt):
    """A mesh pattern class."""

    def __init__(
        self, pattern: Perm = Perm(), shading: Iterable[Tuple[int, int]] = frozenset()
    ):
        self.pattern = pattern
        self.shading = shading if isinstance(shading, frozenset) else frozenset(shading)

        assert all(
            isinstance(coordinate, tuple)
            and len(coordinate) == 2
            and isinstance(coordinate[0], int)
            and isinstance(coordinate[1], int)
            and 0 <= coordinate[0] <= len(self.pattern)
            and 0 <= coordinate[1] <= len(self.pattern)
            for coordinate in self.shading
        )

    @classmethod
    def unrank(cls, pattern: Perm, number: int) -> "MeshPatt":
        """Return the number-th shading of pattern.

        Examples:
            >>> bin(22563)
            '0b101100000100011'
            >>> MeshPatt.unrank(Perm((0, 1, 2)), 386)
            MeshPatt(Perm((0, 1, 2)), [(0, 1), (1, 3), (2, 0)])
        """
        assert 0 <= number < 2 ** ((len(pattern) + 1) ** 2)
        bound = len(pattern) + 1
        shading = (
            divmod(index, bound)
            for index, bit in enumerate(reversed(bin(number)[2:]))
            if bit == "1"
        )
        return cls(pattern, shading)

    @classmethod
    def random(cls, length: int) -> "MeshPatt":
        """Return a random mesh pattern of the specified length.

        Examples:
            >>> mp = set(MeshPatt.unrank(Perm((0, )), i) for i in range(0, 16))
            >>> MeshPatt.random(1) in mp
            True
            >>> len(MeshPatt.random(4))
            4
        """
        return cls.unrank(
            Perm.random(length), random.randint(0, 2 ** ((length + 1) ** 2) - 1)
        )

    @classmethod
    def of_length(
        cls, length: int, patt: Optional[Perm] = None
    ) -> Iterator["MeshPatt"]:
        """Generates all mesh patterns of length n. If the classical pattern is
        specified then only the mesh patterns with the classical pattern as the
        underlying pattern are generated.

        Examples:
            >>> mps = list(MeshPatt.of_length(0))
            >>> len(mps)
            2
            >>> mps[0]
            MeshPatt(Perm(()), [])
            >>> mps[1]
            MeshPatt(Perm(()), [(0, 0)])
            >>> len(list(MeshPatt.of_length(2, Perm((1, 2)))))
            512
        """
        if patt is None:
            for perm in Perm.of_length(length):
                for i in range(2 ** ((length + 1) ** 2)):
                    yield MeshPatt.unrank(perm, i)
        else:
            assert isinstance(patt, Perm)
            for i in range(2 ** ((length + 1) ** 2)):
                yield MeshPatt.unrank(patt, i)

    def get_perm(self) -> "Perm":
        """Returns the permutation part of the pattern.

        Examples:
            >>> MeshPatt(Perm((2, 0, 1)), [(0, 0), (0, 1), (0, 2)]).get_perm()
            Perm((2, 0, 1))
        """
        return self.pattern

    def complement(self) -> "MeshPatt":
        """Returns the complement of the mesh pattern, which has the complement
        of the underlying pattern and every shading flipped across the
        horizontal axis.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).complement()
            MeshPatt(Perm((0,)), [(0, 0)])
            >>> MeshPatt(Perm((0, 2, 1)),
            ... frozenset({(0, 1), (0, 2), (0, 3)})).complement()
            MeshPatt(Perm((2, 0, 1)), [(0, 0), (0, 1), (0, 2)])
        """
        n = len(self)
        return MeshPatt(
            self.pattern.complement(), ((x, n - y) for (x, y) in self.shading)
        )

    def reverse(self) -> "MeshPatt":
        """Returns the reversed mesh patterns, which has the underlying pattern
        reversed and every shading flipped across the vertical axis.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).reverse()
            MeshPatt(Perm((0,)), [(1, 1)])
            >>> MeshPatt(Perm((2, 1, 0)),
            ... frozenset({(3, 2), (2, 2), (1, 1)})).reverse()
            MeshPatt(Perm((0, 1, 2)), [(0, 2), (1, 2), (2, 1)])
        """
        n = len(self)
        return MeshPatt(self.pattern.reverse(), ((n - x, y) for (x, y) in self.shading))

    def inverse(self) -> "MeshPatt":
        """Returns the inverse of the meshpatt, that is the meshpatt with the
        underlying classical pattern as the inverse and the shadings hold the
        same relation between the points. This is equivalent to flipping the
        pattern over the diagonal.

        Examples:
            >>> MeshPatt(Perm((0,)), frozenset({(0, 1)})).inverse()
            MeshPatt(Perm((0,)), [(1, 0)])
        """
        return MeshPatt(self.pattern.inverse(), ((y, x) for (x, y) in self.shading))

    def sub_mesh_pattern(self, indices: Iterable[int]) -> "MeshPatt":
        """Return the mesh pattern induced by unique indices where the pattern is
        the permutation induced by the indices and a region is shaded if and only
        if the corresponding region of self is fully shaded.

        Exampes:
            >>> shading = frozenset({(3, 2), (1, 3), (4, 2), (0, 3), (1, 2),
            ... (4, 3)})
            >>> MeshPatt(Perm((3, 2, 1, 0)),
            ... shading).sub_mesh_pattern((0, 1, 3))
            MeshPatt(Perm((2, 1, 0)), [(0, 2), (1, 2), (3, 2)])
            >>> MeshPatt(Perm((2, 3, 1, 0)),
            ... shading).sub_mesh_pattern((1, 2, 3))
            MeshPatt(Perm((2, 1, 0)), [(3, 2)])
        """
        indices = sorted(indices)
        if not indices:
            return MeshPatt()
        n = len(self)
        pattern = Perm.to_standard(self.pattern[index] for index in indices)
        vertical = [0]
        vertical.extend(index + 1 for index in indices)
        vertical.append(n + 1)
        horizontal = [0]
        horizontal.extend(sorted(self.pattern[index] + 1 for index in indices))
        horizontal.append(n + 1)
        shading = frozenset(
            (x, y)
            for x in range(len(pattern) + 1)
            for y in range(len(pattern) + 1)
            if (
                self.is_shaded(
                    (vertical[x], horizontal[y]),
                    (vertical[x + 1] - 1, horizontal[y + 1] - 1),
                )
                and self.is_pointfree(
                    (vertical[x], horizontal[y]),
                    (vertical[x + 1] - 1, horizontal[y + 1] - 1),
                )
            )
        )
        return MeshPatt(pattern, shading)

    flip_horizontal = complement
    flip_vertical = reverse
    flip_diagonal = inverse

    def rotate(self, times: int = 1) -> "MeshPatt":
        """Rotate the mesh pattern. The parameter determines how often it is rotated.
        A negative value rotates it to the left.

        Exampes:
        >>> MeshPatt(Perm((0, 2, 1)), [(2, 3), (3, 0), (3, 3)]).rotate(-3)
        MeshPatt(Perm((2, 0, 1)), [(0, 0), (3, 0), (3, 1)])
        >>> MeshPatt(Perm((0, 2, 1)), [(2, 3), (3, 0), (3, 3)]).rotate(-2)
        MeshPatt(Perm((1, 0, 2)), [(0, 0), (0, 3), (1, 0)])
        >>> MeshPatt(Perm((0, 2, 1)), [(2, 3), (3, 0), (3, 3)]).rotate(-1)
        MeshPatt(Perm((1, 2, 0)), [(0, 2), (0, 3), (3, 3)])
        >>> MeshPatt(Perm((0, 2, 1)), [(2, 3), (3, 0), (3, 3)]).rotate(0)
        MeshPatt(Perm((0, 2, 1)), [(2, 3), (3, 0), (3, 3)])
        >>> MeshPatt(Perm((0, 2, 1)), [(2, 3), (3, 0), (3, 3)]).rotate(1)
        MeshPatt(Perm((2, 0, 1)), [(0, 0), (3, 0), (3, 1)])
        >>> MeshPatt(Perm((0, 2, 1)), [(2, 3), (3, 0), (3, 3)]).rotate(2)
        MeshPatt(Perm((1, 0, 2)), [(0, 0), (0, 3), (1, 0)])
        >>> MeshPatt(Perm((0, 2, 1)), [(2, 3), (3, 0), (3, 3)]).rotate(3)
        MeshPatt(Perm((1, 2, 0)), [(0, 2), (0, 3), (3, 3)])
        """
        times = times % 4
        if times == 0:
            return self
        n, perm = len(self), self.pattern.rotate(times)
        if times == 1:
            return MeshPatt(perm, ((y, n - x) for x, y in self.shading))
        if times == 2:
            return MeshPatt(perm, ((n - x, n - y) for x, y in self.shading))
        return MeshPatt(perm, ((n - y, x) for x, y in self.shading))

    def all_syms(self) -> Tuple["MeshPatt", ...]:
        """Return the set of all symmetries of the mesh pattern.

        Exampes:
        >>> p = MeshPatt(Perm((0, 1)), [(0, 1), (1, 1)])
        >>> print("\\n".join(repr(s) for s in sorted(p.all_syms())))
        MeshPatt(Perm((0, 1)), [(0, 1), (1, 1)])
        MeshPatt(Perm((0, 1)), [(1, 0), (1, 1)])
        MeshPatt(Perm((0, 1)), [(1, 1), (1, 2)])
        MeshPatt(Perm((0, 1)), [(1, 1), (2, 1)])
        MeshPatt(Perm((1, 0)), [(0, 1), (1, 1)])
        MeshPatt(Perm((1, 0)), [(1, 0), (1, 1)])
        MeshPatt(Perm((1, 0)), [(1, 1), (1, 2)])
        MeshPatt(Perm((1, 0)), [(1, 1), (2, 1)])
        """
        current, symmetries = self, {self, self.inverse()}
        for _ in range(3):
            current = current.rotate()
            symmetries.update((current, current.inverse()))
        return tuple(symmetries)

    def shade(self, *positions: Tuple[int, int]) -> "MeshPatt":
        """Returns the mesh pattern with the added shadings given by positions.

        Exampes:
        >>> MeshPatt(Perm((0, 1)), [(0, 1)]).shade((1, 1))
        MeshPatt(Perm((0, 1)), [(0, 1), (1, 1)])
        >>> MeshPatt(Perm((0, 1)), [(0, 1)]).shade((1, 1), (1, 0))
        MeshPatt(Perm((0, 1)), [(0, 1), (1, 0), (1, 1)])
        """
        return MeshPatt(self.pattern, self.shading | set(positions))

    def add_point(self, pos: Tuple[int, int], shade_dir: int = DIR_NONE) -> "MeshPatt":
        """Returns a mesh pattern with a point added in the box at position
        pos. If shade_dir is specified adds shading in that direction.

        Exampes:
        >>> MeshPatt().add_point((0, 0))
        MeshPatt(Perm((0,)), [])
        >>> p = MeshPatt(Perm((0, 1, 2)), [(1, 0), (2, 1), (3, 2)])
        >>> p.add_point((2, 0), shade_dir=DIR_SOUTH)
        MeshPatt(Perm((1, 2, 0, 3)), [(1, 0), (1, 1), (2, 0), (2, 2), (3, 0), (3, 2), \
(4, 3)])
        """
        assert pos not in self.shading
        x, y = pos
        new_shading = self._add_point_base_shading(x, y)
        if shade_dir == DIR_EAST:
            new_shading.update(((x + 1, y), (x + 1, y + 1)))
        elif shade_dir == DIR_NORTH:
            new_shading.update(((x, y + 1), (x + 1, y + 1)))
        elif shade_dir == DIR_WEST:
            new_shading.update(((x, y), (x, y + 1)))
        elif shade_dir == DIR_SOUTH:
            new_shading.update(((x, y), (x + 1, y)))
        return MeshPatt(self._add_point_new_perm(x, y), new_shading)

    def _add_point_base_shading(self, x: int, y: int) -> Set[Tuple[int, int]]:
        new_shading = set()
        for s_x, s_y in self.shading:
            new_xs, new_ys = [], []
            if s_x <= x:
                new_xs.append(s_x)
            if s_x >= x:
                new_xs.append(s_x + 1)
            if s_y <= y:
                new_ys.append(s_y)
            if s_y >= y:
                new_ys.append(s_y + 1)
            for new_x in new_xs:
                for new_y in new_ys:
                    new_shading.add((new_x, new_y))
        return new_shading

    def _add_point_new_perm(self, x: int, y: int) -> Perm:
        iterator = iter(self.pattern)
        return Perm(
            chain(
                (val if val < y else (val + 1) for val in islice(iterator, x)),
                (y,),
                (val if val < y else (val + 1) for val in iterator),
            )
        )

    def add_increase(self, pos: Tuple[int, int]) -> "MeshPatt":
        """Adds an increasing pattern (0, 1) into the given coordinate.

        Returns: <permuta.MeshPatt>
            The new pattern with the increased pattern inserted into pos.

        Examples:
            >>> MeshPatt(Perm((0,))).add_increase((0, 0))
            MeshPatt(Perm((0, 1, 2)), [])
        """
        x, y = pos
        return self.add_point((x, y)).add_point((x + 1, y + 1))

    def add_decrease(self, pos: Tuple[int, int]) -> "MeshPatt":
        """Adds an decreasing pattern (1, 0) into the given coordinate.

        Examples:
            >>> MeshPatt(Perm((0,))).add_decrease((0, 0))
            MeshPatt(Perm((1, 0, 2)), [])
        """
        x, y = pos
        return self.add_point((x, y)).add_point((x + 1, y))

    def contains(self, *patts: Patt) -> bool:
        """Check if self contains all provided patterns.

        Examples:
            >>> MeshPatt(Perm((0,)), [(0, 1)]).contains(MeshPatt(Perm((0,)), [(0, 0)]))
            False
            >>> MeshPatt(Perm((0,)), [(0, 1)]).contains(MeshPatt(Perm((0,)), []))
            True
        """
        return all(patt in self for patt in patts)

    def avoids(self, *patts: Patt) -> bool:
        """Check if self avoids all provided patterns.

        Examples:
            >>> MeshPatt(Perm((0,)), [(0, 0)]).avoids(MeshPatt(Perm((0,)), [(0, 1)]))
            True
            >>> MeshPatt(Perm((0,)), []).avoids(MeshPatt(Perm((0,)), [(0, 1)]))
            True
            >>> MeshPatt(Perm((0,)), [(0, 1)]).avoids(MeshPatt(Perm((0,)), [(0, 0)]))
            True
            >>> MeshPatt(Perm((0,)), [(0, 1)]).avoids(MeshPatt(Perm((0,)), []))
            False
        """
        return all(patt not in self for patt in patts)

    def occurrences_in(self, patt: Patt, *args, **kwargs) -> Iterator[Tuple[int, ...]]:
        """
        Find all indices of self in patt. Each yielded element is a tuple of integer
        indices of the pattern such that

            Classical pattern:
                Occurrence of instance's perm in patt if no elements land
                in shaded region.

            Mesh pattern:
                Occurrences of instances's perm in the pattern's perm is found, and if
                the sub mesh pattern formed by the occurrence indices is a superset of
                the instance shading, they are included.

        Example:
            >>> mp = MeshPatt(Perm((1, 0, 2)), [(1, 2), (2, 2), (2, 3)])
            >>> p = Perm((3, 1, 0, 2, 4))
            >>> sorted(mp.occurrences_in(p))
            [(0, 1, 4), (0, 2, 4), (0, 3, 4), (1, 2, 3)]
            >>> mp2 = MeshPatt(p, [(0,0), (0,1), (0,2), (1,4), (2,4), (3,3), (3,4),
            ... (3,5), (4,0), (4,3), (4,4), (4,5), (5,0)])
            >>> sorted(mp.occurrences_in(mp2))
            [(0, 2, 4), (0, 3, 4)]
        """
        assert isinstance(patt, (Perm, MeshPatt))
        if isinstance(patt, Perm):
            yield from self._occurrences_in_perm(patt)
        else:
            yield from self._occurrences_in_mesh(patt)

    def _occurrences_in_mesh(self, patt) -> Iterator[Tuple[int, ...]]:
        return (
            occurrence
            for occurrence in self.occurrences_in(patt.pattern)
            if self.shading <= patt.sub_mesh_pattern(occurrence).shading
        )

    def _occurrences_in_perm(self, patt: Perm) -> Iterator[Tuple[int, ...]]:
        for candidate_indices in self.pattern.occurrences_in(patt):
            candidate = [patt[index] for index in candidate_indices]
            x = 0
            for element in patt:
                if element in candidate:
                    x += 1
                    continue
                y = sum(
                    1 for candidate_element in candidate if candidate_element < element
                )
                if (x, y) in self.shading:
                    break
            else:
                yield tuple(candidate_indices)

    def is_shaded(
        self, lower_left: Tuple[int, int], upper_right: Optional[Tuple[int, int]] = None
    ) -> bool:
        """Check if a region of the grid is shaded. If a single point is provided, we
        only check that point. Otherwise we check the rectangle formed by the points.

        Example:
            >>> MeshPatt(Perm((3, 2, 1, 0)), [(0, 0), (0, 1), (0, 2)]).is_shaded((0, 1))
            True
            >>> MeshPatt(Perm((3, 2, 1, 0)), [(0, 0), (0, 1), (0, 2)]).is_shaded((1, 0))
            False
            >>> MeshPatt(Perm((3, 2, 1, 0)), [(0, 0), (0, 1), (1, 1)]).is_shaded(
            ... (0, 0), (1, 1))
            False
            >>> MeshPatt(Perm((3, 2, 1, 0)), [(0, 0), (0, 1), (1, 1), (1, 2), (2, 1),
            ... (2, 2)]).is_shaded((1, 1), (2, 2))
            True
        """
        assert all(0 <= pos <= len(self) for pos in lower_left)
        if upper_right is None:
            return lower_left in self.shading
        assert (
            all(0 <= pos <= len(self) for pos in upper_right)
            and lower_left[0] <= upper_right[0]
            and lower_left[1] <= upper_right[1]
        )
        (left, lower), (right, upper) = lower_left, upper_right
        return all(
            (x, y) in self.shading
            for y in range(lower, upper + 1)
            for x in range(left, right + 1)
        )

    def is_pointfree(
        self, lower_left: Tuple[int, int], upper_right: Tuple[int, int]
    ) -> bool:
        """Check if a the rectangular region defined by the points has any points.

        Examples:
            >>> MeshPatt.random(10).is_pointfree((0, 0), (10, 10))
            False
            >>> MeshPatt(Perm((4, 0, 1, 2, 3))).is_pointfree((0, 2), (2, 3))
            True
        """
        assert (
            all(0 <= pos <= len(self) for pos in (*lower_left, *upper_right))
            and lower_left[0] <= upper_right[0]
            and lower_left[1] <= upper_right[1]
        )
        (left, lower), (right, upper) = lower_left, upper_right
        return not any(lower <= self.pattern[idx] < upper for idx in range(left, right))

    def can_shade(self, pos: Tuple[int, int]) -> List[int]:
        """If it is possible to shade box at provided position according to the shading
        lemma, we return a list of the values of the adjacent points to the box that
        can be used. If not, an empty list is returned.

        Examples:
            >>> MeshPatt(Perm((0,)),[(0, 0)]).can_shade((1, 1))
            []
            >>> MeshPatt(Perm((1, 2, 0)),
            ... [(2, 2),(3, 0),(3, 2),(3, 3)]).can_shade((1, 2))
            [1, 2]
        """
        n, m_patt, positions = len(self), self, []
        # Rotate everything and check NE conditions
        for rot in range(4):
            if m_patt.north_east_shading_lemma_conditions(pos):
                ans = pos[0] - 1, pos[1] - 1
                for _ in range((-rot) % 4):
                    ans = ans[1], n - 1 - ans[0]
                positions.append(ans[1])
            m_patt = m_patt.rotate()
            pos = pos[1], n - pos[0]
        return positions

    def north_east_shading_lemma_conditions(self, pos: Tuple[int, int]) -> bool:
        """Checks if a box at provided position to the northeast of a point satisfies
        the shading lemma's conditions.

        Examples:
            >>> MeshPatt(Perm((0,))).north_east_shading_lemma_conditions((0, 0))
            False
            >>> MeshPatt(Perm((0,))).north_east_shading_lemma_conditions((1, 1))
            True
        """
        x, y = pos
        return not any(
            (
                # if pos is shaded
                (x, y) in self.shading,
                # if pos does not have point in lower-left
                x - 1 < 0 or self.pattern[x - 1] != y - 1,
                # if box in south-west direction is shaded
                (x - 1, y - 1) in self.shading,
                # only one of the boxes to the left and down can be shaded
                all(((x, y - 1) in self.shading, (x - 1, y) in self.shading)),
                # if the box on the lower side of the horizontal line
                # is shaded then the upper one must be shaded
                any(
                    (n_x, y - 1) in self.shading and (n_x, y) not in self.shading
                    for n_x in range(len(self.pattern) + 1)
                    if n_x not in (x - 1, x)
                ),
                # if the box on the left side of the vertical line
                # is shaded then the right one must be shaded
                any(
                    (x - 1, n_y) in self.shading and (x, n_y) not in self.shading
                    for n_y in range(len(self.pattern) + 1)
                    if n_y not in (y - 1, y)
                ),
            )
        )

    def can_simul_shade(
        self, pos1: Tuple[int, int], pos2: Tuple[int, int]
    ) -> List[int]:
        """Returns whether it is possible to shade the boxes at positions pos1,
        pos2 according to the Shading Lemma. Every direction is checked and the
        list of the values of the adjacent points to the box that can be used
        is returned.

        Examples:
            >>> MeshPatt(Perm((0, 2, 1))).can_simul_shade((1, 1), (1, 0))
            [0]
            >>> MeshPatt(Perm((0, 2, 1))).can_simul_shade((3, 2), (3, 1))
            [1]
            >>> MeshPatt(Perm((0, 2, 1))).can_simul_shade((2, 3), (2, 2))
            [2]
            >>> MeshPatt(Perm((0, 2, 1))).can_simul_shade((1, 1), (2, 1))
            []
        """
        n, m_patt, positions = len(self), self, []
        for i in range(4):
            if pos1[1] < pos2[1]:
                pos1, pos2 = pos2, pos1
            if m_patt.north_east_simul_shading_lemma_conditions(pos1, pos2):
                ans = (pos1[0] - 1, pos1[1] - 1)
                for _ in range((-i) % 4):
                    ans = ans[1], n - 1 - ans[0]
                positions.append(ans[1])
            m_patt = m_patt.rotate()
            pos1, pos2 = (pos1[1], n - pos1[0]), (pos2[1], n - pos2[0])
        return positions

    can_shade2 = can_simul_shade

    def north_east_simul_shading_lemma_conditions(
        self, pos1: Tuple[int, int], pos2: Tuple[int, int]
    ) -> bool:
        """Checks if two boxes at provided positions, where pos1 is assumed to be above
        pos2 and to the northeast of a point, satisfy the shading lemma's conditions.

        Examples:
            >>> MeshPatt((0,2,1)).north_east_simul_shading_lemma_conditions((1,1),(1,0))
            True
            >>> MeshPatt((0,2,1)).north_east_simul_shading_lemma_conditions((2,3),(2,2))
            True
            >>> MeshPatt((0,2,1)).north_east_simul_shading_lemma_conditions((3,2),(3,1))
            True
            >>> MeshPatt((0,2,1)).north_east_simul_shading_lemma_conditions((3,3),(3,2))
            False
            >>> MeshPatt((0,2,1)).north_east_simul_shading_lemma_conditions((3,1),(3,0))
            False
        """
        assert pos1[1] >= pos2[1]
        return not any(
            (
                # There must be a point at (pos1[0]-1, pos1[1]-1)
                pos1[0] == 0 or self.pattern[pos1[0] - 1] != pos1[1] - 1,
                # The pos1 must be directly above pos2
                pos1[0] != pos2[0] or pos1[1] - 1 != pos2[1],
                # Either is shaded
                pos1 in self.shading or pos2 in self.shading,
                # The boxes surrounding the point (pos1[0]-1, pos1[1] - 1) must be empty
                (
                    (pos1[0] - 1, pos1[1]) in self.shading
                    or (pos2[0] - 1, pos2[1]) in self.shading
                ),
                # Check the boxes on each side of the vertical line of pos1[0], if the
                # box on the left side is shaded then the box on the right side must be
                # shaded.
                any(
                    (
                        (pos1[0] - 1, y) in self.shading
                        and (pos1[0], y) not in self.shading
                    )
                    for y in range(len(self.pattern) + 1)
                    if y not in (pos1[1], pos1[1] - 1)
                ),
                # Check the boxes on each side of the horizontal line of pos1[1]-1,
                # they must match.
                any(
                    ((x, pos1[1]) in self.shading) != ((x, pos2[1]) in self.shading)
                    for x in range(len(self.pattern) + 1)
                    if x not in (pos1[0], pos1[0] - 1)
                ),
            )
        )

    def shadable_boxes(
        self,
    ) -> Dict[
        int,
        List[Union[Tuple[Tuple[int, int]], Tuple[Tuple[int, int], Tuple[int, int]]]],
    ]:
        """Returns a dictionary of all tuples of shadable boxes with the
        shading lemma, with the keys as the points used to shade the tuples of
        boxes.

        Examples:
        >>> sh = {(3, 2), (3, 0), (4, 2), (1, 0), (0, 3), (1, 2), (0, 4),
        ... (0, 2)}
        >>> m = MeshPatt(Perm((0, 3, 1, 2)), sh)
        >>> dict(m.shadable_boxes())
        {0: [((0, 0),)], 3: [((1, 3),), ((1, 3), (1, 4)), ((1, 4),)]}
        """
        shadable: Dict[
            int,
            List[
                Union[Tuple[Tuple[int, int]], Tuple[Tuple[int, int], Tuple[int, int]]]
            ],
        ] = collections.defaultdict(list)
        n = len(self)
        for x in range(n + 1):
            for y in range(n + 1):
                for pnt in self.can_shade((x, y)):
                    shadable[pnt].append(((x, y),))
                if x < n:
                    for pnt in self.can_simul_shade((x, y), (x + 1, y)):
                        shadable[pnt].append(((x, y), (x + 1, y)))
                if y < n:
                    for pnt in self.can_simul_shade((x, y), (x, y + 1)):
                        shadable[pnt].append(((x, y), (x, y + 1)))
        return shadable

    def non_pointless_boxes(self) -> Set[Tuple[int, int]]:
        """Returns the coordinates of the boxes that have a point on their
        boundaries in one of their four corners.

        Examples:
            >>> m = MeshPatt(Perm((0, 1)), frozenset({(0, 1), (2, 0), (0, 2)}))
            >>> sorted(m.non_pointless_boxes())
            [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]
        """
        return {
            pos
            for idx, val in enumerate(self.pattern)
            for pos in ((idx + 1, val + 1), (idx, val + 1), (idx, val), (idx + 1, val))
        }

    def has_anchored_point(self) -> Tuple[bool, bool, bool, bool]:
        """Checks if the mesh pattern has any point anchored to the boundary.
        Returns a tuple (right, top, left, bottom) where each value represent
        whether the point is anchored to the corresponding direction.

        Examples:
            >>> m = MeshPatt(Perm((0, 1)), {(0, 0), (1, 0), (2, 0), (1, 1)})
            >>> m.has_anchored_point()
            (False, False, False, True)
        """
        n = len(self)
        right = all((n, i) in self.shading for i in range(n + 1))
        top = all((i, n) in self.shading for i in range(n + 1))
        left = all((0, i) in self.shading for i in range(n + 1))
        bottom = all((i, 0) in self.shading for i in range(n + 1))
        return (right, top, left, bottom)

    def rank(self) -> int:
        """Computes the rank of the mesh pattern, the bit string of the
        shadings interpreted as an integer.

        Examples:
            >>> sh = {(0, 0), (3, 0), (0, 2), (2, 1), (2, 3), (1, 2), (3, 3),
            ... (3, 1), (1, 1)}
            >>> m = MeshPatt(Perm((1, 0, 2)), sh)
            >>> rank = m.rank()
            >>> rank
            47717
            >>> bin(rank)
            '0b1011101001100101'
        """
        n, res = len(self), 0
        for (x, y) in self.shading:
            res |= 1 << (x * (n + 1) + y)
        return res

    def ascii_plot(self, cell_size: int = 1) -> str:
        """Return an ascii plot of the given Mesh pattern.

        Examples:
            >>> print(MeshPatt(Perm((0,1,2)), [(2,1), (3,0), (3,1), (3,2), (3,3)]
            ...     ).ascii_plot())
             | | |▒
            -+-+-●-
             | | |▒
            -+-●-+-
             | |▒|▒
            -●-+-+-
             | | |▒
        """

        def roundrobin(*iterables: Iterable[str]) -> Iterable[str]:
            # Recipe credited to George Sakkis
            nexts = cycle(iter(it).__next__ for it in iterables)
            for _ in range(2):
                try:
                    for nxt in nexts:
                        yield nxt()
                except StopIteration:
                    nexts = cycle(islice(nexts, 1))

        def fill_char(char: Tuple[int, int]) -> str:
            if char in self.shading:
                return "\u2592"
            if char[0] == n:
                return ""
            return " "

        assert cell_size >= 1
        n = len(self)
        array = [["+" for i in range(n)] for j in range(n)]
        for idx, val in enumerate(self.pattern):
            array[val][idx] = "\u25cf"
        lines = (
            ("-" * cell_size).join([""] + line + [""]) + "\n"
            for line in reversed(array)
        )
        vlines = (
            ("|".join(fill_char((j, i)) * cell_size for j in range(n + 1)) + "\n")
            * cell_size
            for i in range(n, -1, -1)
        )
        return "".join(roundrobin(vlines, lines))[:-1]

    def to_svg(self, image_scale: float = 1.0) -> str:
        """Return the svg code to plot the mesh pattern. The image size defaults to
        100x100 pixels and the parameter scales that."""
        patt_svg = self.pattern.to_svg(image_scale)
        n = len(self)
        p_scale = 100 / (n + 1)
        line_split = patt_svg.find(">")
        return "".join(
            [
                patt_svg[: line_split + 2],
                "\n".join(
                    (
                        f"<rect x={x*p_scale:.3} y={100-(y+1)*p_scale:.3} width="
                        f'"{p_scale:.3}" height="{p_scale:.3}" style="fill:'
                        "rgb(128,128,128);stroke-width:0;stroke:rgb(255,255,255);"
                        'fill-opacity:0.75" />'
                    )
                    for x, y in self.shading
                ),
                patt_svg[line_split + 1 :],
            ]
        )

    def to_tikz(self) -> str:
        """
        Return the tikz code to plot the mesh pattern. The tikz code requires
        the TikZ library patter.
        """
        n, tab = len(self), " " * 4
        lis = [
            "\\begin{tikzpicture}",
            f"[scale=.3,baseline=(current bounding box.center)]\n{tab}",
            f"\\foreach \\x in {{1,...,{n}}} {{\n{tab*2}",
            f"\\draw[ultra thin] (\\x,0)--(\\x,{n+1}); %vline\n{tab*2}",
            f"\\draw[ultra thin] (0,\\x)--({n+1},\\x); %hline\n{tab}}}",
            "".join(
                (
                    f"\n{tab}\\fill[pattern color = black!75, pattern="
                    f"north east lines] {cell} rectangle +(1,1);"
                )
                for cell in sorted(self.shading)
            ),
            f"\n{tab}",
            f"\n{tab}".join(
                f"\\draw[fill=black] ({idx+1},{val+1}) circle (5pt);"
                for idx, val in enumerate(self.pattern)
            ),
            "\n\\end{tikzpicture}",
        ]
        return "".join(lis)

    def show(self, scale: float = 1.0) -> None:
        """Open a browser tab and display pattern graphically. Image can be
        enlarged with scale parameter"""
        HTMLViewer.open_svg(self.to_svg(image_scale=scale))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.shading == other.shading and self.pattern == other.pattern
        return False

    def __hash__(self) -> int:
        return hash((self.pattern, self.shading))

    def __iter__(self) -> Iterator[Union[Perm, FrozenSet]]:
        return iter((self.pattern, self.shading))

    def __repr__(self) -> str:
        return f"MeshPatt({repr(self.pattern)}, {sorted(self.shading)})"

    def __str__(self) -> str:
        return f"({self.pattern}, {sorted(self.shading)})"

    def __len__(self) -> int:
        return len(self.pattern)

    def __bool__(self) -> bool:
        return bool(self.pattern) or bool(self.shading)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.pattern, sorted(self.shading)) < (
            other.pattern,
            sorted(other.shading),
        )

    def __le__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.pattern, sorted(self.shading)) <= (
            other.pattern,
            sorted(other.shading),
        )

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other.__lt__(self)

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other.__le__(self)

    def __contains__(self, patt: object) -> bool:
        if isinstance(patt, Patt):
            return any(True for _ in patt.occurrences_in(self))
        return False
