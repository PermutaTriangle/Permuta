# type: ignore

import json
import os
import types
from collections import defaultdict
from math import factorial

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


def bisc(A, m, n=None, report=False):
    """
    Mine the forbidden patterns of length up to m from the permutations up to
    length n of a set A: a list of permutations, a property (a function), a
    dictionary (length -> the permutations of that length in the set), or a
    PropertyBitmaps. Without n, a property uses length 7, and the others their
    longest length. mine() reads the lengths up to m and the permutations up
    to n, so the lengths up to max(m, n) that a PropertyBitmaps lacks are
    labelled with its property, and added to it. report prints the progress
    of the search.

    Returns the forbidden patterns found: a dictionary from length to
    {pattern: [shadings]}, where each shading is a set of boxes, and an empty
    one makes the pattern classical.
    """
    if isinstance(A, list):
        D = defaultdict(list)
        for perm in A:
            D[len(perm)].append(perm)
    elif isinstance(A, types.FunctionType):
        if n is None:
            print("I will use permutations up to length 7")
            n = 7
        D = defaultdict(list)
        for i in range(n + 1):
            for perm in Perm.of_length(i):
                if A(perm):
                    D[i].append(perm)

    elif isinstance(A, dict):
        D = A

    elif isinstance(A, PropertyBitmaps):
        if n is None:
            if A.bitmaps:
                n = max(A.bitmaps)
            elif A.prop is not None:
                print("I will use permutations up to length 7")
                n = 7
            else:
                raise ValueError("The PropertyBitmaps has no labels and no property")
        for length in range(max(m, n) + 1):
            if length not in A.bitmaps:
                if A.prop is None:
                    raise ValueError(
                        "bisc needs labels up to length {}, and the PropertyBitmaps "
                        "has none of length {} and no property".format(
                            max(m, n), length
                        )
                    )
                A.add_length(length)
        D = A.good

    elif isinstance(A, _LengthViews):
        D = A

    else:
        print(
            """BiSC can accept inputs:
        1. A list of permutations
        2. A property of permutations
        3. A dictionary of lengths pointing to permutations
        4. A PropertyBitmaps (labels kept as bitmaps)"""
        )
        assert False

    if n is None:
        n = max(D.keys())

    ci, goodpatts = mine(D, m, n, report=report)
    SG = forb(ci, goodpatts, m, report=report)

    return SG


def auto_bisc(prop, labels="lists"):
    """
    Learn a basis of forbidden patterns for a set of permutations, growing
    the length of the patterns and of the permutations they are learned from
    until the patterns found describe the set on every permutation up to
    length L, at least 8. Returns the basis, in the form bisc returns its
    patterns, or None when the input is too short to check a basis.

    prop is the set: a property of permutations (a function), a list of
    permutations, a tuple of two dictionaries (length -> the permutations in
    the set, and those not in it), the name of a set in
    permuta/resources/bisc, or a PropertyBitmaps.

    labels says how the labels of a property are kept:
    "lists" (the default, as before): the good and the bad permutations of
    each length as lists of Perm objects;
    "bitmaps": one bitmap per length (PropertyBitmaps), for the same result in
    far less memory, at the cost of generating a length's permutations again
    each time it is read. Use it when the permutations checked are long: those
    of length 10 take 0.9 to 1.8 GB as lists of Perm objects, depending on the
    Python, and 454 KB as a bitmap, a bit for each permutation (5 MB at length
    11, 60 MB at length 12).

    A PropertyBitmaps can also be given as prop directly. The lengths auto_bisc
    labels with its property are added to it, so a later run reuses them.
    """
    if labels not in ("lists", "bitmaps"):
        raise ValueError('labels must be "lists" or "bitmaps"')
    if labels == "bitmaps":
        if isinstance(prop, types.FunctionType):
            prop = PropertyBitmaps(prop)
        elif not isinstance(prop, PropertyBitmaps):
            raise ValueError(
                'labels="bitmaps" needs a property (a function) or a PropertyBitmaps'
            )
    L = 8  # Want to sanity check on at least S8, and one above n
    n = 4
    m = 2

    if isinstance(prop, list):
        # If a list is passed in then we put it in a dictionary at the start
        A = defaultdict(list)
        # We will put the complement up to S8 into another dictionary
        B = defaultdict(list)
        for perm in prop:
            A[len(perm)].append(perm)
        if L not in A.keys():
            print("You should have permutations up to length at least 8")
            return
        for i in range(max(L + 1, max(A.keys()) + 1)):
            if i > 7:
                print("Populating the dictionary of bad perms of length ", i)
            B[i] = [perm for perm in Perm.of_length(i) if perm not in A[i]]

    elif isinstance(prop, types.FunctionType):
        # If a property is passed in then we use it to populate both
        # both dictionaries up to S8
        A = defaultdict(list)
        B = defaultdict(list)
        for i in range(L + 1):
            A[i] = []
            B[i] = []
            for perm in Perm.of_length(i):
                if prop(perm):
                    A[i].append(perm)
                else:
                    B[i].append(perm)

    elif isinstance(prop, PropertyBitmaps):
        # Labels kept as one bitmap per length: A and B are views of the good
        # and the bad permutations, generated length by length when they are
        # read, instead of lists. The lengths the PropertyBitmaps lacks are
        # labelled with its property, if it has one
        for i in range(L + 1):
            if i not in prop.bitmaps:
                if prop.prop is None:
                    print("You should have labels up to length at least 8")
                    return
                prop.add_length(i)
        A, B = prop.good, prop.bad

    elif (
        isinstance(prop, tuple)
        and isinstance(prop[0], dict)
        and isinstance(prop[1], dict)
    ):
        # If you already have the dictionaries you can pass them in as a tuple
        A = prop[0]
        B = prop[1]
        if L not in A.keys():
            print("You should have permutations up to length at least 8")
            return

    elif isinstance(prop, str):
        # If you pass in a string we assume it is pointing to a file in permsets
        print("Attempting to read perms from permsets")
        good_entry = None
        bad_entry = None
        bisc_dir = os.path.join(os.path.dirname(__file__), "..", "resources", "bisc")
        bisc_dir = os.path.abspath(bisc_dir)

        with os.scandir(bisc_dir) as entries:
            for i, entry in enumerate(entries):
                en = entry.name[:-5]
                spl = en.split("_")
                if spl[0] == prop:
                    if (
                        good_entry is None
                        and spl[1] == "good"
                        and int(spl[2].split("len")[1]) >= L
                    ):
                        good_entry = en
                    if (
                        bad_entry is None
                        and spl[1] == "bad"
                        and int(spl[2].split("len")[1]) >= L
                    ):
                        bad_entry = en
                if good_entry is not None and bad_entry is not None:
                    break
        if good_entry is not None and bad_entry is not None:
            A = read_bisc_file(bisc_dir + "/" + good_entry)
            B = read_bisc_file(bisc_dir + "/" + bad_entry)
        else:
            print("The required files do not exist")
            return

    else:
        print(
            """BiSC can accept inputs:
        1. A list of permutations
        2. A property of permutations
        3. A tuple of two dictionaries of lengths pointing to permutations
        4. A string
        5. A PropertyBitmaps (labels kept as bitmaps)"""
        )
        assert False

    while True:
        print("Learning patterns of length {} using perms of length {}".format(m, n))
        SG = bisc(A, m, n)
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

            elif isinstance(prop, types.FunctionType):
                # Adding perms to the dictionaries
                for i in range(oldL + 1, L + 1):
                    print("Adding perms of length {}".format(i))
                    for perm in Perm.of_length(i):
                        if prop(perm):
                            A[i].append(perm)
                        else:
                            B[i].append(perm)

            elif isinstance(prop, PropertyBitmaps):
                for i in range(oldL + 1, L + 1):
                    if i not in prop.bitmaps:
                        if prop.prop is None:
                            print("You need to add labels of longer permutations")
                            return
                        print("Adding perms of length {}".format(i))
                        prop.add_length(i)

            elif isinstance(prop, tuple) and L > min(max(A.keys()), max(B.keys())):
                print("You need to add longer permutations to the dictionaries")
                return

            elif isinstance(prop, str) and L > min(max(A.keys()), max(B.keys())):
                # If you pass in a string we assume it is pointing to a file in permsets
                print("Attempting to read perms from permsets")
                good_entry = None
                bad_entry = None
                bisc_dir = os.path.join(
                    os.path.dirname(__file__), "..", "resources", "bisc"
                )
                bisc_dir = os.path.abspath(bisc_dir)
                with os.scandir(bisc_dir) as entries:
                    for i, entry in enumerate(entries):
                        en = entry.name[:-5]
                        spl = en.split("_")
                        if spl[0] == prop:
                            if (
                                good_entry is None
                                and spl[1] == "good"
                                and int(spl[2].split("len")[1]) >= L
                            ):
                                good_entry = en
                            if (
                                bad_entry is None
                                and spl[1] == "bad"
                                and int(spl[2].split("len")[1]) >= L
                            ):
                                bad_entry = en
                        if good_entry is not None and bad_entry is not None:
                            break
                if good_entry is not None and bad_entry is not None:
                    A = read_bisc_file(bisc_dir + "/" + good_entry)
                    B = read_bisc_file(bisc_dir + "/" + bad_entry)
                else:
                    print("The required files do not exist")
                    return


def _bitmap_size(length):
    """The number of bytes in the bitmap of a length: a bit for each of its
    permutations."""
    return (factorial(length) + 7) // 8


class PropertyBitmaps:
    """Labels of permutations, one bitmap per length, as input to auto_bisc
    and bisc: which permutations of each length satisfy a property (good) and
    which do not (bad).

    Bit i of a length's bitmap is the label of Perm.unrank(i, length), in
    byte i // 8, from the low bit; so a permutation perm is at bit
    perm.rank() - sum(factorial(k) for k in range(len(perm))). This is the
    order in which Perm.of_length(length) yields the permutations
    (lexicographic), which the views use to iterate. The bitmaps can be given
    (bitmaps={length: bytes}), made from a property (add_length), or both:
    auto_bisc and bisc label the lengths they need and are not given with
    prop, adding them to this object. Without a prop, auto_bisc stops, as for
    a tuple of dictionaries, and bisc raises a ValueError. A bitmap given must
    be bytes-like (bytes, a bytearray or a memoryview), of its length's size,
    with no bit set past the length's permutations.

    auto_bisc reads its good and bad permutations only length by length:
    iterating over a length, counting it, asking whether a length is there.
    The views good and bad do that from the bitmaps, generating a length's
    permutations again each time it is iterated, in the same order as the
    lists a property input makes. A bitmap of S_10 is 454 KB; S_10 as a list
    of Perm objects takes 0.9 GB on PyPy 3.11 and 1.3 to 1.8 GB on CPython.
    """

    def __init__(self, prop=None, bitmaps=None):
        self.prop = prop
        self.bitmaps = {}
        self.good_counts = {}
        for length, bitmap in (bitmaps or {}).items():
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
            if label_bits >> factorial(length):
                raise ValueError(
                    "A bitmap of length {} has bits set past its {} "
                    "permutations".format(length, factorial(length))
                )
            self.bitmaps[length] = bitmap
            self.good_counts[length] = label_bits.bit_count()
        self.good = _LengthViews(self, True)
        self.bad = _LengthViews(self, False)

    def add_length(self, length):
        """Label the permutations of a length with the property, and keep
        their labels as the length's bitmap. It needs a property, and replaces
        the length's bitmap if there is one."""
        bitmap = bytearray(_bitmap_size(length))
        good_count = 0
        for i, perm in enumerate(Perm.of_length(length)):
            if self.prop(perm):
                bitmap[i >> 3] |= 1 << (i & 7)
                good_count += 1
        self.bitmaps[length] = bytes(bitmap)
        self.good_counts[length] = good_count


class _LengthViews:
    """length -> the good (or bad) permutations of that length, read-only, as
    the dictionaries of lists auto_bisc builds from the other inputs."""

    def __init__(self, property_bitmaps, good):
        self.property_bitmaps = property_bitmaps
        self.is_good = good

    def keys(self):
        return self.property_bitmaps.bitmaps.keys()

    def __contains__(self, length):
        return length in self.property_bitmaps.bitmaps

    def __getitem__(self, length):
        if length not in self.property_bitmaps.bitmaps:
            raise KeyError(length)
        return _PermsOfLength(self.property_bitmaps, length, self.is_good)


class _PermsOfLength:
    def __init__(self, property_bitmaps, length, good):
        self.property_bitmaps = property_bitmaps
        self.length = length
        self.wanted_bit = 1 if good else 0

    def __iter__(self):
        bitmap = self.property_bitmaps.bitmaps[self.length]
        wanted_bit = self.wanted_bit
        for i, perm in enumerate(Perm.of_length(self.length)):
            if (bitmap[i >> 3] >> (i & 7)) & 1 == wanted_bit:
                yield perm

    def __len__(self):
        good_count = self.property_bitmaps.good_counts[self.length]
        return good_count if self.wanted_bit else factorial(self.length) - good_count


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
