import numbers

from ..Perm import Perm as _ZBPerm


__all__ = ("Perm", "Permutation")


class Perm:
    """A perm(utation) class."""

    #
    # Methods returning a single Perm instance (albeit __init__ doesn't really)
    #

    def __init__(self, *args):
        if len(args) == 0:
            self._zb_perm = _ZBPerm()
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, numbers.Integral):
                self._zb_perm = _ZBPerm.to_standard(str(arg))
            elif isinstance(arg, _ZBPerm):
                self._zb_perm = arg
            else:
                self._zb_perm = _ZBPerm.to_standard(arg)
        else:
            self._zb_perm = _ZBPerm.to_standard(args)

    @classmethod
    def random(cls, length):
        """Return a random perm of the specified length."""
        return cls(_ZBPerm.random(length))

    @classmethod
    def monotone_increasing(cls, length):
        """Return a monotone increasing perm of the specified length."""
        return cls(_ZBPerm.monotone_increasing(length))

    @classmethod
    def monotone_decreasing(cls, length):
        """Return a monotone decreasing perm of the specified length."""
        return cls(_ZBPerm.monotone_decreasing(length))

    #
    # Methods modifying/combining Perm instances
    #

    def direct_sum(self, *perms):
        """Return the direct sum of the two perms."""
        zb_perm = self._zb_perm.direct_sum(perm._zb_perm)
        return Perm(zb_perm)

    def skew_sum(self, perm):
        """Return the skew sum of the two perms."""
        zb_perm = self._zb_perm.skew_sum(perm._zb_perm)
        return Perm(zb_perm)

    def compose(self, perm):
        """Return the composition of the two perms."""
        zb_perm = self._zb_perm.compose(perm._zb_perm)
        return Perm(zb_perm)

    multiply = compose

    #
    # Methods for basic Perm transforming
    #

    def inverse(self):
        """Return the inverse of the perm."""
        return Perm(self._zb_perm.inverse())

    def reverse(self):
        """Return the reverse of the perm."""
        return Perm(self._zb_perm.reverse())

    def complement(self):
        """Return the complement of the perm."""
        return Perm(self._zb_perm.complement())

    def reverse_complement(self):
        """Return the reverse_complement of the perm."""
        return Perm(self._zb_perm.reverse_complement())

    def shift_right(self, times=1):
        """Return the perm shifted times steps to the right."""
        return Perm(self._zb_perm.shift_right(times))

    def shift_left(self, times=1):
        """Return the perm shifted times steps to the left."""
        return Perm(self._zb_perm.shift_left(times))

    def shift_up(self, times=1):
        """Return the perm shifted times steps up."""
        return Perm(self._zb_perm.shift_up(times))

    def shift_down(self, times=1):
        """Return the perm shifted times steps down."""
        return Perm(self._zb_perm.shift_down(times))

    def flip_horizontally(self):
        """Return the perm flipped horizontally."""
        return Perm(self._zb_perm.flip_horizontal())

    def flip_vertically(self):
        """Return the perm flipped vertically."""
        return Perm(self._zb_perm.flip_vertical())

    def flip_diagonally(self):
        """Return the perm flipped diagonally."""
        return Perm(self._zb_perm.flip_diagonal())

    def flip_antidiagonally(self):
        """Return the perm flipped antidiagonally."""
        return Perm(self._zb_perm.flip_antidiagonal())

    #
    # Statistical methods
    #

    def is_increasing(self):
        """Return True if the perm is increasing, and False otherwise."""
        return self._zb_perm.is_increasing()

    def is_decreasing(self):
        """Return True if the perm is decreasing, and False otherwise."""
        return self._zb_perm.is_decreasing()

    def ascents(self):
        """Return the indices of elements where the next element is greater."""
        return list(element + element for element in self._zb_perm.ascents())

    def descents(self):
        """Return the indices of elements where the next element is greater."""
        return list(element + 1 for element in self._zb_perm.descents())

    def peaks(self):
        """Return the indices of the peaks of the perm."""
        return list(element + 1 for element in self._zb_perm.peaks())

    def valleys(self):
        """Return the indices of the valleys of the perm."""
        return list(element + 1 for element in self._zb_perm.valleys())

    def cycle_decomposition(self):
        """Return the cycle decomposition of the perm."""
        return list(list(element + 1 for element in cycle) for cycle in self._zb_perm.cycle_decomp())

    #
    # Pattern matching methods
    #

    def contains(self, patt):
        """Check if the perm contains the patt."""
        return self._zb_perm.contains(patt._zb_perm)

    def avoids(self, patt):
        """Check if the perm avoids the patt."""
        return self._zb_perm.avoids(patt._zb_perm)

    def occurrences_in(self, perm):
        """Find all occurrences of the patt self in perm."""
        return list(list(perm[index + 1] for index in occurrence_indices)
                    for occurrence_indices
                    in self._zb_perm.occurrences_in(perm._zb_perm))

    def occurrences_of(self, patt):
        """Find all occurrences of patt in the perm self."""
        return patt.occurrences_in(self)

    def occurrence_indices_in(self, perm):
        """Find all indices of occurrences of the patt self in perm."""
        return list(list(index + 1 for index in occurrence)
                    for occurrence
                    in self._zb_perm.occurrences_in(perm._zb_perm))

    def occurrence_indices_of(self, patt):
        """Find all indices of occurrences of patt in the perm self."""
        return patt.occurrence_indices_in(self)

    #
    # General methods
    #

    def apply(self, iterable):
        """Permute an iterable using the perm."""
        return list(self._zb_perm.apply(iterable))

    def __len__(self):
        """Return the length of the perm."""
        return len(self._zb_perm)

    def __iter__(self):
        for element in self._zb_perm:
            yield element + 1

    def __getitem__(self, index):
        """Return the element at the one-based index specified."""
        format_string = "The indices of the perm {} are [{}{}{}]"
        if index < 1 or index > len(self):
            if len(self) == 0:
                message = format_string.format(self, "", "", "")
            elif len(self) == 1:
                message = format_string.format(self, 1, "", "")
            else:
                message = format_string.format(self, 1, ", ..., ", len(self))
            raise IndexError(message)
        return self._zb_perm[index - 1] + 1

    def __call__(self, value):
        """Map value to its image defined by the perm."""
        return self._zb_perm(value - 1) + 1

    def __add__(self, other):
        """Return the direct sum of the perms self and other."""
        return self.direct_sum(other)

    def __sub__(self, other):
        """Return the skew sum of the perms self and other."""
        return self.skew_sum(other)

    def __mul__(self, other):
        """Return the composition of two perms."""
        return self.compose(other)

    def __bytes__(self):
        return bytes(str(self), "ascii")

    def __hash__(self):
        return hash(self._zb_perm)

    def __bool__(self):
        return bool(self._zb_perm)

    def __reversed__(self):
        return self.reverse()

    def __contains__(self, patt):
        return self.contains(patt)
    
    def __pow__(self, power):
        perm = self
        for _ in range(power - 1):
            perm *= self
        return perm

    def __iadd__(self, perm):
        return self + perm

    def __isub__(self, perm):
        return self - perm

    def __imul__(self, perm):
        return self*perm

    def __ipow__(self, power):
        return self**power

    def __ilshift__(self, times):
        return self << times

    def __irshift__(self, times):
        return self >> times

    def __lshift__(self, times):
        return self.shift_left(times)

    def __rshift__(self, times):
        return self.shift_right(times)

    def __eq__(self, other):
        return self._zb_perm == other._zb_perm

    def __lt__(self, other):
        return self._zb_perm < other._zb_perm

    def __le__(self, other):
        return self._zb_perm <= other._zb_perm

    def __gt__(self, other):
        return self._zb_perm > other._zb_perm

    def __ge__(self, other):
        return self._zb_perm >= other._zb_perm

    def __repr__(self):
        if self._zb_perm == _ZBPerm((0,)):
            return "(1)"
        else:
            return str(tuple(self))


Permutation = Perm  # Alias for the more traditional user
