
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
        def con(i, now):
            if len(now) == len(self):
                return True

            if i == len(perm):
                return False

            nxt = now + [perm[i]]
            # TODO: make this faster by incrementally building flattened list
            if (Permutation.to_standard(nxt) ==
                    Permutation.to_standard(self[:len(nxt)])):
                if con(i+1, nxt):
                    return True

            return con(i+1, now)

        return con(0, [])

    def count_occurrences_in(self, perm):
        """Returns the number of occurrences of the pattern perm in the permutation self
        """
        def con(i, now):
            if len(now) == len(self):
                return 1

            if i == len(perm):
                return 0

            c = 0
            nxt = now + [perm[i]]
            # TODO: make this faster by incrementally building flattened list
            if (Permutation.to_standard(nxt) ==
                    Permutation.to_standard(self[:len(nxt)])):
                c += con(i+1, nxt)

            c += con(i+1, now)

            return c

        return con(0, [])

    def count_occurrences_of(self, patt):
        """Returns the number of occurrences of the pattern patt in the permutation self
        """
        return patt.count_occurrences_in(self)

    def occurrences_in(self, perm):
        """Returns the occurrences of the pattern self in the permutation perm."""

        # Calculate all prefix flattenings of the pattern self
        k_standard_patt = [Permutation.to_standard(self[:k]) for k in range(0, len(self))]
        k_standard_patt.append(self)

        # These two lists define a pattern in the permutation perm
        # occurrence is the actual elements and indices is their indices in perm
        occurrence = [None]*len(self)
        indices = occurrence[:]

        # Define function that works with the above defined variables
        # i is the index of the element in perm that is to be considered
        # k is how many elements of the permutation have already been added to occurrence
        # flattened is the flattened occurrence so far
        def con(i, k, flattened):

            # Length of the occurrence has reached length of pattern
            if k == len(self):
                yield indices[:]
                return

            # Not enough elements left to make occurrence
            elements_left = len(perm) - i
            elements_needed = len(self) - k
            if elements_left < elements_needed:
                return

            # TODO: Optimize if elements_left == elements_needed?

            # Incrementally build flattened occurrence
            new_element = perm[i]
            new_flattened = [
                              flattened[n]
                              if occurrence[n] < new_element
                              else
                              flattened[n]+1
                              for n in range(k)
                            ]
            new_element_flattened = 1 + len([
                                              n for n in range(k)
                                              if flattened[n] == new_flattened[n]
                                            ])
            new_flattened.append(new_element_flattened)
            new_flattened = Permutation(new_flattened)

            # Yield occurrences where the ith element is chosen
            if new_flattened == k_standard_patt[k+1]:
                # Still conforms to pattern, so add index and look further
                occurrence[k] = new_element
                indices[k] = i
                for o in con(i+1, k+1, new_flattened):
                    yield o

            # Yield occurrences where the ith element is not chosen
            for o in con(i+1, k, flattened):
                yield o

        for o in con(0, 0, []):
            yield o

    def occurrences_of(self, patt):
        """Returns the occurrences of the pattern patt in the permutation self."""
        return patt.occurrences_in(self)

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
