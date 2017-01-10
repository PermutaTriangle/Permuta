import abc


class PermSetBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def contains(self, perm):
        pass
    def __repr__(self):
        return "<A set of some perms>"
