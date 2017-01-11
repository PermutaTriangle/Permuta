from ..PermSetUnbounded import PermSetUnbounded


class PermSetAll(PermSetUnbounded):
    def contains(self, perm):
        raise NotImplementedError
    def up_to(self, perm):
        raise NotImplementedError
    def __getitem__(self, key):
        raise NotImplementedError
    def __repr__(self):
        return "<The set of all perms>"
