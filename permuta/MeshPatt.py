
import numbers
import sys
import collections

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
    # Static methods
    #

    @staticmethod
    def unrank(pattern, number):
        """Return the number-th shading of pattern.

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

    #
    # Dunder methods
    #

    def __repr__(self):
        return "MeshPatt({self.pattern}, {self.shading})".format(self=self)

    def __len__(self):
        return len(self.pattern)

    def __bool__(self):
        return bool(self.pattern)
