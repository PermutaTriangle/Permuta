import functools
import multiprocessing
import random

from .....descriptors.basis import AbstractBasis, Basis
from .....perm import Perm
from ....finite.permset_finite_specificlength import \
    PermSetFiniteSpecificLength
from ....finite.permset_static import PermSetStatic
from ....unbounded.all.permset_all import PermSetAll
from ..permset_described import PermSetDescribed


class Avoiding(PermSetDescribed):
    """The base class for all avoidance classes."""
    # NOTE: Monkey patching of default subclass happens at end of file
    DESCRIPTOR_CLASS = AbstractBasis

    @property
    def basis(self):
        return self._descriptor

    def __hash__(self):
        return id(self)  # Requires the singleton property

    def __len__(self):
        raise NotImplementedError  # This is a hard task!

    def __repr__(self):
        return "Av({})".format(tuple(self.basis))

    def __str__(self):
        return "<perm set of all perms avoiding {}>".format(self.basis)


class AvoidingGeneric(Avoiding):
    # Empty basis is dispatched to correct/another class (AvoidingEmpty)
    __CLASS_CACHE = {}
    _CACHE_LOCK = multiprocessing.Lock()

    def __new__(cls, basis):
        if basis in AvoidingGeneric.__CLASS_CACHE:
            return AvoidingGeneric.__CLASS_CACHE[basis]
        else:
            instance = super(AvoidingGeneric, cls).__new__(cls)
            # Generic case includes empty permutation
            instance.cache = [set([Perm()])]
            AvoidingGeneric.__CLASS_CACHE[basis] = instance
            return instance

    def _ensure_level(self, level_number):
        # Ensure level is available
        while len(self.cache) <= level_number:
            new_level = set()
            total_indices = len(self.cache)  # really: len(perm) + 1
            if isinstance(self.basis, Basis):
                # Smart way when basis consists only of Perms
                for perm in self.cache[-1]:
                    for index in range(total_indices):
                        new_perm = perm.insert(index)
                        if new_perm.avoids(*self.basis):
                            new_level.add(new_perm)
            else:
                # Necessary non-smart way for e.g. MeshBasis
                for new_perm in PermSetAll().of_length(total_indices):
                    if new_perm.avoids(*self.basis):
                        new_level.add(new_perm)
            self.cache.append(new_level)

    def _get_level(self, level_number):
        with AvoidingGeneric._CACHE_LOCK:
            self._ensure_level(level_number)
        return self.cache[level_number]

    def of_length(self, length):
        # TODO: Cache of instances?
        getter = functools.partial(self._get_level, length)
        return AvoidingGenericSpecificLength(length, self.basis, getter)

    def __getitem__(self, key):
        level_number = 0
        while True:
            level = self._get_level(level_number)
            if len(level) <= key:
                key -= len(level)
            else:  # TODO: So dumb
                return list(level)[key]
            level_number += 1

    def __next__(self):
        if self._iter is None:
            self._ensure_level(self._iter_number)
            cached_perms = self.cache[self._iter_number]
            if len(cached_perms) == 0:
                raise StopIteration
            self._iter = iter(cached_perms)
        try:
            return next(self._iter)
        except StopIteration:
            self._iter = None
            self._iter_number += 1
            return self.__next__()

    def __iter__(self):
        self._iter = None
        self._iter_number = 0
        return self

    def __contains__(self, perm):
        # TODO: Think about heuristics for switching to avoiding the patterns
        #       in the basis instead
        if isinstance(perm, Perm):
            length = len(perm)
            self._ensure_level(length)
            return perm in self.cache[length]
        else:
            raise TypeError

    def is_subclass(self, other):
        """ Check if the `self` is a subclass of `other`. """
        return all(p1 not in self for p1 in other.basis)


class AvoidingGenericSpecificLength(PermSetFiniteSpecificLength):
    """Class for iterating through all perms of a specific length avoiding a
    basis."""

    # __slots__ = ("_length", "_basis", "_get_perms", "_iter")

    def __init__(self, length, basis, get_perms):
        self._length = length
        self._basis = basis
        self._get_perms = get_perms
        self._iter = None

    def of_length(self, length):
        if length != self._length:
            return PermSetStatic()
        else:
            return self

    def random(self):
        return random.choice(self._get_perms())

    def __contains__(self, other):
        """Check if other is a permutation in the set."""
        return isinstance(other, Perm) and other in self._get_perms()

    def __getitem__(self, key):
        raise NotImplementedError

    def __iter__(self):
        self._iter = iter(self._get_perms())
        return self

    def __len__(self):
        return len(self._get_perms())

    def __next__(self):
        return next(self._iter)

    def __str__(self):
        return ("<PermSet of all perms of length {} avoiding {}>"
                "".format(self._length, self._basis))

    def __repr__(self):
        return ("Av({}).of_length({})"
                "".format(repr(tuple(self._basis)), self._length))


# Set default Avoiding class to be dispatched
Avoiding.DEFAULT_CLASS = AvoidingGeneric
