import collections
import operator
import itertools
import numbers
import sys

from permuta.misc import left_floor_and_ceiling

if sys.version_info.major == 2:
    range = xrange


class Permutation(object):
    """A permutation class.

    This class is immutable by agreement.
    """

    __slots__ = (
                 "_perm",
                 "_hash_result",
                 "_pattern_details_result",
                )

    def __init__(self, iterable, check=False):
        """Create a new Permutation with the given list.

        This does not create a copy of the given list.
        Supply a copy of the list if you plan on mutating the original.

        Args:
            self:
                A permutation.
            iterable: [int]
                A list corresponding to a legal permutation.
                Can also be an iterable.
            check: bool
                If True, iterable will be confirmed to be a legal permutation.
        """
        if check:
            assert isinstance(iterable, collections.Iterable), "Non-iterable argument: {}".format(iterable)
            try:
                len_iterable = len(iterable)
            except TypeError:
                len_iterable = sum(1 for _ in iterable)
            used = [False]*len_iterable
            for value in iterable:
                assert isinstance(value, numbers.Integral), "Non-integer type: {}".format(repr(value))
                assert 1 <= value <= len_iterable, "Out of range: {}".format(value)
                assert not used[value-1], "Duplicate element: {}".format(value)
                used[value-1] = True
        self._perm = iterable if isinstance(iterable, list) else list(iterable)
        self._hash_result = None
        self._pattern_details_result = None

    def contained_in(self, *perms):
        """Check if self is a pattern of perms.

        Args:
            self:
                A classical pattern.
            perms: [permuta.Permutation]
                A list of permutations.

        Returns: bool
            True if and only if self is a pattern of all permutations in perms.
        """
        return all(self in perm for perm in perms)

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

    def avoided_by(self, *perms):
        """Check if self is avoided by perms.

        Args:
            self:
                A classical pattern.
            perms: [permuta.Permutation]
                A list of permutations.

        Returns: bool
            True if and only if every permutation in perms avoids self.
        """
        return all(self not in perm for perm in perms)

    def count_occurrences_in(self, perm):
        """Count the number of occurrences of self in perm.

        Args:
            self:
                A classical pattern.
            perm: permuta.Permutation
                A permutation.

        Returns: int
            The number of times self occurs in perm.
        """
        return sum(1 for _ in self.occurrences_in(perm))

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
        if len(self._perm) == 0:
            # Pattern is empty, occurs in all permutations
            # This is needed for the occurrences function to work correctly
            yield []
            return
        if len(self._perm) > len(perm._perm):
            # Pattern is too long to occur in permutation
            return

        # The indices of the occurrence in perm
        occurrence_indices = [None]*len(self._perm)

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
            elements_needed = len(self._perm) - k

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
                # In this case, ubp = len(self) - self[k]
                upper_bound = len(perm._perm) - ubp
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
        if self._pattern_details_result is not None:
            return self._pattern_details_result
        result = []
        index = 0
        for fac_indices in left_floor_and_ceiling(self._perm):
            base_element = self._perm[index]
            compiled = (fac_indices.floor,

                        fac_indices.ceiling,

                        self._perm[index]
                        if fac_indices.floor is None
                        else base_element - self._perm[fac_indices.floor],

                        len(self._perm) - self._perm[index]
                        if fac_indices.ceiling is None
                        else self._perm[fac_indices.ceiling] - base_element,
                        )
            result.append(compiled)
            index += 1
        self._pattern_details_result = result
        return result

    def inverse(self):
        """Return the inverse of the permutation self."""
        len_perm = len(self._perm)
        result = [None]*len_perm
        for index in range(len_perm):
            result[self._perm[index]-1] = index + 1
        return Permutation(result)

    def reverse(self):
        """Return the reverse of the permutation self."""
        return Permutation(self._perm[::-1])

    def complement(self):
        """Return the complement of the permutation self."""
        base = len(self._perm) + 1
        return Permutation(base - element for element in self._perm)

    def reverse_complement(self):
        """Return the reverse complement of self.

        Equivalent to two left or right rotations.
        """
        base = len(self._perm) + 1
        return Permutation(base - element for element in reversed(self._perm))

    def shift(self, times=1):
        """Return self shifted times steps to the right.

        If shift is negative, shifted to the left.
        """
        if len(self._perm) == 0:
            return self
        times = times % len(self._perm)
        if times == 0:
            return self
        index = len(self._perm) - times
        slice_1 = itertools.islice(self._perm, index)
        slice_2 = itertools.islice(self._perm, index, len(self._perm))
        return Permutation(itertools.chain(slice_2, slice_1))

    shift_right = shift
    cyclic_shift = shift
    cyclic_shift_right = shift

    def shift_left(self, times=1):
        """Return self shifted times steps to the left.

        If times is negative, shifted to the right.
        """
        return self.shift_right(-times)

    cyclic_shift_left = shift_left

    def shift_up(self, times=1):
        """Return self shifted times steps up.

        If times is negative, shifted down.
        """
        if len(self._perm) < 2:
            return self
        times = times % len(self._perm)
        if times == 0:
            return self
        bound = len(self._perm) - times
        return Permutation(element - bound
                           if element > bound
                           else element + times
                           for element in self._perm)

    def shift_down(self, times=1):
        """Return self shifted times steps down.

        If times is negative, shifted up.
        """
        return self.shift_up(-times)

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
        len_perm = len(self._perm)
        result = [None]*len_perm

        flipped_pairs = ((len_perm-element, len_perm-index)
                         for index, element in enumerate(self._perm))

        for index, element in flipped_pairs:
            result[index] = element
        return Permutation(result)

    def rotate(self, times=1):
        """Return self rotated 90 degrees to the right."""
        return self._rotate(times)

    rotate_right = rotate

    def rotate_left(self, times=1):
        """Return self rotated 90 degrees to the left."""
        return self._rotate(-times)

    def _rotate(self, times=1):
        """Return self rotated 90 times times degrees to the right."""
        times = times % 4
        if times == 0:
            return self
        elif times == 1:
            return self._rotate_right()
        elif times == 2:
            return self.reverse_complement()
        else:
            return self._rotate_left()

    def _rotate_right(self):
        """Return self rotated 90 degrees to the right."""
        len_perm = len(self._perm)
        result = [None]*len_perm
        for index, value in enumerate(self._perm):
            result[value-1] = len_perm - index
        return Permutation(result)

    def _rotate_left(self):
        """Return self rotated 90 degrees to the left."""
        len_perm = len(self._perm)
        result = [None]*len_perm
        for index, value in enumerate(self._perm):
            result[len_perm - value] = index + 1
        return Permutation(result)

    def is_increasing(self):
        """Return True if the permutation is increasing, and False otherwise."""
        for index in range(len(self._perm)):
            if self._perm[index] != index+1:
                return False
        return True

    def is_decreasing(self):
        """Return True if the permutation is decreasing, and False otherwise."""
        len_perm = len(self._perm)
        for index in range(len_perm):
            if self._perm[index] != len_perm - index:
                return False
        return True

    @classmethod
    def to_standard(cls, iterable):
        """Return the permutation corresponding to lst."""
        try:
            len_iterable = len(iterable)
        except TypeError:
            len_iterable = sum(1 for _ in iterable)
        result = [None]*len_iterable
        value = 1
        for (i, _) in sorted(enumerate(iterable), key=operator.itemgetter(1)):
            result[i] = value
            value += 1
        return cls(result)

    def __call__(self, lst):
        """Return the result of applying self to lst."""
        assert len(lst) == len(self._perm)
        return [lst[index-1] for index in self._perm]

    def __getitem__(self, i):
        return self._perm[i]

    def __len__(self):
        return len(self._perm)

    def __iter__(self):
        return iter(self._perm)

    def __str__(self):
        return str(self._perm)

    def __repr__(self):
        return "Permutation(%s)" % repr(self._perm)

    def __eq__(self, other):
        return isinstance(other, Permutation) and self._perm == other._perm

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return (len(self), self._perm) < (len(other), other._perm)

    def __hash__(self):
        if self._hash_result is None:
            self._hash_result = hash(tuple(self._perm))
        return self._hash_result

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
