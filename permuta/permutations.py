import itertools
import random
import sys

from math import factorial
from permuta import Permutation


class Permutations(itertools.permutations):
    """Class for iterating through all Permutations of a specific length."""

    __slots__ = ("length", "domain")

    def __new__(cls, length):
        domain = list(range(1, length+1))  # TODO: xrange or future
        instance = super(Permutations, cls).__new__(cls, domain)
        instance.domain = domain
        instance.length = length
        return instance

    if sys.version_info.major == 2:
        def next(self):
            return Permutation(super(Permutations, self).next())
    else:
        def __next__(self):
            return Permutation(super(Permutations, self).__next__())

    def __iter__(self):
        return self

    def random_element(self):
        """Return a random permutation of the length."""
        lst = self.domain[:]
        random.shuffle(lst)
        return Permutation(lst)

    def __len__(self):
        return factorial(self.length)

    def __str__(self):
        return "The set of Permutations of length {}".format(self.length)

    def __repr__(self):
        return "Permutations({})".format(self.length)
