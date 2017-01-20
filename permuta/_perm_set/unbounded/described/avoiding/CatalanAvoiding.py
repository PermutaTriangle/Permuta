from .Avoiding import *
from permuta import Perm
from permuta.misc import catalan

class CatalanAvoidingClass(object):
    def __len__(self):
        # TODO: Actually, does not make sense!
        return catalan(self.length)

    def is_polynomial(self):
        return False
