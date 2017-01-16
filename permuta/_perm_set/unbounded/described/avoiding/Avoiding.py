from ..PermSetDescribed import PermSetDescribed
from permuta import Perm
from permuta.descriptors import Basis
from permuta._perm_set.finite import PermSetFiniteSpecificLength
#from permuta._perm_set.finite import PermSetStatic


# PermSet.avoiding([(0, 2, 1), (1, 2, 3, 4, 0)])


class Avoiding(PermSetDescribed):
    descriptor = Basis
    __CLASS_CACHE = {}  # Empty basis is dispatched to correct class (AvoidingEmpty)

    def __new__(cls, basis):
        if basis in Avoiding.__CLASS_CACHE:
            return Avoiding.__CLASS_CACHE[basis]
        else:
            instance = super(Avoiding, cls).__new__(cls)
            instance.cache = [set([Perm()])]  # Generic case includes empty permutation
            instance.basis = basis
            Avoiding.__CLASS_CACHE[basis] = instance
            return instance


    def assure_length(self, length):
        while len(self.cache) <= length:
            next_level = set()
            total_indices = len(self.cache)  # really: len(perm) + 1
            #new_element = indices - 1  # TODO Performance without insert method
            for perm in self.cache[-1]:
                for index in range(total_indices):
                    new_perm = perm.insert(index)
                    if new_perm.avoids(*self.basis.perms):
                        next_level.add(new_perm)
            self.cache.append(next_level)

    def up_to(self, perm):
        # Should return a PermSetAllRange
        raise NotImplementedError

    def of_length(self, length):
        # TODO: Cache of instances
        return AvoidingSpecificLength(length, self)

    def range(self, stop):
        raise NotImplementedError

    def __getitem__(self, key):
        level = 0
        while True:
            self.assure_length(level)
            level_size = len(self.cache[level])
            if level_size <= key:
                key -= level_size
            else:  # TODO: So dumb
                return list(self.cache[level])[key]
            level += 1

    def __next__(self):
        if self._iter is None:
            self._iter = iter(self.of_length(self._iter_number))
        try:
            return next(self._iter)
        except StopIteration:
            self._iter = None
            self._iter_number += 1
            return self.__next__()

    def __iter__(self):
        self._iter = None
        self._iter_number = 0
        return self

    def __contains__(self, perm): # TODO: Raggi, are we happy with this?
        level = len(perm)
        self.assure_length(level)
        return perm in self.cache[level]
        # naive implementation
        # return perm.avoids(*self.basis.perms)


    def __repr__(self):
        return "<The set of all perms avoiding {}>".format(repr(self.basis))


class AvoidingSpecificLength(PermSetFiniteSpecificLength):
    """Class for iterating through all perms of a specific length avoiding a basis."""

    __slots__ = ("_length")

    def __init__(self, length, supervisor):
        self._length = length
        self._supervisor = supervisor
        self._basis = supervisor.basis
        self._iter = None

    @property
    def length(self):
        return self._length

    @property
    def basis(self):
        return self._basis

    @property
    def supervisor(self):
        return self._supervisor

    def random(self):
        raise NotImplementedError

    def __contains__(self, other):
        """Check if other is a permutation in the set."""
        # TODO  When is it better to check for avoidance?
        return isinstance(other, Permutation) and contained in cache

    def __getitem__(self, key):
        raise NotImplementedError

    def __iter__(self):
        self.supervisor.assure_length(self.length)
        self._iter = iter(self.supervisor.cache[self.length])
        return self

    def __len__(self):
        self.supervisor.assure_length(self.length)
        return len(self.supervisor.cache[self.length])

    def __next__(self):
        return next(self._iter)

    def __str__(self):
        return "The set of all perms of length {} avoiding {}".format(self.length, self.basis)

    def __repr__(self):
        return "<PermSet of all perms of length {} avoiding {}>".format(self.length, self.basis)
