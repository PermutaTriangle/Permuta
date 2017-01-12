# TODO: Module docstring

from dis import dis
from collections import Callable

from .Descriptor import Descriptor


class Predicate(Descriptor):  # pylint: disable=too-few-public-methods
    """A predicate class.

    A PermSet can be built with a Predicate instance by using the predicate
    provided to it to see if a perm should be in the PermSet or not.
    """
    def __init__(self, predicate):
        if isinstance(predicate, Callable):
            self.predicate = predicate
        else:
            message = "{} object is not callable".format(repr(predicate))
            raise TypeError(message)
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # Disassemble predicates and see if code is the same
            return dis(self.predicate) == dis(other.predicate)
        else:
            return False
