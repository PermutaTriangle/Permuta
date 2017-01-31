from .Avoiding import *


class Avoiding10(Avoiding):
    descriptor = Basis(Perm((1, 0)))
    def of_length(self, length):
        return Avoiding10SpecificLength(length)
    def __getitem__(self, key):
        return Perm.monotone_increasing(key)
    def __contains__(self, perm):
        return perm.is_increasing()


class Avoiding10SpecificLength(AvoidingSpecificLength):
    __slots__ = ("_length", "_iter")

    def __init__(self, length):
        self._length = length
        self._iter = None

    def random(self):
        return self[0]

    def __contains__(self, other):
        return self[0] == other

    def __getitem__(self, key):
        if key == 0:
            return Perm.monotone_increasing(self._length)
        else:
            raise IndexError

    def __iter__(self):
        self._iter = not None  # Heheh
        return self

    def __len__(self):
        return 1

    def __next__(self):
        if self._iter is None:
            raise StopIteration
        else:
            self._iter = None
            return self[0]
