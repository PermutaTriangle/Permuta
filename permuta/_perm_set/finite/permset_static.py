import random

from permuta import Perm

from .permset_finite import PermSetFinite


class PermSetStatic(PermSetFinite):
    """A static perm set."""
    __slots__ = ("_set", "_generating_function", "_iter")

    def __init__(self, iterable=()):
        self._set = set(iterable)
        self._tuple = tuple(self._set)
        self._generating_function = "X"
        self._iter = None

    @property
    def generating_function(self):
        # TODO Replace with symbolic variables and stuff
        return self._generating_function

    def of_length(self, length):
        return PermSetStatic(perm for perm in self if len(perm) == length)

    def random(self):
        return random.choice(self._tuple)

    def __contains__(self, item):
        return isinstance(item, Perm) and item in self._set

    def __getitem__(self, key):
        return self._tuple[key]

    def __iter__(self):
        self._iter = iter(self._tuple)
        return self

    def __len__(self):
        return len(self._tuple)

    def __next__(self):
        return next(self._iter)

    def __repr__(self):
        return "<A set of {} perms>".format(len(self._tuple))
