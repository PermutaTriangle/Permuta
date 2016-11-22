import collections
import itertools
import numbers
import operator
import sys

from permuta import Pattern, Rotatable, Shiftable, Flippable
from permuta.misc import left_floor_and_ceiling

if sys.version_info.major == 2:
    range = xrange



class Permutation(tuple, Pattern, Rotatable, Shiftable, Flippable):
    """A permutation class."""

    _TYPE_ERROR = "Non-Permutation argument: {}"

    def __new__(cls, iterable=(), check=False):
        """Return a Permutation instance.

        Args:
            self:
                The class of which an instance is requested.
            iterable: <collections.Iterable> or <numbers.Integral>
                An iterable corresponding to a legal permutation.
                Also supports passing just a number with unique digits.
            check: bool
                If True, iterable will be confirmed to correspond to a legal permutation.
        """
        if isinstance(iterable, numbers.Integral):
            number = iterable
            assert 1 <= number <= 987654321  # TODO: Message
            iterable = []
            while number != 0:
                iterable.append(number % 10)
                number //= 10
            iterable = reversed(iterable)
        instance = super(Permutation, cls).__new__(cls, iterable)
        return instance

    def __init__(self, iterable=(), check=False):
        if check:
            used = [False]*len(self)
            for value in self:
                try:
                    assert isinstance(value, numbers.Integral)
                except AssertionError as exception:
                    message = "Non-integer type: {}".format(repr(value))
                    exception.args = (message,)
                    raise
                assert 1 <= value <= len(self), "Out of range: {}".format(value)
                assert not used[value-1], "Duplicate element: {}".format(value)
                used[value-1] = True
        self._cached_pattern_details = None

    def contains(self, *patts):
        """Check if self contains patts.

        Args:
            self:
                A permutation.
            patts: [permuta.Permutation|permuta.MeshPattern]
                A list of classical/mesh patterns.

        Returns: bool
            True if and only if all patterns in patt are contained in self.
        """
        return all(patt in self for patt in patts)

    def avoids(self, *patts):
        """Check if self avoids patts.

        Args:
            self:
                A permutation.
            patts: [permuta.Permutation|permuta.MeshPattern]
                A list of classical/mesh patterns.

        Returns: bool
            True if and only if self avoids all patterns in patts.
        """
        return all(patt not in self for patt in patts)

    def count_occurrences_of(self, patt):
        """Count the number of occurrences of patt in self.

        Args:
            self:
                A permutation.
            patt: permuta.Permutation|permuta.MeshPattern
                A classical/mesh pattern.

        Returns: int
            The number of times patt occurs in self.
        """
        return patt.count_occurrences_in(self)

    def occurrences_in(self, perm):
        """Find all indices of occurrences of self in perm.

        Args:
            self:
                The classical pattern whose occurrences are to be found.
            perm: permuta.Permutation
                The permutation to search for occurrences in.

        Yields: [int]
            The indices of the occurrences of self in perm.
            Each yielded element l is a list of integer indices of the
            permutation perm such that:
            self == permuta.Permutation.to_standard([perm[i] for i in l])
        """
        # Special cases
        if len(self) == 0:
            # Pattern is empty, occurs in all permutations
            # This is needed for the occurrences function to work correctly
            yield []
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
                        yield occurrence_indices[:]
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
            perm: permuta.Permutation
                A classical pattern.

        Yields: [int]
            The indices of the occurrences of self in perm.
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
        # TODO: Docstring
        assert isinstance(iterable, collections.Iterable)
        iterable = tuple(iterable)
        assert len(iterable) == len(self)
        return (iterable[index-1] for index in self)

    def direct_sum(self, *others):
        """Return the direct sum of two or more permutations."""
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
        """Return the skew sum of two or more permutations."""
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
        """Return the inverse of the permutation self."""
        len_perm = len(self)
        result = [None]*len_perm
        for index in range(len_perm):
            result[self[index]-1] = index + 1
        return Permutation(result)

    def reverse(self):
        """Return the reverse of the permutation self."""
        return Permutation(self[::-1])

    def complement(self):
        """Return the complement of the permutation self."""
        base = len(self) + 1
        return Permutation(base - element for element in self)

    def reverse_complement(self):
        """Return the reverse complement of self.

        Equivalent to two left or right rotations.
        """
        base = len(self) + 1
        return Permutation(base - element for element in reversed(self))

    def shift_right(self, times=1):
        """Return self shifted times steps to the right.

        If shift is negative, shifted to the left.
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
        """
        if len(self) < 2:
            return self
        times = times % len(self)
        if times == 0:
            return self
        bound = len(self) - times
        return Permutation(element - bound
                           if element > bound
                           else element + times
                           for element in self)

    def flip_horizontal(self):
        """Return self flipped horizontally."""
        return self.complement()

    def flip_vertical(self):
        """Return self flipped vertically."""
        return self.reverse()

    def flip_diagonal(self):
        """Return self flipped along the diagonal, y = x."""
        return self.inverse()

    def flip_antidiagonal(self):
        """Return self flipped along the antidiagonal, y = len(perm) - x."""
        len_perm = len(self)
        result = [None]*len_perm

        flipped_pairs = ((len_perm-element, len_perm-index)
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

    @classmethod
    def to_standard(cls, iterable):
        """Return the permutation corresponding to lst."""
        # TODO: Do performance testing
        try:
            len_iterable = len(iterable)
        except TypeError:
            iterable = list(iterable)
            len_iterable = len(iterable)
        result = [None]*len_iterable
        value = 1
        for (i, _) in sorted(enumerate(iterable), key=operator.itemgetter(1)):
            result[i] = value
            value += 1
        return cls(result)

    def __call__(self, value):
        # TODO: Docstring
        assert isinstance(value, numbers.Integral)  # TODO: Message
        assert 0 < value <= len(self)  # TODO: Message
        return self[value-1]

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
            patt: permuta.Permutation|permuta.MeshPattern
                A classical/mesh pattern.

        Returns: bool
            True if and only if the pattern patt is contained in self.
        """
        return any(True for _ in patt.occurrences_in(self))
