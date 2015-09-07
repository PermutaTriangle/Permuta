
class Permutation(object):
    def __init__(self, perm, check=False):

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
        return pattern.contained_in(self)

    def avoids(self, pattern):
        return not self.contains(pattern)

    def contained_in(self, perm):
        # self is treated as a pattern
        def con(i, now):
            if len(now) == len(self):
                return True

            if i == len(perm):
                return False

            nxt = now + [perm[i]]
            # TODO: make this faster by incrementally building the flattened list
            if Permutation.to_standard(nxt) == Permutation.to_standard(self[:len(nxt)]):
                if con(i+1, nxt):
                    return True

            return con(i+1, now)

        return con(0, [])


    def inverse(self):
        n = len(self)
        res = [None]*n
        for i in range(n):
            res[self.perm[i]-1] = i+1
        return Permutation(res)

    def rotate_right(self):
        # TODO: is there a nicer name for this?
        idx = [-1] * len(self)
        for i,v in enumerate(self.perm):
            idx[v-1] = i
        res = []
        for i in range(len(self)):
            res.append(len(self) - idx[i])
        return Permutation(res)

    @staticmethod
    def to_standard(lst):
        n = len(lst)
        res = [None]*n
        for j, (x, i) in enumerate(sorted( (lst[i], i) for i in range(n) )):
            res[i] = j+1

        return Permutation(res)

    def __call__(self, lst):
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

    def __lt__(self, other):
        return (len(self), self.perm) < (len(other), other.perm)

    def __hash__(self):
        return hash(tuple(self.perm))

