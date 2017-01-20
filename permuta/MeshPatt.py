
import collections
import numbers
import random
import sys

from permuta import Perm
from permuta.interfaces import Patt, Rotatable, Shiftable, Flippable
from permuta.misc import DIR_EAST, DIR_NORTH, DIR_WEST, DIR_SOUTH, DIR_NONE

MeshPatternBase = collections.namedtuple("MeshPatternBase",
                                         ["pattern", "shading"])
class MeshPatt(MeshPatternBase, Patt, Rotatable, Shiftable, Flippable):
    """A mesh pattern class."""

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
            self:
                A mesh pattern.
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

    def shade(self, positions):
        """Returns the mesh pattern with the added shadings given by positions.

        Args:
            positions: tuple or collections.Iterable
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
            else:
                positions = set(positions)

        return MeshPatt(self.pattern, self.shading | positions)

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
            shaded; otherwise, True if and only if all regions (x, y)
            for x in the range lower_left[0] to upper_right[0] (inclusive) and
            for y in the range lower_left[1] to upper_right[1] (inclusive) are
            shaded.
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
        shading = set()
        binary = reversed(bin(number)[2:])
        for index, bit in enumerate(reversed(bin(number)[2:])):
            if bit == '1':
                shading.add((index // bound, index % bound))
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

    def __repr__(self):
        return "MeshPatt({self.pattern}, {self.shading})".format(self=self)

    def __len__(self):
        return len(self.pattern)

    def __bool__(self):
        return bool(self.pattern) or bool(self.shading)


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
