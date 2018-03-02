# TODO: Module docstring

import abc


class Descriptor(metaclass=abc.ABCMeta):
    # TODO: Docstring
    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def __hash__(self):
        pass


#class ContainmentBasis(Descriptor):
#    def __init__(self, n, o):
#        self.n = n
#        self.o = o
#    def __eq__(self, other):
#        return isinstance(other, self.__class__) and self.n == other.n and self.o == other.o
#
#
#class Predicate(Descriptor):
#    def __init__(self, predicate):
#        self.predicate = predicate
#    def __eq__(self, other):
#        return isinstance(other, self.__class__) and self.predicate == other.predicate
