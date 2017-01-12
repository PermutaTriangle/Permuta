import abc


class PermSetBase(metaclass=abc.ABCMeta):
    def contains(self, perm):
        return perm in self

    @abc.abstractmethod
    def __contains__(self, perm):
        pass

    def __repr__(self):
        return "<A set of some perms>"
