import abc

from ..PermSetBase import PermSetBase


class PermSetUnbounded(PermSetBase):
    @abc.abstractmethod
    def of_length(self, perm):
        pass
