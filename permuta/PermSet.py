import abc
import numbers

from permuta.descriptors import Basis
from permuta.descriptors import Descriptor
from permuta._perm_set import PermSetBase
from permuta._perm_set.finite import PermSetStatic
from permuta._perm_set.unbounded.all import PermSetAll
from permuta._perm_set.unbounded.described import PermSetDescribed


class PermSetMetaclass(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, PermSetBase)
    def __subclasscheck__(self, subclass):
        return issubclass(subclass, PermSetBase)

class PermSet(object, metaclass=PermSetMetaclass):
    def __new__(_cls, descriptor=None):
        if descriptor is None:
            return PermSetAll()
        elif isinstance(descriptor, numbers.Integral):
            # Descriptor is actually just a number
            return PermSetAll().of_length(descriptor)
        elif isinstance(descriptor, Descriptor):
            for described in PermSetDescribed.__subclasses__():
                if isinstance(descriptor, described.descriptor):
                    for cls in described.__subclasses__():
                        if cls.descriptor == descriptor:
                            return cls(descriptor)
                    return described(descriptor)
                    break  # Shouldn't continue looking
            raise RuntimeError("PermSet for descriptor {} not found".format(repr(descriptor)))  # TODO: Something else?
        else:
            # Descriptor might just be a set of perms
            return PermSetStatic(descriptor)

    @classmethod
    def avoiding(cls, basis):
        return cls(Basis(basis))


##
## Creating a new Descriptor and PermSetDescribed
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
#class Vee(PermSetDescribed):
#    descriptor = VeeDescriptor
#    def contains(self, perm):
#        raise NotImplementedError
#    def up_to(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, perm):
#        raise NotImplementedError
