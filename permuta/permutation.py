#from collections import namedtuple
#
## TODO: Is this nice at all?
## Class to make occurrence method cleaner
#LTRDAttr = [
#             "left_floor_index"
#           , "left_ceiling_index"
#           , "minimum_elements_below"
#           , "minimum_elements_above"
#           ]
#class LeftToRightDetail(namedtuple("LeftToRightDetail", LTRDAttr)):
#    __slots__ = ()
#    def __new__(cls, *args, **kwargs):
#        actual = {attr: kwargs[attr] for attr in LTRDAttr}
#        return super(LeftToRightDetail, cls).__new__(cls, **actual)

class Permutation(object):
    """Base Permutation object"""
    def __init__(self, perm, check=False):
        """Create a new Permutation from the given list.
        If check, then check that the permutation is of the correct form"""
        if check:
            assert type(perm) is list
            n = len(perm)
            used = [False]*n

            for x in perm:
                assert type(x) is int
                assert 1 <= x <= n
                assert not used[x-1]
                used[x-1] = True

        self.perm = list(perm)
        self._element_indices_result = None
        self._left_to_right_details_result = None

    def contains(self, pattern):
        """Returns true if permutation self contains a given pattern"""
        if type(pattern) is list:
            pattern = Permutation(pattern)
        return pattern.contained_in(self)

    def avoids(self, pattern):
        """Returns True if self contains no occurrence of pattern"""
        if type(pattern) is list and all( type(patt) is list or type(patt) is Permutation for patt in pattern ):
            for patt in pattern:
                if self.contains(patt):
                    return False
            return True

        return not self.contains(pattern)

    def contained_in(self, perm):
        """Returns true if the permutation self is contained in the
        permutation perm.
        self is treated as a pattern"""
        return any( True for _ in self.occurrences_in(perm) )

    def count_occurrences_in(self, perm):
        """Count the number of occurrences of the pattern self in the permutation perm."""
        return sum(1 for _ in self.occurrences_in(perm))

    def count_occurrences_of(self, patt):
        """Count the number of occurrences of the pattern patt in the permutation self."""
        return patt.count_occurrences_in(self)

    def occurrences_in(self, perm):
        """Find all indices of occurrences of self in perm.

        Args:
            self:
                The classical pattern whose occurrences are to be found.
            perm: permuta.Permutation
                The permutation to search for occurrences in.

        Yields: [int]
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
            elements_left = len(perm) - i
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
                if elements_left < elements_needed:
                    # Can't form an occurrence with remaining elements
                    return
                element = perm[i]
                if lower_bound <= element <= upper_bound:
                    occurrence_indices[k] = i
                    # Yield occurrence
                    if elements_needed == 1:
                        yield occurrence_indices[:]
                    # Yield occurrences where the i-th element is chosen
                    else:
                        for o in con(i+1, k+1):
                            yield o
                # Increment i, that also means elements_left should decrement
                i += 1
                elements_left -= 1

        for o in con(0, 0):
            yield o

    def occurrences_of(self, patt):
        """Find all indices of occurrences of patt in self.

        This method is complementary to permuta.Permutation.occurrences_in.
        It just calls patt.occurrences_in(self) internally.
        See permuta.Permutation.occurrences_in for documentation.
        """
        return patt.occurrences_in(self)

    def _left_to_right_details(self):
        # TODO: Make comment better
        """What is known when scanning self from left to right.

        TODO: Make comments nice and make betterer

        Return: [(int, int, int, int)]
        """
        # If details have been calculated before, return cached result
        if self._left_to_right_details_result is not None:
            return self._left_to_right_details_result
        result = []
        for base_index in range(len(self)):
            left_floor_index = None
            left_ceiling_index = None
            left_floor = 1
            left_ceiling = len(self)
            base_element = self[base_index]
            for index in range(base_index):
                element = self[index]
                if element > base_element:
                    if element <= left_ceiling:
                        left_ceiling_index = index
                        left_ceiling = element
                else:
                    if element >= left_floor:
                        left_floor_index = index
                        left_floor = element
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
                         left_floor_index
                       , left_ceiling_index
                       , left_floor_difference
                       , left_ceiling_difference
                       )
            result.append(compiled)
        self._left_to_right_details_result = result
        return result

    @staticmethod
    def _online_flattening_step(perm, flattened, indices, index_of_new):
        """Single step of online flattening of permutation.

        Args:
            perm: permuta.Permutation
                The permutation the rest of the arguments refer to.
            flattened: [int]
                The flattened list of [perm[i] for i in indices[:len(flattened)]].
                This list is modified by correctly appending perm[index_of_new].
            indices: [int]
                The indices of the elements in perm that have been flattened.
                Only the first len(flattened) are legitimate.
            index_of_new: int
                The index of the perm element to be added to the flattened list.
        Returns: (int, int)
            These are the indices of the next smaller/bigger element in flattened.
            They are None if they do not exist.
            The flattened argument is also modified.
        """
        new_element = perm[index_of_new]
        index_smaller = None  # Index in flattened: One greater in flattened
        index_bigger = None  # Index in flattened: One lesser in flattened
        smaller = 0  # Value of smaller in perm
        bigger = len(perm) + 1  # Value of greater in perm
        not_incremented_counter = 0  # Number of flattened elements not incremented
        for i in range(len(flattened)):
            element = perm[indices[i]]  # Original value of flattened[i]
            if element > new_element:
                # Must increment when new element is added
                flattened[i] += 1
                # If element is closer to new element than last one
                if element < bigger:
                    bigger = element
                    index_bigger = i
            else:
                # Stays the same when new element is added
                not_incremented_counter += 1
                if element > smaller:
                    smaller = element
                    index_smaller = i
        new_element_flattened = 1 + not_incremented_counter
        flattened.append(new_element_flattened)
        return index_smaller, index_bigger

    def inverse(self):
        """Return the inverse of the permutation self"""
        n = len(self)
        res = [None]*n
        for i in range(n):
            res[self.perm[i]-1] = i+1
        return Permutation(res)

    def reverse(self):
        return Permutation(self.perm[::-1])

    def complement(self):
        return Permutation([len(self.perm) - x + 1 for x in self.perm])

    def rotate_right(self):
        idx = [-1] * len(self)
        for i, v in enumerate(self.perm):
            idx[v-1] = i
        res = []
        for i in range(len(self)):
            res.append(len(self) - idx[i])
        return Permutation(res)

    def flip_horizontal(self):
        """Returns the permutation self flipped horizontally"""
        return self.complement()

    def flip_vertical(self):
        """Returns the permutation self flipped vertically"""
        return self.reverse()

    def flip_diagonal(self):
        """Returns the permutation self flipped along the diagonal, y=x"""
        return self.inverse()

    def flip_antidiagonal(self):
        """Returns the permutation self flipped along the
        antidiagonal, y=len(perm)-x"""
        # TODO: implement linear algorithm
        return Permutation([x for _, x in
                            sorted([(-y, len(self.perm)-x) for x, y in
                                    enumerate(self.perm)])])

    def is_increasing(self):
        """Returns true if the permutation is increasing, and false otherwise."""
        for i in range(1,len(self.perm)):
            if self.perm[i-1] > self.perm[i]:
                return False
        return True

    def is_decreasing(self):
        """Returns true if the permutation is decreasing, and false otherwise."""
        for i in range(1,len(self.perm)):
            if self.perm[i-1] < self.perm[i]:
                return False
        return True

    @staticmethod
    def to_standard(lst):
        """Returns the permutation given by mapping every element in lst
        to the lowest possible value that preserves order of the elements"""
        n = len(lst)
        res = [None]*n
        for j, (x, i) in enumerate(sorted((lst[i], i) for i in range(n))):
            res[i] = j+1

        return Permutation(res)

    def __call__(self, lst):
        """Returns the result of applying self to lst"""
        assert len(lst) == len(self)

        n = len(self)
        res = [None]*n
        for i in range(n):
            res[i] = lst[self.perm[i] - 1]

        return res

    def __getitem__(self, i):
        return self.perm[i]

    def __len__(self):
        return len(self.perm)

    def __iter__(self):
        return iter(self.perm)

    def __str__(self):
        return str(self.perm)

    def __repr__(self):
        return 'Permutation(%s)' % repr(self.perm)

    def __eq__(self, other):
        return type(other) is Permutation and self.perm == other.perm

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (len(self), self.perm) < (len(other), other.perm)

    def __hash__(self):
        return hash(tuple(self.perm))
