from ..PermSetUnbounded import PermSetUnbounded
from ...descriptors.Basis import Basis


class Avoiding(PermSetUnbounded):
    descriptor = Basis
    def contains(self, perm):
        raise NotImplementedError
    def up_to(self, perm):
        raise NotImplementedError
    def __getitem__(self, perm):
        raise NotImplementedError
    def __repr__(self):
        return "<The set of all perms avoiding {}>".format(repr(self.descriptor.basis))
