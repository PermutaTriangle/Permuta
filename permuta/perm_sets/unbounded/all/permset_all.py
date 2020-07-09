# TODO: Module docstring

import itertools
import random
from math import factorial

from ....patterns.perm import Perm
from ...finite.permset_finite import PermSetFinite
from ...finite.permset_finite_specificlength import PermSetFiniteSpecificLength
from ...finite.permset_static import PermSetStatic
from ..permset_unbounded import PermSetUnbounded


class PermSetAll(PermSetUnbounded):
    __iter = None
    __iter_number = None

    def up_to(self, perm):
        # Should return a PermSetAllRange
        raise NotImplementedError

    def of_length(self, length):
        return PermSetAllSpecificLength(length)

    def range(self, stop):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, key):
        return Perm.unrank(key)

    def __next__(self):
        if self.__iter is None:
            self.__iter = iter(self[self.__iter_number])
        try:
            return next(self.__iter)
        except StopIteration:
            self.__iter = None
            self.__iter_number += 1
            return self.__next__()

    def __iter__(self):
        self.__iter = None
        self.__iter_number = 0
        return self

    def __contains__(self, perm):
        return isinstance(perm, Perm)  # Why would you even ask?

    def __repr__(self):
        return "PermSet()"

    def __str__(self):
        return "<The set of all perms>"


class PermSetAllSpecificLength(PermSetFiniteSpecificLength):
    """Class for iterating through all perms of a specific length."""

    __slots__ = "_length"

    def __init__(self, length):
        self._length = length

    @property
    def length(self):
        return self._length

    @property
    def domain(self):
        return list(range(self.length))  # tuple instead?

    def of_length(self, length):
        if length != self._length:
            return PermSetStatic([])
        else:
            return self

    def random(self):
        """Return a random perm of the length."""
        all_elements = self.domain
        random.shuffle(all_elements)
        return Perm(all_elements)

    def __contains__(self, other):
        """Check if other is a permutation in the set."""
        return isinstance(other, Perm) and len(other) == self.length

    def __getitem__(self, key):
        return Perm.unrank(key, self.length)

    def __iter__(self):
        return (Perm(x) for x in itertools.permutations(self.domain))

    def __len__(self):
        return factorial(self.length)

    def __repr__(self):
        return "PermSet({})".format(self.length)

    def __str__(self):
        return "<The set of all perms of length {}>".format(self.length)


class PermSetAllFiniteLengthSubset(PermSetFinite):
    pass


class PermSetAllUnboundedLengthSubset(PermSetUnbounded):
    pass
