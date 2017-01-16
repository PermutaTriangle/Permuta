import random

from .PermSetFinite import PermSetFinite


class PermSetStatic(set, PermSetFinite):
    def __init__(self, iterable):
        return super(PermSetStatic, self).__init__(iterable)

    def random(self):
        return random.choice(self)  # TODO
