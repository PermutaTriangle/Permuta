# pylint: disable=too-many-lines,missing-docstring

import itertools
import math
import numbers
import operator
import random
import sys

from permuta._interfaces import Pattern
from permuta._interfaces import Flippable
from permuta._interfaces import Rotatable
from permuta._interfaces import Shiftable
from permuta.misc import left_floor_and_ceiling

if sys.version_info.major == 2:
    range = xrange  #pylint: disable=redefined-builtin,invalid-name,undefined-variable


class Perm(tuple,
           Pattern,
           Rotatable,
           Shiftable,
           Flippable
          ):  # pylint: disable=too-many-ancestors,too-many-public-methods
    """A perm class."""

    _TYPE_ERROR = "'{}' object is not a perm"

    #
    # Methods to modify Perm class settings
    #

    @staticmethod
    def toggle_check():
        # TODO: Docstring and discuss, can settings be done better?
        if Perm._init_helper is Perm._init_checked:
            Perm._init_helper = Perm._init_unchecked
        else:
            Perm._init_helper = Perm._init_checked

    #
    # Methods returning a single Perm instance
    #

    def __new__(cls, iterable=()):  # pylint: disable=unused-argument
        """Return a Perm instance.

        Args:
            cls:
                The class of which an instance is requested.
            iterable: <collections.Iterable> or <numbers.Integral>
                An iterable corresponding to a legal perm.
                Also supports passing just a number with unique digits.

        Raises:
            TypeError:
                Bad argument type.
            ValueError:
                Bad argument, but correct type.

        Examples:
            >>> Perm((0, 3, 1, 2))
            Perm((0, 3, 1, 2))
            >>> Perm(range(5, -1, -1))
            Perm((5, 4, 3, 2, 1, 0))
            >>> Perm(6012354)
            Perm((6, 0, 1, 2, 3, 5, 4))
            >>> Perm.toggle_check()
            >>> Perm("abc")  # Not good
            Traceback (most recent call last):
                ...
            TypeError: 'a' object is not an integer
            >>> Perm("012")
            Perm((0, 1, 2))
        """
        try:
            return tuple.__new__(cls, iterable)
        except TypeError:
            # Try to interpret object as perm
            if isinstance(iterable, numbers.Integral):
                number = iterable
                if not 0 <= number <= 9876543210:
                    raise ValueError("Illegal perm: {}".format(number))
                digit_list = []
                if number == 0:
                    digit_list.append(number)
                else:
                    while number != 0:
                        digit_list.append(number % 10)
                        number //= 10
                    iterable = reversed(digit_list)
                return tuple.__new__(cls, iterable)
            elif isinstance(iterable, str):
                return tuple.__new__(cls, map(int, iterable))
            else:
                raise

    def __init__(self, iterable=()):  # pylint: disable=unused-argument,super-init-not-called
        # Cache for data used when finding occurrences of self in a perm
        self._cached_pattern_details = None
        self._init_helper()

    def _init_unchecked(self):
        pass

    def _init_checked(self):
        used = [False]*len(self)
        for value in self:
            if not isinstance(value, numbers.Integral):
                message = "{} object is not an integer".format(repr(value))
                raise TypeError(message)
            if not 0 <= value < len(self):
                raise ValueError("Element out of range: {}".format(value))
            if used[value]:
                raise ValueError("Duplicate element: {}".format(value))
            used[value] = True

    _init_helper = _init_unchecked

    @classmethod
    def to_standard(cls, iterable):
        """Return the perm corresponding to iterable.

        Duplicate elements are allowed and become consecutive elements (see example).

        The standardize alias is supplied for backwards compatibility with permpy.
        However, the permpy version did not allow for duplicate elements.

        Examples:
            >>> Perm.to_standard("a2gsv3")
            Perm((2, 0, 3, 4, 5, 1))
            >>> Perm.to_standard("caaba")
            Perm((4, 0, 1, 3, 2))
        """
        # TODO: Do performance testing
        try:
            len_iterable = len(iterable)
        except TypeError:
            iterable = list(iterable)
            len_iterable = len(iterable)
        result = [None]*len_iterable
        value = 0
        for (index, _) in sorted(enumerate(iterable), key=operator.itemgetter(1)):
            result[index] = value
            value += 1
        return cls(result)

    standardize = to_standard  # permpy backwards compatibility
    from_iterable = to_standard

    @classmethod
    def one_based(cls, iterable):
        """A way to enter a perm in the traditional permuta way.

        Examples:
            >>> Perm.one_based((4, 1, 3, 2))
            Perm((3, 0, 2, 1))
        """
        return cls(((element-1) for element in iterable))

    one = one_based
    proper = one_based
    scientific = one_based

    @classmethod
    def identity(cls, length):
        """Return the identity perm of the specified length.

        Examples:
            >>> Perm.identity(0)
            Perm(())
            >>> Perm.identity(4)
            Perm((0, 1, 2, 3))
        """
        return cls(range(length))

    @classmethod
    def random(cls, length):
        """Return a random perm of the specified length.

        Examples:
            >>> perm = Perm.random(8)
            >>> len(perm) == 8
            True
            >>> # TODO: test perm in PermSet(8)
        """
        result = list(range(length))
        random.shuffle(result)
        return cls(result)

    @classmethod
    def monotone_increasing(cls, length):
        """Return a monotone increasing perm of the specified length.

        Examples:
            >>> Perm.monotone_increasing(0)
            Perm(())
            >>> Perm.monotone_increasing(4)
            Perm((0, 1, 2, 3))
        """
        return cls(range(length))

    @classmethod
    def monotone_decreasing(cls, length):
        """Return a monotone decreasing perm of the specified length.

        Examples:
            >>> Perm.monotone_decreasing(0)
            Perm(())
            >>> Perm.monotone_decreasing(4)
            Perm((3, 2, 1, 0))
        """
        return cls(range(length-1, -1, -1))

    @classmethod
    def unrank(cls, number, length=None):
        """

        Examples:
            >>> Perm.unrank(0)
            Perm(())
            >>> Perm.unrank(1)
            Perm((0,))
            >>> Perm.unrank(2)
            Perm((0, 1))
            >>> Perm.unrank(3)
            Perm((1, 0))
            >>> Perm.unrank(4)
            Perm((0, 1, 2))
            >>> Perm.unrank(5)
            Perm((0, 2, 1))
        """
        # TODO: Docstring, and do better? Assertions and messages
        #       Implement readably, nicely, and efficiently
        #assert isinstance(number, numbers.Integral)
        #assert 0 <= number
        if length is None:
            # Work out the length and number from the number given
            assert isinstance(number, numbers.Integral)
            assert number >= 0
            if number == 0:
                return cls()
            length = 1
            amount = 1  # Amount of perms of length
            while number > amount:
                number -= amount
                length += 1
                amount *= length
            number -= 1
        else:
            assert isinstance(length, numbers.Integral)
            assert length >= 0
            assert 0 <= number < math.factorial(length)
        return cls(Perm.__unrank(number, length))

    @staticmethod
    def __unrank(number, length):
        candidates = list(range(length))
        for value in range(1, length+1):
            factorial = math.factorial(length - value)
            division = number//factorial
            yield candidates.pop(division)
            number %= factorial

    ind2perm = unrank  # permpy backwards compatibility

    #
    # Methods modifying/combining Perm instances
    #

    def direct_sum(self, *others):
        """Return the direct sum of two or more perms.

        Args:
            self:
                A perm.
            others: <permuta.Perm> argument list
                Perms.

        Returns: <permuta.Perm>
            The direct sum of all the perms.

        Examples:
            >>> Perm((0,)).direct_sum(Perm((1, 0)))
            Perm((0, 2, 1))
            >>> Perm((0,)).direct_sum(Perm((1, 0)), Perm((2, 1, 0)))
            Perm((0, 2, 1, 5, 4, 3))
        """
        result = list(self)
        shift = len(self)
        for index in range(len(others)):
            other = others[index]
            if not isinstance(other, Perm):
                raise TypeError(Perm._TYPE_ERROR.format(repr(other)))
            result.extend(element + shift for element in other)
            shift += len(other)
        return Perm(result)

    def skew_sum(self, *others):
        """Return the skew sum of two or more perms.

        Args:
            self:
                A perm.
            others: <permuta.Perm> argument list
                Perms.

        Returns: <permuta.Perm>
            The skew sum of all the perms.

        Examples:
            >>> Perm((0,)).skew_sum(Perm((0, 1)))
            Perm((2, 0, 1))
            >>> Perm((0,)).skew_sum(Perm((0, 1)), Perm((2, 1, 0)))
            Perm((5, 3, 4, 2, 1, 0))
        """
        shift = sum(len(other) for other in others)
        result = [element + shift for element in self]
        for index in range(len(others)):
            other = others[index]
            if not isinstance(other, Perm):
                raise TypeError(Perm._TYPE_ERROR.format(repr(other)))
            shift -= len(other)
            result.extend(element + shift for element in other)
        return Perm(result)

    def compose(self, *others):
        """Return the composition of two or more perms.

        Args:
            self:
                A perm.
            others: <permuta.Perm> argument list
                Perms.

        Returns: <permuta.Perm>
            The consecutive pointwise application of all the above perms
            in reverse order.

        Raises:
            TypeError:
                An object in the argument list is not a perm.
            ValueError:
                A perm in the argument list is of the wrong length.

        Examples:
            >>> Perm((0, 3, 1, 2)).compose(Perm((2, 1, 0, 3)))
            Perm((1, 3, 0, 2))
            >>> Perm((1, 0, 2)).compose(Perm((0, 1, 2)), Perm((2, 1, 0)))
            Perm((2, 0, 1))
        """
        for other in others:
            if not isinstance(other, Perm):
                raise TypeError(Perm._TYPE_ERROR.format(repr(other)))
            if len(other) != len(self):
                raise ValueError("Perm length mismatch")
        result = [None]*len(self)
        for value in range(len(self)):
            composed_value = value
            for other in reversed(others):
                composed_value = other[composed_value]
            composed_value = self[composed_value]
            result[value] = composed_value
        return Perm(result)

    multiply = compose

    def insert(self, index=None, new_element=None):
        """Return the perm acquired by adding a new element.

        Args:
            index: <int>
                Where in the perm the value is to occur.
                If None, the value defaults to len(self)+1.
            new_element: <int>
                An integer in the range of 0 to len(self) inclusive.
                If None, the element defaults to len(self).

        Returns: <permuta.Perm>
            The perm with the added element (and other elements adjusted
            as needed).

        Raises:
            IndexError:
                Index is not valid.
            ValueError:
                Element passed cannot legally be added to perm.
            TypeError:
                Element passed is not an integer.

        Examples:
            >>> Perm((0, 1)).insert()
            Perm((0, 1, 2))
            >>> Perm((0, 1)).insert(0)
            Perm((2, 0, 1))
            >>> Perm((2, 0, 1)).insert(2, 1)
            Perm((3, 0, 1, 2))
        """
        if index is None:
            index = len(self)+1
        if new_element is None:
            new_element = len(self)
        else:
            if not isinstance(new_element, numbers.Integral):
                raise TypeError("{} object is not an integer".format(repr(new_element)))
            if not 0 <= new_element <= len(self):
                raise ValueError("Element out of range: {}".format(new_element))
        slice_1 = (element if element < new_element else element+1
                   for element in itertools.islice(self, index))
        slice_2 = (element if element < new_element else element+1
                   for element in itertools.islice(self, index, len(self)))
        return Perm(itertools.chain(slice_1, (new_element,), slice_2))

    def remove(self, index=None):
        """Return the perm acquired by removing an element at a specified index.

        Args:
            index: <int>
                The index of the element to be removed.
                If None, the greatest element of the perm is removed.

        Returns: <permuta.Perm>
            The perm without the element (and other elements adjusted if needed).

        Raises:
            IndexError:
                Index is not valid.

        Examples:
            >>> Perm((2, 0, 1)).remove()
            Perm((0, 1))
            >>> Perm((3, 0, 1, 2)).remove(0)
            Perm((0, 1, 2))
            >>> Perm((2, 0, 1)).remove(2)
            Perm((1, 0))
            >>> Perm((0,)).remove(0)
            Perm(())
        """
        if index is None:
            return self.remove_element()
        selected = self[index]
        return Perm(element if element < selected else element-1
                    for element in self if element != selected)

    def remove_element(self, selected=None):
        """Return the perm acquired by removing a specific element from self.

        Args:
            selected: <int>
                The element selected to be removed. It is an integer in the
                range of 0 to len(self) inclusive. If None, it defaults to len(self).

        Returns: <permuta.Perm>
            The perm with the selected element removed (and other
            elements adjusted as needed).

        Raises:
            ValueError:
                Selected element does not belong to perm.
            TypeError:
                Element passed is not an integer.

        Examples:
            >>> Perm((3, 0, 1, 2)).remove_element()
            Perm((0, 1, 2))
            >>> Perm((3, 0, 2, 1)).remove_element(0)
            Perm((2, 1, 0))
        """
        if selected is None:
            selected = len(self)-1
        else:
            if not isinstance(selected, numbers.Integral):
                raise TypeError("{} object is not an integer".format(repr(selected)))
            if not 0 <= selected < len(self):
                raise ValueError("Element out of range: {}".format(selected))
        return Perm(element if element < selected else element-1
                    for element in self if element != selected)

    def inflate(self, components, indices=None):
        """Inflate element(s)."""
        # TODO: Discuss implementation: GOOD: Dict or complete list
        pass

    def __inflate_shifts(self, component):
        """ """
        pass

    #
    # Methods for basic Perm transforming
    #

    def inverse(self):
        """Return the inverse of the perm self.

        Examples:
            >>> Perm((1, 2, 5, 0, 3, 4)).inverse()
            Perm((3, 0, 1, 4, 5, 2))
            >>> Perm((2, 0, 1)).inverse().inverse() == Perm((2, 0, 1))
            True
            >>> Perm((0, 1)).inverse()
            Perm((0, 1))
        """
        len_perm = len(self)
        result = [None]*len_perm
        for index in range(len_perm):
            result[self[index]] = index
        return Perm(result)

    def reverse(self):
        """Return the reverse of the perm self.

        Examples:
            >>> Perm((1, 2, 5, 0, 3, 4)).reverse()
            Perm((4, 3, 0, 5, 2, 1))
            >>> Perm((0, 1)).reverse()
            Perm((1, 0))
        """
        return Perm(self[::-1])

    def complement(self):
        """Return the complement of the perm self.

        Examples:
            >>> Perm((1, 2, 3, 0, 4)).complement()
            Perm((3, 2, 1, 4, 0))
            >>> Perm((2, 0, 1)).complement()
            Perm((0, 2, 1))
        """
        base = len(self) - 1
        return Perm(base - element for element in self)

    def reverse_complement(self):
        """Return the reverse complement of self.

        Equivalent to two left or right rotations.

        Examples:
            >>> Perm((1, 2, 3, 0, 4)).reverse_complement()
            Perm((0, 4, 1, 2, 3))
            >>> Perm((2, 0, 1)).reverse_complement()
            Perm((1, 2, 0))
        """
        base = len(self) - 1
        return Perm(base - element for element in reversed(self))

    def shift_right(self, times=1):
        """Return self shifted times steps to the right.

        If shift is negative, shifted to the left.

        Examples:
            >>> Perm((0, 1, 2)).shift_right()
            Perm((2, 0, 1))
            >>> Perm((0, 1, 2)).shift_right(-4)
            Perm((1, 2, 0))
        """
        if len(self) == 0:
            return self
        times = times % len(self)
        if times == 0:
            return self
        index = len(self) - times
        slice_1 = itertools.islice(self, index)
        slice_2 = itertools.islice(self, index, len(self))
        return Perm(itertools.chain(slice_2, slice_1))

    def shift_left(self, times=1):
        """Return self shifted times steps to the left.

        If shift is negative, shifted to the right.

        Examples:
            >>> Perm((0, 1, 2)).shift_left()
            Perm((1, 2, 0))
            >>> Perm((0, 1, 2)).shift_left(-4)
            Perm((2, 0, 1))
        """
        return self.shift_right(-times)

    shift = shift_right
    cyclic_shift = shift_right
    cyclic_shift_right = shift_right
    cyclic_shift_left = shift_left

    def shift_up(self, times=1):
        """Return self shifted times steps up.

        If times is negative, shifted down.

        Examples:
            >>> Perm((0, 1, 2, 3)).shift_up(1)
            Perm((1, 2, 3, 0))
            >>> Perm((0, 1, 2, 3)).shift_up(-7)
            Perm((1, 2, 3, 0))
            >>> Perm((0,)).shift_up(1234)
            Perm((0,))
        """
        if len(self) == 0:
            return self
        times = times % len(self)
        if times == 0:
            return self
        bound = len(self)
        return Perm((element + times) % bound for element in self)

    def shift_down(self, times=1):
        """Return self shifted times steps down.

        If times is negative, shifted up.

        Examples:
            >>> Perm((0, 1, 2, 3)).shift_down(1)
            Perm((3, 0, 1, 2))
            >>> Perm((0, 1, 2, 3)).shift_down(-7)
            Perm((3, 0, 1, 2))
            >>> Perm((0,)).shift_down(1234)
            Perm((0,))
        """
        return self.shift_up(-times)

    def flip_horizontal(self):
        """Return self flipped horizontally.

        Examples:
            >>> Perm((1, 2, 3, 0, 4)).flip_horizontal()
            Perm((3, 2, 1, 4, 0))
            >>> Perm((2, 0, 1)).flip_horizontal()
            Perm((0, 2, 1))
        """
        return self.complement()

    def flip_vertical(self):
        """Return self flipped vertically.

        Examples:
            >>> Perm((1, 2, 5, 0, 3, 4)).flip_vertical()
            Perm((4, 3, 0, 5, 2, 1))
            >>> Perm((0, 1)).flip_vertical()
            Perm((1, 0))
        """
        return self.reverse()

    def flip_diagonal(self):
        """Return self flipped along the diagonal.

        Examples:
            >>> Perm((1, 2, 5, 0, 3, 4)).flip_diagonal()
            Perm((3, 0, 1, 4, 5, 2))
            >>> Perm((0, 1)).flip_diagonal()
            Perm((0, 1))
        """
        return self.inverse()

    def flip_antidiagonal(self):
        """Return self flipped along the antidiagonal..

        Examples:
            >>> Perm((3, 2, 0, 1)).flip_antidiagonal()
            Perm((3, 2, 0, 1))
            >>> Perm((1, 2, 3, 0, 4)).flip_antidiagonal()
            Perm((0, 2, 3, 4, 1))
            >>> Perm((1, 2, 0, 3)).flip_antidiagonal()
            Perm((0, 2, 3, 1))
        """
        len_perm = len(self)
        result = [None]*len_perm

        flipped_pairs = ((len_perm-element-1, len_perm-index-1)
                         for index, element in enumerate(self))

        for index, element in flipped_pairs:
            result[index] = element
        return Perm(result)

    def _rotate_right(self):
        """Return self rotated 90 degrees to the right."""
        len_perm = len(self)
        result = [None]*len_perm
        for index, value in enumerate(self):
            result[value] = len_perm - index - 1
        return Perm(result)

    def _rotate_left(self):
        """Return self rotated 90 degrees to the left."""
        len_perm = len(self)
        result = [None]*len_perm
        for index, value in enumerate(self):
            result[len_perm - value - 1] = index
        return Perm(result)

    def _rotate_180(self):
        """Return self rotated 180 degrees."""
        return self.reverse_complement()

    #
    # Statistical methods
    #

    def is_increasing(self):
        """Return True if the perm is increasing, and False otherwise."""
        for index in range(len(self)):
            if self[index] != index:
                return False
        return True

    def is_decreasing(self):
        """Return True if the perm is decreasing, and False otherwise."""
        len_perm = len(self)
        for index in range(len_perm):
            if self[index] != len_perm - index - 1:
                return False
        return True

    def fixed_points(self):
        """Return the number of fixed points in self.

        Examples:
            >>> Perm((0, 1, 4, 3, 2)).fixed_points()
            3
            >>> Perm((0, 1, 2, 3, 4)).fixed_points()
            5
            >>> Perm((3, 2, 1, 0)).fixed_points()
            0
        """
        result = 0
        value = 0
        for element in self:
            if element == value:
                result += 1
            value += 1
        return result

    def descents(self):
        """Yield the indices of the descents of self.

        Examples:
            >>> tuple(Perm((0, 1, 3, 2, 4)).descents())
            (3,)
            >>> tuple(Perm((3, 2, 1, 0)).descents())
            (1, 2, 3)
            >>> tuple(Perm((0, 1, 2)).descents())
            ()
        """
        for index in range(1, len(self)):
            if self[index-1] > self[index]:
                yield index

    def descent_set(self):
        """Return the list of descents of self.

        This method is for backwards compatibility with permpy.
        """
        return list(self.descents())

    def count_descents(self):
        """Count the number of descents of self.
        Examples:
            >>> Perm((0, 1, 3, 2, 4)).count_descents()
            1
            >>> Perm((3, 2, 1, 0)).count_descents()
            3
            >>> Perm((0, 1, 2)).count_descents()
            0
        """
        return sum(1 for _ in self.descents())

    num_descents = count_descents  # permpy backwards compatibility

    def ascents(self):
        """Yield the indices of the ascent of self.

        Examples:
            >>> tuple(Perm((0, 1, 3, 2, 4)).ascents())
            (1, 2, 4)
            >>> tuple(Perm((0, 4, 3, 2, 1)).ascents())
            (1,)
            >>> tuple(Perm((3, 2, 1, 0)).ascents())
            ()
        """
        for index in range(1, len(self)):
            if self[index-1] < self[index]:
                yield index

    def ascent_set(self):
        """Return the list of ascents of self.

        This method is for backwards compatibility with permpy.
        """
        return list(self.ascents())

    def count_ascents(self):
        """Count the number of ascents in self.

        Examples:
            >>> Perm((0, 1, 3, 2, 4)).count_ascents()
            3
            >>> Perm((0, 4, 3, 2, 1)).count_ascents()
            1
            >>> Perm((3, 2, 1, 0)).count_ascents()
            0
        """
        return sum(1 for _ in self.ascents())

    num_ascents = count_ascents  # permpy backwards compatibility

    def peaks(self):
        """Yield the indices of the peaks of self.

        The i-th element of a perm is a peak if
            self[i-1] < self[i] > self[i+1].

        Examples:
            >>> tuple(Perm((5, 3, 4, 0, 2, 1)).peaks())
            (2, 4)
            >>> tuple(Perm((1, 2, 0)).peaks())
            (1,)
            >>> tuple(Perm((2, 1, 0)).peaks())
            ()
        """
        if len(self) <= 2:
            return
        ascent = False
        for index in range(1, len(self)-1):
            if self[index-1] < self[index]:
                # Perm ascended
                ascent = True
            else:
                # Perm descended
                if ascent:
                    yield index-1
                ascent = False
        # Check if penultimate element is a peak
        if ascent and self[-2] > self[-1]:
            yield len(self) - 2

    def peak_list(self):
        """Return the list of peaks of self.

        This method is for backwards compatibility with permpy.
        """
        return list(self.peaks())

    def count_peaks(self):
        """Count the number of peaks of self.

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).count_peaks()
            2
            >>> Perm((1, 2, 0)).count_peaks()
            1
            >>> Perm((2, 1, 0)).count_peaks()
            0
        """
        return sum(1 for _ in self.peaks())

    num_peaks = count_peaks  # permpy backwards compatibility

    def valleys(self):
        """Yield the indices of the valleys of self.

        The i-th element of a perm is a valley if
            self[i-1] > self[i] < self[i+1].

        Examples:
            >>> tuple(Perm((5, 3, 4, 0, 2, 1)).valleys())
            (1, 3)
            >>> tuple(Perm((2, 0, 1)).valleys())
            (1,)
            >>> tuple(Perm((1, 2, 0)).valleys())
            ()
        """
        if len(self) <= 2:
            return
        ascent = True
        for index in range(1, len(self)-1):
            if self[index-1] < self[index]:
                # Perm ascended
                if not ascent:
                    yield index-1
                ascent = True
            else:
                # Perm descended
                ascent = False
        # Check if penultimate element is a valley
        if not ascent and self[-2] < self[-1]:
            yield len(self) - 2

    def valley_list(self):
        """Return the list of valleys of self.

        This method is for backwards compatibility with permpy.
        """
        return list(self.valleys())

    def count_valleys(self):
        """Count the number of valleys of self.

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).count_valleys()
            2
            >>> Perm((2, 0, 1)).count_valleys()
            1
            >>> Perm((1, 2, 0)).count_valleys()
            0
        """
        return sum(1 for _ in self.valleys())

    num_valleys = count_valleys  # permpy backwards compatibility

    # TODO: Implement rank method
    #perm2ind = rank  # permpy backwards compatibility

    #
    # Pattern matching methods
    #

    def contains(self, *patts):
        """Check if self contains patts.

        Args:
            self:
                A perm.
            patts: <permuta.Pattern> argument list
                Classical/mesh patterns.

        Returns: <bool>
            True if and only if all patterns in patt are contained in self.

        Examples:
            >>> Perm.monotone_decreasing(7).avoids(Perm((0, 1)))
            True
            >>> Perm((4, 2, 3, 1, 0)).contains(Perm((1, 2, 0)))
            True
            >>> Perm((0, 1, 2)).contains(Perm((1,0)))
            False
            >>> pattern1 = Perm((0, 1))
            >>> pattern2 = Perm((2, 0, 1))
            >>> pattern3 = Perm((0, 3, 1, 2))
            >>> Perm((5, 3, 0, 4, 2, 1)).contains(pattern1, pattern2)
            True
            >>> Perm((5, 3, 0, 4, 2, 1)).contains(pattern2, pattern3)
            False
        """
        return all(patt in self for patt in patts)

    def avoids(self, *patts):
        """Check if self avoids patts.

        Args:
            self:
                A perm.
            patts: <permuta.Pattern> argument list
                Classical/mesh patterns.

        Returns: <bool>
            True if and only if self avoids all patterns in patts.

        Examples:
            >>> Perm.monotone_increasing(8).avoids(Perm((1, 0)))
            True
            >>> Perm((4, 2, 3, 1, 0)).avoids(Perm((1, 2, 0)))
            False
            >>> Perm((0, 1, 2)).avoids(Perm((1,0)))
            True
            >>> pattern1 = Perm((0, 1))
            >>> pattern2 = Perm((2, 0, 1))
            >>> pattern3 = Perm((0, 3, 1, 2))
            >>> pattern4 = Perm((0, 1, 2))
            >>> Perm((5, 3, 0, 4, 2, 1)).avoids(pattern1, pattern2)
            False
            >>> Perm((5, 3, 0, 4, 2, 1)).avoids(pattern2, pattern3)
            False
            >>> Perm((5, 3, 0, 4, 2, 1)).avoids(pattern3, pattern4)
            True
        """
        return all(patt not in self for patt in patts)

    def avoids_set(self, patts):
        """Check if self avoids patts.

        This method is for backwards compatibility with permpy.
        """
        return self.avoids(*tuple(patts))

    def count_occurrences_of(self, patt):
        """Count the number of occurrences of patt in self.

        Args:
            self:
                A perm.
            patt: <permuta.Pattern>
                A classical/mesh pattern.

        Returns: <int>
            The number of times patt occurs in self.

        Examples:
            >>> Perm((0, 1, 2)).count_occurrences_of(Perm((0, 1)))
            3
            >>> Perm((5, 3, 0, 4, 2, 1)).count_occurrences_of(Perm((2, 0, 1)))
            6
        """
        return patt.count_occurrences_in(self)

    occurrences = count_occurrences_of  # permpy backwards compatibility

    def occurrences_in(self, perm):
        """Find all indices of occurrences of self in perm.

        Args:
            self:
                The classical pattern whose occurrences are to be found.
            perm: <permuta.Perm>
                The perm to search for occurrences in.

        Yields: <tuple> of <int>
            The indices of the occurrences of self in perm.
            Each yielded element l is a tuple of integer indices of the
            perm perm such that:
            self == permuta.Perm.to_standard([perm[i] for i in l])

        Examples:
            >>> list(Perm((2, 0, 1)).occurrences_in(Perm((5, 3, 0, 4, 2, 1))))
            [(0, 1, 3), (0, 2, 3), (0, 2, 4), (0, 2, 5), (1, 2, 4), (1, 2, 5)]
            >>> list(Perm((1, 0)).occurrences_in(Perm((1, 2, 3, 0))))
            [(0, 3), (1, 3), (2, 3)]
            >>> list(Perm((0,)).occurrences_in(Perm((1, 2, 3, 0))))
            [(0,), (1,), (2,), (3,)]
            >>> list(Perm().occurrences_in(Perm((1, 2, 3, 0))))
            [()]
        """
        # Special cases
        if len(self) == 0:
            # Pattern is empty, occurs in all perms
            # This is needed for the occurrences function to work correctly
            yield ()
            return
        if len(self) > len(perm):
            # Pattern is too long to occur in perm
            return

        # The indices of the occurrence in perm
        occurrence_indices = [None]*len(self)

        # Get left to right scan details
        pattern_details = self.__pattern_details()

        # Define function that works with the above defined variables
        # i is the index of the element in perm that is to be considered
        # k is how many elements of the perm have already been added to occurrence
        def occurrences(i, k):
            elements_remaining = len(perm) - i
            elements_needed = len(self) - k

            # Get the following variables:
            #   - lfi: Left Floor Index
            #   - lci: Left Ceiling Index
            #   - lbp: Lower Bound Pre-computation
            #   - ubp: Upper Bound pre-computation
            lfi, lci, lbp, ubp = pattern_details[k]

            # Set the bounds for the new element
            if lfi is None:
                # The new element of the occurrence must be at least self[k];
                # i.e., the k-th element of the pattern
                # In this case, lbp = self[k]
                lower_bound = lbp
            else:
                # The new element of the occurrence must be at least as far
                # from its left floor as self[k] is from its left floor
                # In this case, lbp = self[k] - self[lfi]
                occurrence_left_floor = perm[occurrence_indices[lfi]]
                lower_bound = occurrence_left_floor + lbp
            if lci is None:
                # The new element of the occurrence must be at least as less
                # than its maximum possible element---i.e., len(perm)---as
                # self[k] is to its maximum possible element---i.e., len(self)
                # ubp = len(self) - self[k]
                upper_bound = len(perm) - ubp
            else:
                # The new element of the occurrence must be at least as less
                # than its left ceiling as self[k] is to its left ceiling
                # In this case, ubp = self[lci] - self[k]
                upper_bound = perm[occurrence_indices[lci]] - ubp

            # Loop over remaining elements of perm (actually i, the index)
            while 1:
                if elements_remaining < elements_needed:
                    # Can't form an occurrence with remaining elements
                    return
                element = perm[i]
                if lower_bound <= element <= upper_bound:
                    occurrence_indices[k] = i
                    if elements_needed == 1:
                        # Yield occurrence
                        yield tuple(occurrence_indices)
                    else:
                        # Yield occurrences where the i-th element is chosen
                        for occurence in occurrences(i+1, k+1):
                            yield occurence
                # Increment i, that also means elements_remaining should decrement
                i += 1
                elements_remaining -= 1

        for occurence in occurrences(0, 0):
            yield occurence

    def occurrences_of(self, patt):
        """Find all indices of occurrences of patt in self.

        This method is complementary to permuta.Perm.occurrences_in.
        It just calls patt.occurrences_in(self) internally.
        See permuta.Perm.occurrences_in for documentation.

        Args:
            self:
                A perm.
            patt: <permuta.Pattern>
                A classical/mesh pattern.

        Yields: <tuple> of <int>
            The indices of the occurrences of self in perm.

        Examples:
            >>> list(Perm((5, 3, 0, 4, 2, 1)).occurrences_of(Perm((2, 0, 1))))
            [(0, 1, 3), (0, 2, 3), (0, 2, 4), (0, 2, 5), (1, 2, 4), (1, 2, 5)]
            >>> list(Perm((1, 2, 3, 0)).occurrences_of(Perm((1, 0))))
            [(0, 3), (1, 3), (2, 3)]
            >>> list(Perm((1, 2, 3, 0)).occurrences_of(Perm((0,))))
            [(0,), (1,), (2,), (3,)]
            >>> list(Perm((1, 2, 3, 0)).occurrences_of(Perm()))
            [()]
        """
        return patt.occurrences_in(self)

    def __pattern_details(self):
        """Subroutine of occurrences_in method."""
        # If details have been calculated before, return cached result
        if self._cached_pattern_details is not None:
            return self._cached_pattern_details
        result = []
        index = 0
        for fac_indices in left_floor_and_ceiling(self):
            base_element = self[index]
            compiled = (fac_indices.floor,

                        fac_indices.ceiling,

                        self[index]
                        if fac_indices.floor is None
                        else base_element - self[fac_indices.floor],

                        len(self) - self[index]
                        if fac_indices.ceiling is None
                        else self[fac_indices.ceiling] - base_element,
                       )
            result.append(compiled)
            index += 1
        self._cached_pattern_details = result
        return result

    #
    # General methods
    #

    def apply(self, iterable):
        """Permute an iterable using the perm.

        Args:
            self:
                A perm.
            iterable: <collections.Iterable>
                An iterable of len(self) elements.

        Returns: <tuple>
            The elements of iterable in the permuted order.

        Raises:
            TypeError:
                Bad argument type.

        Examples:
            >>> Perm((4, 1, 2, 0, 3)).apply((1, 2, 3, 4, 5))
            (5, 2, 3, 1, 4)
            >>> Perm((4, 1, 2, 0, 3)).apply("abcde")
            ('e', 'b', 'c', 'a', 'd')
            >>> Perm((1, 2, 0, 3)).apply("abcde")
            Traceback (most recent call last):
                ...
            TypeError: Length mismatch
        """
        iterable = tuple(iterable)
        if len(iterable) != len(self):
            raise TypeError("Length mismatch")
        return tuple(iterable[index] for index in self)

    permute = apply  # Alias of Perm.apply

    #
    # Magic/dunder methods
    #

    def __call__(self, value):
        """Map value to its image defined by the perm.

        Examples:
            >>> Perm((3, 1, 2, 0))(0)
            3
            >>> Perm((3, 1, 2, 0))(1)
            1
            >>> Perm((3, 1, 2, 0))(2)
            2
            >>> Perm((3, 1, 2, 0))(3)
            0
        """
        if not isinstance(value, numbers.Integral):
            raise TypeError("{} object is not an integer".format(repr(value)))
        if not 0 <= value < len(self):
            raise ValueError("Element out of range: {}".format(value))
        return self[value]

    def __add__(self, other):
        """Return the direct sum of the perms self and other."""
        return self.direct_sum(other)

    def __sub__(self, other):
        """Return the skew sum of the perms self and other."""
        return self.skew_sum(other)

    def __mul__(self, other):
        """Return the composition of two perms."""
        return self.multiply(other)

    def __repr__(self):
        return "Perm({})".format(super(Perm, self).__repr__())

    def __lt__(self, other):
        return (len(self), tuple(self)) < (len(other), tuple(other))

    def __le__(self, other):
        return (len(self), tuple(self)) <= (len(other), tuple(other))

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return other <= self

    def __contains__(self, patt):
        """Check if self contains patt.

        Args:
            self:
                A perm.
            patt: <permuta.Pattern>
                A classical/mesh pattern.

        Returns: <bool>
            True if and only if the pattern patt is contained in self.
        """
        return any(True for _ in patt.occurrences_in(self))
