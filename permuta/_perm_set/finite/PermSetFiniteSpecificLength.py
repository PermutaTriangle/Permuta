from .PermSetFinite import PermSetFinite


class PermSetFiniteSpecificLength(PermSetFinite):
    @property
    def generating_function(self):
        raise NotImplementedError  # TODO Replace with symbolic variables and stuff
