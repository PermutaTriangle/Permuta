import collections
import itertools
import math
import numbers
import operator
import random
import sys

from permuta import Pattern, Rotatable, Shiftable, Flippable
from permuta.misc import left_floor_and_ceiling

if sys.version_info.major == 2:
    range = xrange


class Permutation(tuple, Pattern, Rotatable, Shiftable, Flippable):
    """A permutation class."""

    _TYPE_ERROR = "'{}' object is not a Permutation"

    def __new__(cls, iterable=(), check=False):
        """Return a Permutation instance.

        Args:
            cls:
                The class of which an instance is requested.
            iterable: <collections.Iterable> or <numbers.Integral>
                An iterable corresponding to a legal permutation.
                Also supports passing just a number with unique digits.
            check: <bool>
                If True, iterable will be confirmed to correspond to a legal permutation.

        Raises:
            TypeError:
                Bad argument.

        Examples:
            >>> Permutation((0,3,1,2))
            Permutation((0, 3, 1, 2))
            >>> Permutation(range(5, -1, -1))
            Permutation((5, 4, 3, 2, 1, 0))
            >>> Permutation(6012354)
            Permutation((6, 0, 1, 2, 3, 5, 4))
            >>> Permutation("abc")  # Not good
            Permutation(('a', 'b', 'c'))
            >>> Permutation("abc", check=True)
            Traceback (most recent call last):
                ...
            TypeError: Non-integer type: 'a'
        """
        try:
            return super(Permutation, cls).__new__(cls, iterable)
        except TypeError:
            if isinstance(iterable, numbers.Integral):
                number = iterable
                if not (0 <= number <= 9876543210):
                    raise TypeError("Bad integer {}".format(number))
                iterable = []
                if number == 0:
                    iterable.append(number)
                else:
                    while number != 0:
                        iterable.append(number % 10)
                        number //= 10
                    iterable = reversed(iterable)
                return super(Permutation, cls).__new__(cls, iterable)
            else:
                raise

    def __init__(self, iterable=(), check=False):
        # TODO: Docstring
        if check:
            used = [False]*len(self)
            for value in self:
                if not isinstance(value, numbers.Integral):
                    message = "Non-integer type: {}".format(repr(value))
                    raise TypeError(message)
                assert 0 <= value < len(self), "Out of range: {}".format(value)
                assert not used[value], "Duplicate element: {}".format(value)
                used[value] = True
        self._cached_pattern_details = None

    @classmethod
    def to_standard(cls, iterable):
        """Return the permutation corresponding to iterable.

        Duplicate elements are allowed and become consecutive elements (see example).

        The standardize alias is supplied for backwards compatibility with permpy.
        However, the permpy version did not allow for duplicate elements.

        Examples:
            >>> Permutation.to_standard("a2gsv3")
            Permutation((2, 0, 3, 4, 5, 1))
            >>> Permutation.to_standard("caaba")
            Permutation((4, 0, 1, 3, 2))
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
    from_iterable = to_standard  # TODO: Acceptable alias?

    @classmethod
    def identity(cls, length):
        """Return the identity permutation of the specified length.

        Examples:
            >>> Permutation.identity(0)
            Permutation(())
            >>> Permutation.identity(4)
            Permutation((0, 1, 2, 3))
        """
        return cls(range(length))

    @classmethod
    def random(cls, length):
        """Return a random permutation of the specified length.

        Examples:
            >>> perm = Permutation.random(8)
            >>> len(perm) == 8
            True
            >>> # TODO: test perm in Permutations(8)
            >>> perm = Permutation(perm, check=True)
        """
        result = list(range(length))
        random.shuffle(result)
        return cls(result)

    @classmethod
    def monotone_increasing(cls, length):
        """Return a monotone increasing permutation of the specified length.

        Examples:
            >>> Permutation.monotone_increasing(0)
            Permutation(())
            >>> Permutation.monotone_increasing(4)
            Permutation((0, 1, 2, 3))
        """
        return cls(range(length))

    @classmethod
    def monotone_decreasing(cls, length):
        """Return a monotone decreasing permutation of the specified length.

        Examples:
            >>> Permutation.monotone_decreasing(0)
            Permutation(())
            >>> Permutation.monotone_decreasing(4)
            Permutation((3, 2, 1, 0))
        """
        return cls(range(length-1, -1, -1))

    @classmethod
    def unrank(cls, number, length=None):
        """

        Examples:
            >>> Permutation.unrank(0)
            Permutation(())
            >>> Permutation.unrank(1)
            Permutation((0,))
            >>> Permutation.unrank(2)
            Permutation((0, 1))
            >>> Permutation.unrank(3)
            Permutation((1, 0))
            >>> Permutation.unrank(4)
            Permutation((0, 1, 2))
            >>> Permutation.unrank(5)
            Permutation((0, 2, 1))
        """
        # TODO: Docstring, and do better? Assertions and messages
        # TODO: The unrank function in permpy was not a good/correct one
        # TODO: Implement readably, nicely, and efficiently
        #assert isinstance(number, numbers.Integral)
        #assert 0 <= number
        if length is None:
            # Work out the length and number from the number given
            assert isinstance(number, numbers.Integral)
            assert number >= 0
            if number == 0:
                return cls()
            length = 1
            amount = 1  # Amount of permutations of length
            while number > amount:
                number -= amount
                length += 1
                amount *= length
            number -= 1
        else:
            assert isinstance(length, numbers.Integral)
            assert length >= 0
            assert 0 <= number < math.factorial(length)
        return cls(Permutation.__unrank(number, length))

    @staticmethod
    def __unrank(number, length):
        candidates = list(range(length))
        for value in range(1, length+1):
            factorial = math.factorial(length - value)
            division = number//factorial
            yield candidates.pop(division)
            number %= factorial

    ind2perm = unrank  # permpy backwards compatibility

    # TODO: This one will not be a class method
    #perm2ind = rank  # permpy backwards compatibility

    def contains(self, *patts):
        """Check if self contains patts.

        Args:
            self:
                A permutation.
            patts: <permuta.Pattern> argument list
                Classical/mesh patterns.

        Returns: <bool>
            True if and only if all patterns in patt are contained in self.

        Examples:
            >>> Permutation.monotone_decreasing(7).avoids(Permutation((0, 1)))
            True
            >>> Permutation((4, 2, 3, 1, 0)).contains(Permutation((1, 2, 0)))
            True
            >>> Permutation((0, 1, 2)).contains(Permutation((1,0)))
            False
            >>> pattern1 = Permutation((0, 1))
            >>> pattern2 = Permutation((2, 0, 1))
            >>> pattern3 = Permutation((0, 3, 1, 2))
            >>> Permutation((5, 3, 0, 4, 2, 1)).contains(pattern1, pattern2)
            True
            >>> Permutation((5, 3, 0, 4, 2, 1)).contains(pattern2, pattern3)
            False
        """
        return all(patt in self for patt in patts)

    def avoids(self, *patts):
        """Check if self avoids patts.

        Args:
            self:
                A permutation.
            patts: <permuta.Pattern> argument list
                Classical/mesh patterns.

        Returns: <bool>
            True if and only if self avoids all patterns in patts.

        Examples:
            >>> Permutation.monotone_increasing(8).avoids(Permutation((1, 0)))
            True
            >>> Permutation((4, 2, 3, 1, 0)).avoids(Permutation((1, 2, 0)))
            False
            >>> Permutation((0, 1, 2)).avoids(Permutation((1,0)))
            True
            >>> pattern1 = Permutation((0, 1))
            >>> pattern2 = Permutation((2, 0, 1))
            >>> pattern3 = Permutation((0, 3, 1, 2))
            >>> pattern4 = Permutation((0, 1, 2))
            >>> Permutation((5, 3, 0, 4, 2, 1)).avoids(pattern1, pattern2)
            False
            >>> Permutation((5, 3, 0, 4, 2, 1)).avoids(pattern2, pattern3)
            False
            >>> Permutation((5, 3, 0, 4, 2, 1)).avoids(pattern3, pattern4)
            True
        """
        return all(patt not in self for patt in patts)

    def avoids_set(patts):
        """Check if self avoids patts.

        This method is for backwards compatibility with permpy.
        """
        return self.avoids(*tuple(patts))

    def count_occurrences_of(self, patt):
        """Count the number of occurrences of patt in self.

        Args:
            self:
                A permutation.
            patt: <permuta.Pattern>
                A classical/mesh pattern.

        Returns: <int>
            The number of times patt occurs in self.

        Examples:
            >>> Permutation((0, 1, 2)).count_occurrences_of(Permutation((0, 1)))
            3
            >>> Permutation((5, 3, 0, 4, 2, 1)).count_occurrences_of(Permutation((2, 0, 1)))
            6
        """
        return patt.count_occurrences_in(self)

    occurrences = count_occurrences_of  # permpy backwards compatibility

    def occurrences_in(self, perm):
        """Find all indices of occurrences of self in perm.

        Args:
            self:
                The classical pattern whose occurrences are to be found.
            perm: <permuta.Permutation>
                The permutation to search for occurrences in.

        Yields: <tuple> of <int>
            The indices of the occurrences of self in perm.
            Each yielded element l is a tuple of integer indices of the
            permutation perm such that:
            self == permuta.Permutation.to_standard([perm[i] for i in l])

        Examples:
            >>> list(Permutation((2, 0, 1)).occurrences_in(Permutation((5, 3, 0, 4, 2, 1))))
            [(0, 1, 3), (0, 2, 3), (0, 2, 4), (0, 2, 5), (1, 2, 4), (1, 2, 5)]
            >>> list(Permutation((1, 0)).occurrences_in(Permutation((1, 2, 3, 0))))
            [(0, 3), (1, 3), (2, 3)]
            >>> list(Permutation((0,)).occurrences_in(Permutation((1, 2, 3, 0))))
            [(0,), (1,), (2,), (3,)]
            >>> list(Permutation().occurrences_in(Permutation((1, 2, 3, 0))))
            [()]
        """
        # Special cases
        if len(self) == 0:
            # Pattern is empty, occurs in all permutations
            # This is needed for the occurrences function to work correctly
            yield ()
            return
        if len(self) > len(perm):
            # Pattern is too long to occur in permutation
            return

        # The indices of the occurrence in perm
        occurrence_indices = [None]*len(self)

        # Get left to right scan details
        pattern_details = self._pattern_details()

        # Upper and lower bound declarations
        upper_bound = None
        lower_bound = None

        # Define function that works with the above defined variables
        # i is the index of the element in perm that is to be considered
        # k is how many elements of the permutation have already been added to occurrence
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

        This method is complementary to permuta.Permutation.occurrences_in.
        It just calls patt.occurrences_in(self) internally.
        See permuta.Permutation.occurrences_in for documentation.

        Args:
            self:
                A permutation.
            patt: <permuta.Pattern>
                A classical/mesh pattern.

        Yields: <tuple> of <int>
            The indices of the occurrences of self in perm.

        Examples:
            >>> list(Permutation((5, 3, 0, 4, 2, 1)).occurrences_of(Permutation((2, 0, 1))))
            [(0, 1, 3), (0, 2, 3), (0, 2, 4), (0, 2, 5), (1, 2, 4), (1, 2, 5)]
            >>> list(Permutation((1, 2, 3, 0)).occurrences_of(Permutation((1, 0))))
            [(0, 3), (1, 3), (2, 3)]
            >>> list(Permutation((1, 2, 3, 0)).occurrences_of(Permutation((0,))))
            [(0,), (1,), (2,), (3,)]
            >>> list(Permutation((1, 2, 3, 0)).occurrences_of(Permutation()))
            [()]
        """
        return patt.occurrences_in(self)

    def _pattern_details(self):
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

    def apply(self, iterable):
        """Permute an iterable using the permutation.

        Args:
            self:
                A permutation.
            iterable: <collections.Iterable>
                An iterable of len(self) elements.

        Returns: <tuple>
            The elements of iterable in the permuted order.

        Raises:
            TypeError:
                Bad argument.

        Examples:
            >>> Permutation((4, 1, 2, 0, 3)).apply((1, 2, 3, 4, 5))
            (5, 2, 3, 1, 4)
            >>> Permutation((4, 1, 2, 0, 3)).apply("abcde")
            ('e', 'b', 'c', 'a', 'd')
            >>> Permutation((1, 2, 0, 3)).apply("abcde")
            Traceback (most recent call last):
                ...
            TypeError: Length mismatch
        """
        iterable = tuple(iterable)
        if len(iterable) != len(self):
            raise TypeError("Length mismatch")
        return tuple(iterable[index] for index in self)

    permute = apply  # Alias of Permutation.apply

    def direct_sum(self, *others):
        """Return the direct sum of two or more permutations.

        Args:
            self:
                A permutation.
            others: <permuta.Permutation> argument list
                Permutations.

        Returns: <permuta.Permutation>
            The direct sum of all the permutations.

        Examples:
            >>> Permutation((0,)).direct_sum(Permutation((1, 0)))
            Permutation((0, 2, 1))
            >>> Permutation((0,)).direct_sum(Permutation((1, 0)), Permutation((2, 1, 0)))
            Permutation((0, 2, 1, 5, 4, 3))
        """
        result = list(self)
        shift = len(self)
        for index in range(len(others)):
            other = others[index]
            if not isinstance(other, Permutation):
                raise TypeError(Permutation._TYPE_ERROR.format(repr(other)))
            result.extend(element + shift for element in other)
            shift += len(other)
        return Permutation(result)

    def skew_sum(self, *others):
        """Return the skew sum of two or more permutations.

        Args:
            self:
                A permutation.
            others: <permuta.Permutation> argument list
                Permutations.

        Returns: <permuta.Permutation>
            The skew sum of all the permutations.

        Examples:
            >>> Permutation((0,)).skew_sum(Permutation((0, 1)))
            Permutation((2, 0, 1))
            >>> Permutation((0,)).skew_sum(Permutation((0, 1)), Permutation((2, 1, 0)))
            Permutation((5, 3, 4, 2, 1, 0))
        """
        shift = sum(len(other) for other in others)
        result = [element + shift for element in self]
        for index in range(len(others)):
            other = others[index]
            if not isinstance(other, Permutation):
                raise TypeError(Permutation._TYPE_ERROR.format(repr(other)))
            shift -= len(other)
            result.extend(element + shift for element in other)
        return Permutation(result)

    def inverse(self):
        """Return the inverse of the permutation self.

        Examples:
            >>> Permutation((1, 2, 5, 0, 3, 4)).inverse()
            Permutation((3, 0, 1, 4, 5, 2))
            >>> Permutation((2, 0, 1)).inverse().inverse() == Permutation((2, 0, 1))
            True
            >>> Permutation((0, 1)).inverse()
            Permutation((0, 1))
        """
        len_perm = len(self)
        result = [None]*len_perm
        for index in range(len_perm):
            result[self[index]] = index
        return Permutation(result)

    def reverse(self):
        """Return the reverse of the permutation self.

        Examples:
            >>> Permutation((1, 2, 5, 0, 3, 4)).reverse()
            Permutation((4, 3, 0, 5, 2, 1))
            >>> Permutation((0, 1)).reverse()
            Permutation((1, 0))
        """
        return Permutation(self[::-1])

    def complement(self):
        """Return the complement of the permutation self.

        Examples:
            >>> Permutation((1, 2, 3, 0, 4)).complement()
            Permutation((3, 2, 1, 4, 0))
            >>> Permutation((2, 0, 1)).complement()
            Permutation((0, 2, 1))
        """
        base = len(self) - 1
        return Permutation(base - element for element in self)

    def reverse_complement(self):
        """Return the reverse complement of self.

        Equivalent to two left or right rotations.

        Examples:
            >>> Permutation((1, 2, 3, 0, 4)).reverse_complement()
            Permutation((0, 4, 1, 2, 3))
            >>> Permutation((2, 0, 1)).reverse_complement()
            Permutation((1, 2, 0))
        """
        base = len(self) - 1
        return Permutation(base - element for element in reversed(self))

    def shift_right(self, times=1):
        """Return self shifted times steps to the right.

        If shift is negative, shifted to the left.

        Examples:
            >>> Permutation((0, 1, 2)).shift_right()
            Permutation((2, 0, 1))
            >>> Permutation((0, 1, 2)).shift_right(-4)
            Permutation((1, 2, 0))
        """
        if len(self) == 0:
            return self
        times = times % len(self)
        if times == 0:
            return self
        index = len(self) - times
        slice_1 = itertools.islice(self, index)
        slice_2 = itertools.islice(self, index, len(self))
        return Permutation(itertools.chain(slice_2, slice_1))

    def shift_up(self, times=1):
        """Return self shifted times steps up.

        If times is negative, shifted down.

        Examples:
            >>> Permutation((0, 1, 2, 3)).shift_up(2)
            Permutation((2, 3, 0, 1))
            >>> Permutation((0, 1, 2, 3)).shift_up(-7)
            Permutation((1, 2, 3, 0))
            >>> Permutation((0,)).shift_up(1234)
            Permutation((0,))
        """
        times = times % len(self)
        if times == 0:
            return self
        bound = len(self)
        return Permutation((element + times) % bound for element in self)

    def flip_horizontal(self):
        """Return self flipped horizontally.
        
        Examples:
            >>> Permutation((1, 2, 3, 0, 4)).flip_horizontal()
            Permutation((3, 2, 1, 4, 0))
            >>> Permutation((2, 0, 1)).flip_horizontal()
            Permutation((0, 2, 1))
        """
        return self.complement()

    def flip_vertical(self):
        """Return self flipped vertically.

        Examples:
            >>> Permutation((1, 2, 5, 0, 3, 4)).flip_vertical()
            Permutation((4, 3, 0, 5, 2, 1))
            >>> Permutation((0, 1)).flip_vertical()
            Permutation((1, 0))
        """
        return self.reverse()

    def flip_diagonal(self):
        """Return self flipped along the diagonal, y = x."""
        return self.inverse()

    def flip_antidiagonal(self):
        """Return self flipped along the antidiagonal, y = len(perm) - x.

        Examples:
            >>> Permutation((3, 2, 0, 1)).flip_antidiagonal()
            Permutation((3, 2, 0, 1))
            >>> Permutation((1, 2, 3, 0, 4)).flip_antidiagonal()
            Permutation((0, 2, 3, 4, 1))
            >>> Permutation((1, 2, 0, 3)).flip_antidiagonal()
            Permutation((0, 2, 3, 1))
        """
        len_perm = len(self)
        result = [None]*len_perm

        flipped_pairs = ((len_perm-element-1, len_perm-index-1)
                         for index, element in enumerate(self))

        for index, element in flipped_pairs:
            result[index] = element
        return Permutation(result)

    def _rotate_right(self):
        """Return self rotated 90 degrees to the right."""
        len_perm = len(self)
        result = [None]*len_perm
        for index, value in enumerate(self):
            result[value-1] = len_perm - index
        return Permutation(result)

    def _rotate_left(self):
        """Return self rotated 90 degrees to the left."""
        len_perm = len(self)
        result = [None]*len_perm
        for index, value in enumerate(self):
            result[len_perm - value] = index + 1
        return Permutation(result)

    def _rotate_180(self):
        """Return self rotated 180 degrees."""
        return self.reverse_complement()

    def is_increasing(self):
        """Return True if the permutation is increasing, and False otherwise."""
        for index in range(len(self)):
            if self[index] != index+1:
                return False
        return True

    def is_decreasing(self):
        """Return True if the permutation is decreasing, and False otherwise."""
        len_perm = len(self)
        for index in range(len_perm):
            if self[index] != len_perm - index:
                return False
        return True

    def fixed_points(self):
        """Return the number of fixed points in self."""
        result = 0
        value = 1
        for element in self:
            if element == value:
                result += 1
            value += 1
        return result

    def descents(self):
        """Yield the indices of the descents of self."""
        for index in range(1, len(self)):
            if self[index-1] > self[index]:
                yield index

    def descent_set(self):
        """Return the list of descents of self.

        This method is for backwards compatibility with permpy.
        """
        return list(self.descents())

    def count_descents(self):
        """Count the number of descents of self."""
        return sum(1 for _ in self.descents())

    num_descents = count_descents  # permpy backwards compatibility

    def ascents(self):
        """Yield the indices of the ascent of self."""
        for index in range(1, len(self)):
            if self[index-1] < self[index]:
                yield index

    def ascent_set(self):
        """Return the list of ascents of self.

        This method is for backwards compatibility with permpy.
        """
        return list(self.ascents())

    def count_ascents(self):
        """Count the number of ascents in self."""
        return sum(1 for _ in self.ascents())

    num_ascents = count_ascents  # permpy backwards compatibility

    def peaks(self):
        """Yield the indices of the peaks of self.

        The i-th element of a permutation is a peak if
            self[i-1] < self[i] > self[i+1].
        """
        # TODO: Have an argument about docstrings with Murray
        if len(self) <= 2:
            return
        ascent = False
        for index in range(1, len(self)-1):
            if self[index-1] < self[index]:
                # Permutation ascended
                ascent = True
            else:
                # Permutation descended
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
        """Count the number of peaks of self."""
        return sum(1 for _ in self.peaks())

    num_peaks = count_peaks  # permpy backwards compatibility

    def valleys(self):
        """Yield the indices of the valleys of self.

        The i-th element of a permutation is a valley if
            self[i-1] > self[i] < self[i+1].
        """
        # TODO: Have an argument about docstrings with Murray
        if len(self) <= 2:
            return
        ascent = True
        for index in range(1, len(self)-1):
            if self[index-1] < self[index]:
                # Permutation ascended
                if not ascent:
                    yield index-1
                ascent = True
            else:
                # Permutation descended
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
        """Count the number of valleys of self."""
        return sum(1 for _ in self.valleys())

    num_valleys = count_valleys  # permpy backwards compatibility

    def __call__(self, value):
        # TODO: Docstring
        assert isinstance(value, numbers.Integral)  # TODO: Message
        assert 0 <= value < len(self)  # TODO: Message
        return self[value]

    def __add__(self, other):
        """Return the direct sum of the permutations self and other."""
        return self.direct_sum(other)

    def __sub__(self, other):
        """Return the skew sum of the permutations self and other."""
        return self.skew_sum(other)

    def __repr__(self):
        return "Permutation({})".format(super(Permutation, self).__repr__())

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
                A permutation.
            patt: <permuta.Pattern>
                A classical/mesh pattern.

        Returns: <bool>
            True if and only if the pattern patt is contained in self.
        """
        return any(True for _ in patt.occurrences_in(self))
