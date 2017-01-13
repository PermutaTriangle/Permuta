import abc

from ..PermSetBase import PermSetBase


class PermSetUnbounded(PermSetBase):
    @abc.abstractmethod
    def range(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def of_length(self, perm):
        pass

    def up_to(self, length):
        self.range(length)
