from .Avoiding import AvoidingSpecificLength

from permuta.misc import catalan


class CatalanAvoidingSpecificLength(AvoidingSpecificLength):
    def __len__(self):
        return catalan(self.length)
