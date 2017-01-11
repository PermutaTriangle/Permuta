# TODO: Module docstring

import itertools
import random
import sys

from math import factorial

from permuta import Perm
from permuta._permset import PermSetBase
from permuta._permset.unbounded import PermSetUnbounded


if sys.version_info.major == 2:
    range = xrange  # pylint: disable=redefined-builtin,invalid-name,undefined-variable


class PermSetAll(PermSetUnbounded):  # TODO: docstring
    __PERM_SET_CACHE = {}
    def contains(self, perm):
        raise NotImplementedError
    def up_to(self, perm):
        raise NotImplementedError
    def __getitem__(self, key):
        return PermSetDispatcher(key)
    def __repr__(self):
        return "<The set of all perms>"


class PermSetAllSpecificLength(PermSetBase, itertools.permutations):  # TODO: Inherit from proper superclass
    """Class for iterating through all perms of a specific length."""

    __slots__ = ("length", "domain")

    def __new__(cls, length):
        domain = list(range(length))
        instance = super(PermSetAllSpecificLength, cls).__new__(cls, domain)
        # Initialize, even if it should technically be done in __init__
        instance.domain = domain
        instance.length = length
        return instance

    def is_polynomial(self):
        return False

    def random(self):
        """Return a random perm of the length."""
        random.shuffle(self.domain)  # TODO: Not use domain attribute?
        return Perm(self.domain)

    if sys.version_info.major == 2:
        def next(self):
            return Perm(super(PermSetAllSpecificLength, self).next())  # pylint: disable=no-member
    else:
        def __next__(self):
            return Perm(super(PermSetAllSpecificLength, self).__next__())  # pylint: disable=no-member

    def __contains__(self, other):
        """Check if other is a permutation in the set."""
        return isinstance(other, Permutation) and len(other) == self.length

    def __len__(self):
        return factorial(self.length)

    def __str__(self):
        return "The set of all perms of length {}".format(self.length)

    def __repr__(self):
        return "<PermSet of all perms of length {}>".format(self.length)
