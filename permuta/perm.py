import bisect
import collections
import itertools
import math
import numbers
import operator
import random
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

from .interfaces.flippable import Flippable
from .interfaces.patt import Patt
from .interfaces.rotatable import Rotatable
from .interfaces.shiftable import Shiftable
from .misc.iterable_floor_and_ceiling import left_floor_and_ceiling

__all__ = ("Perm",)

if TYPE_CHECKING:
    tuple_class = Tuple[int]
else:
    tuple_class = tuple


class Perm(tuple_class, Patt, Rotatable, Shiftable, Flippable):
    """A perm class."""

    _TYPE_ERROR: ClassVar[str] = "'{}' object is not a perm"

    #
    # Methods returning a single Perm instance
    #

    def __new__(cls, iterable: Iterable[int] = (), check: bool = False) -> "Perm":
        """Return a Perm instance.

        Raises:
            TypeError:
                Bad argument type.
            ValueError:
                Bad argument, but correct type.

        Examples:
            >>> Perm((0, 3, 1, 2))
            Perm((0, 3, 1, 2))
            >>> Perm(range(5, -1, -1))
            Perm((5, 4, 3, 2, 1, 0))
            >>> Perm("abc", check=True)  # Not good
            Traceback (most recent call last):
                ...
            TypeError: ''a'' object is not an integer
        """
        return tuple.__new__(cls, iterable)

    def __init__(self, iterable: Iterable[int] = (), check: bool = False) -> None:
        # Cache for data used when finding occurrences of self in a perm
        self._cached_pattern_details: Optional[
            List[Tuple[Optional[int], Optional[int], int, int]]
        ] = None
        if check:
            self._init_checked()

    def _init_checked(self) -> None:
        """Checks if a suitable iterable given when initialised."""
        used = [False] * len(self)
        for val in self:
            if not isinstance(val, numbers.Integral):
                message = "'{}' object is not an integer".format(repr(val))
                raise TypeError(message)
            if not 0 <= val < len(self):
                raise ValueError("Element out of range: {}".format(val))
            if used[val]:
                raise ValueError("Duplicate element: {}".format(val))
            used[val] = True

    _to_standard_cache: ClassVar[Dict[Tuple, "Perm"]] = {}

    @classmethod
    def to_standard(cls, iterable: Iterable) -> "Perm":
        """Return the perm corresponding to iterable.

        Duplicate elements are allowed and become consecutive elements (see
        example).

        The standardize alias is supplied for backwards compatibility with
        permpy.  However, the permpy version did not allow for duplicate
        elements.

        Examples:
            >>> Perm.to_standard("a2gsv3")
            Perm((2, 0, 3, 4, 5, 1))
            >>> Perm.to_standard("caaba")
            Perm((4, 0, 1, 3, 2))
        """
        iterable = tuple(iterable)
        if iterable not in Perm._to_standard_cache:
            Perm._to_standard_cache[iterable] = cls(
                idx
                for (idx, _) in sorted(enumerate(iterable), key=operator.itemgetter(1))
            ).inverse()
        return Perm._to_standard_cache[iterable]

    standardize = to_standard  # permpy backwards compatibility
    from_iterable = to_standard

    @classmethod
    def from_integer(cls, integer: int) -> "Perm":
        """Return the perm corresponding to the integer given. The permutation
        can be given one-based or zero-base but it will be returned in 0-based.

        Examples:
            >>> Perm.from_integer(123)
            Perm((0, 1, 2))
            >>> Perm.from_integer(321)
            Perm((2, 1, 0))
            >>> Perm.from_integer(201)
            Perm((2, 0, 1))
        """
        if not 0 <= integer <= 9876543210:
            raise ValueError(f"Illegal perm: {integer}")
        if integer == 0:
            return Perm((0,))
        digit_list: List[int] = []
        while integer != 0:
            digit_list.append(integer % 10)
            integer //= 10
        return Perm.to_standard(reversed(digit_list))

    @classmethod
    def from_string(cls, string: str, check: bool = False) -> "Perm":
        """Return the perm corresponding to the string given.

        Examples:
            >>> Perm.from_string("203451")
            Perm((2, 0, 3, 4, 5, 1))
            >>> Perm.from_string("40132")
            Perm((4, 0, 1, 3, 2))
        """
        if string == "ε":
            return cls((), check=check)
        return cls(map(int, string), check=check)

    @classmethod
    def one_based(cls, iterable: Iterable[int]) -> "Perm":
        """A way to enter a perm in the traditional permuta way.

        Examples:
            >>> Perm.one_based((4, 1, 3, 2))
            Perm((3, 0, 2, 1))
        """
        return cls((val - 1 for val in iterable))

    one = one_based
    proper = one_based
    scientific = one_based

    @classmethod
    def identity(cls, length: int) -> "Perm":
        """Return the identity perm of the specified length.

        Examples:
            >>> Perm.identity(0)
            Perm(())
            >>> Perm.identity(4)
            Perm((0, 1, 2, 3))
        """
        return cls(range(length))

    @classmethod
    def random(cls, length: int) -> "Perm":
        """Return a random perm of the specified length.

        Examples:
            >>> perm = Perm.random(8)
            >>> len(perm) == 8
            True
            >>> # TODO: test perm in PermSet(8)
        """
        result = list(range(length))
        random.shuffle(result)
        return cls(result)

    @classmethod
    def monotone_increasing(cls, length: int) -> "Perm":
        """Return a monotone increasing perm of the specified length.

        Examples:
            >>> Perm.monotone_increasing(0)
            Perm(())
            >>> Perm.monotone_increasing(4)
            Perm((0, 1, 2, 3))
        """
        return cls(range(length))

    @classmethod
    def monotone_decreasing(cls, length: int) -> "Perm":
        """Return a monotone decreasing perm of the specified length.

        Examples:
            >>> Perm.monotone_decreasing(0)
            Perm(())
            >>> Perm.monotone_decreasing(4)
            Perm((3, 2, 1, 0))
        """
        return cls(range(length - 1, -1, -1))

    @classmethod
    def unrank(cls, number: int, length: Optional[int] = None) -> "Perm":
        """
        Get permutation by lexicographical order.

        Examples:
            >>> Perm.unrank(0)
            Perm(())
            >>> Perm.unrank(1)
            Perm((0,))
            >>> Perm.unrank(2)
            Perm((0, 1))
            >>> Perm.unrank(3)
            Perm((1, 0))
            >>> Perm.unrank(4)
            Perm((0, 1, 2))
            >>> Perm.unrank(5)
            Perm((0, 2, 1))
            >>> Perm.unrank(1, 3)
            Perm((0, 2, 1))
        """
        factorial = [1, 1]
        if length is None:
            if number == 0:
                return cls()
            length = 1
            while number > factorial[-1]:
                number -= factorial[-1]
                length += 1
                factorial.append(factorial[-1] * length)
            number -= 1
        return cls(Perm._unrank(number, length, factorial))

    @staticmethod
    def _unrank(number: int, length: int, factorial: List[int]) -> Iterator[int]:
        for i in range(len(factorial), length + 1):
            factorial.append(i * factorial[-1])
        assert length >= 0
        assert 0 <= number < factorial[length]
        candidates = list(range(length))
        for val in range(1, length + 1):
            division, number = divmod(number, factorial[length - val])
            yield candidates.pop(division)

    ind2perm = unrank  # permpy backwards compatibility

    #
    # Methods modifying/combining Perm instances
    #

    def direct_sum(self, *others: "Perm") -> "Perm":
        """Return the direct sum of two or more perms.

        Examples:
            >>> Perm((0,)).direct_sum(Perm((1, 0)))
            Perm((0, 2, 1))
            >>> Perm((0,)).direct_sum(Perm((1, 0)), Perm((2, 1, 0)))
            Perm((0, 2, 1, 5, 4, 3))
        """
        result = list(self)
        shift = len(self)
        for other in others:
            result.extend(val + shift for val in other)
            shift += len(other)
        return Perm(result)

    def skew_sum(self, *others: "Perm") -> "Perm":
        """Return the skew sum of two or more perms.

        Examples:
            >>> Perm((0,)).skew_sum(Perm((0, 1)))
            Perm((2, 0, 1))
            >>> Perm((0,)).skew_sum(Perm((0, 1)), Perm((2, 1, 0)))
            Perm((5, 3, 4, 2, 1, 0))
        """
        shift = sum(len(other) for other in others)
        result = [val + shift for val in self]
        for other in others:
            shift -= len(other)
            result.extend(val + shift for val in other)
        return Perm(result)

    def compose(self, *others: "Perm") -> "Perm":
        """Return the composition of two or more perms.

        Examples:
            >>> Perm((0, 3, 1, 2)).compose(Perm((2, 1, 0, 3)))
            Perm((1, 3, 0, 2))
            >>> Perm((1, 0, 2)).compose(Perm((0, 1, 2)), Perm((2, 1, 0)))
            Perm((2, 0, 1))
        """
        assert all(
            isinstance(other, Perm) and len(other) == len(self) for other in others
        )
        return Perm(self._composed_value(idx, *others) for idx in range(len(self)))

    def _composed_value(self, idx: int, *others: "Perm") -> int:
        for other in reversed(others):
            idx = other[idx]
        return self[idx]

    multiply = compose

    def insert(
        self, index: Optional[int] = None, new_element: Optional[int] = None
    ) -> "Perm":
        """Return the perm acquired by adding a new element at index. The index defaults
        to the right end and value defaults to len(self).

        Raises:
            IndexError:
                Index is not valid.
            ValueError:
                Element passed cannot legally be added to perm.

        Examples:
            >>> Perm((0, 1)).insert()
            Perm((0, 1, 2))
            >>> Perm((0, 1)).insert(0)
            Perm((2, 0, 1))
            >>> Perm((2, 0, 1)).insert(2, 1)
            Perm((3, 0, 1, 2))
        """
        if index is None:
            index = len(self) + 1
        if new_element is None:
            new_element = len(self)
        else:
            if not 0 <= new_element <= len(self):
                raise ValueError("Element out of range: {}".format(new_element))
        slice_1 = (
            val if val < new_element else val + 1
            for val in itertools.islice(self, index)
        )
        slice_2 = (
            val if val < new_element else val + 1
            for val in itertools.islice(self, index, len(self))
        )
        return Perm(itertools.chain(slice_1, (new_element,), slice_2))

    def remove(self, index: Optional[int] = None) -> "Perm":
        """Return the perm acquired by removing an element at a specified index. It
        defaults to the greatest element.

        Raises:
            IndexError:
                Index is not valid.

        Examples:
            >>> Perm((2, 0, 1)).remove()
            Perm((0, 1))
            >>> Perm((3, 0, 1, 2)).remove(0)
            Perm((0, 1, 2))
            >>> Perm((2, 0, 1)).remove(2)
            Perm((1, 0))
            >>> Perm((0,)).remove(0)
            Perm(())
        """
        if index is None:
            return self.remove_element()
        selected = self[index]
        return Perm(
            val if val < selected else val - 1 for val in self if val != selected
        )

    def remove_element(self, selected: Optional[int] = None) -> "Perm":
        """Return the perm acquired by removing a specific element from self. It
        defaults to the largest element.

        Raises:
            ValueError:
                Selected element does not belong to perm.

        Examples:
            >>> Perm((3, 0, 1, 2)).remove_element()
            Perm((0, 1, 2))
            >>> Perm((3, 0, 2, 1)).remove_element(0)
            Perm((2, 1, 0))
        """
        if selected is None:
            selected = len(self) - 1
        else:
            if not 0 <= selected < len(self):
                raise ValueError("Element out of range: {}".format(selected))
        return Perm(
            val if val < selected else val - 1 for val in self if val != selected
        )

    def inflate(self, components: Iterable["Perm"]) -> "Perm":
        """Inflate elements of the permutation to create a new one.

        Examples:
            >>> Perm((0, 1)).inflate([Perm((1, 0)), Perm((2, 1, 0))])
            Perm((1, 0, 4, 3, 2))
            >>> Perm((1, 0, 2)).inflate([None, Perm((0, 1)), Perm((0, 1))])
            Perm((2, 0, 1, 3, 4))
            >>> # Can also deflate points
            >>> Perm((0, 1)).inflate([Perm(), Perm()])
            Perm(())
        """
        components = tuple(components)
        assert len(components) == len(self)
        shift = 0
        shifts = [0] * len(self)
        for index in self.inverse():
            shifts[index] = shift
            component = components[index]
            shift += 1 if component is None else len(component)
        perm_elements: List[int] = []
        for index, component in enumerate(components):
            if component is None:
                perm_elements.append(shifts[index])
            else:
                shift = shifts[index]
                perm_elements.extend(element + shift for element in component)
        return Perm(perm_elements)

    def contract_inc_bonds(self) -> "Perm":
        # TODO: test
        monblocks = self.monotone_block_decomposition_ascending(with_ones=True)
        return Perm.to_standard([start for start, _ in monblocks])

    def contract_dec_bonds(self) -> "Perm":
        # TODO: test
        monblocks = self.monotone_block_decompositon_descending(with_ones=True)
        return Perm.to_standard([start for start, _ in monblocks])

    def contract_bonds(self) -> None:
        # TODO: reimplement by calling contract_{inc,dec}_bonds or remove
        raise NotImplementedError()

    #
    # Methods for basic Perm transforming
    #

    def inverse(self) -> "Perm":
        """Return the inverse of the perm self.

        Examples:
            >>> Perm((1, 2, 5, 0, 3, 4)).inverse()
            Perm((3, 0, 1, 4, 5, 2))
            >>> Perm((2, 0, 1)).inverse().inverse() == Perm((2, 0, 1))
            True
            >>> Perm((0, 1)).inverse()
            Perm((0, 1))
        """
        result = [0] * len(self)
        for idx, val in enumerate(self):
            result[val] = idx
        return Perm(result)

    def reverse(self) -> "Perm":
        """Return the reverse of the perm self.

        Examples:
            >>> Perm((1, 2, 5, 0, 3, 4)).reverse()
            Perm((4, 3, 0, 5, 2, 1))
            >>> Perm((0, 1)).reverse()
            Perm((1, 0))
        """
        return Perm(self[::-1])

    def complement(self) -> "Perm":
        """Return the complement of the perm self.

        Examples:
            >>> Perm((1, 2, 3, 0, 4)).complement()
            Perm((3, 2, 1, 4, 0))
            >>> Perm((2, 0, 1)).complement()
            Perm((0, 2, 1))
        """
        base = len(self) - 1
        return Perm(base - element for element in self)

    def reverse_complement(self) -> "Perm":
        """Return the reverse complement of self. Equivalent to two left or right
        rotations.

        Examples:
            >>> Perm((1, 2, 3, 0, 4)).reverse_complement()
            Perm((0, 4, 1, 2, 3))
            >>> Perm((2, 0, 1)).reverse_complement()
            Perm((1, 2, 0))
        """
        base = len(self) - 1
        return Perm(base - element for element in reversed(self))

    def shift_right(self, times: int = 1) -> "Perm":
        """Return self shifted times steps to the right. If shift is negative, shifted
        to the left.

        Examples:
            >>> Perm((0, 1, 2)).shift_right()
            Perm((2, 0, 1))
            >>> Perm((0, 1, 2)).shift_right(-4)
            Perm((1, 2, 0))
        """
        if len(self) == 0:
            return self
        times = times % len(self)
        if times == 0:
            return self
        index = len(self) - times
        slice_1 = itertools.islice(self, index)
        slice_2 = itertools.islice(self, index, len(self))
        return Perm(itertools.chain(slice_2, slice_1))

    def shift_left(self, times: int = 1) -> "Perm":
        """Return self shifted times steps to the left. If shift is negative, shifted
        to the right.

        Examples:
            >>> Perm((0, 1, 2)).shift_left()
            Perm((1, 2, 0))
            >>> Perm((0, 1, 2)).shift_left(-4)
            Perm((2, 0, 1))
        """
        return self.shift_right(-times)

    shift = shift_right
    cyclic_shift = shift_right
    cyclic_shift_right = shift_right
    cyclic_shift_left = shift_left

    def shift_up(self, times: int = 1) -> "Perm":
        """Return self shifted times steps up. If times is negative, shifted down.

        Examples:
            >>> Perm((0, 1, 2, 3)).shift_up(1)
            Perm((1, 2, 3, 0))
            >>> Perm((0, 1, 2, 3)).shift_up(-7)
            Perm((1, 2, 3, 0))
            >>> Perm((0,)).shift_up(1234)
            Perm((0,))
        """
        if len(self) == 0:
            return self
        times = times % len(self)
        if times == 0:
            return self
        bound = len(self)
        return Perm((val + times) % bound for val in self)

    def shift_down(self, times: int = 1) -> "Perm":
        """Return self shifted times steps down. If times is negative, shifted up.

        Examples:
            >>> Perm((0, 1, 2, 3)).shift_down(1)
            Perm((3, 0, 1, 2))
            >>> Perm((0, 1, 2, 3)).shift_down(-7)
            Perm((3, 0, 1, 2))
            >>> Perm((0,)).shift_down(1234)
            Perm((0,))
        """
        return self.shift_up(-times)

    def flip_horizontal(self) -> "Perm":
        """Return self flipped horizontally.

        Examples:
            >>> Perm((1, 2, 3, 0, 4)).flip_horizontal()
            Perm((3, 2, 1, 4, 0))
            >>> Perm((2, 0, 1)).flip_horizontal()
            Perm((0, 2, 1))
        """
        return self.complement()

    def flip_vertical(self) -> "Perm":
        """Return self flipped vertically.

        Examples:
            >>> Perm((1, 2, 5, 0, 3, 4)).flip_vertical()
            Perm((4, 3, 0, 5, 2, 1))
            >>> Perm((0, 1)).flip_vertical()
            Perm((1, 0))
        """
        return self.reverse()

    def flip_diagonal(self) -> "Perm":
        """Return self flipped along the diagonal.

        Examples:
            >>> Perm((1, 2, 5, 0, 3, 4)).flip_diagonal()
            Perm((3, 0, 1, 4, 5, 2))
            >>> Perm((0, 1)).flip_diagonal()
            Perm((0, 1))
        """
        return self.inverse()

    def flip_antidiagonal(self) -> "Perm":
        """Return self flipped along the antidiagonal..

        Examples:
            >>> Perm((3, 2, 0, 1)).flip_antidiagonal()
            Perm((3, 2, 0, 1))
            >>> Perm((1, 2, 3, 0, 4)).flip_antidiagonal()
            Perm((0, 2, 3, 4, 1))
            >>> Perm((1, 2, 0, 3)).flip_antidiagonal()
            Perm((0, 2, 3, 1))
        """
        n = len(self)
        result = [0] * n
        flipped_pairs = ((n - val - 1, n - idx - 1) for idx, val in enumerate(self))
        for idx, val in flipped_pairs:
            result[idx] = val
        return Perm(result)

    def _rotate_right(self) -> "Perm":
        """Return self rotated 90 degrees to the right."""
        n = len(self)
        result = [0] * n
        for idx, val in enumerate(self):
            result[val] = n - idx - 1
        return Perm(result)

    def _rotate_left(self) -> "Perm":
        """Return self rotated 90 degrees to the left."""
        n = len(self)
        result = [0] * n
        for idx, val in enumerate(self):
            result[n - val - 1] = idx
        return Perm(result)

    def _rotate_180(self) -> "Perm":
        """Return self rotated 180 degrees."""
        return self.reverse_complement()

    def all_syms(self) -> Tuple["Perm", ...]:
        """Returns all symmetries of the permutation in a PermSet, all possible
        combinations of revers, complement and inverse.
        """
        syms = {self, self.inverse()}
        curr = self
        for _ in range(3):
            curr = curr.rotate()
            syms.update((curr, curr.inverse()))
        return tuple(syms)

    #
    # Statistical methods
    #

    def is_increasing(self) -> bool:
        """Return True if the perm is increasing, and False otherwise."""
        return all(idx == val for idx, val in enumerate(self))

    def is_decreasing(self) -> bool:
        """Return True if the perm is decreasing, and False otherwise."""
        n = len(self)
        return all(val == n - idx - 1 for idx, val in enumerate(self))

    def count_fixed_points(self) -> int:
        """Return the number of fixed points in self.

        Examples:
            >>> Perm((0, 1, 4, 3, 2)).count_fixed_points()
            3
            >>> Perm((0, 1, 2, 3, 4)).count_fixed_points()
            5
            >>> Perm((3, 2, 1, 0)).count_fixed_points()
            0
        """
        return sum(1 for _ in self.fixed_points())

    def fixed_points(self) -> Iterator[int]:
        """Yield the index of the fixed points in self.

        Examples:
            >>> tuple(Perm((0, 2, 1, 3)).fixed_points())
            (0, 3)
            >>> tuple(Perm((0, 1, 4, 3, 2)).fixed_points())
            (0, 1, 3)
        """
        return (idx for idx, val in enumerate(self) if idx == val)

    def strong_fixed_points(self) -> Iterator[int]:
        """Yield the index of the strong fixed points in self.

        Examples:
            >>> tuple(Perm((0, 2, 1, 3)).strong_fixed_points())
            (0, 3)
            >>> tuple(Perm((0, 1, 4, 3, 2)).strong_fixed_points())
            (0, 1)
        """
        if self != Perm(()):
            n = len(self)
            curmax = self[0]
            for idx, val in enumerate(self):
                if idx == val:
                    if val >= curmax:
                        if idx == n - 1 or val < min(
                            self[i] for i in range(idx + 1, n)
                        ):
                            yield idx

    def is_skew_decomposable(self) -> bool:
        """Determines whether the permutation is expressible as the skew sum of
        two permutations.

        >>> p = Perm.random(8).direct_sum(Perm.random(12))
        >>> p.skew_decomposable()
        False
        >>> p.complement().skew_decomposable()
        True
        """
        n = len(self)
        return any(
            set(range(n - i, n)) == set(itertools.islice(self, i)) for i in range(1, n)
        )

    skew_decomposable = is_skew_decomposable  # permpy backwards compatibility

    def is_sum_decomposable(self) -> bool:
        """Determines whether the permutation is expressible as the direct sum of
        two permutations.

        >>> p = Perm.random(4).direct_sum(Perm.random(15))
        >>> p.sum_decomposable()
        True
        >>> p.reverse().sum_decomposable()
        False
        """
        return any(
            set(range(i)) == set(itertools.islice(self, i)) for i in range(1, len(self))
        )

    sum_decomposable = is_sum_decomposable  # permpy backwards compatibility

    def descents(self) -> Iterator[int]:
        """Yield the 0-based descents of self.

        Examples:
            >>> tuple(Perm((0, 1, 3, 2, 4)).descents())
            (2,)
            >>> tuple(Perm((3, 2, 1, 0)).descents())
            (0, 1, 2)
            >>> tuple(Perm((0, 1, 2)).descents())
            ()
        """
        return (
            idx
            for idx, (prev, curr) in enumerate(
                zip(self, itertools.islice(self, 1, None))
            )
            if prev > curr
        )

    def descent_set(self) -> List[int]:
        """Return the list of descents of self.

        This method is for backwards compatibility with permpy.
        """
        return list(self.descents())

    def count_descents(self) -> int:
        """Count the number of descents of self.
        Examples:
            >>> Perm((0, 1, 3, 2, 4)).count_descents()
            1
            >>> Perm((3, 2, 1, 0)).count_descents()
            3
            >>> Perm((0, 1, 2)).count_descents()
            0
        """
        return sum(1 for _ in self.descents())

    num_descents = count_descents  # permpy backwards compatibility

    def ascents(self) -> Iterator[int]:
        """Yield the 0-based ascent of self.

        Examples:
            >>> tuple(Perm((0, 1, 3, 2, 4)).ascents())
            (0, 1, 3)
            >>> tuple(Perm((0, 4, 3, 2, 1)).ascents())
            (0,)
            >>> tuple(Perm((3, 2, 1, 0)).ascents())
            ()
        """
        return (
            idx
            for idx, (prev, curr) in enumerate(
                zip(self, itertools.islice(self, 1, None))
            )
            if prev < curr
        )

    def ascent_set(self) -> List[int]:
        """Return the list of ascents of self.

        This method is for backwards compatibility with permpy.
        """
        return list(self.ascents())

    def count_ascents(self) -> int:
        """Count the number of ascents in self.

        Examples:
            >>> Perm((0, 1, 3, 2, 4)).count_ascents()
            3
            >>> Perm((0, 4, 3, 2, 1)).count_ascents()
            1
            >>> Perm((3, 2, 1, 0)).count_ascents()
            0
        """
        return sum(1 for _ in self.ascents())

    num_ascents = count_ascents  # permpy backwards compatibility

    def peaks(self) -> Iterator[int]:
        """Yield the indices of the peaks of self. The i-th element of a perm is a peak
        if self[i-1] < self[i] > self[i+1].

        Examples:
            >>> tuple(Perm((5, 3, 4, 0, 2, 1)).peaks())
            (2, 4)
            >>> tuple(Perm((1, 2, 0)).peaks())
            (1,)
            >>> tuple(Perm((2, 1, 0)).peaks())
            ()
        """
        return (
            idx + 1
            for idx, (prev, curr, nxt) in enumerate(
                zip(
                    itertools.islice(self, 0, None),
                    itertools.islice(self, 1, None),
                    itertools.islice(self, 2, None),
                )
            )
            if prev < curr > nxt
        )

    def peak_list(self) -> List[int]:
        """Return the list of peaks of self. This method is for backwards compatibility
        with permpy.
        """
        return list(self.peaks())

    def count_peaks(self) -> int:
        """Count the number of peaks of self.

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).count_peaks()
            2
            >>> Perm((1, 2, 0)).count_peaks()
            1
            >>> Perm((2, 1, 0)).count_peaks()
            0
        """
        return sum(1 for _ in self.peaks())

    num_peaks = count_peaks  # permpy backwards compatibility

    def valleys(self) -> Iterator[int]:
        """Yield the indices of the valleys of self. The i-th element of a perm is a
        valley if self[i-1] > self[i] < self[i+1].

        Examples:
            >>> tuple(Perm((5, 3, 4, 0, 2, 1)).valleys())
            (1, 3)
            >>> tuple(Perm((2, 0, 1)).valleys())
            (1,)
            >>> tuple(Perm((1, 2, 0)).valleys())
            ()
        """
        return (
            idx + 1
            for idx, (prev, curr, nxt) in enumerate(
                zip(
                    itertools.islice(self, 0, None),
                    itertools.islice(self, 1, None),
                    itertools.islice(self, 2, None),
                )
            )
            if prev > curr < nxt
        )

    def valley_list(self) -> List[int]:
        """Return the list of valleys of self. This method is for backwards
        compatibility with permpy.
        """
        return list(self.valleys())

    def count_valleys(self) -> int:
        """Count the number of valleys of self.

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).count_valleys()
            2
            >>> Perm((2, 0, 1)).count_valleys()
            1
            >>> Perm((1, 2, 0)).count_valleys()
            0
        """
        return sum(1 for _ in self.valleys())

    num_valleys = count_valleys  # permpy backwards compatibility

    def bends(self) -> Iterator[int]:
        """Yield the indices at which the permutation changes direction. That
        is, the number of non-monotone consecutive triples of the permutation.
        A permutation p can be expressed as the concatenation of len(p.bends())
        + 1 monotone segments.

        Examples:
            >>> list(Perm((5, 3, 4, 0, 2, 1)).bends())
            [1, 2, 3, 4]
            >>> list(Perm((2, 0, 1)).bends())
            [1]
        """
        return (
            idx + 1
            for idx, (prev, curr, nxt) in enumerate(
                zip(
                    itertools.islice(self, 0, None),
                    itertools.islice(self, 1, None),
                    itertools.islice(self, 2, None),
                )
            )
            if (prev < curr > nxt) or (prev > curr < nxt)
        )

    def bend_list(self) -> List[int]:
        """Returns the list of indices at which the permutation changes
        direction. That is, the number of non-monotone consecutive triples of
        the permutation. A permutation p can be expressed as the concatenation
        of len(p.bend_list()) + 1 monotone segments.

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).bend_list()
            [1, 2, 3, 4]
            >>> Perm((2, 0, 1)).bend_list()
            [1]
        """
        return list(self.bends())

    def order(self) -> int:
        """Returns the order of the permutation.

        Examples:
            >>> Perm((4, 3, 5, 0, 2, 1)).order()
            6
            >>> Perm((0, 1, 2)).order()
            1
        """
        acc = 1
        for cycle in map(len, self.cycle_decomp()):
            acc = (acc * cycle) // math.gcd(acc, cycle)
        return acc

    # TODO: reimplement the following four functions to return generators
    def ltrmin(self) -> List[int]:
        """Returns the positions of the left-to-right minima.

        Examples:
            >>> Perm((2, 4, 3, 0, 1)).ltrmin()
            [0, 3]
        """
        lis = []
        minval = len(self) + 1
        for idx, val in enumerate(self):
            if val < minval:
                lis.append(idx)
                minval = val
        return lis

    def rtlmin(self) -> List[int]:
        """Returns the positions of the right-to-left minima.

        Examples:
            >>> Perm((2, 0, 4, 1, 5, 3)).rtlmin()
            [1, 3, 5]
        """
        rev_perm = self.reverse()
        return [len(self) - val - 1 for val in rev_perm.ltrmin()][::-1]

    def ltrmax(self) -> List[int]:
        """Returns the positions of the left-to-right maxima.

        Examples:
            >>> Perm((2, 0, 4, 1, 5, 3)).ltrmax()
            [0, 2, 4]
        """
        return [len(self) - i - 1 for i in Perm(self[::-1]).rtlmax()][::-1]

    def rtlmax(self) -> List[int]:
        """Returns the positions of the right-to-left maxima.

        Examples:
            >>> Perm((2, 4, 3, 0, 1)).rtlmax()
            [1, 2, 4]
        """
        return [len(self) - i - 1 for i in self.complement().reverse().ltrmin()][::-1]

    def count_ltrmin(self) -> int:
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self.ltrmin())

    def count_ltrmax(self) -> int:
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self.ltrmax())

    def count_rtlmin(self) -> int:
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self.rtlmin())

    def count_rtlmax(self) -> int:
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self.rtlmax())

    num_ltrmin = count_ltrmin

    def count_inversions(self) -> int:
        """Returns the number of inversions of the permutation, i.e., the
        number of pairs i,j such that i < j and self(i) > self(j).

        Example:
            >>> Perm((3, 0, 2, 1)).count_inversions()
            4
            >>> Perm.monotone_decreasing(6).count_inversions() == 5*6 / 2
            True
            >>> Perm.monotone_increasing(7).count_inversions()
            0
        """
        bit_len = len(self) + 1
        bit = [0] * bit_len
        for element in reversed(self):
            bit_index = element + 1
            # Count lesser elements to the right
            while element:
                bit[0] += bit[element]
                # Flip the right most set bit
                element &= element - 1
            # Increment frequency for current element
            while bit_index < bit_len:
                bit[bit_index] += 1
                # Increase index by the largest power of two that divides it
                bit_index += bit_index & -bit_index
        return bit[0]

    def inversions(self) -> Iterator[Tuple[int, int]]:
        """Yield the inversions of the permutation, i.e., the pairs i,j
        such that i < j and self(i) > self(j).

        TODO: Reimplement in NlogN time.
        Example:
            >>> tuple(Perm((3, 0, 2, 1)).inversions())
            ((0, 1), (0, 2), (0, 3), (2, 3))
        """
        n = len(self)
        for i, prev in enumerate(self):
            for j in range(i + 1, n):
                if prev > self[j]:
                    yield i, j

    def count_non_inversions(self) -> int:
        """Returns the number of non_inversions of the permutation, i.e., the
        number of pairs i,j such that i < j and self[i] < self[j].

        Examples:
            >>> Perm((3, 0, 2, 1, 4)).count_non_inversions()
            6
            >>> Perm.monotone_increasing(7).count_non_inversions() == (6 * 7)/2
            True
        """
        n = len(self)
        return n * (n - 1) // 2 - self.count_inversions()

    def non_inversions(self) -> Iterator[Tuple[int, int]]:
        """Yields the non_inversions of the permutation, i.e., the pairs i,j
        such that i < j and self[i] < self[j].

        Examples:
            >>> tuple(Perm((3, 0, 2, 1, 4)).non_inversions())
            ((0, 4), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4))
        """
        n = len(self)
        for i, prev in enumerate(self):
            for j in range(i + 1, n):
                if prev < self[j]:
                    yield i, j

    def min_gapsize(self) -> int:
        """Returns the minimum gap between any two entries in the permutation
        (computed with the taxicab metric).

        Examples:
            >>> Perm((2, 0, 3, 1)).min_gapsize()
            3
        """
        return min(
            abs(i - j) + abs(self[i] - self[j])
            for i, j in itertools.combinations(range(len(self)), 2)
        )

    def count_bonds(self) -> int:
        """Counts the number of bonds, that is the number of adjacent locations
        with adjacent values.

        Examples:
            >>> Perm((0, 1, 2)).count_bonds()
            2
            >>> Perm((2, 1, 0)).count_bonds()
            2
            >>> Perm((4, 0, 3, 2, 1, 5)).count_bonds()
            2
        """
        return self.count_dec_bonds() + self.count_inc_bonds()

    num_bonds = count_bonds
    bonds = count_bonds  # permpy backwards compatibility

    def inc_bonds(self) -> Iterator[int]:
        """Yields the indices of the increasing bonds, that is the indices of
        the ascents with adjacent values.

        Examples:
            >>> list(Perm((2, 3, 4, 5, 0, 1)).inc_bonds())
            [0, 1, 2, 4]
        """
        return (
            idx
            for idx, (prev, curr) in enumerate(
                zip(self, itertools.islice(self, 1, None))
            )
            if curr == prev + 1
        )

    def count_inc_bonds(self) -> int:
        """Counts the number of increasing bonds.

        Examples:
            >>> Perm((0, 2, 3, 1)).count_inc_bonds()
            1
            >>> Perm((2, 3, 4, 5, 0, 1)).count_inc_bonds()
            4
        """
        return len(list(self.inc_bonds()))

    num_inc_bonds = count_inc_bonds

    def dec_bonds(self) -> Iterator[int]:
        """Yields the indices of the decreasing bonds, that is the indices of
        the descents with adjacent values.

        Examples:
            >>> list(Perm((1, 0, 3, 2, 5, 4)).dec_bonds())
            [0, 2, 4]
        """
        return (
            idx
            for idx, (prev, curr) in enumerate(
                zip(self, itertools.islice(self, 1, None))
            )
            if prev == curr + 1
        )

    def count_dec_bonds(self) -> int:
        """Counts the number of decreasing bonds.

        Examples:
            >>> Perm((2, 1, 0, 3)).count_dec_bonds()
            2
            >>> Perm((1, 0, 3, 2, 5, 4)).count_dec_bonds()
            3
        """
        return len(list(self.dec_bonds()))

    num_dec_bonds = count_dec_bonds

    def major_index(self) -> int:
        """Returns the major index of the permutation, that is the sum of the
        positions of the descents of the permutation.

        Examples:
            >>> Perm((3, 1, 2, 4, 0)).major_index()
            5
            >>> Perm((0, 2, 1)).major_index()
            2
        """
        return sum(1 + desc for desc in self.descents())

    def longestruns_ascending(self) -> Tuple[int, List[int]]:
        """Returns the longest ascending runs in the permutation as a pair of
        the length and a list of the starting indices.
        """
        n = len(self)
        if n == 0:
            return (0, [])
        perm_list = list(self)
        maxi = 1
        res: List[int] = []
        cur = 0
        for i in range(1, n):
            if perm_list[i - 1] < perm_list[i]:
                if (i - cur + 1) > maxi:
                    del res
                    res = []
                    maxi = i - cur + 1
            else:
                if (i - cur) == maxi:
                    res.append(cur)
                cur = i
        if n - cur == maxi:
            res.append(cur)
        return (maxi, res)

    def longestruns_descending(self) -> Tuple[int, List[int]]:
        """Returns the longest descending runs in the permutation as a pair of
        the length and a list of the starting indices.
        """
        return self.complement().longestruns_ascending()

    def longestruns(self) -> Tuple[int, List[int]]:
        """Returns the longest ascending runs in the permutation as a pair of
        the length and a list of the starting indices.
        """
        return self.longestruns_ascending()

    def length_of_longestrun_ascending(self) -> int:
        """Returns the length of the longest ascending run in the permutation.
        """
        return self.longestruns_ascending()[0]

    def length_of_longestrun_descending(self) -> int:
        """Returns the length of the longest descending run in the permutation.
        """
        return self.complement().length_of_longestrun_ascending()

    def length_of_longestrun(self) -> int:
        """Returns the length of the longest ascending run in the permutation.
        """
        return self.length_of_longestrun_ascending()

    def cycle_decomp(self) -> List[List[int]]:
        """Calculates the cycle decomposition of the permutation. Returns a list
        of cycles, each of which is represented as a list.

        >>> Perm((4, 2, 7, 0, 3, 1, 6, 5)).cycle_decomp()
        [[4, 3, 0], [6], [7, 5, 1, 2]]
        """
        n = len(self)
        seen: Set[int] = set()
        cyclelist = []
        while len(seen) < n:
            max_not_seen = max(set(range(n)) - seen)
            cycle = [max_not_seen]
            val = self(max_not_seen)
            seen.add(val)
            while val != max_not_seen:
                cycle.append(val)
                val = self(val)
                seen.add(val)
            cyclelist.append(cycle)
        cyclelist.reverse()
        return cyclelist

    def count_cycles(self) -> int:
        """Returns the number of cycles in the permutation.

        >>> Perm((5, 3, 8, 1, 0, 4, 2, 7, 6)).count_cycles()
        4
        """
        return len(self.cycle_decomp())

    num_cycles = count_cycles  # permpy backwards compatibility

    def is_involution(self) -> bool:
        """Checks if the permutation is an involution, i.e., is equal to it's
        own inverse.

        Examples:
            >>> Perm((2, 1, 0)).is_involution()
            True
            >>> Perm((3, 0, 2, 4, 1, 5)).is_involution()
            False
        """

        return self == self.inverse()

    def is_identity(self) -> bool:
        """Checks if the permutation is the identity.

        >>> p = Perm.random(10)
        >>> (p * p.inverse()).is_identity()
        True
        """

        return self == Perm.identity(len(self))

    def rank(self) -> int:
        """Computes the rank of a permutation.
        Examples:
            >>> Perm((0, 1)).rank()
            2
            >>> Perm((0, 2, 1, 3)).rank()
            12
        """
        n = len(self)
        if n == 0:
            return 0
        fact = [1]
        for i in range(n):
            fact.append(fact[i] * (i + 1))
        res = 0
        vals: List[int] = list()
        for idx, val in enumerate(self):
            ordered_pos = bisect.bisect_left(vals, val)
            res += (val - ordered_pos) * fact[n - idx - 1] + fact[n - idx - 1]
            vals.insert(ordered_pos, val)
        return res

    perm2ind = rank  # permpy backwards compatibility

    def threepats(self) -> Dict["Perm", int]:
        """Returns a dictionary of the number of occurrences of each
        permutation pattern of length 3.

        Examples:
            >>> res = Perm((2, 1, 0, 3)).threepats()
            >>> res[Perm((1, 0, 2))]
            3
            >>> res[Perm((1, 2, 0))]
            0
        """
        return collections.Counter(
            Perm.to_standard((left, mid, right))
            for left, mid, right in itertools.combinations(self, 3)
        )

    def fourpats(self) -> Dict["Perm", int]:
        """Returns a dictionary of the number of occurrences of each
        permutation pattern of length 4.

        Examples:
            >>> res = Perm((1, 0, 3, 5, 2, 4)).fourpats()
            >>> res[Perm((0, 2, 3, 1))]
            2
            >>> res[Perm((3, 1, 2, 0))]
            0
        """
        return collections.Counter(
            Perm.to_standard((left, mid_left, mid_right, right))
            for left, mid_left, mid_right, right in itertools.combinations(self, 4)
        )

    def rank_val(self, i: int) -> int:
        """Returns the 'rank value'(?) of index i, the number of inversions
        with the value at i being the greater element.


        Examples:
            >>> Perm((3, 0, 2, 1)).rank_val(0)
            3
            >>> Perm((0, 2, 4, 3, 1)).rank_val(1)
            1
        """
        return len([j for j in range(i + 1, len(self)) if self[j] < self[i]])

    def rank_encoding(self) -> List[int]:
        """Returns the 'rank value'(?) of each index in the permutation, the
        number of inversions 'caused' by the values at each index.

        Examples:
            >>> Perm((3, 0, 2, 1)).rank_encoding()
            [3, 0, 1, 0]
            >>> Perm((0, 2, 4, 3, 1)).rank_encoding()
            [0, 1, 2, 1, 0]
        """
        return [self.rank_val(i) for i in range(len(self))]

    #
    # Decomposition and generation from self methods
    #
    def sum_decomposition(self) -> List["Perm"]:
        """
        Return the sum decomposition of the permutation.
        """
        res: List[Perm] = []
        max_val = -1
        curr_block_start_idx = 0
        for idx, val in enumerate(self):
            max_val = max(max_val, val)
            if idx == max_val:
                res.append(Perm.to_standard(self[curr_block_start_idx : idx + 1]))
                curr_block_start_idx = idx + 1
        return res

    def skew_decomposition(self) -> List["Perm"]:
        """
        Return the skew decomposition of the permutation.
        """
        res: List[Perm] = []
        min_val = len(self) + 1
        curr_block_start_idx = 0
        for idx, val in enumerate(self):
            min_val = min(min_val, val)
            if len(self) - idx - 1 == min_val:
                res.append(Perm.to_standard(self[curr_block_start_idx : idx + 1]))
                curr_block_start_idx = idx + 1
        return res

    def block_decomposition(
        self, return_patterns: bool = False
    ) -> Union[List[List[int]], List["Perm"]]:
        """Returns the list of all blocks(intervals) in the permutation that
        are of length at least 2. The returned list of lists contains the
        indices of blocks of length i in index i.

        When return_patterns is set to True, a list of patterns is returned
        instead of list of list of indices.

        Examples:
            >>> Perm((5, 3, 0, 1, 2, 4, 7, 6)).block_decomposition()
            [[], [], [2, 3, 6], [2], [1], [1], [0], []]
            >>> sorted(Perm((4, 1, 0, 5, 2, 3)).block_decomposition(True))
            [Perm((0, 1)), Perm((1, 0))]
        """
        # TODO: Split in two
        n = len(self)
        blocks: List[List[int]] = [[] for i in range(n)]
        for idx, val in enumerate(self):
            min_val, max_val = val, val
            for length in range(2, n - idx + 1):
                if length == n:
                    continue
                end = idx + length - 1
                min_val, max_val = min(min_val, self[end]), max(max_val, self[end])
                if max_val - min_val == length - 1:
                    blocks[length].append(idx)

        if return_patterns:
            patterns: Set["Perm"] = set()
            for length, block in enumerate(blocks):
                for start in block:
                    patterns.add(Perm.to_standard(self[start : start + length]))
            return list(patterns)
        return blocks

    all_intervals = block_decomposition  # permpy backwards compatibility
    decomposition = block_decomposition

    def monotone_block_decomposition(
        self, with_ones: bool = False
    ) -> List[Tuple[int, int]]:
        """Returns the list of all monotone blocks(intervals) in the
        permutation. Depending on the with_ones parameter it will return the
        length 1 blocks. The blocks are pairs of indices, the start and end
        index.

        Examples:
            >>> Perm((2, 6, 3, 7, 4, 5, 1, 0)).monotone_block_decomposition()
            [(4, 5), (6, 7)]
            >>> Perm((2, 6, 3, 4, 5, 1, 0)).monotone_block_decomposition(True)
            [(0, 0), (1, 1), (2, 4), (5, 6)]
            >>> Perm((0, 1, 2, 3, 4, 5)).monotone_block_decomposition()
            [(0, 5)]
        """
        blocks = []
        diff, start, length = (0,) * 3
        for i in range(1, len(self)):
            if math.fabs(self[i] - self[i - 1]) == 1 and (
                length == 0 or self[i] - self[i - 1] == diff
            ):
                length += 1
                diff = self[i] - self[i - 1]
            else:
                blocks.append((start, start + length))
                start = i
                length = 0
                diff = 0
        if len(self) != 0:
            blocks.append((start, start + length))

        if with_ones:
            return blocks
        return [block for block in blocks if block[1] - block[0] > 0]

    def monotone_block_decomposition_ascending(
        self, with_ones: bool = False
    ) -> List[Tuple[int, int]]:
        # TODO: test, untested
        # TODO: rename to refer to runs, which this function basically
        #       computes, brakes the permutation up into its runs.
        blocks = []
        start = 0
        length = 0
        for i in range(1, len(self)):
            if self[i] + 1 == self[i - 1]:
                length += 1
            else:
                blocks.append((start, start + length))
                start = i
                length = 0
        if len(self) != 0:
            blocks.append((start, start + length))

        if with_ones:
            return blocks
        return [block for block in blocks if block[1] - block[0] > 0]

    def monotone_block_decompositon_descending(
        self, with_ones: bool = False
    ) -> List[Tuple[int, int]]:
        # TODO: test, untested
        return self.complement().monotone_block_decomposition_ascending(with_ones)

    # permpy backwards compatibility
    all_monotone_intervals = monotone_block_decomposition

    def monotone_quotient(self) -> "Perm":
        """Return the permutation pattern consisting of the starting values of
        the monotone blocks in the permutation. Simply contracts the monotone
        blocks.

        Examples:
            >>> Perm((0, 2, 1, 5, 6, 4, 3)).monotone_block_decomposition(True)
            [(0, 0), (1, 2), (3, 4), (5, 6)]
            >>> Perm((0, 2, 1, 5, 6, 4, 3)).monotone_quotient()
            Perm((0, 1, 3, 2))
        """
        return Perm.to_standard(
            (
                self[start]
                for start, _ in self.monotone_block_decomposition(with_ones=True)
            )
        )

    def maximum_block(self) -> Tuple[int, int]:
        """Finds the biggest interval, and returns (i,j) is one is found,
        where i is the size of the interval, and j is the index of the first
        entry in the interval. Returns (0,0) if no interval is found, i.e.,
        if the permutation is simple.

        Example:
            >>> Perm((0, 2, 1, 5, 6, 7, 4, 3)).maximum_block()
            (7, 1)
        """
        blocks = self.block_decomposition()
        for length, indexlist in reversed(list(enumerate(blocks))):
            if len(indexlist) != 0:
                return (length, indexlist[0])
        return (0, 0)

    maximal_interval = maximum_block  # permpy backwards compatibility

    def simple_location(self) -> Tuple[int, int]:
        """Searches for an interval, and returns (i,j) if one is found, where i
        is the size of the interval, and j is the first index of the interval.

        Returns (0,0) if no interval is found, i.e., if the permutation is
        simple.

        Simply calls the Perm.maximum_block(), the maximum block is any block.
        """
        return self.maximum_block()

    def is_simple(self) -> bool:
        """Checks if the permutation is simple.

        Example:
            >>> Perm((2, 0, 3, 1)).is_simple()
            True
            >>> Perm((2, 0, 1)).is_simple()
            False
        """
        i, _ = self.simple_location()
        return i == 0

    def is_strongly_simple(self) -> bool:
        """Checks if the permutation is strongly simple, that is if the
        permutation is simple and any of permutation of one less length in the
        downset is simple.

        Example:
            >>> Perm((4, 1, 6, 3, 0, 7, 2, 5)).is_strongly_simple()
            True
        """
        return self.is_simple() and all([patt.is_simple() for patt in self.children()])

    def children(self) -> List["Perm"]:
        """Returns all patterns of length one less than the permutation. One
        layer of the downset, also called the shadow.

        Example:
            >>> sorted(Perm((2, 0, 1)).children())
            [Perm((0, 1)), Perm((1, 0))]
            >>> sorted(Perm((4, 1, 6, 3, 0, 7, 2, 5)).children())[:2]
            [Perm((1, 5, 3, 0, 6, 2, 4)), Perm((3, 0, 5, 2, 6, 1, 4))]
        """
        return list(set(self.remove(i) for i in range(len(self))))

    shrink_by_one = children

    # TODO: discuss return value conventions, should this return PermSet
    # instead of set of Perm? maybe list of Perm?
    def coveredby(self) -> List["Perm"]:
        """Returns one layer of the upset of the permutation.

        Examples:
            >>> sorted(Perm((0, 1)).coveredby())[:3]
            [Perm((0, 1, 2)), Perm((0, 2, 1)), Perm((1, 0, 2))]
        """
        n = len(self)
        return list({self.insert(i, j) for i in range(n + 1) for j in range(n + 1)})

    def count_rtlmax_ltrmin_layers(self) -> int:
        """Counts the layers in the right-to-left maxima, left-to-right minima
        decomposition.
        """
        return len(self.rtlmax_ltrmin_decomposition())

    num_rtlmax_ltrmin_layers = count_rtlmax_ltrmin_layers

    def rtlmax_ltrmin_decomposition(self) -> List[List[int]]:
        """Returns the right-to-left maxima, left-to-right minima
        decomposition. The decomposition consists of layers, starting with the
        first layer which is union of the right-to-left maximas and the
        left-to-right minimas and the next layer is defined similarly for the
        permutation with the first layer removed and so on.

        TODO: If this function is to be kept, then it probably should return
        the layers as indices in the original permutation.
        """
        perm = Perm(self)
        num_layers = 0
        layers = []
        while len(perm) > 0:
            num_layers += 1
            positions = sorted(list(set(perm.rtlmax() + perm.ltrmin())))
            layers.append(positions)
            perm = Perm([perm[i] for i in range(len(perm)) if i not in positions])
        return layers

    #
    # Pattern matching methods
    #

    def contains(self, *patts: "Patt") -> bool:
        """Check if self contains patts.

        Examples:
            >>> Perm.monotone_decreasing(7).avoids(Perm((0, 1)))
            True
            >>> Perm((4, 2, 3, 1, 0)).contains(Perm((1, 2, 0)))
            True
            >>> Perm((0, 1, 2)).contains(Perm((1,0)))
            False
            >>> pattern1 = Perm((0, 1))
            >>> pattern2 = Perm((2, 0, 1))
            >>> pattern3 = Perm((0, 3, 1, 2))
            >>> Perm((5, 3, 0, 4, 2, 1)).contains(pattern1, pattern2)
            True
            >>> Perm((5, 3, 0, 4, 2, 1)).contains(pattern2, pattern3)
            False
        """
        return all(patt in self for patt in patts)

    def avoids(self, *patts: "Patt") -> bool:
        """Check if self avoids patts.

        Examples:
            >>> Perm.monotone_increasing(8).avoids(Perm((1, 0)))
            True
            >>> Perm((4, 2, 3, 1, 0)).avoids(Perm((1, 2, 0)))
            False
            >>> Perm((0, 1, 2)).avoids(Perm((1,0)))
            True
            >>> pattern1 = Perm((0, 1))
            >>> pattern2 = Perm((2, 0, 1))
            >>> pattern3 = Perm((0, 3, 1, 2))
            >>> pattern4 = Perm((0, 1, 2))
            >>> Perm((5, 3, 0, 4, 2, 1)).avoids(pattern1, pattern2)
            False
            >>> Perm((5, 3, 0, 4, 2, 1)).avoids(pattern2, pattern3)
            False
            >>> Perm((5, 3, 0, 4, 2, 1)).avoids(pattern3, pattern4)
            True
        """
        return all(patt not in self for patt in patts)

    def avoids_set(self, patts: Iterable["Patt"]) -> bool:
        """Check if self avoids patts.

        This method is for backwards compatibility with permpy.
        """
        return self.avoids(*tuple(patts))

    def count_occurrences_of(self, patt: "Patt") -> int:
        """Count the number of occurrences of patt in self.

        Examples:
            >>> Perm((0, 1, 2)).count_occurrences_of(Perm((0, 1)))
            3
            >>> Perm((5, 3, 0, 4, 2, 1)).count_occurrences_of(Perm((2, 0, 1)))
            6
        """
        return patt.count_occurrences_in(self)

    occurrences = count_occurrences_of  # permpy backwards compatibility

    def occurrences_in(
        self,
        patt: "Patt",
        self_colours: List[int] = None,
        patt_colours: List[int] = None,
    ) -> Union[Iterator[List[Tuple[int, ...]]], Iterator[Tuple[()]]]:
        """Find all indices of occurrences of self in patt. If the optional colours
        are provided, in an occurrences the colours of the patterns have to match the
        colours of the permutation.

        Examples:
            >>> list(Perm((2, 0, 1)).occurrences_in(Perm((5, 3, 0, 4, 2, 1))))
            [(0, 1, 3), (0, 2, 3), (0, 2, 4), (0, 2, 5), (1, 2, 4), (1, 2, 5)]
            >>> list(Perm((1, 0)).occurrences_in(Perm((1, 2, 3, 0))))
            [(0, 3), (1, 3), (2, 3)]
            >>> list(Perm((0,)).occurrences_in(Perm((1, 2, 3, 0))))
            [(0,), (1,), (2,), (3,)]
            >>> list(Perm().occurrences_in(Perm((1, 2, 3, 0))))
            [()]
        """
        if not isinstance(patt, Perm):
            patt = patt.pattern

        # Special cases
        if len(self) == 0:
            # Pattern is empty, occurs in all perms
            # This is needed for the occurrences function to work correctly
            yield ()
            return
        if len(self) > len(patt):
            # Pattern is too long to occur in perm
            return

        # The indices of the occurrence in perm
        occurrence_indices = [None] * len(self)

        # Get left to right scan details
        pattern_details = self.__pattern_details()

        # Define function that works with the above defined variables
        # i is the index of the element in perm that is to be considered
        # k is how many elements of the perm have already been added to
        # occurrence
        def occurrences(i, k):
            elements_remaining = len(patt) - i
            elements_needed = len(self) - k

            # Get the following variables:
            #   - lfi: Left Floor Index
            #   - lci: Left Ceiling Index
            #   - lbp: Lower Bound Pre-computation
            #   - ubp: Upper Bound Pre-computation
            lfi, lci, lbp, ubp = pattern_details[k]

            # Set the bounds for the new element
            if lfi is None:
                # The new element of the occurrence must be at least self[k];
                # i.e., the k-th element of the pattern
                # In this case, lbp = self[k]
                lower_bound = lbp
            else:
                # The new element of the occurrence must be at least as far
                # from its left floor as self[k] is from its left floor
                # In this case, lbp = self[k] - self[lfi]
                occurrence_left_floor = patt[occurrence_indices[lfi]]
                lower_bound = occurrence_left_floor + lbp
            if lci is None:
                # The new element of the occurrence must be at least as less
                # than its maximum possible element---i.e., len(perm)---as
                # self[k] is to its maximum possible element---i.e., len(self)
                # In this case, ubp = len(self) - self[k]
                upper_bound = len(patt) - ubp
            else:
                # The new element of the occurrence must be at least as less
                # than its left ceiling as self[k] is to its left ceiling
                # In this case, ubp = self[lci] - self[k]
                upper_bound = patt[occurrence_indices[lci]] - ubp

            # Loop over remaining elements of perm (actually i, the index)
            while True:
                if elements_remaining < elements_needed:
                    # Can't form an occurrence with remaining elements
                    return
                element = patt[i]
                compare_colours = (
                    self_colours is None or patt_colours[i] == self_colours[k]
                )
                if compare_colours and lower_bound <= element <= upper_bound:
                    occurrence_indices[k] = i
                    if elements_needed == 1:
                        # Yield occurrence
                        yield tuple(occurrence_indices)
                    else:
                        # Yield occurrences where the i-th element is chosen
                        for occurrence in occurrences(i + 1, k + 1):
                            yield occurrence
                # Increment i, that also means elements_remaining should
                # decrement
                i += 1
                elements_remaining -= 1

        for occurrence in occurrences(0, 0):
            yield occurrence

    def occurrences_of(
        self, patt: "Patt"
    ) -> Union[Iterator[List[Tuple[int, ...]]], Iterator[Tuple[()]]]:
        """Find all indices of occurrences of patt in self. This method is complementary
        to permuta.Perm.occurrences_in. It just calls patt.occurrences_in(self)
        internally. See permuta.Perm.occurrences_in for documentation.

        Examples:
            >>> list(Perm((5, 3, 0, 4, 2, 1)).occurrences_of(Perm((2, 0, 1))))
            [(0, 1, 3), (0, 2, 3), (0, 2, 4), (0, 2, 5), (1, 2, 4), (1, 2, 5)]
            >>> list(Perm((1, 2, 3, 0)).occurrences_of(Perm((1, 0))))
            [(0, 3), (1, 3), (2, 3)]
            >>> list(Perm((1, 2, 3, 0)).occurrences_of(Perm((0,))))
            [(0,), (1,), (2,), (3,)]
            >>> list(Perm((1, 2, 3, 0)).occurrences_of(Perm()))
            [()]
        """
        return patt.occurrences_in(self)

    def __pattern_details(self) -> List[Tuple[Optional[int], Optional[int], int, int]]:
        """Subroutine of occurrences_in method."""
        # If details have been calculated before, return cached result
        if self._cached_pattern_details is not None:
            return self._cached_pattern_details
        result = []
        index = 0
        for fac_indices in left_floor_and_ceiling(self):
            base_element = self[index]
            compiled = (
                fac_indices.floor,
                fac_indices.ceiling,
                self[index]
                if fac_indices.floor is None
                else base_element - self[fac_indices.floor],
                len(self) - self[index]
                if fac_indices.ceiling is None
                else self[fac_indices.ceiling] - base_element,
            )
            result.append(compiled)
            index += 1
        self._cached_pattern_details = result
        return result

    #
    # General methods
    #

    def apply(self, iterable: Iterable[int]) -> Tuple[int, ...]:
        """Permute an iterable using the perm.

        Examples:
            >>> Perm((4, 1, 2, 0, 3)).apply((1, 2, 3, 4, 5))
            (5, 2, 3, 1, 4)
            >>> Perm((4, 1, 2, 0, 3)).apply("abcde")
            ('e', 'b', 'c', 'a', 'd')
            >>> Perm((1, 2, 0, 3)).apply("abcde")
            Traceback (most recent call last):
                ...
            ValueError: Length mismatch
        """
        iterable = tuple(iterable)
        if len(iterable) != len(self):
            raise ValueError("Length mismatch")
        return tuple(iterable[index] for index in self)

    permute = apply  # Alias of Perm.apply

    #
    # Visualization methods
    #
    def ascii_plot(self, cell_size: int = 1) -> str:
        """Return an ascii plot of the given Permutation.

        Examples:
            >>> print(Perm((0,1,2)).ascii_plot())
             | | |
            -+-+-●-
             | | |
            -+-●-+-
             | | |
            -●-+-+-
             | | |
        """
        if cell_size > 0:
            empty_char = "+"
        elif cell_size == 0:
            empty_char = "  "
        else:
            raise ValueError("`cell_size` must be positive")
        point_char = "\u25cf"
        n = self.__len__()
        array = [[empty_char for i in range(n)] for j in range(n)]
        for i in range(n):
            array[self[i]][i] = point_char
        array.reverse()
        lines = [("-" * cell_size).join([""] + line + [""]) + "\n" for line in array]
        vline = (" " * cell_size + "|") * n + "\n"
        s = (vline * cell_size).join([""] + lines + [""])
        return str(s[:-1])

    def cycle_notation(self) -> str:
        """Returns the cycle notation representation of the permutation.

        Examples:
            >>> Perm((5, 3, 0, 1, 2, 4)).cycle_notation()
            '( 3 1 ) ( 5 4 2 0 )'
            """
        if len(self) == 0:
            return "( )"
        base = 0
        stringlist = [
            "( " + " ".join([str(x + base) for x in cyc]) + " )"
            for cyc in self.cycle_decomp()
        ]
        return " ".join(stringlist)

    cycles = cycle_notation  # permpy backwards compatibility

    def to_tikz(self) -> str:
        """
        Return the tikz code to plot the permutation.
        """
        s = r"\begin{tikzpicture}"
        s += r"[scale=.3,baseline=(current bounding box.center)]"
        s += "\n\t"
        s += r"\foreach \x in {1,...," + str(len(self)) + "} {"
        s += "\n\t\t"
        s += r"\draw[ultra thin] (\x,0)--(\x," + str(len(self) + 1) + "); %vline"
        s += "\n\t\t"
        s += r"\draw[ultra thin] (0,\x)--(" + str(len(self) + 1) + r",\x); %hline"
        s += "\n\t"
        s += r"}"
        for (idx, val) in enumerate(self):
            s += "\n\t"
            s += (
                r"\draw[fill=black] ("
                + str(idx + 1)
                + ","
                + str(val + 1)
                + ") circle (5pt);"
            )
        s += "\n"
        s += r"\end{tikzpicture}"
        return s

    #
    # Magic/dunder methods
    #

    def __call__(self, value: int) -> int:
        """Map value to its image defined by the perm.

        Examples:
            >>> Perm((3, 1, 2, 0))(0)
            3
            >>> Perm((3, 1, 2, 0))(1)
            1
            >>> Perm((3, 1, 2, 0))(2)
            2
            >>> Perm((3, 1, 2, 0))(3)
            0
        """
        assert 0 <= value < len(self)
        return self[value]

    def __add__(self, other) -> "Perm":
        """Return the direct sum of the perms self and other."""
        if not isinstance(other, Perm):
            raise NotImplementedError
        return self.direct_sum(other)

    def __sub__(self, other) -> "Perm":
        """Return the skew sum of the perms self and other."""
        return self.skew_sum(other)

    def __mul__(self, other) -> "Perm":
        """Return the composition of two perms."""
        return self.compose(other)

    def __repr__(self) -> "str":
        return f"Perm({super(Perm, self).__repr__()})"

    def __str__(self) -> "str":
        if not self:
            return "\u03B5"
        if len(self) <= 10:
            return "".join(str(i) for i in self)
        return "".join(f"({i})" for i in self)

    def __lt__(self, other: tuple) -> bool:
        return (len(self), tuple(self)) < (len(other), tuple(other))

    def __le__(self, other: tuple) -> bool:
        return (len(self), tuple(self)) <= (len(other), tuple(other))

    def __gt__(self, other: tuple) -> bool:
        return other.__lt__(self)

    def __ge__(self, other: tuple) -> bool:
        return other.__le__(self)

    def __contains__(self, patt) -> bool:
        return any(True for _ in patt.occurrences_in(self))

    def __getitem__(self, key):
        return tuple.__getitem__(self, key)

    def __len__(self):
        return tuple.__len__(self)
