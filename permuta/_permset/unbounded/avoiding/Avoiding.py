#
# PermSetUnbounded subclasses: Avoiding
#


class Avoiding(PermSetUnbounded):
    descriptor = Basis
    def contains(self, perm):
        raise NotImplementedError
    def up_to(self, perm):
        raise NotImplementedError
    def __getitem__(self, perm):
        raise NotImplementedError


class Avoiding1(Avoiding):
    descriptor = Basis(1)
    def contains(self, perm):
        raise NotImplementedError
    def __getitem__(self, perm):
        raise NotImplementedError


class Avoiding2(Avoiding):
    descriptor = Basis(2)
