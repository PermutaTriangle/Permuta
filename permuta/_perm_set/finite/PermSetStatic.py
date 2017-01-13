import random

from .PermSetFinite import PermSetFinite


class PermSetStatic(tuple, PermSetFinite):
    def __new__(cls, iterable):
        return tuple.__new__(cls, sorted(list(iterable)))

    def random(self):
        return random.choice(self)
