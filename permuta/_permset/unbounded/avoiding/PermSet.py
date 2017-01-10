import abc
import numbers

from permuta._permset.descriptors import Basis, Descriptor
import permuta._permset as _permset


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


#
# PermSetBase and the two subclass groups
#


class PermSetBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def contains(self, perm):
        pass


class PermSetUnbounded(PermSetBase):
    def __init__(self, descriptor):
        self.descriptor = descriptor
    @abc.abstractmethod
    def up_to(self, perm):
        pass
    @abc.abstractmethod
    def __getitem__(self, key):
        pass


class PermSetRestricted(PermSetBase):
    def __init__(self, descriptor):
        self.descriptor = descriptor
    @abc.abstractmethod
    def random(self, perm):
        pass


##
## PermSetRestricted subclasses
##
#
#
#class PermSetSingleLength(PermSetRestricted):
#    # Abstract class?
#    pass
#
#
#class PermSetStatic(PermSetRestricted):
#    # Abstract class?
#    pass
#
#
##
## PermSetUnbounded subclasses
##
#
#
##
## PermSetUnbounded subclasses: All permutations
##
#
#
#class PermSetAll(PermSetUnbounded):
#    def contains(self, perm):
#        raise NotImplementedError
#    def up_to(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, key):
#        return PermSetSingleLength()
#
#
##
## PermSetUnbounded subclasses: Avoiding
##
#
#
#class Avoiding(PermSetUnbounded):
#    descriptor = Basis
#    def contains(self, perm):
#        raise NotImplementedError
#    def up_to(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, perm):
#        raise NotImplementedError
#
#
#class Avoiding1(Avoiding):
#    descriptor = Basis(1)
#    def contains(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, perm):
#        raise NotImplementedError
#
#
#class Avoiding2(Avoiding):
#    descriptor = Basis(2)
#
#
##
## PermSetUnbounded subclasses: Containing
##
#
#
#class Containing(PermSetUnbounded):
#    descriptor = ContainmentBasis
#    def contains(self, perm):
#        raise NotImplementedError
#    def up_to(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, perm):
#        raise NotImplementedError
#
#
#class Containing12(Containing):
#    descriptor = ContainmentBasis(1, 2)
#    def contains(self, perm):
#        raise NotImplementedError
#    def up_to(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, perm):
#        raise NotImplementedError
#
#
#class Containing23(Containing):
#    descriptor = ContainmentBasis(2, 3)
#    def contains(self, perm):
#        raise NotImplementedError
#    def up_to(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, perm):
#        raise NotImplementedError
#
#
##
## PermSetUnbounded subclasses: Predicated
##
#
#
#class Predicated(PermSetUnbounded):
#    descriptor = Predicate
#    def contains(self, perm):
#        raise NotImplementedError
#    def up_to(self, perm):
#        raise NotImplementedError
#    def __getitem__(self, perm):
#        raise NotImplementedError
#
#
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
