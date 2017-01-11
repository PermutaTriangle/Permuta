import abc

from ..PermSetBase import PermSetBase


class PermSetRestricted(PermSetBase):
    def __init__(self, descriptor):
        self.descriptor = descriptor
    @abc.abstractmethod
    def random(self, perm):
        pass
