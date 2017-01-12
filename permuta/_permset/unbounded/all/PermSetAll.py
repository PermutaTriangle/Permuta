# TODO: Module docstring

import itertools
import random
import numbers
import sys

from math import factorial

from permuta import Perm
from permuta._permset import PermSetBase
from permuta._permset.unbounded import PermSetUnbounded


if sys.version_info.major == 2:
    range = xrange  # pylint: disable=redefined-builtin,invalid-name,undefined-variable


class PermSetAll(PermSetUnbounded):
    __iter = None
    __iter_number = None

    def up_to(self, perm):
        # Should return a PermSetAllRange
        raise NotImplementedError

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

    def __getitem__(self, key):
        assert isinstance(key, numbers.Integral)
        perm_set = PermSetAll.__CACHE.get(key)
        if perm_set is None:
            perm_set = PermSetAllSpecificLength(key)
            PermSetAll.__CACHE[key] = perm_set
        return perm_set

    def __repr__(self):
        return "<The set of all perms>"


class PermSetAllSpecificLength(PermSetBase):  # TODO: Inherit from proper superclass
    """Class for iterating through all perms of a specific length."""

    __slots__ = ("_length")

    def __init__(self, length):
        if not isinstance(length, numbers.Integral):
            raise TypeError("{} not int".format(repr(length)))  # TODO
        elif length < 0:
            raise ValueError("Length {} is negative".format(length))  # TODO
        self._length = length

    @property
    def length(self):
        return self._length

    @property
    def domain(self):
        return list(range(self.length))

    def random(self):
        """Return a random perm of the length."""
        all_elements = self.domain
        random.shuffle(all_elements)
        return Perm(all_elements)

    def __contains__(self, other):
        """Check if other is a permutation in the set."""
        return isinstance(other, Permutation) and len(other) == self.length

    def __iter__(self):
        return PermSetAllSpecificLengthIterator(self.domain)

    def __len__(self):
        return factorial(self.length)

    def __str__(self):
        return "The set of all perms of length {}".format(self.length)

    def __repr__(self):
        return "<PermSet of all perms of length {}>".format(self.length)


class PermSetAllSpecificLengthIterator(itertools.permutations):
    def __next__(self):
        return Perm(super(PermSetAllSpecificLengthIterator, self).__next__())  # pylint: disable=no-member


class PermSetAllRange(PermSetBase):  # TODO: Inherit from proper superclass
    pass
