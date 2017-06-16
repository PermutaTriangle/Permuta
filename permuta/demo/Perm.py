"""A wrapper around the permuta Perm class."""


import numbers
import tempfile
import warnings
import webbrowser

try:
    import seaborn
    _SEABORN_AVAILABLE = True
except ImportError:
    _SEABORN_AVAILABLE = False
    warnings.warn("Unable to load seaborn for PermClass plotting")

from ..Perm import Perm as _ZBPerm


__all__ = ("Perm", "Permutation")


def _assert_perm(perm):
    """Helper function for this module."""
    # TODO: Do we want to use this function anyway?
    if not isinstance(perm, Perm):
        raise TypeError("Not a perm: {}".format(perm))
    else:
        return True


class Perm:
    """A perm(utation) object.

    It attempts to interpret anything you throw at it, but it's probably best
    to stick to giving a single sequence argument like Perm([1, 3, 2, 4]).
    
    Examples:
        >>> Perm()  # Empty perm
        ()
        >>> Perm([])  # Another empty perm
        ()
        >>> Perm(132)  # From number
        (1, 3, 2)
        >>> Perm(248)  # Attempted interpretation
        (1, 2, 3)
        >>> Perm("1234")  # From string
        (1, 2, 3, 4)
        >>> Perm("dcab")  # This is equivalent to ...
        (4, 3, 1, 2)
        >>> Perm(["d", "c", "a", "b"])  # ... this
        (4, 3, 1, 2)
        >>> Perm(0, 0, 2, 1)  # Index is tie-breaker
        (1, 2, 4, 3)
        >>> Perm("Ragnar", "Christian", "Henning")
        (3, 1, 2)
        >>> Perm.monotone_increasing(4)
        (1, 2, 3, 4)
        >>> Perm.monotone_decreasing(3)
        (3, 2, 1)
        >>> random_perm = Perm.random(7)

    See also:
        Perm.monotone_decreasing
        Perm.monotone_increasing
        Perm.random
    """

    #
    # Methods returning a single Perm instance (albeit __init__ doesn't really)
    #

    def __init__(self, *args):
        try:
            if len(args) == 0:
                self._zb_perm = _ZBPerm()
            elif len(args) == 1:
                arg = args[0]
                if isinstance(arg, _ZBPerm):
                    self._zb_perm = arg
                elif isinstance(arg, Perm):
                    self._zb_perm = arg._zb_perm
                elif isinstance(arg, numbers.Integral):
                    self._zb_perm = _ZBPerm.to_standard(str(arg))
                else:
                    self._zb_perm = _ZBPerm.to_standard(arg)
            else:
                    self._zb_perm = _ZBPerm.to_standard(args)
        except:
            format_string = "Don't know how to get a perm from args: {}"
            message = format_string.format(args)
            raise ValueError(message)

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

    def direct_sum(self, perm):
        """Return the direct sum of the two perms.
        
        See also:
            Perm.__sum__
        """
        perm = Perm(perm)
        zb_perm = self._zb_perm.direct_sum(perm._zb_perm)
        return Perm(zb_perm)

    def skew_sum(self, perm):
        """Return the skew sum of the two perms.
        
        See also:
            Perm.__sub__
        """
        perm = Perm(perm)
        zb_perm = self._zb_perm.skew_sum(perm._zb_perm)
        return Perm(zb_perm)

    def compose(self, perm):
        """Return the composition of the two perms.
        
        See also:
            Perm.multiply
            Perm.__mul__
        """
        perm = Perm(perm)
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
        """Return the reverse complement of the perm."""
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

    def rotate_left(self, times=1):
        """Return the perm rotated times left."""
        return Perm(self._zb_perm.rotate_left(times))

    def rotate_right(self, times=1):
        """Return the perm rotated times right."""
        return Perm(self._zb_perm.rotate_right(times))

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
        """Return the indices of values where the next value is greater.
        
        See also:
            Perm.total_ascents
        """
        return list(value + 1 for value in self._zb_perm.ascents())

    def total_ascents(self):
        """Return the number of ascents in the perm."""
        return sum(1 for _ in self._zb_perm.ascents())

    def descents(self):
        """Return the indices of values where the next value is greater.
        
        See also:
            Perm.total_descents
        """
        return list(value + 1 for value in self._zb_perm.descents())

    def total_descents(self):
        """Return the number of descents in the perm."""
        return sum(1 for _ in self._zb_perm.descents())

    def peaks(self):
        """Return the indices of the peaks of the perm.
        
        See also:
            Perm.total_peaks
        """
        return list(value + 1 for value in self._zb_perm.peaks())

    def total_peaks(self):
        """Return the number of peaks in the perm."""
        return sum(1 for _ in self._zb_perm.peaks())

    def valleys(self):
        """Return the indices of the valleys of the perm.
        
        See also:
            Perm.total_valleys
        """
        return list(value + 1 for value in self._zb_perm.valleys())

    def total_valleys(self):
        """Return the number of valleys in the perm."""
        return sum(1 for _ in self._zb_perm.valleys())

    def cycles(self):
        """Return the cycle decomposition of the perm.
        
        See also:
            Perm.cycle_decomposition
            Perm.total_cycles
        """
        return list(list(value + 1 for value in cycle) for cycle in self._zb_perm.cycle_decomp())

    cycle_decomposition = cycles

    def total_cycles(self):
        """Return the number of cycles in the perm."""
        return sum(1 for _ in self._zb_perm.cycle_decomp())

    def inversions(self):
        """Return the list of the inversions of the perm.
        
        See also:
            Perm.total_inversions
        """
        return self.occurrences_of(21)

    def total_inversions(self):
        """Return the number of inversions in the perm."""
        return len(self.inversions())

    def fixed_points(self):
        """Return the fixed points of the perm.
        
        See also:
            Perm.total_fixed_points
        """
        return [value
                for index, value
                in enumerate(self, 1)
                if index == value]

    def total_fixed_points(self):
        """Return the number of fixed points in the perm."""
        return sum(1
                   for index, value
                   in enumerate(self, 1)
                   if index == value)

    def major_index(self):
        """Return the major index of the perm."""
        return self._zb_perm.majorindex()

    #
    # Pattern matching methods
    #

    def contains(self, patt):
        """Check if the perm contains the patt.
        
        See also:
            Perm.avoids
            Perm.occurrence*
        """
        patt = Perm(patt)
        return self._zb_perm.contains(patt._zb_perm)

    def avoids(self, patt):
        """Check if the perm avoids the patt.
        
        See also:
            Perm.contains
            Perm.occurrence*
        """
        patt = Perm(patt)
        return self._zb_perm.avoids(patt._zb_perm)

    def occurrences_in(self, perm):
        """Find all occurrences of the patt self in perm.

        See also:
            Perm.avoids
            Perm.contains
            Perm.occurrence*
        """
        perm = Perm(perm)
        return list(list(perm[index + 1] for index in occurrence_indices)
                    for occurrence_indices
                    in self._zb_perm.occurrences_in(perm._zb_perm))

    def occurrences_of(self, patt):
        """Find all occurrences of patt in the perm self.

        See also:
                Perm.avoids
                Perm.contains
                Perm.occurrence*
        """
        patt = Perm(patt)
        return patt.occurrences_in(self)

    def occurrence_indices_in(self, perm):
        """Find all indices of occurrences of the patt self in perm.

        See also:
                Perm.avoids
                Perm.contains
                Perm.occurrence*
        """
        perm = Perm(perm)
        return list(list(index + 1 for index in occurrence)
                    for occurrence
                    in self._zb_perm.occurrences_in(perm._zb_perm))

    def occurrence_indices_of(self, patt):
        """Find all indices of occurrences of patt in the perm self.

        See also:
                Perm.avoids
                Perm.contains
                Perm.occurrence*
        """
        patt = Perm(patt)
        return patt.occurrence_indices_in(self)

    #
    # Visualization methods
    #

    def plot(self, *, browser=False, filename=None, file_format=None, **kwargs):
        """Display or save the perm with seaborn/matplotlib.

        Returns an Axes object or None if seaborn is unavailable.

        Keyword arguments:
            browser: If True, sends the image to a browser for viewing.
            filename: Where to save the image.
            file_format: The file format if one wishes to force one.

        Other keyword arguments are passed to seaborn.heatmap.
        The default keyword arguments passed are:
            cbar=False
            cmap="Greys"
            square=True
            vmax=1
            vmin=0
            xticklabels=False
            yticklabels=False

        Tips:
            Set the "xticklabels" kwarg as range(len(self)) for a labelled
            x-axis and the "yticklabels kwarg as range(len(self), -1, -1) for
            a labelled y-axis.
        """
        if not _SEABORN_AVAILABLE:
            return None

        # Compile the data
        n = len(self)
        data = [[0]*n for _ in range(n)]
        for index, value in enumerate(self):
            data[n - value][index] += 1

        # Create the figure
        axes = seaborn.heatmap(data,
                               **(dict(self.plot.default_kwargs, **kwargs)
                                  if kwargs else
                                  self.plot.default_kwargs))
        figure = axes.get_figure()

        # Possibly display and/or save the figure
        if filename:
            figure.savefig(filename,
                           format=file_format,
                           bbox_inches="tight",
                           pad_inches=0)
            if browser:
                webbrowser.open(filename)
        elif browser:
            with tempfile.NamedTemporaryFile(delete=False) as file_pointer:
                figure.savefig(file_pointer,
                               format="svg" if file_format is None else file_format,
                               bbox_inches="tight")
                file_pointer.flush()
                webbrowser.open(file_pointer.name)

        return axes

    plot.default_kwargs = {  # TODO: Good place for default kwargs?
        "cbar": False,
        "cmap": "Greys",
        "square": True,
        "vmax": 1,
        "vmin": 0,
        "xticklabels": False,
        "yticklabels": False
    }

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
        for value in self._zb_perm:
            yield value + 1

    def __getitem__(self, index):
        """Return the value at the one-based index specified."""
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
        for value in reversed(self._zb_perm):
            yield value + 1

    def __contains__(self, patt):
        return self.contains(patt)
    
    def __pow__(self, power):
        perm = self
        for _ in range(power - 1):
            perm *= self
        return perm

    def __iadd__(self, perm):
        return self + Perm(perm)

    def __isub__(self, perm):
        return self - Perm(perm)

    def __imul__(self, perm):
        return self*Perm(perm)

    def __ipow__(self, power):
        return self**power

    def __lshift__(self, times):
        return self.shift_left(times)

    def __ilshift__(self, times):
        return self << times

    def __rshift__(self, times):
        return self.shift_right(times)

    def __irshift__(self, times):
        return self >> times

    def __eq__(self, other):
        _assert_perm(other)
        return self._zb_perm == other._zb_perm

    def __lt__(self, other):
        _assert_perm(other)
        return self._zb_perm < other._zb_perm

    def __le__(self, other):
        _assert_perm(other)
        return self._zb_perm <= other._zb_perm

    def __gt__(self, other):
        _assert_perm(other)
        return self._zb_perm > other._zb_perm

    def __ge__(self, other):
        _assert_perm(other)
        return self._zb_perm >= other._zb_perm

    def __repr__(self):
        if self._zb_perm == _ZBPerm((0,)):
            return "(1)"
        else:
            return str(tuple(self))


Permutation = Perm  # Alias for the more traditional user
