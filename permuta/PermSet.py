import abc
import numbers

from permuta._permset.descriptors.Basis import Basis
from permuta._permset.descriptors.Basis import Descriptor
from permuta._permset.PermSetBase import PermSetBase
from permuta._permset.unbounded.PermSetUnbounded import PermSetUnbounded
from permuta._permset.unbounded.all.PermSetAll import PermSetAll


class PermSetMetaclass(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, PermSetBase)
    def __subclasscheck__(self, subclass):
        return issubclass(subclass, PermSetBase)

class PermSet(object, metaclass=PermSetMetaclass):
    def __new__(_cls, descriptor=None):
        if descriptor is None:
            return PermSetAll(True)
        elif isinstance(descriptor, numbers.Integral):
            return PermSetAll(True)[descriptor]
        elif isinstance(descriptor, Descriptor):
            for generic in PermSetUnbounded.__subclasses__():
                if isinstance(descriptor, generic.descriptor):
                    for cls in generic.__subclasses__():
                        if cls.descriptor == descriptor:
                            return cls(descriptor)
                    return generic(descriptor)
                    break  # Shouldn't continue looking
            raise RuntimeError("PermSet for descriptor {} not found".format(repr(descriptor)))  # TODO: Something else?
        else:
            raise RuntimeError("I don't know")  # TODO: Not raise an exception?

    @classmethod
    def avoiding(_cls, basis):
        return PermSet(Basis(basis))


##
## Creating a new Descriptor and PermSetUnbounded
##
#
#
#class VeeDescriptor(Descriptor):
#    def __init__(self):
#        pass
#    def __eq__(self, other):
#        return True
#
#
#class Vee(PermSetUnbounded):
#    descriptor = VeeDescriptor
#    def contains(self, perm):
#        raise NotImplementedError
#    def up_to(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, perm):
#        raise NotImplementedError
