import abc


class PermSetBase(metaclass=abc.ABCMeta):
    """Base class for all perm sets."""
    def contains(self, perm):
        # This comes for free when __contains__ is implemented
        return perm in self

    @abc.abstractmethod
    def of_length(self, perm):
        pass

    @abc.abstractmethod
    def __contains__(self, perm):
        pass

    @abc.abstractmethod
    def __getitem__(self, key):
        pass

    @abc.abstractmethod
    def __len__(self, key):
        pass

    def __str__(self):
        # Base __str__ which subclasses should override
        return "a perm set"

    def __repr__(self):
        # Base __repr__ which subclasses should override
        return "<A set of some perms>"
