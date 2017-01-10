import abc


class PermSetBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def contains(self, perm):
        pass
