# pylint: disable=super-init-not-called
# pylint: disable=too-many-lines
# pylint: disable=too-many-public-methods

import bisect
import collections
import itertools
import math
import numbers
import operator
import random
from typing import (
    TYPE_CHECKING,
    Callable,
    ClassVar,
    Deque,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from permuta.misc import HTMLViewer
from permuta.misc.math import is_prime

from .patt import Patt

__all__ = ("Perm",)

# Remove when pypy is 3.7 compatible andn replace TupleType with Tuple[int]
if TYPE_CHECKING:
    TupleType = Tuple[int]
else:
    TupleType = tuple
ApplyType = TypeVar("ApplyType")


class Perm(TupleType, Patt):
    """A perm class."""

    _TO_STANDARD_CACHE: ClassVar[Dict[Tuple, "Perm"]] = {}

    def __new__(cls, iterable: Iterable[int] = ()) -> "Perm":
        """Return a Perm instance.

        Examples:
            >>> Perm((0, 3, 1, 2))
            Perm((0, 3, 1, 2))
            >>> Perm(range(5, -1, -1))
            Perm((5, 4, 3, 2, 1, 0))
        """
        return tuple.__new__(cls, iterable)

    def __init__(self, _iterable: Iterable[int] = ()) -> None:
        # Cache for data used when finding occurrences of self in a perm
        self._cached_pattern_details: Optional[List[Tuple[int, int, int, int]]] = None

    @classmethod
    def clear_cache(cls):
        """Clears to_standardize cache."""
        cls._TO_STANDARD_CACHE = {}

    @classmethod
    def to_standard(cls, iterable: Iterable) -> "Perm":
        """Return the perm corresponding to iterable. Duplicate elements
        are allowed and become consecutive elements (see example).

        Examples:
            >>> Perm.to_standard("a2gsv3")
            Perm((2, 0, 3, 4, 5, 1))
            >>> Perm.to_standard("caaba")
            Perm((4, 0, 1, 3, 2))
        """
        iterable = tuple(iterable)
        if iterable not in cls._TO_STANDARD_CACHE:
            cls._TO_STANDARD_CACHE[iterable] = cls(
                idx
                for (idx, _) in sorted(enumerate(iterable), key=operator.itemgetter(1))
            ).inverse()
        return cls._TO_STANDARD_CACHE[iterable]

    standardize = to_standard
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
        assert 0 <= integer <= 9876543210
        if integer == 0:
            return Perm((0,))
        digit_list: List[int] = []
        while integer != 0:
            digit_list.append(integer % 10)
            integer //= 10
        return cls.to_standard(reversed(digit_list))

    @classmethod
    def from_string(cls, string: str) -> "Perm":
        """Return the perm corresponding to the string given.

        Examples:
            >>> Perm.from_string("203451")
            Perm((2, 0, 3, 4, 5, 1))
            >>> Perm.from_string("40132")
            Perm((4, 0, 1, 3, 2))
        """
        if string == "ε":
            return cls(())
        return cls(map(int, string))

    @classmethod
    def one_based(cls, iterable: Iterable[int]) -> "Perm":
        """A way to enter a perm in the traditional permuta way.

        Examples:
            >>> Perm.one_based((4, 1, 3, 2))
            Perm((3, 0, 2, 1))
        """
        return cls(val - 1 for val in iterable)

    one = one_based
    proper = one_based
    scientific = one_based

    @classmethod
    def from_iterable_validated(cls, iterable: Union[str, Iterable[int]]) -> "Perm":
        """Creates a permutation from either a string or an iterable of integers and
        validates that it is a bijection on {0,1,...,n-1}.

        Examples:
            >>> Perm.from_iterable_validated((0, 4, 1, 3, 2))
            Perm((0, 4, 1, 3, 2))
            >>> Perm.from_iterable_validated("04132")
            Perm((0, 4, 1, 3, 2))
            >>> Perm.from_iterable_validated((2, 3, 1))
            Traceback (most recent call last):
            ...
            ValueError: Element out of range: 3
            >>> Perm.from_iterable_validated((2, 1, 1))
            Traceback (most recent call last):
            ...
            ValueError: Duplicate element: 1
            >>> Perm.from_iterable_validated((2, None, 1))
            Traceback (most recent call last):
            ...
            TypeError: 'None' object is not an integer

        Raises:
            TypeError: If the perm has non integer values.
            ValueError: If not a bijection.
        """
        if isinstance(iterable, str):
            iterable = map(int, iterable)
        perm = cls(iterable)
        used = [False] * len(perm)
        for val in perm:
            if not isinstance(val, numbers.Integral):
                raise TypeError(f"'{repr(val)}' object is not an integer")
            if not 0 <= val < len(perm):
                raise ValueError(f"Element out of range: {val}")
            if used[val]:
                raise ValueError(f"Duplicate element: {val}")
            used[val] = True
        return perm

    @classmethod
    def random(cls, length: int) -> "Perm":
        """Return a random perm of the specified length.

        Examples:
            >>> perm = Perm.random(8)
            >>> len(perm) == 8
            True
        """
        result = list(range(length))
        random.shuffle(result)
        return cls(result)

    @classmethod
    def of_length(cls, length: int) -> Iterator["Perm"]:
        """Generate all permutations of a given length in lexicographical order.

        Examples:
            >>> list(Perm.of_length(2))
            [Perm((0, 1)), Perm((1, 0))]
        """
        yield from (cls(perm) for perm in itertools.permutations(range(length)))

    @classmethod
    def up_to_length(cls, length: int) -> Iterator["Perm"]:
        """Generate all permutations up to a and including a given
        length in lexicographical order.

        Examples:
            >>> list(Perm.up_to_length(2))
            [Perm(()), Perm((0,)), Perm((0, 1)), Perm((1, 0))]
        """
        for n in range(length + 1):
            yield from (cls(perm) for perm in itertools.permutations(range(n)))

    @classmethod
    def first(cls, count: int) -> Iterator["Perm"]:
        """Generate all permutations in lexicographical order up to a count.

        Examples:
            >>> list(Perm.first(5))
            [Perm(()), Perm((0,)), Perm((0, 1)), Perm((1, 0)), Perm((0, 1, 2))]
        """
        yield from itertools.islice(cls._all(), count)

    @classmethod
    def _all(cls) -> Iterator["Perm"]:
        length = 0
        while True:
            yield from cls.of_length(length)
            length += 1

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

    monotone_increasing = identity

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
        if number == 0:
            return cls.identity(0 if length is None else length)
        factorial = [1, 1]
        if length is None:
            while number > factorial[-1]:
                number -= factorial[-1]
                factorial.append(factorial[-1] * len(factorial))
            return cls(cls._unrank(number - 1, len(factorial) - 1, factorial))
        for i in range(len(factorial), length):
            factorial.append(i * factorial[-1])
        return cls(cls._unrank(number, length, factorial))

    @staticmethod
    def _unrank(number: int, length: int, factorial: List[int]) -> Iterator[int]:
        assert length >= 0
        assert 0 <= number < factorial[length - 1] * length
        candidates = list(range(length))
        for val in range(1, length + 1):
            division, number = divmod(number, factorial[length - val])
            yield candidates.pop(division)

    ind2perm = unrank

    def get_perm(self) -> "Perm":
        """Returns the permutation part of the pattern.

        Examples:
            >>> Perm((3,2,1,0)).get_perm()
            Perm((3, 2, 1, 0))
        """
        return self

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

        Examples:
            >>> Perm((0, 1)).insert()
            Perm((0, 1, 2))
            >>> Perm((0, 1)).insert(0)
            Perm((2, 0, 1))
            >>> Perm((2, 0, 1)).insert(2, 1)
            Perm((3, 0, 1, 2))
        """
        n = len(self)
        if index is None:
            index = n + 1
        if new_element is None:
            new_element = n
        assert 0 <= index <= n + 1
        assert 0 <= new_element <= n
        slice_1 = (
            val if val < new_element else val + 1
            for val in itertools.islice(self, index)
        )
        slice_2 = (
            val if val < new_element else val + 1
            for val in itertools.islice(self, index, n)
        )
        return Perm(itertools.chain(slice_1, (new_element,), slice_2))

    def remove(self, index: Optional[int] = None) -> "Perm":
        """Return the perm acquired by removing an element at a specified index. It
        defaults to the greatest element.

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

        Examples:
            >>> Perm((3, 0, 1, 2)).remove_element()
            Perm((0, 1, 2))
            >>> Perm((3, 0, 2, 1)).remove_element(0)
            Perm((2, 1, 0))
        """
        if selected is None:
            if len(self) == 0:
                return self
            selected = len(self) - 1
        assert 0 <= selected < len(self)
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
        return Perm(reversed(self))

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

    flip_horizontal = complement
    flip_vertical = reverse
    flip_diagonal = inverse

    def flip_antidiagonal(self) -> "Perm":
        """Return self flipped along the antidiagonal.

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
        for idx, val in ((n - val - 1, n - idx - 1) for idx, val in enumerate(self)):
            result[idx] = val
        return Perm(result)

    def rotate(self, times: int = 1) -> "Perm":
        """Rotate the permutation. The parameter determines how often it is rotated.
        A negative value rotates it to the left.

        Examples:
            >>> Perm((0, 4, 1, 3, 2)).rotate(-3)
            Perm((4, 2, 0, 1, 3))
            >>> Perm((0, 4, 1, 3, 2)).rotate(-2)
            Perm((2, 1, 3, 0, 4))
            >>> Perm((0, 4, 1, 3, 2)).rotate(-1)
            Perm((1, 3, 4, 2, 0))
            >>> Perm((0, 4, 1, 3, 2)).rotate(0)
            Perm((0, 4, 1, 3, 2))
            >>> Perm((0, 4, 1, 3, 2)).rotate(1)
            Perm((4, 2, 0, 1, 3))
            >>> Perm((0, 4, 1, 3, 2)).rotate()
            Perm((4, 2, 0, 1, 3))
            >>> Perm((0, 4, 1, 3, 2)).rotate(2)
            Perm((2, 1, 3, 0, 4))
            >>> Perm((0, 4, 1, 3, 2)).rotate(3)
            Perm((1, 3, 4, 2, 0))
        """
        times = times % 4
        if times == 0:
            return self
        if times == 2:
            return self.reverse_complement()
        n = len(self)
        result = [0] * n
        if times == 1:
            for idx, val in enumerate(self):
                result[val] = n - idx - 1
        else:
            for idx, val in enumerate(self):
                result[n - val - 1] = idx
        return Perm(result)

    def all_syms(self) -> Tuple["Perm", ...]:
        """Returns all symmetries of the permutation in a PermSet, all possible
        combinations of reverse, complement and inverse.

        Examples:
            >>> sorted(Perm((0, 2, 1)).all_syms())
            [Perm((0, 2, 1)), Perm((1, 0, 2)), Perm((1, 2, 0)), Perm((2, 0, 1))]
        """
        syms = {self, self.inverse()}
        curr: "Perm" = self
        for _ in range(3):
            curr = curr.rotate()
            syms.update((curr, curr.inverse()))
        return tuple(syms)

    def is_increasing(self) -> bool:
        """Return True if the perm is increasing, and False otherwise.

        Examples:
            >>> Perm((0, 2, 1, 3)).is_increasing()
            False
            >>> Perm((0, 1)).is_increasing()
            True
        """
        return all(idx == val for idx, val in enumerate(self))

    def is_decreasing(self) -> bool:
        """Return True if the perm is decreasing, and False otherwise.

        Examples:
            >>> Perm((3, 2, 0, 1)).is_decreasing()
            False
            >>> Perm((3, 2, 1, 0)).is_decreasing()
            True
        """
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
        return (idx for idx in self.ltrmax() if idx == self[idx])

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

    skew_decomposable = is_skew_decomposable

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

    sum_decomposable = is_sum_decomposable

    def descents(self, step_size: Optional[int] = None) -> Iterator[int]:
        """Yield the 0-based descents of self. If step size is specified it only yields
        descents of that size, otherwise it yields all descents.

        Examples:
            >>> tuple(Perm((0, 1, 3, 2, 4)).descents())
            (2,)
            >>> tuple(Perm((0, 1, 3, 2, 4)).descents(step_size=2))
            ()
            >>> tuple(Perm((3, 1, 0, 2)).descents())
            (0, 1)
            >>> tuple(Perm((3, 1, 0, 2)).descents(step_size=2))
            (0,)
            >>> tuple(Perm((0, 1, 2)).descents())
            ()
        """

        if step_size is None:
            return (
                idx
                for idx, (prev, curr) in enumerate(
                    zip(self, itertools.islice(self, 1, None))
                )
                if prev > curr
            )

        if step_size < 1:
            raise ValueError("Step size has to be 1 or more")

        return (
            idx
            for idx, (prev, curr) in enumerate(
                zip(self, itertools.islice(self, 1, None))
            )
            if prev == curr + step_size
        )

    def descent_set(self, step_size: Optional[int] = None) -> List[int]:
        """Return the list of descents of self. If step size is specified it only
        returns a list of descents of that size,
        otherwise it returns list of all descents.

        Examples:
            >>> Perm((0, 4, 3, 1, 2)).descent_set()
            [1, 2]
            >>> Perm((0, 4, 3, 1, 2)).descent_set(step_size=2)
            [2]
            >>> Perm((3, 2, 1, 0)).descent_set()
            [0, 1, 2]
            >>> Perm((0, 1, 2)).descent_set()
            []
        """
        return list(self.descents(step_size))

    def count_descents(self, step_size: Optional[int] = None) -> int:
        """Count the number of descents of self. If step size is specified
        if only counts descents of that size, otherwise it counts all descents.

        Examples:
            >>> Perm((0, 4, 3, 1, 2)).count_descents()
            2
            >>> Perm((0, 4, 3, 1, 2)).count_descents(step_size=2)
            1
            >>> Perm((3, 2, 1, 0)).count_descents()
            3
            >>> Perm((0, 1, 2)).count_descents()
            0
        """
        return sum(1 for _ in self.descents(step_size))

    num_descents = count_descents

    def ascents(self, step_size: Optional[int] = None) -> Iterator[int]:
        """Yield the 0-based ascent of self. If step size is specified it only yields
        ascents of that size, otherwise it yields all ascents.

        Examples:
            >>> tuple(Perm((0, 1, 3, 2, 4)).ascents())
            (0, 1, 3)
            >>> tuple(Perm((0, 1, 3, 2, 4)).ascents(step_size=2))
            (1, 3)
            >>> tuple(Perm((0, 4, 3, 2, 1)).ascents())
            (0,)
            >>> tuple(Perm((0, 4, 3, 2, 1)).ascents(step_size=1))
            ()
            >>> tuple(Perm((3, 2, 1, 0)).ascents())
            ()
        """

        if step_size is None:
            return (
                idx
                for idx, (prev, curr) in enumerate(
                    zip(self, itertools.islice(self, 1, None))
                )
                if prev < curr
            )

        if step_size < 1:
            raise ValueError("Step size has to be 1 or more")

        return (
            idx
            for idx, (prev, curr) in enumerate(
                zip(self, itertools.islice(self, 1, None))
            )
            if prev + step_size == curr
        )

    def ascent_set(self, step_size: Optional[int] = None) -> List[int]:
        """Return the list of ascents of self. If step size is specified it only
        returns a list of ascents of that size,
        otherwise it returns list of all ascents.

        Examples:
            >>> Perm((0, 1, 3, 2, 4)).ascent_set()
            [0, 1, 3]
            >>> Perm((0, 1, 3, 2, 4)).ascent_set(step_size=2)
            [1, 3]
            >>> Perm((0, 4, 3, 2, 1)).ascent_set()
            [0]
            >>> Perm((3, 2, 1, 0)).ascent_set()
            []
        """
        return list(self.ascents(step_size))

    def count_ascents(self, step_size: Optional[int] = None) -> int:
        """Count the number of ascents in self. If step size is specified
        if only counts ascents of that size, otherwise it counts all ascents.

        Examples:
            >>> Perm((0, 1, 3, 2, 4)).count_ascents()
            3
            >>> Perm((0, 1, 3, 2, 4)).count_ascents(step_size=2)
            2
            >>> Perm((0, 4, 3, 2, 1)).count_ascents()
            1
            >>> Perm((3, 2, 1, 0)).count_ascents()
            0
        """
        return sum(1 for _ in self.ascents(step_size))

    num_ascents = count_ascents

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
        """Return the list of peaks of self.

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).peak_list()
            [2, 4]
            >>> Perm((1, 2, 0)).peak_list()
            [1]
            >>> Perm((2, 1, 0)).peak_list()
            []
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

    num_peaks = count_peaks
    count_pinnacles = count_peaks
    num_pinnacles = count_peaks

    def pinnacles(self) -> Iterator[int]:
        """Yield the pinnacles of self. The value of the i-th element of a perm is
        a pinnacle if self[i-1] < self[i] > self[i+1].
        See: https://arxiv.org/abs/2105.10388
        https://arxiv.org/abs/1704.05494
        https://arxiv.org/abs/2001.07325

        Examples:
            >>> tuple(Perm((5, 3, 4, 0, 2, 1)).pinnacles())
            (4, 2)
            >>> tuple(Perm((1, 2, 0)).pinnacles())
            (2,)
            >>> tuple(Perm((2, 1, 0)).pinnacles())
            ()
        """
        return (
            curr
            for (prev, curr, nxt) in zip(
                itertools.islice(self, 0, None),
                itertools.islice(self, 1, None),
                itertools.islice(self, 2, None),
            )
            if prev < curr > nxt
        )

    def pinnacle_set(self) -> List[int]:
        """Return the pinnacle set of self.
        See: https://arxiv.org/abs/2105.10388
        https://arxiv.org/abs/1704.05494
        https://arxiv.org/abs/2001.07325

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).pinnacle_set()
            [4, 2]
            >>> Perm((1, 2, 0)).pinnacle_set()
            [2]
            >>> Perm((2, 1, 0)).pinnacle_set()
            []
        """
        return list(self.pinnacles())

    def count_column_sum_primes(self) -> int:
        """Returns the number of primes in the column sums of the two line notation
        of a permutation.
        See: https://www.findstat.org/StatisticsDatabase/St001285/
        https://arxiv.org/abs/1809.01012

        Examples:
            >>> Perm((0,)).count_column_sum_primes()
            1
            >>> Perm((0, 1)).count_column_sum_primes()
            1
            >>> Perm((1, 0)).count_column_sum_primes()
            2
        """
        return sum(1 for idx, val in enumerate(self) if is_prime(val + idx + 2))
        # + 2 because both values are 0 indexed

    num_column_sum_primes = count_column_sum_primes

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
        """Return the list of valleys of self.

        Examples:
            >>> Perm((5, 3, 4, 0, 2, 1)).valley_list()
            [1, 3]
            >>> Perm((2, 0, 1)).valley_list()
            [1]
            >>> Perm((1, 2, 0)).valley_list()
            []
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

    num_valleys = count_valleys

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

    def ltrmin(self) -> Iterator[int]:
        """Returns the positions of the left-to-right minima.

        Examples:
            >>> list(Perm((2, 4, 3, 0, 1)).ltrmin())
            [0, 3]
        """
        min_val = len(self)
        for idx, val in enumerate(self):
            if val < min_val:
                min_val = val
                yield idx

    def rtlmin(self) -> Iterator[int]:
        """Returns the positions of the right-to-left minima.

        Examples:
            >>> list(Perm((2, 0, 4, 1, 5, 3)).rtlmin())
            [1, 3, 5]
        """
        yield from reversed(self._rtlmin_reverse_list())

    def _rtlmin_reverse_list(self) -> List[int]:
        lis, (n, min_val) = [], (len(self),) * 2
        for idx, val in enumerate(reversed(self)):
            if val < min_val:
                min_val = val
                lis.append(n - idx - 1)
        return lis

    def ltrmax(self) -> Iterator[int]:
        """Returns the positions of the left-to-right maxima.

        Examples:
            >>> list(Perm((2, 0, 4, 1, 5, 3)).ltrmax())
            [0, 2, 4]
        """
        max_val = -1
        for idx, val in enumerate(self):
            if val > max_val:
                max_val = val
                yield idx

    def rtlmax(self) -> Iterator[int]:
        """Returns the positions of the right-to-left maxima.

        Examples:
            >>> list(Perm((2, 4, 3, 0, 1)).rtlmax())
            [1, 2, 4]
        """
        yield from reversed(self._rtlmax_reverse_list())

    def _rtlmax_reverse_list(self) -> List[int]:
        lis, n, max_val = [], len(self), -1
        for idx, val in enumerate(reversed(self)):
            if val > max_val:
                max_val = val
                lis.append(n - idx - 1)
        return lis

    def count_ltrmin(self) -> int:
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return sum(1 for _ in self.ltrmin())

    def count_ltrmax(self) -> int:
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return sum(1 for _ in self.ltrmax())

    def count_rtlmin(self) -> int:
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self._rtlmin_reverse_list())

    def count_rtlmax(self) -> int:
        """Counts the number of left-to-right minimas.

        Example:
            >>> Perm((2, 4, 3, 0, 1)).count_ltrmin()
            2
        """
        return len(self._rtlmax_reverse_list())

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

    def count_bounces(self) -> int:
        """The Number of "bounces" in a permutation.
        See https://www.findstat.org/StatisticsDatabase/St000133/#

        Examples:
            >>> Perm((0,)).count_bounces()
            0
            >>> Perm((0, 1)).count_bounces()
            1
            >>> Perm((1, 0)).count_bounces()
            0
        """
        n = len(self)
        if n == 0:
            return 0
        inv = self.inverse()
        bounce_arr = [inv[0] + 1]
        while bounce_arr[-1] < n:
            bounce_arr.append(max(inv[: bounce_arr[-1] + 1]) + 1)
        return sum(n - i for i in bounce_arr)

    def max_drop_size(self):
        """The maximum drop size of a permutation.
        See: https://www.findstat.org/StatisticsDatabase/St000141/
        https://arxiv.org/abs/1306.5428
        https://mathscinet.ams.org/mathscinet/search/publdoc.html?pg1=MR&s1=MR2673024

        Examples:
            >>> Perm((0,)).max_drop_size()
            0
            >>> Perm((0, 1)).max_drop_size()
            0
            >>> Perm((1, 0)).max_drop_size()
            1
            >>> Perm((2, 0, 1)).max_drop_size()
            2
        """
        return max((val - idx for idx, val in enumerate(self)), default=0)

    def holeyness(self) -> int:
        """The holeyness of a permutation.
        See: https://www.findstat.org/StatisticsDatabase/St001469/
        https://mathoverflow.net/questions/340179/how-rare-are-unholey-permutations

        Examples:
            >>> Perm((1, 0)).holeyness()
            0
            >>> Perm((0, 1, 2)).holeyness()
            0
            >>> Perm((0, 2, 1)).holeyness()
            1
            >>> Perm((1, 0, 2)).holeyness()
            1
        """

        def _delta(d_set: Set[int]) -> int:
            return sum(1 for x in d_set if x + 1 not in d_set)

        def _set_generator(num: int) -> Iterator[Set[int]]:
            for y in range(0, num + 1):
                for x in itertools.combinations(range(num), y):
                    yield set(x)

        return max(
            _delta({self[s] for s in tmp_set}) - _delta(tmp_set)
            for tmp_set in _set_generator(len(self))
        )

    def count_stack_sorts(self):
        """The number of stack-sorts needed to sort a permutation.
        See: https://www.findstat.org/StatisticsDatabase/St000028/
        https://mathscinet.ams.org/mathscinet/search/publdoc.html?pg1=MR&s1=MR2028290
        https://arxiv.org/abs/1110.1219
        https://mathscinet.ams.org/mathscinet/search/publdoc.html?pg1=MR&s1=MR0445948
        https://mathscinet.ams.org/mathscinet/search/publdoc.html?pg1=MR&s1=MR1168135

        Examples:
        >>> Perm(()).count_stack_sorts()
        0
        >>> Perm((0,)).count_stack_sorts()
        0
        >>> Perm((0, 1)).count_stack_sorts()
        0
        >>> Perm((1, 0)).count_stack_sorts()
        1
        >>> Perm((1, 2, 0)).count_stack_sorts()
        2
        >>> Perm((2, 1, 0)).count_stack_sorts()
        1
        """
        num_sorts = 0
        identity = list(self.identity(len(self)))
        perm_list = list(self)
        while perm_list != identity:
            perm_list = self._stack_sort(perm_list)
            num_sorts += 1
        return num_sorts

    def count_pop_stack_sorts(self):
        """The number of pop-stack-sorts needed to sort a permutation.
        See: https://www.findstat.org/StatisticsDatabase/St001090/
        http://www.arxiv.org/abs/1710.04978
        http://www.arxiv.org/abs/1801.05005
        http://www.arxiv.org/abs/1911.03104

        Examples:
        >>> Perm(()).count_pop_stack_sorts()
        0
        >>> Perm((0,)).count_pop_stack_sorts()
        0
        >>> Perm((0, 1)).count_pop_stack_sorts()
        0
        >>> Perm((1, 0)).count_pop_stack_sorts()
        1
        >>> Perm((4, 0, 2, 1, 3, 5)).count_pop_stack_sorts()
        4
        >>> Perm((4, 3, 2, 1, 0, 5)).count_pop_stack_sorts()
        1
        >>> Perm((5, 1, 4, 3, 0, 2)).count_pop_stack_sorts()
        4
        """
        num_sorts = 0
        perm = self
        while not perm.is_increasing():
            perm = perm.pop_stack_sort()
            num_sorts += 1
        return num_sorts

    def cyclic_peaks(self) -> Iterator[int]:
        """Yields the indexes of cyclic peaks in the permutation.
        Satisfies: i < x > P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> list(Perm((3, 2, 0, 1)).cyclic_peaks())
            [0, 1]
            >>> list(Perm((1, 0, 2)).cyclic_peaks())
            [0]
            >>> list(Perm((0, 1, 2)).cyclic_peaks())
            []
            >>> list(Perm((2, 0, 1)).cyclic_peaks())
            [0]
            >>> list(Perm((1, 3, 0, 2)).cyclic_peaks())
            [1]
            >>> list(Perm((0, 1, 2, 3)).cyclic_peaks())
            []
            >>> list(Perm((0, 2, 1, 3)).cyclic_peaks())
            [1]
        """
        for idx, val in enumerate(self):
            if idx < val > self[val]:
                yield idx

    def cyclic_peaks_list(self) -> List[int]:
        """Returns a list of indexes of the cyclic peaks in the permutation.
        Satisfies: i < x > P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((3, 2, 0, 1)).cyclic_peaks_list()
            [0, 1]
            >>> Perm((1, 0, 2)).cyclic_peaks_list()
            [0]
            >>> Perm((0, 1, 2)).cyclic_peaks_list()
            []
            >>> Perm((2, 0, 1)).cyclic_peaks_list()
            [0]
            >>> Perm((1, 3, 0, 2)).cyclic_peaks_list()
            [1]
            >>> Perm((0, 1, 2, 3)).cyclic_peaks_list()
            []
            >>> Perm((0, 2, 1, 3)).cyclic_peaks_list()
            [1]
        """
        return list(self.cyclic_peaks())

    def count_cyclic_peaks(self) -> int:
        """Returns the number of cyclic peaks in the permutation.
        Satisfies: i < x > P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((3, 2, 0, 1)).count_cyclic_peaks()
            2
            >>> Perm((1, 0, 2)).count_cyclic_peaks()
            1
            >>> Perm((0, 1, 2)).count_cyclic_peaks()
            0
            >>> Perm((2, 0, 1)).count_cyclic_peaks()
            1
            >>> Perm((1, 3, 0, 2)).count_cyclic_peaks()
            1
            >>> Perm((0, 1, 2, 3)).count_cyclic_peaks()
            0
            >>> Perm((0, 2, 1, 3)).count_cyclic_peaks()
            1
        """
        return sum(1 for _ in self.cyclic_peaks())

    def cyclic_valleys(self) -> Iterator[int]:
        """Yields the indexes of cyclic valleys in the permutation.
        Satisfies: i > x < P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> list(Perm((1, 3, 0, 2)).cyclic_valleys())
            [2]
            >>> list(Perm((2, 1, 0)).cyclic_valleys())
            [2]
            >>> list(Perm((1, 2, 3, 0)).cyclic_valleys())
            [3]
            >>> list(Perm((1, 2, 0)).cyclic_valleys())
            [2]
            >>> list(Perm((2, 0, 1)).cyclic_valleys())
            [1]
            >>> list(Perm((0, 1, 2)).cyclic_valleys())
            []
        """
        for idx, val in enumerate(self):
            if idx > val < self[val]:
                yield idx

    def cyclic_valleys_list(self) -> List[int]:
        """Returns a list of index of the cyclic valleys in the permutation.
        Satisfies: i > x < P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((1, 3, 0, 2)).cyclic_valleys_list()
            [2]
            >>> Perm((2, 1, 0)).cyclic_valleys_list()
            [2]
            >>> Perm((1, 2, 3, 0)).cyclic_valleys_list()
            [3]
            >>> Perm((1, 2, 0)).cyclic_valleys_list()
            [2]
            >>> Perm((2, 0, 1)).cyclic_valleys_list()
            [1]
            >>> Perm((0, 1, 2)).cyclic_valleys_list()
            []
        """
        return list(self.cyclic_valleys())

    def count_cyclic_valleys(self) -> int:
        """Returns the number of cyclic valleys in the permutation.
        Satisfies: i > x < P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((1, 3, 0, 2)).count_cyclic_valleys()
            1
            >>> Perm((2, 1, 0)).count_cyclic_valleys()
            1
            >>> Perm((1, 2, 3, 0)).count_cyclic_valleys()
            1
            >>> Perm((1, 2, 0)).count_cyclic_valleys()
            1
            >>> Perm((2, 0, 1)).count_cyclic_valleys()
            1
            >>> Perm((0, 1, 2)).count_cyclic_valleys()
            0
        """
        return sum(1 for _ in self.cyclic_valleys())

    def double_excedance(self) -> Iterator[int]:
        """Yields the indexes of double excedances in the permutation.
        Satisfies: i < x < P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> list(Perm((1, 0, 3, 2)).double_excedance())
            []
            >>> list(Perm((1, 3, 0, 2)).double_excedance())
            [0]
            >>> list(Perm((2, 1, 0)).double_excedance())
            []
            >>> list(Perm((3, 1, 0, 2)).double_excedance())
            []
            >>> list(Perm((1, 2, 3, 0)).double_excedance())
            [0, 1]
            >>> list(Perm((2, 0, 3, 1)).double_excedance())
            [0]
        """
        for idx, val in enumerate(self):
            if idx < val < self[val]:
                yield idx

    def double_excedance_list(self) -> List[int]:
        """Returns a list of indees of the double excedances in the permutation.
        Satisfies: i < x < P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((1, 0, 3, 2)).double_excedance_list()
            []
            >>> Perm((1, 3, 0, 2)).double_excedance_list()
            [0]
            >>> Perm((2, 1, 0)).double_excedance_list()
            []
            >>> Perm((3, 1, 0, 2)).double_excedance_list()
            []
            >>> Perm((1, 2, 3, 0)).double_excedance_list()
            [0, 1]
            >>> Perm((2, 0, 3, 1)).double_excedance_list()
            [0]
        """
        return list(self.double_excedance())

    def count_double_excedance(self) -> int:
        """Returns the number of double excedances in the permutation.
        Satisfies: i < x < P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((1, 0, 3, 2)).count_double_excedance()
            0
            >>> Perm((1, 3, 0, 2)).count_double_excedance()
            1
            >>> Perm((2, 1, 0)).count_double_excedance()
            0
            >>> Perm((3, 1, 0, 2)).count_double_excedance()
            0
            >>> Perm((1, 2, 3, 0)).count_double_excedance()
            2
            >>> Perm((2, 0, 3, 1)).count_double_excedance()
            1
        """
        return sum(1 for _ in self.double_excedance())

    def double_drops(self) -> Iterator[int]:
        """Yields the indexes of double drops in the permutation.
        Satisfies: i > x > P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> list(Perm((2, 0, 1)).double_drops())
            [2]
            >>> list(Perm((1, 0, 2)).double_drops())
            []
            >>> list(Perm((2, 1, 3, 0)).double_drops())
            []
            >>> list(Perm((2, 0, 3, 1)).double_drops())
            [3]
            >>> list(Perm((3, 0, 1, 2)).double_drops())
            [2, 3]
            >>> list(Perm((2, 0, 1, 3)).double_drops())
            [2]
        """
        for idx, val in enumerate(self):
            if idx > val > self[val]:
                yield idx

    def double_drops_list(self) -> List[int]:
        """Returns a list of indexes of the double drops in the permutation.
        Satisfies: i > x > P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((2, 0, 1)).double_drops_list()
            [2]
            >>> Perm((1, 0, 2)).double_drops_list()
            []
            >>> Perm((2, 1, 3, 0)).double_drops_list()
            []
            >>> Perm((2, 0, 3, 1)).double_drops_list()
            [3]
            >>> Perm((3, 0, 1, 2)).double_drops_list()
            [2, 3]
            >>> Perm((2, 0, 1, 3)).double_drops_list()
            [2]
        """
        return list(self.double_drops())

    def count_double_drops(self) -> int:
        """Counts the number of double drops in the permutation.
        Satisfies: i > x > P(x), where x = P(i)
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((2, 0, 1)).count_double_drops()
            1
            >>> Perm((1, 0, 2)).count_double_drops()
            0
            >>> Perm((2, 1, 3, 0)).count_double_drops()
            0
            >>> Perm((2, 0, 3, 1)).count_double_drops()
            1
            >>> Perm((3, 0, 1, 2)).count_double_drops()
            2
            >>> Perm((2, 0, 1, 3)).count_double_drops()
            1
        """
        return sum(1 for _ in self.double_drops())

    def foremaxima(self) -> List[int]:
        """Returns a list of indexes of the foremaxima of the permutation.
        If P(i) is both a double ascent and ltrmax it is a foremaximum.
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((3, 2, 5, 0, 1, 4)).foremaxima()
            []
            >>> Perm((3, 4, 1, 0, 5, 2)).foremaxima()
            []
            >>> Perm((1, 3, 5, 2, 4, 0)).foremaxima()
            [0, 1]
            >>> Perm((2, 3, 5, 4, 1, 6, 0)).foremaxima()
            [1]
            >>> Perm((1, 3, 2, 5, 4, 0, 6)).foremaxima()
            [0]
            >>> Perm((2, 5, 4, 1, 3, 0)).foremaxima()
            []
        """
        double_ascents = set(self.ascent_set(step_size=2))
        ltrmax = set(self.ltrmax())
        return list(double_ascents & ltrmax)

    def count_foremaxima(self):
        """Returns the number of foremaxima in the permutation.
        If P(i) is both a double ascent and ltrmax it is a foremaximum.
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((3, 2, 5, 0, 1, 4)).count_foremaxima()
            0
            >>> Perm((3, 4, 1, 0, 5, 2)).count_foremaxima()
            0
            >>> Perm((1, 3, 5, 2, 4, 0)).count_foremaxima()
            2
            >>> Perm((2, 3, 5, 4, 1, 6, 0)).count_foremaxima()
            1
            >>> Perm((1, 3, 2, 5, 4, 0, 6)).count_foremaxima()
            1
            >>> Perm((2, 5, 4, 1, 3, 0)).count_foremaxima()
            0
        """
        return len(self.foremaxima())

    def afterminima(self) -> List[int]:
        """Returns a list of indexes of the afterminima of the permutation.
        If P(i) is both a double ascent and rtlmin it is a afterminimum.
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((3, 1, 4, 6, 5, 0, 2)).afterminima()
            [5]
            >>> Perm((2, 1, 0)).afterminima()
            []
            >>> Perm((1, 5, 0, 3, 2, 4, 6)).afterminima()
            [4, 5]
            >>> Perm((2, 0, 1, 3)).afterminima()
            [2]
            >>> Perm((0, 2, 1, 3, 4)).afterminima()
            [0, 2]
            >>> Perm((3, 1, 0, 2, 4, 6, 5)).afterminima()
            [2, 3, 4]
            >>> Perm((3, 4, 0, 2, 1)).afterminima()
            [2]
        """
        double_ascents = set(self.ascent_set(step_size=2))
        rtlmin = set(self.rtlmin())
        return list(double_ascents & rtlmin)

    def count_afterminima(self):
        """Returns the number of afterminima in the permutation.
        If P(i) is both a double ascent and rtlmin it is a afterminimum.
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((3, 1, 4, 6, 5, 0, 2)).count_afterminima()
            1
            >>> Perm((2, 1, 0)).count_afterminima()
            0
            >>> Perm((1, 5, 0, 3, 2, 4, 6)).count_afterminima()
            2
            >>> Perm((2, 0, 1, 3)).count_afterminima()
            1
            >>> Perm((0, 2, 1, 3, 4)).count_afterminima()
            2
            >>> Perm((3, 1, 0, 2, 4, 6, 5)).count_afterminima()
            3
            >>> Perm((3, 4, 0, 2, 1)).count_afterminima()
            1
        """
        return len(self.afterminima())

    def aftermaxima(self):
        """Returns a list of indexes of the aftermaxima of the permutation.
        If P(i) is both a double descent and rtlmax it is an aftermaximum.
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((4, 1, 2, 5, 3, 0, 6)).aftermaxima()
            []
            >>> Perm((5, 4, 3, 1, 2, 0)).aftermaxima()
            [2, 4]
            >>> Perm((1, 2, 0)).aftermaxima()
            [1]
            >>> Perm((2, 4, 0, 3, 1)).aftermaxima()
            [3]
            >>> Perm((1, 3, 2, 0)).aftermaxima()
            [2]
            >>> Perm((2, 0, 1)).aftermaxima()
            [0]
            >>> Perm((1, 4, 2, 0, 3)).aftermaxima()
            [1]
        """
        double_descents = set(self.descents(step_size=2))
        rtlmax = set(self.rtlmax())
        return list(double_descents & rtlmax)

    def count_aftermaxima(self):
        """Returns the number of aftermaxima in the permutation.
        If P(i) is both a double descent and rtlmax it is an afermaximum.
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((4, 1, 2, 5, 3, 0, 6)).count_aftermaxima()
            0
            >>> Perm((5, 4, 3, 1, 2, 0)).count_aftermaxima()
            2
            >>> Perm((1, 2, 0)).count_aftermaxima()
            1
            >>> Perm((2, 4, 0, 3, 1)).count_aftermaxima()
            1
            >>> Perm((1, 3, 2, 0)).count_aftermaxima()
            1
            >>> Perm((2, 0, 1)).count_aftermaxima()
            1
            >>> Perm((1, 4, 2, 0, 3)).count_aftermaxima()
            1
        """
        return len(self.aftermaxima())

    def foreminima(self):
        """Returns a list of indexes of the foreminima of the permutation.
        If P(i) is both a double descent and ltrmin it is a foreminimum.
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((5, 6, 0, 1, 3, 4, 2)).foreminima()
            []
            >>> Perm((3, 1, 4, 0, 2)).foreminima()
            [0]
            >>> Perm((3, 1, 2, 5, 4, 0)).foreminima()
            [0]
            >>> Perm((3, 1, 4, 2, 0)).foreminima()
            [0]
            >>> Perm((3, 1, 0, 5, 4, 2)).foreminima()
            [0]
            >>> Perm((2, 0, 1)).foreminima()
            [0]
            >>> Perm((6, 4, 2, 3, 5, 1, 0)).foreminima()
            [0, 1]
        """
        double_descents = set(self.descents(step_size=2))
        ltrmin = set(self.ltrmin())
        return list(double_descents & ltrmin)

    def count_foreminima(self):
        """Returns the number of foreminima in the permutation.
        If P(i) is both a double descent and ltrmin it is a foreminimum.
        See: https://arxiv.org/abs/1908.01084

        Examples:
            >>> Perm((5, 6, 0, 1, 3, 4, 2)).count_foreminima()
            0
            >>> Perm((3, 1, 4, 0, 2)).count_foreminima()
            1
            >>> Perm((3, 1, 2, 5, 4, 0)).count_foreminima()
            1
            >>> Perm((3, 1, 4, 2, 0)).count_foreminima()
            1
            >>> Perm((3, 1, 0, 5, 4, 2)).count_foreminima()
            1
            >>> Perm((2, 0, 1)).count_foreminima()
            1
            >>> Perm((6, 4, 2, 3, 5, 1, 0)).count_foreminima()
            2
        """
        return len(self.foreminima())

    def inversions(self) -> Iterator[Tuple[int, int]]:
        """Yield the inversions of the permutation, i.e., the pairs i,j
        such that i < j and self(i) > self(j).

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

    def all_bonds(self) -> Iterator[int]:
        """Generate all bonds, that is the adjacent locations with adjacent values.

        Examples:
            >>> list(Perm((0, 1, 2)).all_bonds())
            [0, 1]
            >>> list(Perm((2, 1, 0)).all_bonds())
            [0, 1]
            >>> list(Perm((4, 0, 3, 2, 1, 5)).all_bonds())
            [2, 3]
        """
        return (
            idx
            for idx, (prev, curr) in enumerate(
                zip(self, itertools.islice(self, 1, None))
            )
            if curr == prev + 1 or prev == curr + 1
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
        return sum(1 for _ in self.all_bonds())

    num_bonds = count_bonds
    bonds = count_bonds

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
        return sum(1 for _ in self.inc_bonds())

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
        return sum(1 for _ in self.dec_bonds())

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

    def depth(self) -> int:
        """Return the depth of the permutation. See https://arxiv.org/pdf/1202.4765.pdf.

        Examples:
            >>> Perm((3, 1, 2, 4, 0)).depth()
            4
            >>> Perm((0, 2, 1)).depth()
            1
        """
        return sum(val - idx for idx, val in enumerate(self) if val > idx)

    def maximal_decreasing_run(self) -> int:
        """Returns the longest decreasing run of consecutive elements starting
        from the leargest.

        Examples:
            >>> Perm((3, 1, 2, 4, 0)).maximal_decreasing_run()
            1
            >>> Perm((0, 2, 1)).maximal_decreasing_run()
            2
            >>> Perm((5, 0, 4, 1, 2, 3)).maximal_decreasing_run()
            3
        """
        n = len(self)
        next_val, max_not_included = n - 1, -1
        for val in self:
            if val == next_val:
                next_val -= 1
            elif val > max_not_included:
                max_not_included = val
            if next_val < max_not_included:
                break
        return n - next_val - 1

    def longestruns_ascending(self) -> Tuple[int, List[int]]:
        """Returns the longest ascending runs in the permutation as a pair of
        the length and a list of the starting indices.

        Examples:
            >>> Perm((0, 2, 1, 4, 3, 5)).longestruns_ascending()
            (2, [0, 2, 4])
            >>> Perm((4, 3, 0, 1, 2)).longestruns_ascending()
            (3, [2])
            >>> Perm((2, 1, 0)).longestruns_ascending()
            (1, [0, 1, 2])
        """
        n = len(self)
        if n == 0:
            return (0, [])
        maxi, cur = 1, 0
        res: List[int] = []
        for idx, (prev, curr) in enumerate(zip(self, itertools.islice(self, 1, None))):
            if prev < curr:
                if idx - cur + 2 > maxi:
                    res.clear()
                    maxi = idx - cur + 2
            else:
                if idx - cur + 1 == maxi:
                    res.append(cur)
                cur = idx + 1
        if n - cur == maxi:
            res.append(cur)
        return (maxi, res)

    def longestruns_descending(self) -> Tuple[int, List[int]]:
        """Returns the longest descending runs in the permutation as a pair of
        the length and a list of the starting indices.

        Examples:
            >>> Perm((0, 1, 2, 3)).longestruns_descending()
            (1, [0, 1, 2, 3])
            >>> Perm((1, 2, 0)).longestruns_descending()
            (2, [1])
            >>> Perm((2, 1, 3, 0)).longestruns_descending()
            (2, [0, 2])
        """
        return self.complement().longestruns_ascending()

    def length_of_longestrun_ascending(self) -> int:
        """Returns the length of the longest ascending run in the permutation.

        Examples:
            >>> Perm((0, 1, 2, 3)).length_of_longestrun_ascending()
            4
            >>> Perm((1, 2, 0)).length_of_longestrun_ascending()
            2
        """
        return self.longestruns_ascending()[0]

    def length_of_longestrun_descending(self) -> int:
        """Returns the length of the longest descending run in the permutation.

        Examples:
            >>> Perm((0, 1, 2, 3)).length_of_longestrun_descending()
            1
            >>> Perm((1, 2, 0)).length_of_longestrun_descending()
            2
        """
        return self.complement().length_of_longestrun_ascending()

    def cycle_decomp(self) -> Deque[List[int]]:
        """Calculates the cycle decomposition of the permutation. Returns a list
        of cycles, each of which is represented as a list.

        Examples:
            >>> Perm((4, 2, 7, 0, 3, 1, 6, 5)).cycle_decomp()
            deque([[4, 3, 0], [6], [7, 5, 1, 2]])
        """
        n = len(self)
        remaining_elements = set(range(n))
        cyclelist: Deque[List[int]] = collections.deque()
        while remaining_elements:
            max_not_seen = max(remaining_elements)
            cycle, val = [max_not_seen], self[max_not_seen]
            remaining_elements.remove(val)
            while val != max_not_seen:
                cycle.append(val)
                val = self(val)
                remaining_elements.remove(val)
            cyclelist.appendleft(cycle)
        return cyclelist

    def count_cycles(self) -> int:
        """Returns the number of cycles in the permutation.

        >>> Perm((5, 3, 8, 1, 0, 4, 2, 7, 6)).count_cycles()
        4
        """
        return len(self.cycle_decomp())

    num_cycles = count_cycles

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

    is_identity = is_increasing

    def rank(self) -> int:
        """Computes the rank of a permutation.
        Examples:
            >>> Perm((0, 1)).rank()
            2
            >>> Perm((0, 2, 1, 3)).rank()
            12
        """
        n, res = len(self), 0
        fact = [1]
        for i in range(n):
            fact.append(fact[i] * (i + 1))
        vals: List[int] = list()
        for idx, val in enumerate(self):
            ordered_pos = bisect.bisect_left(vals, val)
            res += (val - ordered_pos) * fact[n - idx - 1] + fact[n - idx - 1]
            vals.insert(ordered_pos, val)
        return res

    perm2ind = rank

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

    def rank_encoding(self) -> List[int]:
        """Returns the rank_encoding of each index in the permutation, the
        number of inversions 'caused' by the values at each index.

        Examples:
            >>> Perm((3, 0, 2, 1)).rank_encoding()
            [3, 0, 1, 0]
            >>> Perm((0, 2, 4, 3, 1)).rank_encoding()
            [0, 1, 2, 1, 0]
        """
        rank_encoding = [0] * len(self)
        for left, _ in self.inversions():
            rank_encoding[left] += 1
        return rank_encoding

    def sum_decomposition(self) -> List["Perm"]:
        """Return the sum decomposition of the permutation.

        Examples:
            >>> Perm((0, 1, 2)).sum_decomposition()
            [Perm((0,)), Perm((0,)), Perm((0,))]
            >>> Perm((1, 2, 0, 4, 3)).sum_decomposition()
            [Perm((1, 2, 0)), Perm((1, 0))]
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
        """Return the skew decomposition of the permutation.

        Examples:
            >>> Perm((5, 3, 4, 1, 0, 2)).skew_decomposition()
            [Perm((0,)), Perm((0, 1)), Perm((1, 0, 2))]
            >>> Perm((5, 1, 2, 0, 3, 4)).skew_decomposition()
            [Perm((0,)), Perm((1, 2, 0, 3, 4))]
        """
        n = len(self)
        res: List[Perm] = []
        min_val = n + 1
        curr_block_start_idx = 0
        for idx, val in enumerate(self):
            min_val = min(min_val, val)
            if n - idx - 1 == min_val:
                res.append(Perm.to_standard(self[curr_block_start_idx : idx + 1]))
                curr_block_start_idx = idx + 1
        return res

    def block_decomposition_as_pattern(self) -> List["Perm"]:
        """Return block decomposition as a list of perm.

        Examples:
            >>> sorted(Perm((4, 1, 0, 5, 2, 3)).block_decomposition_as_pattern())
            [Perm((0, 1)), Perm((1, 0))]
        """
        patterns: Set["Perm"] = set()
        for length, block in enumerate(self.block_decomposition()):
            for start in block:
                patterns.add(Perm.to_standard(self[start : start + length]))
        return list(patterns)

    def block_decomposition(self) -> List[List[int]]:
        """Returns the list of all blocks (intervals) in the permutation that
        are of length at least 2. The returned list of lists contains the
        indices of blocks of length i in index i.

        Examples:
            >>> Perm((5, 3, 0, 1, 2, 4, 7, 6)).block_decomposition()
            [[], [], [2, 3, 6], [2], [1], [1], [0], []]
        """
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
        return blocks

    all_intervals = block_decomposition
    decomposition = block_decomposition

    def monotone_block_decomposition(
        self, with_ones: bool = False
    ) -> Iterator[Tuple[int, int]]:
        """Returns the iterator of all monotone blocks(intervals) in the
        permutation. Depending on the with_ones parameter it will return the
        length 1 blocks. The blocks are pairs of indices, the start and end
        index.

        Examples:
            >>> list(Perm((2, 6, 3, 7, 4, 5, 1, 0)).monotone_block_decomposition())
            [(4, 5), (6, 7)]
            >>> list(Perm((2, 6, 3, 4, 5, 1, 0)).monotone_block_decomposition(True))
            [(0, 0), (1, 1), (2, 4), (5, 6)]
            >>> list(Perm((0, 1, 2, 3, 4, 5)).monotone_block_decomposition())
            [(0, 5)]
        """
        yield from self._block_decomposition_generator(
            lambda curr, prev: abs(curr - prev) == 1, with_ones
        )

    def monotone_block_decomposition_ascending(
        self, with_ones: bool = False
    ) -> Iterable[Tuple[int, int]]:
        """Returns the iterator of all ascending blocks(intervals) in the
        permutation. Depending on the with_ones parameter it will return the
        length 1 blocks. The blocks are pairs of indices, the start and end
        index.

        Examples:
            >>> list(Perm((1, 0, 2, 3)).monotone_block_decomposition_ascending(True))
            [(0, 0), (1, 1), (2, 3)]
            >>> list(Perm((0, 2, 1)).monotone_block_decomposition_ascending(False))
            []
        """
        yield from self._block_decomposition_generator(
            lambda prev, curr: curr - prev == 1, with_ones
        )

    def monotone_block_decomposition_descending(
        self, with_ones: bool = False
    ) -> Iterator[Tuple[int, int]]:
        """Returns the iterator of all descending blocks(intervals) in the
        permutation. Depending on the with_ones parameter it will return the
        length 1 blocks. The blocks are pairs of indices, the start and end
        index.

        Examples:
            >>> list(Perm((2,1,0,5,4,3)).monotone_block_decomposition_descending(True))
            [(0, 2), (3, 5)]
            >>> list(Perm((0, 2, 1)).monotone_block_decomposition_descending(False))
            [(1, 2)]
        """
        yield from self._block_decomposition_generator(
            lambda prev, curr: prev - curr == 1, with_ones
        )

    all_monotone_intervals = monotone_block_decomposition

    def _block_decomposition_generator(
        self, comparator: Callable[[int, int], bool], with_ones: bool = False
    ) -> Iterator[Tuple[int, int]]:
        diff, start, length = (0,) * 3
        for idx, (prev, curr) in enumerate(zip(self, itertools.islice(self, 1, None))):
            if comparator(prev, curr) and (length == 0 or curr - prev == diff):
                length += 1
                diff = curr - prev
            else:
                if length > 0 or with_ones:
                    yield start, start + length
                diff, start, length = 0, idx + 1, 0
        if len(self) != 0 and (length > 0 or with_ones):
            yield start, start + length

    def contract_inc_bonds(self) -> "Perm":
        """Turn entries, consecutive in position and increasing in value, then
        standardize the resulting permutation.

        Examples:
            >>> Perm((1, 0, 5, 3, 4, 2)).contract_inc_bonds()
            Perm((1, 0, 4, 3, 2))
        """
        monblocks = self.monotone_block_decomposition_ascending(with_ones=True)
        return Perm.to_standard(self[start] for start, _ in monblocks)

    def contract_dec_bonds(self) -> "Perm":
        """Turn entries, consecutive in position and decreasing in value, then
        standardize the resulting permutation.

        Examples:
            >>> Perm((1, 0, 5, 3, 4, 2)).contract_dec_bonds()
            Perm((0, 4, 2, 3, 1))
        """
        monblocks = self.monotone_block_decomposition_descending(with_ones=True)
        return Perm.to_standard(self[start] for start, _ in monblocks)

    def contract_bonds(self) -> "Perm":
        """Turn entries, consecutive in position and decreasing or increasing in value,
        into a single element, then standardize the resulting permutation.

        Examples:
            >>> Perm((1, 0, 5, 3, 4, 2)).contract_bonds()
            Perm((0, 3, 2, 1))
        """
        monblocks = self.monotone_block_decomposition(with_ones=True)
        return Perm.to_standard(self[start] for start, _ in monblocks)

    def monotone_quotient(self) -> "Perm":
        """Return the permutation pattern consisting of the starting values of
        the monotone blocks in the permutation. Simply contracts the monotone
        blocks.

        Examples:
            >>> list(Perm((0, 2, 1, 5, 6, 4, 3)).monotone_block_decomposition(True))
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
        """Finds the biggest interval, and returns (i,j) if one is found,
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

    maximal_interval = maximum_block
    simple_location = maximum_block

    def is_simple(self) -> bool:
        """Checks if the permutation is simple.

        Example:
            >>> Perm((2, 0, 3, 1)).is_simple()
            True
            >>> Perm((2, 0, 1)).is_simple()
            False
        """
        return self.simple_location()[0] == 0

    def is_strongly_simple(self) -> bool:
        """Checks if the permutation is strongly simple, that is if the
        permutation is simple and any of permutation of one less length in the
        downset is simple.

        Example:
            >>> Perm((4, 1, 6, 3, 0, 7, 2, 5)).is_strongly_simple()
            True
        """
        return self.is_simple() and all(patt.is_simple() for patt in self.children())

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

    def coveredby(self) -> List["Perm"]:
        """Returns one layer of the upset of the permutation.

        Examples:
            >>> sorted(Perm((0, 1)).coveredby())[:3]
            [Perm((0, 1, 2)), Perm((0, 2, 1)), Perm((1, 0, 2))]
        """
        n = len(self)
        return list(set(self.insert(i, j) for i in range(n + 1) for j in range(n + 1)))

    def count_rtlmax_ltrmin_layers(self) -> int:
        """Counts the layers in the right-to-left maxima, left-to-right minima
        decomposition.

        Examples:
            >>> Perm((2, 7, 3, 1, 4, 8, 6, 0, 5)).count_rtlmax_ltrmin_layers()
            3
            >>> Perm((5, 4, 3, 0, 2, 1)).count_rtlmax_ltrmin_layers()
            1
        """
        return sum(1 for _ in self.rtlmax_ltrmin_decomposition())

    num_rtlmax_ltrmin_layers = count_rtlmax_ltrmin_layers

    def rtlmax_ltrmin_decomposition(self) -> Iterator[List[int]]:
        """Returns the right-to-left maxima, left-to-right minima
        decomposition. The decomposition consists of layers, starting with the
        first layer which is union of the right-to-left maximas and the
        left-to-right minimas and the next layer is defined similarly for the
        permutation with the first layer removed and so on.

        Examples:
            >>> list(Perm((2, 7, 3, 1, 4, 8, 6, 0, 5)).rtlmax_ltrmin_decomposition())
            [[0, 3, 5, 6, 7, 8], [0, 2], [0]]
            >>> list(Perm((5, 4, 3, 0, 2, 1)).rtlmax_ltrmin_decomposition())
            [[0, 1, 2, 3, 4, 5]]
        """
        perm = self
        while len(perm) > 0:
            pos_set = set(itertools.chain(perm.rtlmax(), perm.ltrmin()))
            yield sorted(pos_set)
            perm = Perm(perm[i] for i in range(len(perm)) if i not in pos_set)

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
        """Check if self avoids patts for an iterable of patterns.

        Examples:
            >>> (Perm([4, 0, 1, 2, 3]).avoids_set([Perm([2, 1, 0]), Perm([1, 0])]))
            False
            >>> Perm([4, 0, 1, 2, 3]).avoids_set([Perm([2, 1, 0]), Perm([1, 2, 0])])
            True
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

    occurrences = count_occurrences_of

    def occurrences_in(
        self, patt: "Patt", *args, **kwargs
    ) -> Iterator[Tuple[int, ...]]:
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
        self_colours, patt_colours = (None, None) if len(args) < 2 else args
        n, patt = len(self), patt.get_perm()

        if n == 0:
            yield ()
            return
        if n > len(patt):
            return

        # The indices of the occurrence in perm
        occurrence_indices = [0] * n
        pattern_details = self._pattern_details()

        # Define function that works with the above defined variables
        # i is the index of the element in perm that is to be considered
        # k is how many elements of the perm have already been added to
        # occurrence
        def occurrences(i, k):
            elements_remaining = len(patt) - i
            elements_needed = n - k

            # lfi = left floor index
            # lci = left ceiling index
            # lbp = lower bound pre-computation
            # ubp = upper bound pre-computation
            lfi, lci, lbp, ubp = pattern_details[k]

            # Set the bounds for the new element
            if lfi == -1:
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
            if lci == -1:
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
                        yield tuple(occurrence_indices)
                    else:
                        yield from occurrences(i + 1, k + 1)
                i, elements_remaining = i + 1, elements_remaining - 1

        yield from occurrences(0, 0)

    def occurrences_of(self, patt: "Patt") -> Union[Iterator[Tuple[int, ...]]]:
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

    def left_floor_and_ceiling(self) -> Iterator[Tuple[int, int]]:
        """For each element, return the pair of indices of (largest less, smalllest
        greater) to the left, if they exist. If not, -1 is used instead.

        Examples:
            >>> list(Perm((2, 5, 0, 3, 6, 4, 7, 1)).left_floor_and_ceiling())
            [(-1, -1), (0, -1), (-1, 0), (0, 1), (1, -1), (3, 1), (4, -1), (2, 0)]
        """
        deq: Deque[Tuple[int, int]] = collections.deque()
        smallest, biggest = -1, -1
        for idx, val in enumerate(self):
            if idx == 0:
                deq.append((val, idx))
                smallest, biggest = val, val
                yield (-1, -1)
            elif val < smallest:
                # Rotate until smallest val is at front
                while deq[0][0] != smallest:
                    deq.rotate(-1)
                yield (-1, deq[0][1])
                deq.appendleft((val, idx))
                smallest = val
            elif val > biggest:
                # Rotate until biggest val is at end
                while deq[-1][0] != biggest:
                    deq.rotate(-1)
                yield (deq[-1][1], -1)
                deq.append((val, idx))
                biggest = val
            else:
                while not deq[-1][0] <= val <= deq[0][0]:
                    deq.rotate(1)
                yield (deq[-1][1], deq[0][1])
                deq.appendleft((val, idx))

    def _pattern_details(self) -> List[Tuple[int, int, int, int]]:
        if self._cached_pattern_details is None:
            self._cached_pattern_details = [
                (
                    floor,
                    ceiling,
                    val if floor == -1 else val - self[floor],
                    len(self) - val if ceiling == -1 else self[ceiling] - val,
                )
                for val, (floor, ceiling) in zip(self, self.left_floor_and_ceiling())
            ]
        return self._cached_pattern_details

    def apply(self, iterable: Iterable[ApplyType]) -> Tuple[ApplyType, ...]:
        """Permute an iterable using the perm.

        Examples:
            >>> Perm((4, 1, 2, 0, 3)).apply((1, 2, 3, 4, 5))
            (5, 2, 3, 1, 4)
            >>> Perm((4, 1, 2, 0, 3)).apply("abcde")
            ('e', 'b', 'c', 'a', 'd')
        """
        iterable = tuple(iterable)
        assert len(iterable) == len(self)
        return tuple(iterable[index] for index in self)

    permute = apply

    @staticmethod
    def _is_sorted(lis: List[int]) -> bool:
        return all(val == idx for idx, val in enumerate(lis))

    @staticmethod
    def _stack_sort(perm_slice: List[int]) -> List[int]:
        """Helper function for the stack sorting function on perms"""
        n = len(perm_slice)
        if n in (0, 1):
            return perm_slice
        max_i, max_v = max(enumerate(perm_slice), key=lambda pos_elem: pos_elem[1])
        # Recursively solve without largest
        if max_i == 0:
            n_lis = Perm._stack_sort(perm_slice[1:n])
        elif max_i == n - 1:
            n_lis = Perm._stack_sort(perm_slice[0 : n - 1])
        else:
            n_lis = Perm._stack_sort(perm_slice[0:max_i])
            n_lis.extend(Perm._stack_sort(perm_slice[max_i + 1 : n]))
        n_lis.append(max_v)
        return n_lis

    def stack_sort(self) -> "Perm":
        """Stack sorting the permutation"""
        return Perm(Perm._stack_sort(list(self)))

    def stack_sortable(self) -> bool:
        """Returns true if perm is stack sortable."""
        return self.stack_sort().is_increasing()

    def pop_stack_sort(self) -> "Perm":
        """Pop-stack sorting the permutation"""
        stack: Deque[int] = collections.deque()
        result: List[int] = []
        for num in self:
            if stack and num > stack[0]:
                result.extend(stack)
                stack.clear()
            stack.appendleft(num)

        result.extend(stack)
        return Perm(result)

    def pop_stack_sortable(self) -> bool:
        """Returns true if perm is pop-stack sortable."""
        return self.pop_stack_sort().is_increasing()

    @staticmethod
    def _bubble_sort(perm_slice: List[int]) -> List[int]:
        """Helper function for the bubble sorting function on perms"""
        n = len(perm_slice)
        if n in (0, 1):
            return perm_slice
        max_i, max_v = max(enumerate(perm_slice), key=lambda pos_elem: pos_elem[1])
        # Recursively solve without largest
        if max_i == 0:
            n_lis = perm_slice[1:n]
        elif max_i == n - 1:
            n_lis = Perm._bubble_sort(perm_slice[0 : n - 1])
        else:
            n_lis = Perm._bubble_sort(perm_slice[0:max_i])
            n_lis.extend(perm_slice[max_i + 1 : n])
        n_lis.append(max_v)
        return n_lis

    def bubble_sort(self) -> "Perm":
        """Bubble sorting the permutation"""
        return Perm(Perm._bubble_sort(list(self)))

    def bubble_sortable(self) -> bool:
        """Returns true if perm is stack sortable."""
        return self.bubble_sort().is_increasing()

    @staticmethod
    def _quick_sort(perm_slice: List[int]) -> List[int]:
        """Helper function for the quick sorting function on perms"""
        assert not perm_slice or set(perm_slice) == set(
            range(min(perm_slice), max(perm_slice) + 1)
        )
        n = len(perm_slice)
        if n == 0:
            return perm_slice
        maxind = -1
        # Note that perm does not need standardizing as sfp uses left to right maxima.
        for maxind in Perm(perm_slice).strong_fixed_points():
            pass
        if maxind != -1:
            lis: List[int] = (
                Perm._quick_sort(perm_slice[:maxind])
                + [perm_slice[maxind]]
                + Perm._quick_sort(perm_slice[maxind + 1 :])
            )
        else:
            firstval = perm_slice[0]
            lis = (
                list(filter(lambda x: x < firstval, perm_slice))
                + [perm_slice[0]]
                + list(filter(lambda x: x > firstval, perm_slice))
            )
        return lis

    def quick_sort(self) -> "Perm":
        """Quick sorting the permutation"""
        return Perm(Perm._quick_sort(list(self)))

    def quick_sortable(self) -> bool:
        """Returns true if perm is quicksort sortable."""
        return self.quick_sort().is_increasing()

    def bkv_sortable(self, patterns: Tuple[Patt, ...] = ()) -> bool:
        """Check if a permutation is BKV sortable.
        See:
            https://arxiv.org/pdf/1907.08142.pdf
            https://arxiv.org/pdf/2004.01812.pdf
        """
        # See
        n = len(self)
        inp = collections.deque(self)
        # the right stack read from top to bottom
        # the left stack read from top to bottom
        right_stack: Deque[int] = collections.deque([])
        left_stack: Deque[int] = collections.deque([])
        expected = 0
        print(self)
        while expected < n:
            print("inp", inp)
            print("left_stack", left_stack)
            print("right_stack", right_stack)
            print("------------------------------")
            if inp:
                right_stack.appendleft(inp[0])
                if Perm.to_standard(right_stack).avoids(*patterns):
                    inp.popleft()
                    continue
                right_stack.popleft()

            if right_stack:
                left_stack.appendleft(right_stack[0])
                if Perm.to_standard(left_stack).is_increasing():
                    right_stack.popleft()
                    continue
                left_stack.popleft()

            assert left_stack
            # Normally, we would gather elements from left stack but since we only care
            # about wether it sorts the permutation, we just compare it against
            # expected.
            if expected != left_stack.popleft():
                return False
            expected += 1
        return True

    def west_2_stack_sortable(self) -> bool:
        """Returns true if perm can be sorted by two passes through a stack"""
        return self.stack_sort().stack_sort().is_increasing()

    def west_3_stack_sortable(self) -> bool:
        """Returns true if perm can be sorted by three passes through a stack"""
        return self.stack_sort().stack_sort().stack_sort().is_increasing()

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
        assert cell_size >= 0
        empty_char, point_char, n = "+" if cell_size > 0 else "  ", "\u25cf", len(self)
        array = [[empty_char for i in range(n)] for j in range(n)]
        for i in range(n):
            array[self[i]][i] = point_char
        array.reverse()
        lines = [("-" * cell_size).join([""] + line + [""]) + "\n" for line in array]
        vline = (" " * cell_size + "|") * n + "\n"
        return str((vline * cell_size).join([""] + lines + [""])[:-1])

    def cycle_notation(self) -> str:
        """Returns the cycle notation representation of the permutation.

        Examples:
            >>> Perm((5, 3, 0, 1, 2, 4)).cycle_notation()
            '( 3 1 ) ( 5 4 2 0 )'
        """
        if len(self) == 0:
            return "( )"
        return " ".join(
            f'( {" ".join(str(x) for x in cyc)} )' for cyc in self.cycle_decomp()
        )

    cycles = cycle_notation

    def to_svg(self, image_scale: float = 1.0) -> str:
        """Return the svg code to plot the permutation. The image size defaults to
        100x100 pixels and the parameter scales that.
        """
        n = len(self)
        p_scale = 100 / (n + 1)
        i_scale = int(image_scale * 100)
        return "".join(
            [
                '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" '
                f'width="{i_scale}" height="{i_scale}" viewBox="0 0 100 100">\n',
                "\n".join(
                    (
                        f'<line x1="{i*p_scale:.3}" y1="0" x2="{i*p_scale:.3}" '
                        f'y2="100" style="stroke:rgb(0,0,0);stroke-width:{10/(n+1):.3}"'
                        f' />\n<line x1="0" y1="{i*p_scale}" x2="100" y2="'
                        f'{i*p_scale:.3}" style="stroke:rgb(0,0,0);stroke-width:'
                        f'{10/(n+1):.3}" />'
                    )
                    for i in range(1, n + 1)
                ),
                "\n",
                "\n".join(
                    (
                        f'<circle cx="{(idx+1)*p_scale:.3}" cy="'
                        f'{100-(val+1)*p_scale:.3}" r="{p_scale/4:.3}" stroke="black"'
                        f' stroke-width="{10/(n+1):.3}" fill="rgb(0,0,0)" />'
                    )
                    for (idx, val) in enumerate(self)
                ),
                "\n</svg>",
            ]
        )

    def to_tikz(self) -> str:
        """
        Return the tikz code to plot the permutation.
        """
        n, tab = len(self), "    "
        return "".join(
            [
                "\\begin{tikzpicture}[scale=.3,baseline=(current bounding box.center)]",
                f"\n{tab}\\foreach \\x in {{1,...,{n}}} {{\n{tab*2}",
                f"\\draw[ultra thin] (\\x,0)--(\\x,{n+1}); %vline\n{tab*2}",
                f"\\draw[ultra thin] (0,\\x)--({n+1},\\x); %hline\n{tab}}}\n{tab}",
                f"\n{tab}".join(
                    f"\\draw[fill=black] ({idx + 1},{val + 1}) circle (5pt);"
                    for (idx, val) in enumerate(self)
                ),
                "\n\\end{tikzpicture}",
            ]
        )

    def containment_to_tikz(self, pattern: "Perm") -> Iterator[str]:
        """Return the tikz picture of the pattern within self."""
        return (self._pattern_to_tikz(occ) for occ in self.occurrences_of(pattern))

    def _pattern_to_tikz(self, occurrence: Tuple[int, ...]) -> str:
        init = self.to_tikz()
        init = init[0 : init.rfind("\\end{tikzpicture}")]
        reds = "\n".join(
            f"    \\draw[red] ({idx + 1},{self[idx] + 1}) circle (10pt);"
            for idx in occurrence
        )
        return f"{init}{reds}\n\\end{{tikzpicture}}"

    def show(self, scale: float = 1.0) -> None:
        """Open a browser tab and display permutation graphically. Image can be
        enlarged with scale parameter"""
        HTMLViewer.open_svg(self.to_svg(image_scale=scale))

    def __call__(self, value: int) -> int:
        assert 0 <= value < len(self)
        return self[value]

    def __add__(self, other: object) -> "Perm":
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.direct_sum(other)

    def __sub__(self, other: object) -> "Perm":
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.skew_sum(other)

    def __mul__(self, other: object) -> "Perm":
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.compose(other)

    def __repr__(self) -> "str":
        return f"Perm({super().__repr__()})"

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

    def __len__(self) -> int:
        return tuple.__len__(self)

    def __contains__(self, patt: object) -> bool:
        if isinstance(patt, Patt):
            return any(True for _ in patt.occurrences_in(self))
        return False
