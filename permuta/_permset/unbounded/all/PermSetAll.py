import abc
import numbers

from .. import PermSetUnbounded


class PermSetAll(PermSetUnbounded):
    def contains(self, perm):
        raise NotImplementedError
    def up_to(self, perm):
        raise NotImplementedError
    def __getitem__(self, key):
        raise NotImplementedError
