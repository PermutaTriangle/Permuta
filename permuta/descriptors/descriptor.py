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
