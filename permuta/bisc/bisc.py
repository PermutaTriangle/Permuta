import bisect
import functools
import json
import os
import types
from array import array
from collections.abc import Collection, Mapping, Sequence
from math import factorial
from typing import (
    Callable,
    Dict,
    Final,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

from permuta.bisc.bisc_subfunctions import (
    forb,
    mine,
    patterns_suffice_for_bad,
    patterns_suffice_for_good,
    run_clean_up,
    show_me,
    show_me_basis,
    to_sg_format,
)
from permuta.patterns.perm import Perm

# The forbidden patterns bisc and auto_bisc return: length -> {pattern:
# [shadings]}, each shading a set of boxes, and an empty one making the pattern
# classical
_Patterns = Dict[int, Dict[Perm, List[Set[Tuple[int, int]]]]]


def bisc(
    A: Union[
        List[Perm],
        Callable[[Perm], bool],
        Mapping[int, Collection[Perm]],
        "PropertyBitmaps",
    ],
    m: int,
    n: Optional[int] = None,
    report: bool = False,
) -> _Patterns:
    """
    Mine the forbidden patterns of length up to m from the permutations up to
    length n of a set A: a list of permutations, a property (a function), a
    dictionary or another Mapping (length -> the permutations of that length
    in the set), or a PropertyBitmaps. Each is turned into a PropertyBitmaps,
    whose good permutations of each length up to max(m, n) mine() reads.
    Without n, a property uses length 7, and the others their longest length.
    - A list's permutations are the good ones, and a length with none listed
      is empty.
    - A property labels the lengths up to n, and a length past n, when m > n,
      is read as empty.
    - A Mapping is read for each length up to max(m, n), and one it lacks is
      its KeyError.
    - A PropertyBitmaps labels the lengths up to max(m, n) it lacks with its
      property, and they are added to it; without a property, a ValueError
      names the first.
    report prints the progress of the search.

    Returns the forbidden patterns found: a dictionary from length to
    {pattern: [shadings]}, where each shading is a set of boxes, and an empty
    one makes the pattern classical.
    """
    if isinstance(A, list):
        if n is None:
            n = max(len(perm) for perm in A)
        perms_by_length: Dict[int, List[Perm]] = {
            length: [] for length in range(max(m, n) + 1)
        }
        for perm in A:
            if len(perm) in perms_by_length:
                perms_by_length[len(perm)].append(perm)
        property_bitmaps = _from_perms_by_length(perms_by_length)

    elif isinstance(A, types.FunctionType):
        if n is None:
            print("I will use permutations up to length 7")
            n = 7
        property_bitmaps = PropertyBitmaps(A)
        for length in range(n + 1):
            property_bitmaps.add_length(length)
        # mine() reads the lengths up to m too, and a length past n is read as
        # empty: none of its permutations is good
        for length in range(n + 1, m + 1):
            property_bitmaps._keep(length, _new_indices(length), 0)

    elif isinstance(A, Mapping):
        if n is None:
            n = max(A.keys())
        property_bitmaps = _from_perms_by_length(
            {length: A[length] for length in range(max(m, n) + 1)}
        )

    elif isinstance(A, PropertyBitmaps):
        property_bitmaps = A
        if n is None:
            if A.bitmaps:
                n = max(A.bitmaps)
            elif A.prop is not None:
                print("I will use permutations up to length 7")
                n = 7
            else:
                raise ValueError("The PropertyBitmaps has no bitmaps and no property")
        for length in range(max(m, n) + 1):
            if length not in A.bitmaps:
                if A.prop is None:
                    raise ValueError(
                        "bisc needs bitmaps up to length {}, and the PropertyBitmaps "
                        "has none of length {} and no property".format(
                            max(m, n), length
                        )
                    )
                A.add_length(length)

    else:
        print(
            """BiSC can accept inputs:
        1. A list of permutations
        2. A property of permutations
        3. A dictionary of lengths pointing to permutations
        4. A PropertyBitmaps"""
        )
        assert False

    ci, goodpatts = mine(property_bitmaps.good, m, n, report=report)
    SG: _Patterns = forb(ci, goodpatts, m, report=report)

    return SG


def auto_bisc(
    prop: Union[
        Callable[[Perm], bool],
        List[Perm],
        Tuple[Dict[int, List[Perm]], Dict[int, List[Perm]]],
        str,
        "PropertyBitmaps",
    ],
) -> Optional[_Patterns]:
    """
    Learn a basis of forbidden patterns for a set of permutations, growing
    the length of the patterns and of the permutations they are learned from
    until the patterns found describe the set on every permutation up to
    length L, at least 8. Returns the basis, in the form bisc returns its
    patterns, or None when the input is too short to check a basis.

    prop is the set: a property of permutations (a function), a list of
    permutations, a tuple of two dictionaries (length -> the permutations in
    the set, and those not in it), the name of a set in
    permuta/resources/bisc, or a PropertyBitmaps. Each is turned into a
    PropertyBitmaps at the start, whose views give the good and the bad
    permutations of each length.
    - A property labels the lengths up to 8 at the start, and each longer one
      when auto_bisc first needs it.
    - A list's permutations are the good ones, and the others are bad.
    - For a tuple of dictionaries, or a stored set, the good and the bad
      permutations of each length up to the shorter dictionary's longest must
      not overlap, and must together be all of that length's permutations, or
      a ValueError is raised. A length one of them lacks is empty in it, and a
      permutation given twice on one side counts once.
    - A PropertyBitmaps labels the lengths it lacks with its property, and
      they are added to it, so that a later run reuses them. Without a
      property, auto_bisc stops when it needs a length it lacks, as it does
      for a tuple of dictionaries.
    """
    L = 8  # Want to sanity check on at least S8, and one above n
    n = 4
    m = 2

    if isinstance(prop, list):
        # If a list is passed in then its permutations are the good ones, and
        # the others up to its longest length are the bad ones
        listed_lengths = {len(perm) for perm in prop}
        if L not in listed_lengths:
            print("You should have permutations up to length at least 8")
            return None
        longest_length = max(listed_lengths)
        # Printed as when the bad permutations were made into lists, so that
        # what auto_bisc prints does not change; now they are read from the
        # labels of the good ones
        for i in range(L, longest_length + 1):
            print("Populating the dictionary of bad perms of length ", i)
        perms_by_length: Dict[int, List[Perm]] = {
            length: [] for length in range(longest_length + 1)
        }
        for perm in prop:
            perms_by_length[len(perm)].append(perm)
        property_bitmaps = _from_perms_by_length(perms_by_length)

    elif isinstance(prop, types.FunctionType):
        # If a property is passed in then it labels the lengths up to S8 now,
        # and the longer ones as they are needed
        property_bitmaps = PropertyBitmaps(prop)
        for i in range(L + 1):
            property_bitmaps.add_length(i)

    elif isinstance(prop, PropertyBitmaps):
        # The lengths the PropertyBitmaps lacks are labeled with its
        # property, if it has one
        property_bitmaps = prop
        for i in range(L + 1):
            if i not in property_bitmaps.bitmaps:
                if property_bitmaps.prop is None:
                    print("You should have bitmaps up to length at least 8")
                    return None
                property_bitmaps.add_length(i)

    elif (
        isinstance(prop, tuple)
        and isinstance(prop[0], dict)
        and isinstance(prop[1], dict)
    ):
        # If you already have the dictionaries you can pass them in as a tuple
        if L not in prop[0].keys():
            print("You should have permutations up to length at least 8")
            return None
        property_bitmaps = _from_good_and_bad(prop[0], prop[1])
        if L - 1 not in property_bitmaps.bitmaps:
            # The bad permutations stop short of the lengths up to L - 1, which
            # auto_bisc learns from before its sanity checks reach L
            print("You need to add longer permutations to the dictionaries")
            return None

    elif isinstance(prop, str):
        # If you pass in a string we assume it is pointing to a file in permsets
        print("Attempting to read perms from permsets")
        stored_set = _read_stored_set(prop, L)
        if stored_set is None:
            print("The required files do not exist")
            return None
        property_bitmaps = _from_good_and_bad(*stored_set)

    else:
        print(
            """BiSC can accept inputs:
        1. A list of permutations
        2. A property of permutations
        3. A tuple of two dictionaries of lengths pointing to permutations
        4. A string
        5. A PropertyBitmaps"""
        )
        assert False

    # length -> the good (A) and the bad (B) permutations of that length
    A, B = property_bitmaps.good, property_bitmaps.bad

    while True:
        print("Learning patterns of length {} using perms of length {}".format(m, n))
        SG = bisc(property_bitmaps, m, n)
        show_me(SG, more=True)

        if SG != {}:
            print("Sanity checking the learned patterns up to length {}".format(L))
            val, avoiding_perms = patterns_suffice_for_bad(
                SG, L, B, stop_on_failure=True
            )
        else:
            val = False

        if val:
            print(
                "These patterns seem to suffice, I will now try to find a small basis"
            )

            ib = len(SG[min(SG.keys())].keys())
            while True:
                print("Trying to find a basis with at most {} patterns".format(ib))
                print("using perms of length {}".format(n))
                bases, dict_numbs_to_patts = run_clean_up(SG, B, n, limit_monitors=ib)

                if bases:
                    basis = bases[0]
                    show_me_basis(basis, dict_numbs_to_patts)

                    sg: _Patterns = to_sg_format(basis, dict_numbs_to_patts)

                    val, avoiding_perms = patterns_suffice_for_bad(
                        sg, L, B, stop_on_failure=True
                    )

                    if not val:
                        print("A bad basis was chosen.")
                        print("Increasing perm length to {}".format(n + 1))
                        n += 1
                        continue

                    val, containing_perms = patterns_suffice_for_good(
                        sg, L, A, stop_on_failure=True
                    )
                    if not val:
                        print("This is a bad basis. Need to learn from longer perms")
                        n += 1
                        break  # breaking out of the inner while-loop

                else:
                    print("No bases found. Increasing number of patterns in basis")
                    ib += 1
                    val = False

                if val:
                    print(
                        "!!! Found a basis with {} patts of length at most {}".format(
                            ib, m
                        )
                    )
                    print("!!! for the input using perms of length {}".format(n))
                    print("Basis: ", sg)
                    return sg

        else:
            print("Need to learn longer patterns")
            n += 1
            m += 1

        oldL = L
        if L < n + 1:
            L = n + 1
            if isinstance(prop, list) and L > max(A.keys()):
                print("You need to input a longer list of permutations")
                return None

            elif isinstance(prop, (types.FunctionType, PropertyBitmaps)):
                # The property labels the new lengths
                for i in range(oldL + 1, L + 1):
                    if i not in property_bitmaps.bitmaps:
                        if property_bitmaps.prop is None:
                            print("You need to add bitmaps of longer permutations")
                            return None
                        print("Adding perms of length {}".format(i))
                        property_bitmaps.add_length(i)

            elif isinstance(prop, tuple) and L > max(A.keys()):
                print("You need to add longer permutations to the dictionaries")
                return None

            elif isinstance(prop, str) and L > max(A.keys()):
                # If you pass in a string we assume it is pointing to a file in permsets
                print("Attempting to read perms from permsets")
                stored_set = _read_stored_set(prop, L)
                if stored_set is None:
                    print("The required files do not exist")
                    return None
                property_bitmaps = _from_good_and_bad(*stored_set)
                A, B = property_bitmaps.good, property_bitmaps.bad


def _bitmap_size(length: int) -> int:
    """The number of bytes in the bitmap of a length: a bit for each of its
    permutations."""
    return (factorial(length) + 7) // 8


def _set_label(bitmap: bytearray, index: int) -> None:
    """Set the label of the permutation at index: bit index % 8 of byte
    index // 8."""
    bitmap[index // 8] |= 1 << (index % 8)


def _label(bitmap: Union[bytes, bytearray], index: int) -> int:
    """The label (0 or 1) of the permutation at index."""
    return (bitmap[index // 8] >> (index % 8)) & 1


# A view unranks the permutations it wants, rather than generating all of the
# length's, when at most one in this many is wanted. Unranking one costs about 5
# (CPython 3.11) to 13 (PyPy 3.11) times as much as generating and testing one,
# measured at lengths 8 to 12, and 16 is above both
_UNRANK_WHEN_ONE_IN = 16


def _wanted_indices(
    bitmap: Union[bytes, bytearray], length: int, wanted_bit: int
) -> Iterator[int]:
    """The indices, in increasing order, of the permutations of a length whose
    label is wanted_bit. A byte with no such label is skipped whole."""
    skipped_byte = 0xFF if wanted_bit == 0 else 0
    permutation_count = factorial(length)
    for byte_index, byte in enumerate(bitmap):
        if byte != skipped_byte:
            for index in range(
                8 * byte_index, min(8 * byte_index + 8, permutation_count)
            ):
                if _label(bitmap, index) == wanted_bit:
                    yield index


# The sorted indices of a length's good permutations are kept in an array of
# this type code, unsigned integers of 8 bytes, while every index of the length
# fits in one: to length 20, since 21! is above 2**64. Past that they are kept in
# a list
_INDEX_TYPECODE: Final = "Q"
_INDEX_BITS = 8 * array(_INDEX_TYPECODE).itemsize
_Indices = Union["array[int]", List[int]]

# A length's labels, as a PropertyBitmaps keeps them: its bitmap, or the sorted
# indices of its good permutations
_Labels = Union[bytes, bytearray, _Indices]

# A length keeps the sorted indices of its good permutations, _INDEX_BITS bits
# each, rather than its bitmap, a bit for each of its permutations, when fewer
# than one in this many of them are good: the indices are then the smaller
_SPARSE_WHEN_ONE_IN = _INDEX_BITS


def _new_indices(length: int, indices: Iterable[int] = ()) -> _Indices:
    """The sorted indices of a length's good permutations, given in increasing
    order: an array while every index of the length fits in its items, and a
    list past that."""
    if factorial(length) <= 1 << _INDEX_BITS:
        return array(_INDEX_TYPECODE, indices)
    return list(indices)


def _most_indices(length: int) -> int:
    """The most good permutations of a length that are kept as indices: fewer
    than one in _SPARSE_WHEN_ONE_IN of its permutations."""
    return (factorial(length) - 1) // _SPARSE_WHEN_ONE_IN


def _is_sparse(good_count: int, length: int) -> bool:
    """Whether a length with good_count good permutations keeps their indices
    rather than its bitmap."""
    return good_count <= _most_indices(length)


def _label_in(labels: _Labels, index: int) -> int:
    """The label (0 or 1) of the permutation at index, from a length's labels
    in either form."""
    if isinstance(labels, (array, list)):
        position = bisect.bisect_left(labels, index)
        return int(position < len(labels) and labels[position] == index)
    return _label(labels, index)


def _bitmap_from_indices(length: int, indices: Iterable[int]) -> bytearray:
    """The bitmap of a length with the bits at the given indices set."""
    bitmap = bytearray(_bitmap_size(length))
    for index in indices:
        _set_label(bitmap, index)
    return bitmap


# Bitmaps are read this many bytes at a time, each chunk as one int, to count
# their bits or the bits two of them share, so that no int is made of a whole
# bitmap
_CHUNK_BYTES = 1 << 16


def _count_labels(bitmap: Union[bytes, bytearray]) -> int:
    """The number of bits set in a bitmap: its good permutations."""
    view = memoryview(bitmap)
    return sum(
        int.from_bytes(view[start : start + _CHUNK_BYTES], "little").bit_count()
        for start in range(0, len(view), _CHUNK_BYTES)
    )


class PropertyBitmaps:
    """A property's values on the permutations, length by length: which
    permutations of each length satisfy it (good) and which do not (bad).
    bisc and auto_bisc turn each of their inputs into one, and read its good
    and bad permutations through its views, good and bad.

    A length's labels are its bitmap: bit i is the label of Perm.unrank(i,
    length), bit i % 8 of byte i // 8, from the low bit. So a permutation perm
    is at bit perm.rank() - sum(factorial(k) for k in range(len(perm))), and
    the bits are in the order in which Perm.of_length(length) yields the
    permutations (lexicographic). The bitmap of length n is (n! + 7) // 8
    bytes. A length with fewer than one good permutation in 64 keeps instead
    the sorted indices of its good permutations (their bits), 8 bytes each,
    which then take less space. So no length takes more than its bitmap:
    three permutations of length 14 take 24 bytes, where its bitmap takes
    10.9 GB. Past length 20, whose indices can exceed 8 bytes, they are kept
    in a list, and there is no longest length.

    The labels can be given as bitmaps (bitmaps={length: bytes}), made from a
    property (add_length), or both: auto_bisc and bisc label the lengths they
    need and are not given with prop, adding them to this object. Without a
    prop, auto_bisc stops, as for a tuple of dictionaries, and bisc raises a
    ValueError. A bitmap given must be bytes-like (bytes, a bytearray or a
    memoryview), or a TypeError is raised. It must be of its length's size,
    with no bit set past the length's permutations, or a ValueError is
    raised. Changing a bytearray after giving it does not change the labels.

    The attributes bitmaps (length -> its bitmap, a read-only Mapping) and
    good_counts (length -> the number of good permutations) are for reading.
    The bitmap of a length kept as indices is built when bitmaps is asked
    for it.

    The views read the labels length by length: iterating over a length,
    counting it, asking whether a length is there, or whether a permutation
    is in a length. A bitmap of S_10 is 454 KB; S_10 as a list of Perm
    objects takes 0.9 GB on PyPy 3.11 and 1.3 to 1.8 GB on CPython.
    """

    def __init__(
        self,
        prop: Optional[Callable[[Perm], bool]] = None,
        bitmaps: Optional[Mapping[int, Union[bytes, bytearray, memoryview]]] = None,
    ) -> None:
        self.prop = prop
        # length -> its labels, in the form their number chooses (_is_sparse)
        self._labels: Dict[int, _Labels] = {}
        self.good_counts: Dict[int, int] = {}
        if bitmaps is not None:
            for length, bitmap in bitmaps.items():
                if not isinstance(bitmap, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        "A bitmap must be bytes, a bytearray or a memoryview, "
                        "not {}".format(type(bitmap).__name__)
                    )
                if isinstance(bitmap, memoryview):
                    # Its bytes, whatever the view's format and shape
                    bitmap = bytes(bitmap)
                if len(bitmap) != _bitmap_size(length):
                    raise ValueError(
                        "A bitmap of length {} has {} bytes, and must have {}".format(
                            length, len(bitmap), _bitmap_size(length)
                        )
                    )
                # The size check leaves spare bits in the last byte only at
                # lengths 0 to 3 (7, 7, 6 and 2 of them), since n! is a
                # multiple of 8 from n = 4 on. A spare bit set would be counted
                # as a good permutation: len() of the good view would disagree
                # with its iteration, and len() of the bad view could go
                # negative.
                spare_bit_count = 8 * len(bitmap) - factorial(length)
                if spare_bit_count and bitmap[-1] >> (8 - spare_bit_count):
                    raise ValueError(
                        "A bitmap of length {} has bits set past its {} "
                        "permutations".format(length, factorial(length))
                    )
                good_count = _count_labels(bitmap)
                if _is_sparse(good_count, length):
                    good_indices = _new_indices(
                        length, _wanted_indices(bitmap, length, 1)
                    )
                    self._keep(length, good_indices, good_count)
                elif isinstance(bitmap, bytes):
                    self._keep(length, bitmap, good_count)
                else:
                    # A copy, so that a change to the bytearray does not change
                    # the labels
                    self._keep(length, bytes(bitmap), good_count)
        self.bitmaps: Mapping[int, bytes] = _Bitmaps(self)
        self.good = _LengthViews(self, wanted_bit=1)
        self.bad = _LengthViews(self, wanted_bit=0)

    def _keep(self, length: int, labels: _Labels, good_count: int) -> None:
        """Keep a length's labels, in the form their number chooses, with that
        number of good permutations. The views read them from here."""
        self._labels[length] = labels
        self.good_counts[length] = good_count

    def add_length(self, length: int) -> None:
        """Label the permutations of a length with the property, and keep the
        length's labels, replacing any it has. The indices of the good
        permutations are kept while they are few; once there are more than a
        length keeps as indices, they are set in the length's bitmap, and the
        rest of the length is labeled in it. It needs a property."""
        if self.prop is None:
            raise ValueError(
                "The PropertyBitmaps has no property to label length {} "
                "with".format(length)
            )
        most_indices = _most_indices(length)
        good_indices = _new_indices(length)
        perms = enumerate(Perm.of_length(length))
        for index, perm in perms:
            if self.prop(perm):
                good_indices.append(index)
                if len(good_indices) > most_indices:
                    break
        else:
            self._keep(length, good_indices, len(good_indices))
            return
        # Too many for indices: they are set in the bitmap, and the loop goes
        # on in it from the next permutation, with a bit to set for each good
        # one and nothing more
        bitmap = _bitmap_from_indices(length, good_indices)
        good_count = len(good_indices)
        del good_indices
        for index, perm in perms:
            if self.prop(perm):
                _set_label(bitmap, index)
                good_count += 1
        self._keep(length, bitmap, good_count)


class _Bitmaps(Mapping[int, bytes]):
    """length -> its bitmap, read-only: the bitmap kept, or, for a length kept
    as the indices of its good permutations, one built from them when
    asked."""

    def __init__(self, property_bitmaps: PropertyBitmaps) -> None:
        self.property_bitmaps = property_bitmaps

    def __getitem__(self, length: int) -> bytes:
        labels = self.property_bitmaps._labels[length]
        if isinstance(labels, (array, list)):
            return bytes(_bitmap_from_indices(length, labels))
        return bytes(labels)

    def __contains__(self, length: object) -> bool:
        # Mapping's would build the bitmap of a length kept as indices, to
        # answer whether the length is there
        return length in self.property_bitmaps._labels

    def __iter__(self) -> Iterator[int]:
        return iter(self.property_bitmaps._labels)

    def __len__(self) -> int:
        return len(self.property_bitmaps._labels)


class _LengthViews(Mapping[int, "_PermsOfLength"]):
    """length -> the good (or bad) permutations of that length, read-only: a
    Mapping whose keys are the lengths with labels, through which bisc and
    auto_bisc read the permutations. wanted_bit is the label of the
    permutations it gives: 1 for the good ones, 0 for the bad ones."""

    def __init__(self, property_bitmaps: PropertyBitmaps, wanted_bit: int) -> None:
        self.property_bitmaps = property_bitmaps
        self.wanted_bit = wanted_bit

    def __getitem__(self, length: int) -> "_PermsOfLength":
        if length not in self.property_bitmaps._labels:
            raise KeyError(length)
        return _PermsOfLength(self.property_bitmaps, length, wanted_bit=self.wanted_bit)

    def __iter__(self) -> Iterator[int]:
        return iter(self.property_bitmaps._labels)

    def __len__(self) -> int:
        return len(self.property_bitmaps._labels)


class _PermsOfLength(Collection[Perm]):
    """The good (or bad) permutations of one length, read from its labels: a
    Collection. Iterating yields those whose label is the one wanted, in
    lexicographic order. For a length kept as the indices of its good
    permutations, the good ones are unranked from them, and the bad ones are
    the others, generated in order. From a bitmap, when few are wanted they
    are unranked, and otherwise the length's permutations are generated and
    each bit is tested. len() is the count kept with the labels, and a
    permutation is in it when its label is the one wanted."""

    def __init__(
        self, property_bitmaps: PropertyBitmaps, length: int, wanted_bit: int
    ) -> None:
        self.property_bitmaps = property_bitmaps
        self.length = length
        self.wanted_bit = wanted_bit

    def __contains__(self, perm: object) -> bool:
        # A permutation of this length: a Perm, or any other sequence of the
        # numbers 0 to length - 1, each once
        if not (
            isinstance(perm, Sequence)
            and len(perm) == self.length
            and all(isinstance(value, int) for value in perm)
            and set(perm) == set(range(self.length))
        ):
            return False
        labels = self.property_bitmaps._labels[self.length]
        index = Perm(perm).rank() - _shorter_count(self.length)
        return _label_in(labels, index) == self.wanted_bit

    def __iter__(self) -> Iterator[Perm]:
        labels = self.property_bitmaps._labels[self.length]
        wanted_bit = self.wanted_bit
        wanted_count = len(self)
        if wanted_count == 0:
            # Nothing to yield, and no need to read the labels
            return
        if isinstance(labels, (array, list)):
            if wanted_bit:
                for index in labels:
                    yield Perm.unrank(index, self.length)
            else:
                # The good indices are in increasing order, as the
                # permutations are generated
                good_indices = iter(labels)
                next_good_index = next(good_indices, None)
                for index, perm in enumerate(Perm.of_length(self.length)):
                    if index == next_good_index:
                        next_good_index = next(good_indices, None)
                    else:
                        yield perm
        elif wanted_count * _UNRANK_WHEN_ONE_IN <= factorial(self.length):
            for index in _wanted_indices(labels, self.length, wanted_bit):
                yield Perm.unrank(index, self.length)
        else:
            for index, perm in enumerate(Perm.of_length(self.length)):
                if _label(labels, index) == wanted_bit:
                    yield perm

    def __len__(self) -> int:
        good_count = self.property_bitmaps.good_counts[self.length]
        return good_count if self.wanted_bit else factorial(self.length) - good_count


@functools.lru_cache(maxsize=None)
def _shorter_count(length: int) -> int:
    """The number of permutations shorter than length: a permutation's bit is
    its rank() less this."""
    return sum(factorial(shorter_length) for shorter_length in range(length))


def _indices_of(length: int, perms: Iterable[Perm]) -> Iterator[int]:
    """The indices (bits) of permutations given as ones of a length. One of
    another length raises a ValueError."""
    shorter_count = _shorter_count(length)
    for perm in perms:
        if len(perm) != length:
            raise ValueError(
                "The permutation {!r} of length {} is given as one of length "
                "{}".format(perm, len(perm), length)
            )
        if not isinstance(perm, Perm):
            perm = Perm(perm)
        yield perm.rank() - shorter_count


def _labels_of(length: int, perms: Collection[Perm]) -> Tuple[_Labels, int]:
    """The labels of a length whose good permutations are the ones given, in
    the form their number chooses, and that number. A permutation given
    twice counts once."""
    if _is_sparse(len(perms), length):
        good_indices = _new_indices(length, sorted(set(_indices_of(length, perms))))
        return good_indices, len(good_indices)
    bitmap = _bitmap_from_indices(length, _indices_of(length, perms))
    good_count = _count_labels(bitmap)
    if _is_sparse(good_count, length):
        # Permutations given more than once made them look many
        return _new_indices(length, _wanted_indices(bitmap, length, 1)), good_count
    return bitmap, good_count


def _overlap_count(labels: _Labels, other_labels: _Labels) -> int:
    """The number of permutations good in both of two labels of one length."""
    if isinstance(labels, (array, list)):
        return sum(_label_in(other_labels, index) for index in labels)
    if isinstance(other_labels, (array, list)):
        return sum(_label_in(labels, index) for index in other_labels)
    view, other_view = memoryview(labels), memoryview(other_labels)
    return sum(
        (
            int.from_bytes(view[start : start + _CHUNK_BYTES], "little")
            & int.from_bytes(other_view[start : start + _CHUNK_BYTES], "little")
        ).bit_count()
        for start in range(0, len(view), _CHUNK_BYTES)
    )


def _from_perms_by_length(
    perms_by_length: Mapping[int, Collection[Perm]],
) -> PropertyBitmaps:
    """A PropertyBitmaps, with no property, whose good permutations of each
    length are the ones given for it."""
    property_bitmaps = PropertyBitmaps()
    for length, perms in perms_by_length.items():
        property_bitmaps._keep(length, *_labels_of(length, perms))
    return property_bitmaps


def _from_good_and_bad(
    good: Mapping[int, Collection[Perm]], bad: Mapping[int, Collection[Perm]]
) -> PropertyBitmaps:
    """A PropertyBitmaps, with no property, from the good and the bad
    permutations of each length up to the shorter mapping's longest. A length
    one of them lacks is empty in it, and a permutation given twice on one
    side counts once. The good and the bad permutations of each length must
    not overlap, and must together be all of its permutations, or a
    ValueError is raised."""
    property_bitmaps = PropertyBitmaps()
    for length in range(min(max(good), max(bad)) + 1):
        good_labels, good_count = _labels_of(length, good.get(length, ()))
        bad_labels, bad_count = _labels_of(length, bad.get(length, ()))
        in_both_count = _overlap_count(good_labels, bad_labels)
        in_neither_count = factorial(length) - (good_count + bad_count - in_both_count)
        if in_both_count or in_neither_count:
            raise ValueError(
                "The good and the bad permutations of length {} must not overlap "
                "and must together be all of its {} permutations (in both: {}, "
                "in neither: {})".format(
                    length, factorial(length), in_both_count, in_neither_count
                )
            )
        property_bitmaps._keep(length, good_labels, good_count)
    return property_bitmaps


def _read_stored_set(
    name: str, min_length: int
) -> Optional[Tuple[Dict[int, List[Perm]], Dict[int, List[Perm]]]]:
    """The good and the bad permutations of the set stored under name in
    permuta/resources/bisc, from the first of its files of each kind that go
    up to min_length or further, or None if there are none."""
    good_entry = None
    bad_entry = None
    bisc_dir = os.path.join(os.path.dirname(__file__), "..", "resources", "bisc")
    bisc_dir = os.path.abspath(bisc_dir)

    with os.scandir(bisc_dir) as entries:
        for entry in entries:
            entry_name = entry.name[:-5]
            name_parts = entry_name.split("_")
            if name_parts[0] == name:
                if (
                    good_entry is None
                    and name_parts[1] == "good"
                    and int(name_parts[2].split("len")[1]) >= min_length
                ):
                    good_entry = entry_name
                if (
                    bad_entry is None
                    and name_parts[1] == "bad"
                    and int(name_parts[2].split("len")[1]) >= min_length
                ):
                    bad_entry = entry_name
            if good_entry is not None and bad_entry is not None:
                break
    if good_entry is not None and bad_entry is not None:
        return (
            read_bisc_file(bisc_dir + "/" + good_entry),
            read_bisc_file(bisc_dir + "/" + bad_entry),
        )
    return None


def create_bisc_input(N, prop):
    """
    Create a dictionary, D, containing keys 1, 2, 3, ..., N. Each key points to
    a list of permutations satisfying the property prop. The dictionary E has
    the same keys and they point to the complement.
    """

    A, B = {}, {}

    for n in range(N + 1):
        An, Bn = [], []

        for perm in Perm.of_length(n):
            if prop(perm):
                An.append(perm)
            else:
                Bn.append(perm)

        A[n], B[n] = An, Bn

    return A, B


def write_bisc_files(n: int, prop, info: str) -> None:
    """Create a dictionary, D, containing keys 1, 2, 3, ..., n. Each key points to
    a list of permutations satisfying the property prop. The dictionary E has
    the same keys and they point to the complement.
    """
    good, bad = create_bisc_input(n, prop)
    write_json_to_file(good, f"{info}_good_len{n}.json")
    write_json_to_file(bad, f"{info}_bad_len{n}.json")


def write_json_to_file(json_obj, file_name):
    try:
        with open(file_name, "a+") as f:
            f.write(json.dumps(json_obj))
    except OSError:
        print(f"Could not write to file: {file_name}")


def from_json(json_string):
    json_obj = json.loads(json_string)
    return {int(key): list(map(Perm, values)) for key, values in json_obj.items()}


def read_bisc_file(path):
    try:
        with open(f"{path}.json", "r") as f:
            return from_json(f.readline())
    except (ValueError, TypeError, OSError) as e:
        print(f"File is invalid: {path}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        return {}
