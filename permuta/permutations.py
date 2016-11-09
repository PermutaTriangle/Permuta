import itertools
import random

from math import factorial
from permutation import Permutation


class Permutations(itertools.permutations):
    """Class for iterating through all Permutations of a specific length."""

    def __new__(cls, length):
        domain = tuple(range(1, length+1))
        instance = super(Permutations, cls).__new__(cls, domain)
        return instance

    def __init__(self, length):
        self.length = length

    def next(self):
        return Permutation(super(Permutations, self).next())

    def random_element(self):
        """Return a random permutation of the length."""
        lst = list(range(1, self.length+1))
        random.shuffle(lst)
        return Permutation(lst)

    def __len__(self):
        return factorial(self.length)

    def __str__(self):
        return "The set of Permutations of length {}".format(self.length)

    def __repr__(self):
        return "Permutations({})".format(self.length)
