from ..PermSetDescribed import PermSetDescribed
from permuta import Perm
from permuta.descriptors import Basis


class Avoiding(PermSetDescribed):
    descriptor = Basis
    def contains(self, perm):
        raise NotImplementedError
    def up_to(self, perm):
        raise NotImplementedError
    def __getitem__(self, perm):
        raise NotImplementedError
    def __repr__(self):
        return "<The set of all perms avoiding {}>".format(repr(self.descriptor.basis))
