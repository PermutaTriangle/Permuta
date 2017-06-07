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

    def direct_sum(self, *others):
        """Return the direct sum of two or more perms."""
        zb_perm = self._zb_perm.direct_sum(other._zb_perm for other in others)
        return Perm(zb_perm)

    def skew_sum(self, *others):
        """Return the skew sum of two or more perms."""
        zb_perm = self._zb_perm.skew_sum(other._zb_perm for other in others)
        return Perm(zb_perm)

    def compose(self, *others):
        """Return the composition of two or more perms."""
        zb_perm = self._zb_perm.compose(other._zb_perm for other in others)
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
        """Return self shifted times steps to the right."""
        return Perm(self._zb_perm.shift_right(times))

    def shift_left(self, times=1):
        """Return self shifted times steps to the left."""
        return Perm(self._zb_perm.shift_left(times))

    def shift_up(self, times=1):
        """Return self shifted times steps up."""
        return Perm(self._zb_perm.shift_up(times))

    def shift_down(self, times=1):
        """Return self shifted times steps down."""
        return Perm(self._zb_perm.shift_down(times))

    def flip_horizontally(self):
        """Return self flipped horizontally."""
        return Perm(self._zb_perm.flip_horizontal())

    def flip_vertically(self):
        """Return self flipped vertically."""
        return Perm(self._zb_perm.flip_vertically())

    def flip_diagonally(self):
        """Return self flipped diagonally."""
        return Perm(self._zb_perm.flip_diagonally())

    def flip_antidiagonally(self):
        """Return self flipped antidiagonally."""
        return Perm(self._zb_perm.flip_antidiagonally())

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
        return list(i + 1 for i in self._zb_perm.ascents())

    def descents(self):
        """Return the indices of elements where the next element is greater."""
        return list(i + 1 for i in self._zb_perm.descents())

    def peaks(self):
        """Return the indices of the peaks of the perm."""
        return list(i + 1 for i in self._zb_perm.peaks())

    def valleys(self):
        """Return the indices of the valleys of the perm."""
        return list(i + 1 for i in self._zb_perm.valleys())

    def cycle_decomposition(self):
        """Return the cycle decomposition of the perm."""
        return list(list(i + 1 for i in cycle) for cycle in self._zb_perm.cycle_decomp())

    #
    # Pattern matching methods
    #

    # TODO

    #
    # General methods
    #

    def apply(self, iterable):
        """Permute an iterable using the perm."""
        return self._zb_perm.apply(iterable)

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
            return str(tuple(n + 1 for n in self._zb_perm))


Permutation = Perm  # Alias for the more traditional user
