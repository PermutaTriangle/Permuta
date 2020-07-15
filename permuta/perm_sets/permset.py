import numbers

from .basis import AbstractBasis, detect_basis_cls
from .finite.permset_static import PermSetStatic
from .permset_base import PermSetBase
from .unbounded.all.permset_all import PermSetAll
from .unbounded.described.avoiding.avoiding import Avoiding
from .unbounded.described.permset_described import PermSetDescribed

__all__ = [
    "PermSet",
    "Av",
    "AvoidanceClass",
]


class PermSetMetaclass(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, PermSetBase)

    def __subclasscheck__(self, subclass):
        return issubclass(subclass, PermSetBase)


class PermSet(object, metaclass=PermSetMetaclass):
    def __new__(cls, descriptor=None):
        if descriptor is None:
            return PermSetAll()
        elif isinstance(descriptor, numbers.Integral):
            # Descriptor is actually just a number
            return PermSetAll().of_length(descriptor)
        elif isinstance(descriptor, AbstractBasis):
            return cls._dispatch_described(descriptor)
        else:
            # Descriptor might just be a set of perms
            return PermSetStatic(descriptor)

    @classmethod
    def _dispatch_described(cls, descriptor):
        # Loop through all the described superclasses; e.g. Avoiding
        for described_superclass in PermSetDescribed.__subclasses__():
            # Check if descriptor's class is of that of the superclasses'
            # descriptor
            if isinstance(descriptor, described_superclass.DESCRIPTOR_CLASS):
                # The correct superclass has been found!
                # Try to find subclass specifically for this descriptor
                described_class = cls._find_described_class(
                    descriptor, PermSetDescribed
                )
                if described_class is None:
                    return described_superclass.DEFAULT_CLASS(descriptor)
                else:
                    return described_class(descriptor)
        # TODO: Something else?
        raise RuntimeError(
            "PermSet for descriptor {} not found".format(repr(descriptor))
        )

    @classmethod
    def _find_described_class(cls, descriptor, current_class):
        # TODO: Use metaclasses to track subclasses, rather than this mess
        if descriptor == current_class.DESCRIPTOR:
            return current_class
        else:
            for subclass in current_class.__subclasses__():
                described_class = cls._find_described_class(descriptor, subclass)
                if described_class is not None:
                    return described_class
            return None

    @classmethod
    def avoiding(cls, basis):
        BasisCls = detect_basis_cls(basis)
        return cls(BasisCls(basis))


class AvoidanceClassMetaclass(type):
    def __instancecheck__(self, instance):
        return isinstance(instance, Avoiding)

    def __subclasscheck__(self, subclass):
        return issubclass(subclass, Avoiding)


class Av(object, metaclass=AvoidanceClassMetaclass):
    def __new__(cls, basis=None):
        if basis is None or len(basis) == 0:
            return PermSetAll()
        return PermSet.avoiding(basis)


AvoidanceClass = Av
