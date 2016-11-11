import abc

ABC = abc.ABCMeta("ABC", (object,), {})


class Pattern(ABC):

    @abc.abstractmethod
    def contained_in(self, *perms):
        pass

    @abc.abstractmethod
    def avoided_by(self, *perms):
        pass

    @abc.abstractmethod
    def count_occurrences_in(self, perm):
        pass

    @abc.abstractmethod
    def occurrences_in(self, perm):
        pass
