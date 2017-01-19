
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
        return bool(self.pattern)
