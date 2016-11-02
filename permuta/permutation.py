from permuta.misc import left_floor_and_ceiling
import collections
import itertools
import numbers
import sys
if sys.version_info.major is 2:
    range = xrange

class Permutation(object):
    """A permutation class.

    This class is immutable by agreement.
    """

    __slots__ = (
                  "perm"
                , "_hash_result"
                , "_left_to_right_details_result"
                )

    def __init__(self, l, check=False):
        """Create a new Permutation with the given list.

        This does not create a copy of the given list.
        Supply a copy of the list if you plan on mutating the original.

        Args:
            self:
                A permutation.
            l: [int]
                A list corresponding to a legal permutation.
                Can also be an iterable.
            check: bool
                If True, l will be confirmed to be a legal permutation.
        """
        if check:
            assert isinstance(l, collections.Iterable), "Non-iterable argument: {}".format(l)
            try:
                n = len(l)
            except TypeError:
                n = sum(1 for _ in l)
            used = [False]*n
            for x in l:
                assert isinstance(x, numbers.Integral), "Non-integer type: {}".format(repr(x))
                assert 1 <= x <= n, "Out of range: {}".format(x)
                assert not used[x-1], "Duplicate element: {}".format(x)
                used[x-1] = True
        self.perm = l if type(l) is list else list(l)
        self._hash_result = None
        self._left_to_right_details_result = None

    def contained_in(self, *perms):
        """Check if self is a pattern of perms.

        Args:
            self:
                A classical pattern.
            perms: [permuta.Permutation]
                A list of permutations.

        Returns: bool
            True iff self is a pattern of all permutations in perms.
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
            True iff all patterns in patt are contained in self.
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
            True iff self avoids all patterns in patts.
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
            True iff every permutation in perms avoids self.
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
        if len(self) == 0:
            # Pattern is empty, occurs in all permutations
            # This is needed for the con function to work correctly
            yield []
            return

        # The indices of the occurrence in perm
        occurrence_indices = [None]*len(self)

        # Get left to right scan details
        details = self._left_to_right_details()

        # Define function that works with the above defined variables
        # i is the index of the element in perm that is to be considered
        # k is how many elements of the permutation have already been added to occurrence
        def con(i, k):
            elements_remaining = len(perm) - i
            elements_needed = len(self) - k
            left_floor_index, left_ceiling_index, left_floor_diff, left_ceiling_diff = details[k]
            # Set the bounds for the new element
            lower_bound = left_floor_diff
            if left_floor_index is None:
                lower_bound += 1
            else:
                lower_bound += perm[occurrence_indices[left_floor_index]]
            upper_bound = -left_ceiling_diff
            if left_ceiling_index is None:
                upper_bound += len(perm)
            else:
                upper_bound += perm[occurrence_indices[left_ceiling_index]]

            # Loop over remaining elements of perm (actually i, the index)
            while 1:
                if elements_remaining < elements_needed:
                    # Can't form an occurrence with remaining elements
                    return
                element = perm[i]
                if lower_bound <= element <= upper_bound:
                    occurrence_indices[k] = i
                    # Yield occurrence
                    # TODO: will bringing this conditional out of loop speed things up?
                    if elements_needed == 1:
                        yield occurrence_indices[:]
                    # Yield occurrences where the i-th element is chosen
                    else:
                        for o in con(i+1, k+1):
                            yield o
                # Increment i, that also means elements_remaining should decrement
                i += 1
                elements_remaining -= 1

        for o in con(0, 0):
            yield o

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

    def _left_to_right_details(self):
        # If details have been calculated before, return cached result
        if self._left_to_right_details_result is not None:
            return self._left_to_right_details_result
        result = []
        index = 0
        for fac in left_floor_and_ceiling(self):
            base_element = self[index]
            left_floor = 1 if fac.floor is None else self[fac.floor]
            left_ceiling = len(self) if fac.ceiling is None else self[fac.ceiling]
            # left_floor_difference:
            # How much greater than the left floor the element must be,
            # or how much greater than 1 it must be if left floor does not exist
            left_floor_difference = base_element - left_floor
            # left_ceiling_difference:
            # Subtract this number from the length of the permutation an
            # occurrence is being searched for in to get an upper bound for the
            # allowed value. Tighten the bound by subtracting from the left
            # ceiling value if its index is not None.
            left_ceiling_difference = left_ceiling - base_element
            compiled = (
                         fac.floor
                       , fac.ceiling
                       , left_floor_difference
                       , left_ceiling_difference
                       )
            result.append(compiled)
            index += 1
        self._left_to_right_details_result = result
        return result

    def inverse(self):
        """Return the inverse of the permutation self."""
        n = len(self)
        result = [None]*n
        for i in range(n):
            result[self[i]-1] = i+1
        return Permutation(result)

    def reverse(self):
        """Return the reverse of the permutation self."""
        return Permutation(self[::-1])

    def complement(self):
        """Return the complement of the permutation self."""
        return Permutation(len(self) - e + 1 for e in self)

    def shift(self, n=1):
        """Return self rotated n steps to the right.

        If n is negative, rotate to the left.
        """
        if len(self) is 0:
            return self
        n = n % len(self)
        if n is 0:
            return self
        i = len(self) - n
        slice_1 = itertools.islice(self, i)
        slice_2 = itertools.islice(self, i, len(self))
        return Permutation(itertools.chain(slice_2, slice_1))

    shift_right = shift

    def shift_left(self, n=1):
        """Return self rotated n steps to the left.

        If n is negative, rotate to the right.
        """
        return self.shift_right(-n)

    def flip_horizontal(self):
        """Return self flipped horizontally."""
        return self.complement()

    def flip_vertical(self):
        """Return self flipped vertically."""
        return self.reverse()

    def flip_diagonal(self):
        """Return self flipped along the diagonal, y=x."""
        return self.inverse()

    def flip_antidiagonal(self):
        """Return self flipped along the antidiagonal, y=len(perm)-x."""
        # TODO: Determine whether a linear time algorithm is better
        return Permutation(
                            x
                            for _, x in
                            sorted(
                                    (-y, len(self.perm)-x)
                                    for x, y in
                                    enumerate(self.perm)
                                  )
                          )

    def rotate_right(self):
        """Docstring"""
        # TODO: Write docstring and make generic version
        index = [-1] * len(self)
        for i, v in enumerate(self):
            index[v-1] = i
        result = []
        for i in range(len(self)):
            result.append(len(self) - index[i])
        return Permutation(result)

    def is_increasing(self):
        """Return True if the permutation is increasing, and False otherwise."""
        for i in range(1,len(self)):
            if self[i-1] > self[i]:
                return False
        return True

    def is_decreasing(self):
        """Return True if the permutation is decreasing, and False otherwise."""
        for i in range(1,len(self)):
            if self[i-1] < self[i]:
                return False
        return True

    @classmethod
    def to_standard(cls, lst):
        """Return the permutation corresponding to lst."""
        n = len(lst)
        result = [None]*n
        for j, (x, i) in enumerate(sorted((lst[i], i) for i in range(n))):
            result[i] = j+1
        return cls(result)

    def __call__(self, lst):
        """Return the result of applying self to lst."""
        assert len(lst) == len(self)
        return [lst[i-1] for i in self]

    def __getitem__(self, i):
        return self.perm[i]

    def __len__(self):
        return len(self.perm)

    def __iter__(self):
        return iter(self.perm)

    def __str__(self):
        return str(self.perm)

    def __repr__(self):
        return "Permutation(%s)" % repr(self.perm)

    def __eq__(self, other):
        return type(other) is Permutation and self.perm == other.perm

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (len(self), self.perm) < (len(other), other.perm)

    def __hash__(self):
        if self._hash_result is None:
            self._hash_result = hash(tuple(self.perm))
        return self._hash_result

    def __contains__(self, patt):
        """Check if self contains patt.

        Args:
            self:
                A permutation.
            patt: permuta.Permutation|permuta.MeshPattern
                A classical/mesh pattern.

        Returns: bool
            True iff the pattern patt is contained in self.
        """
        return any(True for _ in patt.occurrences_in(self))
