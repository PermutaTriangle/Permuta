import json
import os
import types
from collections.abc import Collection, Mapping
from math import factorial
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Tuple, Union

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
):
    """
    Mine the forbidden patterns of length up to m from the permutations up to
    length n of a set A: a list of permutations, a property (a function), a
    dictionary or another Mapping (length -> the permutations of that length
    in the set), or a PropertyBitmaps. Each is turned into a PropertyBitmaps,
    whose good permutations of each length up to max(m, n) mine() reads.
    Without n, a property uses length 7, and the others their longest length.
    - A list sets the bits of the permutations it lists, and a length with
      none listed is empty.
    - A property labels the lengths up to n; a length past n, when m > n, is
      empty, as it was in the lists before.
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
        # The property labels the lengths up to n. mine() reads those up to m
        # too, and a length past n is empty, as it was in the lists before
        property_bitmaps = PropertyBitmaps(
            A,
            bitmaps={
                length: bytes(_bitmap_size(length)) for length in range(n + 1, m + 1)
            },
        )
        for length in range(n + 1):
            property_bitmaps.add_length(length)

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
    SG = forb(ci, goodpatts, m, report=report)

    return SG


def auto_bisc(
    prop: Union[
        Callable[[Perm], bool],
        List[Perm],
        Tuple[Dict[int, List[Perm]], Dict[int, List[Perm]]],
        str,
        "PropertyBitmaps",
    ],
):
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
    - A property labels each length when auto_bisc first needs it.
    - A list sets the bits of the permutations it lists, and the others are
      bad.
    - A tuple of dictionaries, or a stored set, must give each permutation of
      each length up to the shorter dictionary's longest exactly once, as good
      or as bad, or a ValueError is raised. A length one of them lacks is
      empty in it.
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
            return
        longest_length = max(listed_lengths)
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
        # The lengths the PropertyBitmaps lacks are labelled with its
        # property, if it has one
        property_bitmaps = prop
        for i in range(L + 1):
            if i not in property_bitmaps.bitmaps:
                if property_bitmaps.prop is None:
                    print("You should have bitmaps up to length at least 8")
                    return
                property_bitmaps.add_length(i)

    elif (
        isinstance(prop, tuple)
        and isinstance(prop[0], dict)
        and isinstance(prop[1], dict)
    ):
        # If you already have the dictionaries you can pass them in as a tuple
        if L not in prop[0].keys():
            print("You should have permutations up to length at least 8")
            return
        property_bitmaps = _from_good_and_bad(prop[0], prop[1])

    elif isinstance(prop, str):
        # If you pass in a string we assume it is pointing to a file in permsets
        print("Attempting to read perms from permsets")
        stored_set = _read_stored_set(prop, L)
        if stored_set is None:
            print("The required files do not exist")
            return
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

                    sg = to_sg_format(basis, dict_numbs_to_patts)

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
                return

            elif isinstance(prop, (types.FunctionType, PropertyBitmaps)):
                # The property labels the new lengths
                for i in range(oldL + 1, L + 1):
                    if i not in property_bitmaps.bitmaps:
                        if property_bitmaps.prop is None:
                            print("You need to add bitmaps of longer permutations")
                            return
                        print("Adding perms of length {}".format(i))
                        property_bitmaps.add_length(i)

            elif isinstance(prop, tuple) and L > max(A.keys()):
                print("You need to add longer permutations to the dictionaries")
                return

            elif isinstance(prop, str) and L > max(A.keys()):
                # If you pass in a string we assume it is pointing to a file in permsets
                print("Attempting to read perms from permsets")
                stored_set = _read_stored_set(prop, L)
                if stored_set is None:
                    print("The required files do not exist")
                    return
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


def _label(bitmap: bytes, index: int) -> int:
    """The label (0 or 1) of the permutation at index."""
    return (bitmap[index // 8] >> (index % 8)) & 1


class PropertyBitmaps:
    """A property's values on the permutations, one bitmap per length: which
    permutations of each length satisfy it (good) and which do not (bad).
    bisc and auto_bisc turn each of their inputs into one, and read its good
    and bad permutations through its views, good and bad.

    Bit i of a length's bitmap is the label of Perm.unrank(i, length): bit
    i % 8 of byte i // 8, from the low bit. So a permutation perm is at bit
    perm.rank() - sum(factorial(k) for k in range(len(perm))), and the bits
    are in the order in which Perm.of_length(length) yields the permutations
    (lexicographic). The bitmaps can be given (bitmaps={length: bytes}), made
    from a property (add_length), or both: auto_bisc and bisc label the
    lengths they need and are not given with prop, adding them to this
    object. Without a prop, auto_bisc stops, as for a tuple of dictionaries,
    and bisc raises a ValueError. A bitmap given must be bytes-like (bytes, a
    bytearray or a memoryview), of its length's size, with no bit set past
    the length's permutations.

    The views read the bitmaps length by length: iterating over a length,
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
        self.bitmaps: Dict[int, bytes] = {}
        self.good_counts: Dict[int, int] = {}
        if bitmaps is not None:
            for length, bitmap in bitmaps.items():
                if not isinstance(bitmap, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        "A bitmap must be bytes, a bytearray or a memoryview, "
                        "not {}".format(type(bitmap).__name__)
                    )
                bitmap = bytes(bitmap)
                if len(bitmap) != _bitmap_size(length):
                    raise ValueError(
                        "A bitmap of length {} has the wrong size".format(length)
                    )
                label_bits = int.from_bytes(bitmap, "little")
                # The size check leaves spare bits in the last byte only at
                # lengths 0 to 3 (7, 7, 6 and 2 of them), since n! is a
                # multiple of 8 from n = 4 on. A spare bit set would be counted
                # as a good permutation: len() of the good view would disagree
                # with its iteration, and len() of the bad view could go
                # negative.
                if label_bits >> factorial(length):
                    raise ValueError(
                        "A bitmap of length {} has bits set past its {} "
                        "permutations".format(length, factorial(length))
                    )
                self.bitmaps[length] = bitmap
                self.good_counts[length] = label_bits.bit_count()
        self.good = _LengthViews(self, True)
        self.bad = _LengthViews(self, False)

    def add_length(self, length: int) -> None:
        """Label the permutations of a length with the property, and keep
        their labels as the length's bitmap. It needs a property, and replaces
        the length's bitmap if there is one."""
        if self.prop is None:
            raise ValueError(
                "The PropertyBitmaps has no property to label length {} "
                "with".format(length)
            )
        bitmap = bytearray(_bitmap_size(length))
        good_count = 0
        for index, perm in enumerate(Perm.of_length(length)):
            if self.prop(perm):
                _set_label(bitmap, index)
                good_count += 1
        self.bitmaps[length] = bytes(bitmap)
        self.good_counts[length] = good_count


class _LengthViews(Mapping[int, "_PermsOfLength"]):
    """length -> the good (or bad) permutations of that length, read-only: a
    Mapping whose keys are the lengths with a bitmap, through which bisc and
    auto_bisc read the permutations."""

    def __init__(self, property_bitmaps: PropertyBitmaps, good: bool) -> None:
        self.property_bitmaps = property_bitmaps
        self.is_good = good

    def __getitem__(self, length: int) -> "_PermsOfLength":
        if length not in self.property_bitmaps.bitmaps:
            raise KeyError(length)
        return _PermsOfLength(self.property_bitmaps, length, self.is_good)

    def __iter__(self) -> Iterator[int]:
        return iter(self.property_bitmaps.bitmaps)

    def __len__(self) -> int:
        return len(self.property_bitmaps.bitmaps)


class _PermsOfLength(Collection[Perm]):
    """The good (or bad) permutations of one length, read from its bitmap: a
    Collection. Iterating generates the length's permutations in
    lexicographic order and yields those whose bit is the one wanted; len()
    is the count kept with the bitmap; and a permutation is in it when its
    bit is the one wanted."""

    def __init__(
        self, property_bitmaps: PropertyBitmaps, length: int, good: bool
    ) -> None:
        self.property_bitmaps = property_bitmaps
        self.length = length
        self.wanted_bit = 1 if good else 0

    def __contains__(self, perm: object) -> bool:
        if not isinstance(perm, Perm) or len(perm) != self.length:
            return False
        bitmap = self.property_bitmaps.bitmaps[self.length]
        index = perm.rank() - _shorter_count(self.length)
        return _label(bitmap, index) == self.wanted_bit

    def __iter__(self) -> Iterator[Perm]:
        bitmap = self.property_bitmaps.bitmaps[self.length]
        wanted_bit = self.wanted_bit
        for index, perm in enumerate(Perm.of_length(self.length)):
            if _label(bitmap, index) == wanted_bit:
                yield perm

    def __len__(self) -> int:
        good_count = self.property_bitmaps.good_counts[self.length]
        return good_count if self.wanted_bit else factorial(self.length) - good_count


def _shorter_count(length: int) -> int:
    """The number of permutations shorter than length: a permutation's bit is
    its rank() less this."""
    return sum(factorial(shorter_length) for shorter_length in range(length))


def _bitmap_of(length: int, perms: Iterable[Perm]) -> bytearray:
    """The bitmap of a length with the bits of the given permutations set. A
    permutation given twice sets its bit once."""
    bitmap = bytearray(_bitmap_size(length))
    shorter_count = _shorter_count(length)
    for perm in perms:
        if len(perm) != length:
            raise ValueError(
                "A permutation of length {} is given as one of length {}".format(
                    len(perm), length
                )
            )
        if not isinstance(perm, Perm):
            perm = Perm(perm)
        _set_label(bitmap, perm.rank() - shorter_count)
    return bitmap


def _from_perms_by_length(
    perms_by_length: Mapping[int, Iterable[Perm]],
) -> PropertyBitmaps:
    """A PropertyBitmaps, with no property, whose good permutations of each
    length are the ones given for it."""
    return PropertyBitmaps(
        bitmaps={
            length: _bitmap_of(length, perms)
            for length, perms in perms_by_length.items()
        }
    )


def _from_good_and_bad(
    good: Mapping[int, Collection[Perm]], bad: Mapping[int, Collection[Perm]]
) -> PropertyBitmaps:
    """A PropertyBitmaps, with no property, from the good and the bad
    permutations of each length up to the shorter mapping's longest. A length
    one of them lacks is empty in it. Each permutation of each length must be
    given exactly once, as good or as bad, or a ValueError is raised."""
    bitmaps = {}
    for length in range(min(max(good), max(bad)) + 1):
        good_bitmap = _bitmap_of(length, good.get(length, ()))
        bad_bitmap = _bitmap_of(length, bad.get(length, ()))
        good_bits = int.from_bytes(good_bitmap, "little")
        bad_bits = int.from_bytes(bad_bitmap, "little")
        every_bit = (1 << factorial(length)) - 1
        if good_bits & bad_bits or good_bits | bad_bits != every_bit:
            raise ValueError(
                "The good and the bad permutations of length {} must be all of "
                "its {} permutations, each once".format(length, factorial(length))
            )
        bitmaps[length] = good_bitmap
    return PropertyBitmaps(bitmaps=bitmaps)


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
            en = entry.name[:-5]
            spl = en.split("_")
            if spl[0] == name:
                if (
                    good_entry is None
                    and spl[1] == "good"
                    and int(spl[2].split("len")[1]) >= min_length
                ):
                    good_entry = en
                if (
                    bad_entry is None
                    and spl[1] == "bad"
                    and int(spl[2].split("len")[1]) >= min_length
                ):
                    bad_entry = en
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
