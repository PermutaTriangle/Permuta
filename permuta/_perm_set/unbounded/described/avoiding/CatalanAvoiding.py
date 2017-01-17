from .Avoiding import *
from permuta import Perm

class CatalanAvoidingClass(object):
    def __len__(self):
        return catalan(self.n)

    def is_polynomial(self):
        return False
