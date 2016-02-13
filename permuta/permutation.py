
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
