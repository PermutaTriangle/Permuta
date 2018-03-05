import bisect
import collections
import fractions
import itertools
import math
import numbers
import operator
import random
import sys

from permuta.interfaces import Flippable, Patt, Rotatable, Shiftable
from permuta.misc import left_floor_and_ceiling

if sys.version_info.major == 2:
    range = xrange


__all__ = ("Perm",)


class Perm(tuple,
           Patt,
           Rotatable,
           Shiftable,
           Flippable):
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

    def __new__(cls, iterable=()):
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
            TypeError: ''a'' object is not an integer
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
                    digit_list.reverse()
                return tuple.__new__(cls, digit_list)
            else:
                raise

    def __init__(self, iterable=()):
        # Cache for data used when finding occurrences of self in a perm
        self._cached_pattern_details = None
        self._init_helper()

    def _init_unchecked(self):
        pass

    def _init_checked(self):
        used = [False]*len(self)
        for value in self:
            if not isinstance(value, numbers.Integral):
                message = "'{}' object is not an integer".format(repr(value))
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

        Duplicate elements are allowed and become consecutive elements (see
        example).

        The standardize alias is supplied for backwards compatibility with
        permpy.  However, the permpy version did not allow for duplicate
        elements.

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
        for (index, _) in sorted(enumerate(iterable),
                                 key=operator.itemgetter(1)):
            result[index] = value
            value += 1
        return cls(result)

    standardize = to_standard  # permpy backwards compatibility
    from_iterable = to_standard

    @classmethod
    def from_string(cls, string):
        """Return the perm corresponding to the string given.

        Examples:
            >>> Perm.from_string("203451")
            Perm((2, 0, 3, 4, 5, 1))
            >>> Perm.from_string("40132")
            Perm((4, 0, 1, 3, 2))
        """
        if isinstance(string, str):
            return cls(map(int, string))
        # TODO: throw exception when not a string

    @classmethod
    def one_based(cls, iterable):
        """A way to enter a perm in the traditional permuta way.

        Examples:
            >>> Perm.one_based((4, 1, 3, 2))
            Perm((3, 0, 2, 1))
        """
        return cls((element - 1 for element in iterable))

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
            >>> Perm.unrank(1, 3)
            Perm((0, 2, 1))
        """
        # TODO: Docstring, and do better? Assertions and messages
        #       Implement readably, nicely, and efficiently
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
        for other in others:
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
                raise TypeError(
                    "'{}' object is not an integer".format(repr(new_element)))
            if not 0 <= new_element <= len(self):
                raise ValueError(
                    "Element out of range: {}".format(new_element))
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
            The perm without the element (and other elements adjusted).

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
                range of 0 to len(self) inclusive. If None, it defaults to
                len(self) - 1.

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
                raise TypeError(
                    "'{}' object is not an integer".format(repr(selected)))
            if not 0 <= selected < len(self):
                raise ValueError("Element out of range: {}".format(selected))
        return Perm(element if element < selected else element-1
                    for element in self if element != selected)

    def inflate(self, components):
        """Inflate elements of the permutation to create a new one.

        Args:
            component: <collections.Iterable> of <permuta.Perm>
                This can also be a dict with keys and perms...

        Returns: <permuta.Perm>

        Examples:
            >>> Perm((0, 1)).inflate([Perm((1, 0)), Perm((2, 1, 0))])
            Perm((1, 0, 4, 3, 2))
            >>> Perm((1, 0, 2)).inflate([None, Perm((0, 1)), Perm((0, 1))])
            Perm((2, 0, 1, 3, 4))
            >>> Perm((0, 2, 1)).inflate({2: Perm((0, 1, 2))})
            Traceback (most recent call last):
                ...
            NotImplementedError
            >>> # Can also deflate points
            >>> Perm((0, 1)).inflate([Perm(), Perm()])
            Perm(())
        """
        # TODO: Spitshine method and docstring
        if isinstance(components, collections.Mapping):
            raise NotImplementedError
        elif isinstance(components, collections.Iterable):
            components = tuple(components)
            assert len(components) == len(self)
            shift = 0
            shifts = [0]*len(self)
            for index in self.inverse():
                shifts[index] = shift
                component = components[index]
                shift += 1 if component is None else len(component)
            perm_elements = []
            for index, component in enumerate(components):
                if component is None:
                    perm_elements.append(shifts[index])
                else:
                    shift = shifts[index]
                    perm_elements.extend(element +
                                         shift for element in component)
            return Perm(perm_elements)
        else:
            raise TypeError

    def contract_inc_bonds(self):
        # TODO: test
        monblocks = self.monotone_block_decompositon_ascending(with_ones=True)
        return Perm.to_standard([start for (start, end) in monblocks])

    def contract_dec_bonds(self):
        # TODO: test
        monblocks = self.monotone_block_decompositon_descending(with_ones=True)
        return Perm.to_standard([start for (start, end) in monblocks])

    def contract_bonds(self):
        # TODO: reimplement by calling contract_{inc,dec}_bonds or remove
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

    def all_syms(self):
        """Returns all symmetries of the permutation in a PermSet, all possible
        combinations of revers, complement and inverse.
        """
        # TODO: finish PermSet
        # S = PermSet([self])
        # S = S.union(PermSet([P.reverse() for P in S]))
        # S = S.union(PermSet([P.complement() for P in S]))
        # S = S.union(PermSet([P.inverse() for P in S]))
        # return S
        pass

    def is_representative(self):
        """Checks if the permutation is representative, that is, all the
        symmetries of the permutation are the same.
        """
        # return self == sorted(self.all_syms())[0]
        pass

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

    def count_fixed_points(self):
        """Return the number of fixed points in self.

        Examples:
            >>> Perm((0, 1, 4, 3, 2)).count_fixed_points()
            3
            >>> Perm((0, 1, 2, 3, 4)).count_fixed_points()
            5
            >>> Perm((3, 2, 1, 0)).count_fixed_points()
            0
        """
        result = 0
        value = 0
        for element in self:
            if element == value:
                result += 1
            value += 1
        return result

    # TODO: Implement a function that returns a list of fixed points.

    fixed_points = count_fixed_points

    def is_skew_decomposable(self):
        """Determines whether the permutation is expressible as the skew sum of
        two permutations.

        >>> p = Perm.random(8).direct_sum(Perm.random(12))
        >>> p.skew_decomposable()
        False
        >>> p.complement().skew_decomposable()
        True
        """

        p = list(self)
        n = self.__len__()
        for i in range(1, n):
            if set(range(n-i, n)) == set(p[0:i]):
                return True
        return False

    skew_decomposable = is_skew_decomposable  # permpy backwards compatibility

    def is_sum_decomposable(self):
        """Determines whether the permutation is expressible as the direct sum of
        two permutations.

        >>> p = Perm.random(4).direct_sum(Perm.random(15))
        >>> p.sum_decomposable()
        True
        >>> p.reverse().sum_decomposable()
        False
        """

        p = list(self)
        n = self.__len__()
        for i in range(1, n):
            if set(range(0, i)) == set(p[0:i]):
                return True
        return False

    sum_decomposable = is_sum_decomposable  # permpy backwards compatibility

    def descents(self):
        """Yield the 0-based descents of self.

        Examples:
            >>> tuple(Perm((0, 1, 3, 2, 4)).descents())
            (2,)
            >>> tuple(Perm((3, 2, 1, 0)).descents())
            (0, 1, 2)
            >>> tuple(Perm((0, 1, 2)).descents())
            ()
        """
        for index in range(len(self) - 1):
            if self[index] > self[index + 1]:
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
        """Yield the 0-based ascent of self.

        Examples:
            >>> tuple(Perm((0, 1, 3, 2, 4)).ascents())
            (0, 1, 3)
            >>> tuple(Perm((0, 4, 3, 2, 1)).ascents())
            (0,)
            >>> tuple(Perm((3, 2, 1, 0)).ascents())
            ()
        """
        for index in range(len(self) - 1):
            if self[index] < self[index + 1]:
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

    def bends(self):
        """Yield the indices at which the permutation changes direction. That
        is, the number of non-monotone consecutive triples of the permutation.
        A permutation p can be expressed as the concatenation of len(p.bends())
        + 1 monotone segments.

        Examples:
            >>> list(Perm((5, 3, 4, 0, 2, 1)).bends())
            [1, 2, 3, 4]
            >>> list(Perm((2, 0, 1)).bends())
            [1]
        """
        if len(self) <= 2:
            return
        ascent = self[0] < self[1]
        for index in range(1, len(self) - 1):
            if self[index] > self[index + 1] and ascent:
                yield index
            elif self[index] < self[index + 1] and not ascent:
                yield index
            ascent = self[index] < self[index + 1]

    def bend_list(self):
        """Returns the list of indices at which the permutation changes
        direction. That is, the number of non-monotone consecutive triples of
        the permutation. A permutation p can be expressed as the concatenation
        of len(p.bend_list()) + 1 monotone segments.

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).bend_list()
            [1, 2, 3, 4]
            >>> Perm((2, 0, 1)).bend_list()
            [1]
        """
        return list(self.bends())

    def order(self):
        """Returns the order of the permutation.

        Examples:
            >>> Perm((4, 3, 5, 0, 2, 1)).order()
            6
            >>> Perm((0, 1, 2)).order()
            1
        """
        acc = 1
        for l in map(len, self.cycle_decomp()):
            acc = (acc * l) // fractions.gcd(acc, l)
        return acc

    # TODO: reimplement the following four functions to return generators
    def ltrmin(self):
        """Returns the positions of the left-to-right minima.

        Examples:
            >>> Perm(24301).ltrmin()
            [0, 3]
        """
        L = []
        minval = len(self) + 1
        for idx, val in enumerate(self):
            if val < minval:
                L.append(idx)
                minval = val
        return L

    def rtlmin(self):
        """Returns the positions of the right-to-left minima.

        Examples:
            >>> Perm(204153).rtlmin()
            [1, 3, 5]
        """
        rev_perm = self.reverse()
        return [len(self) - val - 1 for val in rev_perm.ltrmin()][::-1]

    def ltrmax(self):
        """Returns the positions of the left-to-right maxima.

        Examples:
            >>> Perm(204153).ltrmax()
            [0, 2, 4]
        """
        return [len(self)-i-1 for i in Perm(self[::-1]).rtlmax()][::-1]

    def rtlmax(self):
        """Returns the positions of the right-to-left maxima.

        Examples:
            >>> Perm(24301).rtlmax()
            [1, 2, 4]
        """
        return [
            len(self)-i-1 for i in self.complement().reverse().ltrmin()][::-1]

    def count_ltrmin(self):
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self.ltrmin())

    def count_ltrmax(self):
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self.ltrmax())

    def count_rtlmin(self):
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self.rtlmin())

    def count_rtlmax(self):
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self.rtlmax())

    num_ltrmin = count_ltrmin

    def count_inversions(self):
        """Returns the number of inversions of the permutation, i.e., the
        number of pairs i,j such that i < j and self(i) > self(j).

        TODO: Reimplement in NlogN time.

        >>> Perm(3021).count_inversions()
        4
        >>> Perm.monotone_decreasing(6).count_inversions() == 5*6 / 2
        True
        >>> Perm.monotone_increasing(7).count_inversions()
        0
        """

        p = list(self)
        n = self.__len__()
        inv = 0
        for i in range(n):
            for j in range(i+1, n):
                if p[i] > p[j]:
                    inv += 1
        return inv

    inversions = count_inversions

    # TODO: Implement function that returns list of inversions.

    # TODO: Reimplement using count_inversions.
    def count_noninversions(self):
        """Returns the number of noninversions of the permutation, i.e., the
        number of pairs i,j such that i < j and self[i] < self[j].

        Examples:
            >>> Perm((3, 0, 2, 1, 4)).count_noninversions()
            6
            >>> Perm.monotone_increasing(7).count_noninversions() == (6 * 7)/2
            True
        """
        inv = 0
        for i in range(len(self)):
            for j in range(i + 1, len(self)):
                if self[i] < self[j]:
                    inv += 1
        return inv

    def min_gapsize(self):
        """Returns the minimum gap between any two entries in the permutation
        (computed with the taxicab metric).

        TODO: currently uses the naive algorithm --- can be improved

        Examples:
            >>> Perm(2031).min_gapsize()
            3
        """
        min_dist = len(self)
        for i, j in itertools.combinations(range(len(self)), 2):
            h_dist = abs(i - j)
            v_dist = abs(self[i] - self[j])
            dist = h_dist + v_dist
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def count_bonds(self):
        """Counts the number of bonds, that is the number of adjacent locations
        with adjacent values.

        Examples:
            >>> Perm((0, 1, 2)).count_bonds()
            2
            >>> Perm((2, 1, 0)).count_bonds()
            2
            >>> Perm((4, 0, 3, 2, 1, 5)).count_bonds()
            2
        """
        return self.count_dec_bonds() + self.count_inc_bonds()

    num_bonds = count_bonds
    bonds = count_bonds  # permpy backwards compatibility

    def inc_bonds(self):
        """Yields the indices of the increasing bonds, that is the indices of
        the ascents with adjacent values.

        Examples:
            >>> list(Perm((2, 3, 4, 5, 0, 1)).inc_bonds())
            [0, 1, 2, 4]
        """
        for i in range(len(self) - 1):
            if self[i + 1] == self[i] + 1:
                yield i

    def count_inc_bonds(self):
        """Counts the number of increasing bonds.

        Examples:
            >>> Perm((0, 2, 3, 1)).count_inc_bonds()
            1
            >>> Perm((2, 3, 4, 5, 0, 1)).count_inc_bonds()
            4
        """
        return len(list(self.inc_bonds()))

    num_inc_bonds = count_inc_bonds

    def dec_bonds(self):
        """Yields the indices of the decreasing bonds, that is the indices of
        the descents with adjacent values.

        Examples:
            >>> list(Perm((1, 0, 3, 2, 5, 4)).dec_bonds())
            [0, 2, 4]
        """
        for i in range(len(self) - 1):
            if self[i] == self[i + 1] + 1:
                yield i

    def count_dec_bonds(self):
        """Counts the number of decreasing bonds.

        Examples:
            >>> Perm((2, 1, 0, 3)).count_dec_bonds()
            2
            >>> Perm((1, 0, 3, 2, 5, 4)).count_dec_bonds()
            3
        """
        return len(list(self.dec_bonds()))

    num_dec_bonds = count_dec_bonds

    def majorindex(self):
        """Returns the major index of the permutation, that is the sum of the
        positions of the descents of the permutation.

        Examples:
            >>> Perm((3, 1, 2, 4, 0)).majorindex()
            5
            >>> Perm((0, 2, 1)).majorindex()
            2
        """
        desc = list(self.descents())
        return sum(desc) + len(desc)

    def longestruns_ascending(self):
        """Returns the longest ascending runs in the permutation as a pair of
        the length and a list of the starting indices.
        """
        n = self.__len__()
        if n == 0:
            return (0, [])
        p = list(self)
        maxi = 1
        res = []
        cur = 0
        for i in range(1, n):
            if p[i-1] < p[i]:
                if (i - cur + 1) > maxi:
                    del res
                    res = []
                    maxi = i - cur + 1
            else:
                if (i - cur) == maxi:
                    res.append(cur)
                cur = i
        if n - cur == maxi:
            res.append(cur)
        return (maxi, res)

    def longestruns_descending(self):
        """Returns the longest descending runs in the permutation as a pair of
        the length and a list of the starting indices.
        """
        return self.complement().longestruns_ascending()

    def longestruns(self):
        """Returns the longest ascending runs in the permutation as a pair of
        the length and a list of the starting indices.
        """
        return self.longestruns_ascending()

    def length_of_longestrun_ascending(self):
        """Returns the length of the longest ascending run in the permutation.
        """
        return self.longestruns_ascending()[0]

    def length_of_longestrun_descending(self):
        """Returns the length of the longest descending run in the permutation.
        """
        return self.complement().length_of_longestrun_ascending()

    def length_of_longestrun(self):
        """Returns the length of the longest ascending run in the permutation.
        """
        return self.length_of_longestrun_ascending()

    def cycle_decomp(self):
        """Calculates the cycle decomposition of the permutation. Returns a list
        of cycles, each of which is represented as a list.

        >>> Perm((4, 2, 7, 0, 3, 1, 6, 5)).cycle_decomp()
        [[4, 3, 0], [6], [7, 5, 1, 2]]
        """
        n = self.__len__()
        seen = set()
        cyclelist = []
        while len(seen) < n:
            a = max(set(range(n)) - seen)
            cyc = [a]
            b = self(a)
            seen.add(b)
            while b != a:
                cyc.append(b)
                b = self(b)
                seen.add(b)
            cyclelist.append(cyc)
        cyclelist.reverse()
        return cyclelist

    def count_cycles(self):
        """Returns the number of cycles in the permutation.

        >>> Perm((5, 3, 8, 1, 0, 4, 2, 7, 6)).count_cycles()
        4
        """
        return len(self.cycle_decomp())

    num_cycles = count_cycles  # permpy backwards compatibility

    def is_involution(self):
        """Checks if the permutation is an involution, i.e., is equal to it's
        own inverse.

        Examples:
            >>> Perm((2, 1, 0)).is_involution()
            True
            >>> Perm((3, 0, 2, 4, 1, 5)).is_involution()
            False
        """

        return self == self.inverse()

    def is_identity(self):
        """Checks if the permutation is the identity.

        >>> p = Perm.random(10)
        >>> (p * p.inverse()).is_identity()
        True
        """

        return self == Perm.identity(len(self))

    def rank(self):
        """Computes the rank of a permutation.
        Examples:
            >>> Perm((0, 1)).rank()
            2
            >>> Perm((0, 2, 1, 3)).rank()
            12
        """
        if len(self) == 0:
            return 0
        fact = [1]
        for i in range(len(self)):
            fact.append(fact[i] * (i + 1))
        res = 0
        vals = list()
        for i in range(len(self)):
            r = bisect.bisect_left(vals, self[i])
            res += ((self[i] - r) * fact[len(self) - i - 1] +
                    fact[len(self) - i - 1])
            vals.insert(r, self[i])
        return res

    perm2ind = rank  # permpy backwards compatibility

    def threepats(self):
        """Returns a dictionary of the number of occurrences of each
        permutation pattern of length 3.

        Examples:
            >>> res = Perm((2, 1, 0, 3)).threepats()
            >>> res[Perm((1, 0, 2))]
            3
            >>> res[Perm((1, 2, 0))]
            0
        """
        patnums = {Perm((0, 1, 2)): 0, Perm((0, 2, 1)): 0, Perm((1, 0, 2)): 0,
                   Perm((1, 2, 0)): 0, Perm((2, 0, 1)): 0, Perm((2, 1, 0)): 0}
        for i, j, k in itertools.combinations(range(len(self)), 3):
            patnums[Perm.to_standard((self[i], self[j], self[k]))] += 1
        return patnums

    def fourpats(self):
        """Returns a dictionary of the number of occurrences of each
        permutation pattern of length 4.

        Examples:
            >>> res = Perm((1, 0, 3, 5, 2, 4)).fourpats()
            >>> res[Perm((0, 2, 3, 1))]
            2
            >>> res[Perm((3, 1, 2, 0))]
            0
        """
        patnums = {Perm((0, 1, 2, 3)): 0, Perm((0, 1, 3, 2)): 0,
                   Perm((0, 2, 1, 3)): 0, Perm((0, 2, 3, 1)): 0,
                   Perm((0, 3, 1, 2)): 0, Perm((0, 3, 2, 1)): 0,
                   Perm((1, 0, 2, 3)): 0, Perm((1, 0, 3, 2)): 0,
                   Perm((1, 2, 0, 3)): 0, Perm((1, 2, 3, 0)): 0,
                   Perm((1, 3, 0, 2)): 0, Perm((1, 3, 2, 0)): 0,
                   Perm((2, 0, 1, 3)): 0, Perm((2, 0, 3, 1)): 0,
                   Perm((2, 1, 0, 3)): 0, Perm((2, 1, 3, 0)): 0,
                   Perm((2, 3, 0, 1)): 0, Perm((2, 3, 1, 0)): 0,
                   Perm((3, 0, 1, 2)): 0, Perm((3, 0, 2, 1)): 0,
                   Perm((3, 1, 0, 2)): 0, Perm((3, 1, 2, 0)): 0,
                   Perm((3, 2, 0, 1)): 0, Perm((3, 2, 1, 0)): 0}

        for i, j, k, l in itertools.combinations(range(len(self)), 4):
            patnums[Perm.to_standard((self[i], self[j],
                                      self[k], self[l]))] += 1
        return patnums

    def rank_val(self, i):
        """Returns the 'rank value'(?) of index i, the number of inversions
        with the value at i being the greater element.


        Examples:
            >>> Perm((3, 0, 2, 1)).rank_val(0)
            3
            >>> Perm((0, 2, 4, 3, 1)).rank_val(1)
            1
        """
        return len([j for j in range(i + 1, len(self)) if self[j] < self[i]])

    def rank_encoding(self):
        """Returns the 'rank value'(?) of each index in the permutation, the
        number of inversions 'caused' by the values at each index.

        Examples:
            >>> Perm((3, 0, 2, 1)).rank_encoding()
            [3, 0, 1, 0]
            >>> Perm((0, 2, 4, 3, 1)).rank_encoding()
            [0, 1, 2, 1, 0]
        """
        return [self.rank_val(i) for i in range(len(self))]

    #
    # Decomposition and generation from self methods
    #

    def block_decomposition(self, return_patterns=False):
        """Returns the list of all blocks(intervals) in the permutation that
        are of length at least 2. The returned list of lists contains the
        indices of blocks of length i in index i.

        When return_patterns is set to True, a list of patterns is returned
        instead of list of list of indices.

        Examples:
            >>> Perm((5, 3, 0, 1, 2, 4, 7, 6)).block_decomposition()
            [[], [], [2, 3, 6], [2], [1], [1], [0], []]
            >>> sorted(Perm((4, 1, 0, 5, 2, 3)).block_decomposition(True))
            [Perm((0, 1)), Perm((1, 0))]
        """
        blocks = [[] for i in range(len(self))]
        for start in range(0, len(self)):
            mn, mx = self[start], self[start]
            for length in range(2, len(self) - start + 1):
                if length == len(self):
                    continue
                end = start + length - 1
                mn, mx = min(mn, self[end]), max(mx, self[end])
                if mx - mn == length - 1:
                    blocks[length].append(start)

        if return_patterns:
            patterns = set()
            for length in range(0, len(blocks)):
                for start in blocks[length]:
                    patterns.add(Perm.to_standard(self[start:start + length]))
            return list(patterns)
        else:
            return blocks

    all_intervals = block_decomposition  # permpy backwards compatibility
    decomposition = block_decomposition

    def monotone_block_decomposition(self, with_ones=False):
        """Returns the list of all monotone blocks(intervals) in the
        permutation. Depending on the with_ones parameter it will return the
        length 1 blocks. The blocks are pairs of indices, the start and end
        index.

        Examples:
            >>> Perm((2, 6, 3, 7, 4, 5, 1, 0)).monotone_block_decomposition()
            [(4, 5), (6, 7)]
            >>> Perm((2, 6, 3, 4, 5, 1, 0)).monotone_block_decomposition(True)
            [(0, 0), (1, 1), (2, 4), (5, 6)]
            >>> Perm((0, 1, 2, 3, 4, 5)).monotone_block_decomposition()
            [(0, 5)]
        """
        blocks = []
        diff = 0
        start = 0
        length = 0
        for i in range(1, len(self)):
            if (math.fabs(self[i] - self[i - 1]) == 1 and
                    (length == 0 or self[i] - self[i - 1] == diff)):
                length += 1
                diff = self[i] - self[i - 1]
            else:
                blocks.append((start, start + length))
                start = i
                length = 0
                diff = 0
        if len(self):
            blocks.append((start, start + length))

        if with_ones:
            return blocks
        return [block for block in blocks if block[1] - block[0] > 0]

    def monotone_block_decompositon_ascending(self, with_ones=False):
        # TODO: test, untested
        # TODO: rename to refer to runs, which this function basically
        #       computes, brakes the permutation up into its runs.
        blocks = []
        start = 0
        length = 0
        for i in range(1, len(self)):
            if self[i] + 1 == self[i - 1]:
                length += 1
            else:
                blocks.append((start, start + length))
                start = i
                length = 0
        if len(self):
            blocks.append((start, start + length))

        if with_ones:
            return blocks
        return [block for block in blocks if block[1] - block[0] > 0]

    def monotone_block_decompositon_descending(self, with_ones=False):
        # TODO: test, untested
        return self.complement().monotone_block_decomposition_ascending(
            with_ones)

    # permpy backwards compatibility
    all_monotone_intervals = monotone_block_decomposition

    def monotone_quotient(self):
        """Return the permutation pattern consisting of the starting values of
        the monotone blocks in the permutation. Simply contracts the monotone
        blocks.

        Examples:
            >>> Perm((0, 2, 1, 5, 6, 4, 3)).monotone_block_decomposition(True)
            [(0, 0), (1, 2), (3, 4), (5, 6)]
            >>> Perm((0, 2, 1, 5, 6, 4, 3)).monotone_quotient()
            Perm((0, 1, 3, 2))
        """
        return Perm.to_standard(
            [self[start] for (start, end) in
             self.monotone_block_decomposition(with_ones=True)])

    def maximum_block(self):
        '''Finds the biggest interval, and returns (i,j) is one is found,
        where i is the size of the interval, and j is the index of the first
        entry in the interval.

        Returns (0,0) if no interval is found, i.e., if the permutation is
        simple.

        Example:
            >>> Perm((0, 2, 1, 5, 6, 7, 4, 3)).maximum_block()
            (7, 1)
        '''
        blocks = self.block_decomposition()
        for length, indexlist in reversed(list(enumerate(blocks))):
            if len(indexlist):
                return (length, indexlist[0])
        return (0, 0)

    maximal_interval = maximum_block  # permpy backwards compatibility

    def simple_location(self):
        '''Searches for an interval, and returns (i,j) if one is found, where i
        is the size of the interval, and j is the first index of the interval.

        Returns (0,0) if no interval is found, i.e., if the permutation is
        simple.

        Simply calls the Perm.maximum_block(), the maximum block is any block.
        '''
        return self.maximum_block()

    def is_simple(self):
        """Checks if the permutation is simple.

        Example:
            >>> Perm((2, 0, 3, 1)).is_simple()
            True
            >>> Perm((2, 0, 1)).is_simple()
            False
        """
        (i, j) = self.simple_location()
        return i == 0

    def is_strongly_simple(self):
        """Checks if the permutation is strongly simple, that is if the
        permutation is simple and any of permutation of one less length in the
        downset is simple.

        Example:
            >>> Perm((4, 1, 6, 3, 0, 7, 2, 5)).is_strongly_simple()
            True
        """
        return self.is_simple() and all([p.is_simple()
                                         for p in self.children()])

    def children(self):
        """Returns all patterns of length one less than the permutation. One
        layer of the downset, also called the shadow.

        Example:
            >>> sorted(Perm((2, 0, 1)).children())
            [Perm((0, 1)), Perm((1, 0))]
            >>> sorted(Perm((4, 1, 6, 3, 0, 7, 2, 5)).children())[:2]
            [Perm((1, 5, 3, 0, 6, 2, 4)), Perm((3, 0, 5, 2, 6, 1, 4))]
        """
        return list(set(self.remove(i) for i in range(len(self))))

    shrink_by_one = children

    # TODO: discuss return value conventions, should this return PermSet
    # instead of set of Perm? maybe list of Perm?
    def coveredby(self):
        """Returns one layer of the upset of the permutation.

        Examples:
            >>> sorted(Perm((0, 1)).coveredby())[:3]
            [Perm((0, 1, 2)), Perm((0, 2, 1)), Perm((1, 0, 2))]
        """
        S = set()
        n = len(self)
        for i in range(n + 1):
            for j in range(n + 1):
                S.add(self.insert(i, j))
        return list(S)

    # TODO: discuss return value conventions, should this return PermSet
    # instead of set of Perm? maybe list of Perm?
    def buildupset(self, height):
        """Returns height-th layer of the upset of the permutation
        """
        n = len(self)
        L = [set() for i in range(n)]
        L.append(set([self]))
        for i in range(n + 1, height):
            oldS = list(L[i - 1])
            newS = set()
            for perm in oldS:
                newS = newS.union(perm.coveredby())
            L.append(newS)
        return L

    def sum_indecomposable_sequence(self):
        S = self.downset()
        return [len([p for p in S if len(p) == i and not p.sum_decomposable()])
                for i in range(1, max([len(p) for p in S])+1)]

    def count_rtlmax_ltrmin_layers(self):
        """Counts the layers in the right-to-left maxima, left-to-right minima
        decomposition.
        """
        return len(self.rtlmax_ltrmin_decomposition())

    num_rtlmax_ltrmin_layers = count_rtlmax_ltrmin_layers

    def rtlmax_ltrmin_decomposition(self):
        """Returns the right-to-left maxima, left-to-right minima
        decomposition. The decomposition consists of layers, starting with the
        first layer which is union of the right-to-left maximas and the
        left-to-right minimas and the next layer is defined similarly for the
        permutation with the first layer removed and so on.

        TODO: If this function is to be kept, then it probably should return
        the layers as indices in the original permutation.
        """
        P = Perm(self)
        num_layers = 0
        layers = []
        while len(P) > 0:
            num_layers += 1
            positions = sorted(list(set(P.rtlmax()+P.ltrmin())))
            layers.append(positions)
            P = Perm([P[i] for i in range(len(P)) if i not in positions])
        return layers

    #
    # Pattern matching methods
    #

    def contains(self, *patts):
        """Check if self contains patts.

        Args:
            self:
                A perm.
            patts: <permuta.Patt> argument list
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
            patts: <permuta.Patt> argument list
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
            patt: <permuta.Patt>
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
        # k is how many elements of the perm have already been added to
        # occurrence
        def occurrences(i, k):
            elements_remaining = len(perm) - i
            elements_needed = len(self) - k

            # Get the following variables:
            #   - lfi: Left Floor Index
            #   - lci: Left Ceiling Index
            #   - lbp: Lower Bound Pre-computation
            #   - ubp: Upper Bound Pre-computation
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
                # In this case, ubp = len(self) - self[k]
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
                # Increment i, that also means elements_remaining should
                # decrement
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
            patt: <permuta.Patt>
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
                        else self[fac_indices.ceiling] - base_element,)
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
            ValueError: Length mismatch
        """
        iterable = tuple(iterable)
        if len(iterable) != len(self):
            raise ValueError("Length mismatch")
        return tuple(iterable[index] for index in self)

    permute = apply  # Alias of Perm.apply

    #
    # Visualization methods
    #
    def _ascii_plot(self):
        """Prints a simple plot of the given Permutation."""
        n = self.__len__()
        array = [[' ' for i in range(n)] for j in range(n)]
        for i in range(n):
            array[self[i]][i] = '*'
        array.reverse()
        s = '\n'.join((' '.join(l) for l in array))
        return s

    def cycle_notation(self):
        """Returns the cycle notation representation of the permutation.

        Examples:
            >>> Perm((5, 3, 0, 1, 2, 4)).cycle_notation()
            '( 3 1 ) ( 5 4 2 0 )'
            """
        if len(self) == 0:
            return '( )'
        base = 0
        stringlist = ['( ' + ' '.join([str(x + base) for x in cyc]) + ' )'
                      for cyc in self.cycle_decomp()]
        return ' '.join(stringlist)

    cycles = cycle_notation  # permpy backwards compatibility

    def plot(self, show=True, ax=None, use_mpl=True, fname=None, **kwargs):
        """Draws a matplotlib plot of the permutation. Can be used for both
        quick visualization, or to build a larger figure. Unrecognized
        arguments are passed as options to the axes object to allow for
        customization (i.e., setting a figure title, or setting labels on the
        axes). Falls back to an ascii_plot if matplotlib isn't found, or if
        use_mpl is set to False.
        """
        # TODO: check if matplotlib is imported
        # TODO: either remove or implement this function, currently not making
        #       sense
        if not use_mpl:
            return self._ascii_plot()
        xs = [val for val in range(len(self))]
        ys = [val for val in self]
        plt = None
        if not ax:
            ax = plt.gca()
        # scat = ax.scatter(xs, ys, s=40, c='k')
        ax_settings = {'xticks': xs, 'yticks': ys,
                       'xticklabels': '', 'yticklabels': '',
                       'xlim': (min(xs) - 1, max(xs) + 1),
                       'ylim': (min(ys) - 1, max(ys) + 1)}
        ax.set(**ax_settings)
        ax.set(**kwargs)
        ax.set_aspect('equal')
        if fname:
            fig = plt.gcf()
            fig.savefig(fname, dpi=300)
        if show:
            plt.show()
        return ax

    def to_tikz(self):
        s = r'\begin{tikzpicture}'
        s += r'[scale=.3,baseline=(current bounding box.center)]'
        s += '\n\t'
        s += r'\draw[ultra thick] (1,0) -- ('+str(len(self))+',0);'
        s += '\n\t'
        s += r'\draw[ultra thick] (0,1) -- (0,'+str(len(self))+');'
        s += '\n\t'
        s += r'\foreach \x in {1,...,'+str(len(self))+'} {'
        s += '\n\t\t'
        s += r'\draw[thick] (\x,.09)--(\x,-.5);'
        s += '\n\t\t'
        s += r'\draw[thick] (.09,\x)--(-.5,\x);'
        s += '\n\t'
        s += r'}'
        for (i, e) in enumerate(self):
            s += '\n\t'
            s += r'\draw[fill=black] ('+str(i+1)+','+str(e+1)+') circle (5pt);'
        s += '\n'
        s += r'\end{tikzpicture}'
        return s

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
            raise TypeError(
                "'{}' object is not an integer".format(repr(value)))
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
        return self.compose(other)

    def __repr__(self):
        return "Perm({})".format(super(Perm, self).__repr__())

    def __lt__(self, other):
        return (len(self), tuple(self)) < (len(other), tuple(other))

    def __le__(self, other):
        return (len(self), tuple(self)) <= (len(other), tuple(other))

    def __gt__(self, other):
        return other.__lt__(self)

    def __ge__(self, other):
        return other.__le__(self)

    def __contains__(self, patt):
        """Check if self contains patt.

        Args:
            self:
                A perm.
            patt: <permuta.Patt>
                A classical/mesh pattern.

        Returns: <bool>
            True if and only if the pattern patt is contained in self.
        """
        return any(True for _ in patt.occurrences_in(self))
