import functools
import multiprocessing
import random

from .. import Avoiding, AvoidingGeneric
from permuta import Perm
from permuta._perm_set.finite import PermSetFiniteSpecificLength, PermSetStatic
from permuta.descriptors import Basis

class SimplesAvoiding(Avoiding):
    """The base class for all avoidance classes."""
    # NOTE: Monkey patching of default subclass happens at end of file
    DESCRIPTOR_CLASS = Basis

    @property
    def basis(self):
        return self._descriptor

    def __hash__(self):
        return id(self)  # Requires the singleton property

    def __repr__(self):
        result = ["Av_S("]
        for perm in self.basis:
            result.append(str(perm))
            result.append(", ")
        result[-1] = ")"
        return "".join(result)

    def __str__(self):
        return "perm set of all simple perms avoiding {!s}".format(self.basis)

class SimplesAvoidingGeneric(SimplesAvoiding):
    # Empty basis is dispatched to correct/another class (AvoidingEmpty)
    __CLASS_CACHE = {}
    _CACHE_LOCK = multiprocessing.Lock()

    def __new__(cls, basis):
        if basis in SimplesAvoidingGeneric.__CLASS_CACHE:
            return SimplesAvoidingGeneric.__CLASS_CACHE[basis]
        else:
            instance = super(SimplesAvoidingGeneric, cls).__new__(cls)
            # Generic case includes empty permutation
            instance.cache = [set([Perm()])]
            instance._cache_with_index = [set([])]
            SimplesAvoidingGeneric.__CLASS_CACHE[basis] = instance
            return instance
    def _leftmost_simple_deletion_index(self, perm):
        result = 0
        while(result < len(perm) and not perm.remove(result).is_simple()):
            result += 1
        return result

    def _exceptional_simples(self, n):
        if n == 1:
            return [Perm((0,))]
        elif n % 2 != 0:
            return []
        elif n == 4:
            return [Perm((2,0,3,1)), Perm((1,3,0,2))]

        k = n // 2
        values = []
        for i in range(n):
            if i % 2 == 0:
                values.append(k+i // 2)
            else:
                values.append(i // 2)
        result = [Perm(values)]
        result.append(result[0].reverse())
        result.append(result[0].inverse())
        result.append(result[1].inverse())
        return result
    
    def _is_simple_insertion_candidate(self, perm, i, v):
        if (i == 0 or i == len(perm)) and (v == 0 or v == len(perm)):
            return False
        if i < len(perm) and (perm[i] == v or perm[i] == v-1):
            return False
        if i > 0 and (perm[i-1] == v or perm[i-1] == v-1):
            return False
        return True

    def _get_simple_extensions(self, perm, insertion_index):
        result = []
        for v in range(0, len(perm)+1):
            if _is_simple_insertion_candidate(perm, insertion_index, v):
                result.append(perm.insert(insertion_index, v))
        return result

    def _left_simple_extensions(self, perm, leftmost_simple_deletion_index):
        result = []
        insertion_index = 0
        while insertion_index <= leftmost_simple_deletion_index:
            for q in self._get_simple_extensions(perm, insertion_index):
                i = 0
                while i < insertion_index and not q.remove(i).is_simple():
                    i += 1
                if i == insertion_index:
                    result.append((q, i))
            insertion_index += 1

        if leftmost_simple_deletion_index == len(perm):
            return result # Exceptional case

        if leftmost_simple_deletion_index == 0:
            # In this case, an insertion into the next position can only 
            # remove this simple deletion if it's the min or max
            if self._is_simple_insertion_candidate(perm, insertion_index, 0):
                q = perm.insert(insertion_index, 0)
                result.append((q, insertion_index))
            if self._is_simple_insertion_candidate(perm, insertion_index, len(perm)):
                q = perm.insert(insertion_index, len(perm))
                result.append((q, insertion_index))
        else:
            # Now the only chance is that we have added an element just
            # above or below the one lying just to the left of the
            # simple deletion point
            v = perm[leftmost_simple_deletion_index-1]
            if self._is_simple_insertion_candidate(perm, insertion_index, v):
                q = perm.insert(insertion_index, v)
                if self._leftmost_simple_deletion_index(q) == insertion_index:
                    result.append((q, insertion_index))
            if self._is_simple_insertion_candidate(perm, insertion_index, v+1):
                q = perm.insert(insertion_index, v+1)
                if self._leftmost_simple_deletion_index(q) == insertion_index:
                    result.append((q, insertion_index))

        insertion_index += 1
        v = perm[leftmost_simple_deletion_index]
        while insertion_index <= len(perm):
            # Now the only possibility is that the old value which
            # could be deleted lies between the value we're adding
            # and one of the adjacent points
            if self._is_simple_insertion_candidate(perm, insertion_index, v):
                q = perm.insert(insertion_index, v)
                if self._leftmost_simple_deletion_index(q) == insertion_index:
                    result.append((q, insertion_index))
            if self._is_simple_insertion_candidate(perm, insertion_index, v+1):
                q = perm.insert(insertion_index, v+1)
                if self._leftmost_simple_deletion_index(q) == insertion_index:
                    result.append((q, insertion_index))
            insertion_index += 1
        
        return result

    def _ensure_level(self, level_number):
        # Ensure level is available
        patts = self.basis
        while len(self.cache) <= level_number:
            new_level = set()
            total_indices = len(self.cache)  # really: len(perm) + 1
            for perm in self._exceptional_simples(total_indices):
                if perm.avoids(*patts):
                    new_level.add((perm, total_indices))
            for (perm, j) in self._cache_with_index[-1]:
                for new_perm in self._left_simple_extensions(perm, j):
                    if new_perm[0].avoids(*patts):
                        new_level.add(new_perm)
            self._cache_with_index(new_level)
            self.cache.append(set(perm for (perm, j) in new_level))

    def _get_level(self, level_number):
        with SimplesAvoidingGeneric._CACHE_LOCK:
            self._ensure_level(level_number)
        return self.cache[level_number]

    def of_length(self, length):
        # TODO: Cache of instances?
        getter = functools.partial(self._get_level, length)
        return SimplesAvoidingGenericSpecificLength(length, self.basis, getter)

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
            raise TypeError  # TODO


class SimplesAvoidingGenericSpecificLength(PermSetFiniteSpecificLength):
    """Class for iterating through all simple perms of a specific length avoiding a
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
        result = ["Av_S", str(self._length), "("]
        for perm in self._basis:
            result.append(str(perm))
            result.append(", ")
        result[-1] = ")"
        return "".join(result)

    def __repr__(self):
        format_string = "<PermSet of all simple perms of length {} avoiding {}>"
        result = format_string.format(self._length, repr(self._basis))
        return result

# Set default SimplesAvoiding class to be dispatched
SimplesAvoiding.DEFAULT_CLASS = SimplesAvoidingGeneric
