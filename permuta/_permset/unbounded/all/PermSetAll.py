import collections
import itertools
import random
import sys

from math import factorial

from permuta import Perm
from permuta.math import catalan


if sys.version_info.major == 2:
    range = xrange  # pylint: disable=redefined-builtin,invalid-name,undefined-variable


from ..PermSetUnbounded import PermSetUnbounded


class PermSetAll(PermSetUnbounded):
    def contains(self, perm):
        raise NotImplementedError
    def up_to(self, perm):
        raise NotImplementedError
    def __getitem__(self, key):
        return PermSetAllSpecificLength(key)
    def __repr__(self):
        return "<The set of all perms>"


class PermSetAllSpecificLength(itertools.permutations):
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

    if sys.version_info.major == 2:
        def next(self):
            return Perm(super(PermSetAllSpecificLength, self).next())  # pylint: disable=no-member
    else:
        def __next__(self):
            return Perm(super(PermSetAllSpecificLength, self).__next__())  # pylint: disable=no-member

    def __iter__(self):
        return self

    def random(self):
        """Return a random permutation of the length."""
        number = random.randint(0, len(self)-1)
        return Perm.unrank(number, self.length)

    def __len__(self):
        return factorial(self.length)

    def __str__(self):
        return "The set of all perms of length {}".format(self.length)

    def __str__(self):
        return "<PermSet of all perms of length {}".format(self.length)

    def __contains__(self, other):
        """Check if other is a permutation in the set."""
        return isinstance(other, Permutation) and len(other) == self.length
