import abc

ABC = abc.ABCMeta("ABC", (object,), {})


class Pattern(ABC):

    def avoided_by(self, *perms):
        return all(self not in perm for perm in perms)

    def contained_in(self, *perms):
        return all(self in perm for perm in perms)

    def count_occurrences_in(self, perm):
        return sum(1 for _ in self.occurrences_in(perm))

    @abc.abstractmethod
    def occurrences_in(self, perm):
        pass
