"""Tests of how bisc and auto_bisc take each kind of input: the default n of a
list, a mapping, a PropertyBitmaps and a property; m > n for a list and a
mapping; a list with permutations longer than max(m, n); where auto_bisc stops
on a short list or tuple and on a stored set it cannot find; a stored set whose
name holds underscores; report=True; the printed output of each input kind;
growth that would label a length it was given; and where a view starts to
unrank. The expected values are the answers bisc and auto_bisc gave before they
kept their input as bitmaps, or follow from the mathematics."""

import contextlib
import importlib
import io
import os

import pytest

from permuta.bisc.bisc import PropertyBitmaps, auto_bisc, bisc, create_bisc_input
from permuta.bisc.perm_properties import smooth
from permuta.patterns.perm import Perm

bisc_module = importlib.import_module("permuta.bisc.bisc")

BASIS_231 = {3: {Perm((1, 2, 0)): [set()]}}
WEST_2_AT_5 = {4: {Perm((1, 2, 3, 0)): [set()], Perm((2, 1, 3, 0)): [{(1, 4)}]}}


def good_by_length(prop, longest):
    return {
        length: [perm for perm in Perm.of_length(length) if prop(perm)]
        for length in range(longest + 1)
    }


def listed(good):
    return [perm for perms in good.values() for perm in perms]


def bitmaps_of(good):
    bitmaps = {}
    for length, perms in good.items():
        members = set(perms)
        label_bits = 0
        for index, perm in enumerate(Perm.of_length(length)):
            if perm in members:
                label_bits |= 1 << index
        bitmaps[length] = label_bits.to_bytes(
            (len(list(Perm.of_length(length))) + 7) // 8, "little"
        )
    return bitmaps


def run(function, *args):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        result = function(*args)
    return result, output.getvalue()


# The default n of each input kind
@pytest.mark.parametrize("kind", ["list", "mapping", "bitmaps"])
def test_bisc_without_n_reads_up_to_the_longest_length(kind):
    # West-2-stack-sortable needs perms of length 5: n = 4 gives another answer
    good = good_by_length(Perm.west_2_stack_sortable, 5)
    make = {
        "list": lambda: listed(good),
        "mapping": lambda: good,
        "bitmaps": lambda: PropertyBitmaps(bitmaps=bitmaps_of(good)),
    }[kind]
    assert bisc(make(), 4) == WEST_2_AT_5
    assert bisc(make(), 4, 4) != WEST_2_AT_5


def test_bisc_of_a_property_without_n_labels_up_to_7_and_says_so():
    seen = set()

    def prop(perm):
        seen.add(len(perm))
        return perm.stack_sortable()

    answer, printed = run(bisc, prop, 3)
    assert answer == BASIS_231
    assert seen == set(range(8))
    assert printed == "I will use permutations up to length 7\n"


def test_bisc_chooses_n_by_the_input_kind(monkeypatch):
    """Without n, bisc learns from the permutations up to the longest length of
    a list, a mapping or a PropertyBitmaps, however short, and up to length 7
    for a property, or a PropertyBitmaps with no labels."""
    chosen = []

    def recording_mine(goodperms, M, N=None, report=False):
        chosen.append(N)
        return [], {}

    monkeypatch.setattr(bisc_module, "mine", recording_mine)
    good = good_by_length(Perm.stack_sortable, 5)
    for A in (
        listed(good),
        good,
        PropertyBitmaps(bitmaps=bitmaps_of(good)),
        PropertyBitmaps(Perm.stack_sortable, bitmaps={0: b"\x01", 1: b"\x01"}),
        Perm.stack_sortable,
        PropertyBitmaps(Perm.stack_sortable),
    ):
        assert run(bisc, A, 2)[0] == {}
    assert chosen == [5, 5, 5, 1, 7, 7]
    run(bisc, listed(good), 2, 3)
    assert chosen[-1] == 3


def test_a_property_bitmaps_without_a_property_names_the_first_length_it_lacks():
    # length 0 is a length too: the callers test the length returned for None
    lacking_0 = PropertyBitmaps(bitmaps={1: b"\x01", 2: b"\x03"})
    assert lacking_0._label_missing(range(3)) == 0
    with pytest.raises(ValueError, match="none of length 0 and no property"):
        bisc(lacking_0, 2)
    # the length is max(m, n), here n
    message = (
        "bisc needs bitmaps up to length 3, and the PropertyBitmaps has none of "
        "length 1 and no property"
    )
    with pytest.raises(ValueError, match=message):
        bisc(PropertyBitmaps(bitmaps={0: b"\x01"}), 1, 3)
    should_have = "You should have bitmaps up to length at least 8\n"
    assert run(auto_bisc, PropertyBitmaps(bitmaps={1: b"\x01"})) == (None, should_have)
    short = PropertyBitmaps(bitmaps=bitmaps_of(good_by_length(Perm.stack_sortable, 5)))
    assert run(auto_bisc, short) == (None, should_have)


def test_label_missing_reports_each_length_it_labels():
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable, bitmaps={1: b"\x01"})
    assert run(property_bitmaps._label_missing, range(3), True) == (
        None,
        "Adding perms of length 0\nAdding perms of length 2\n",
    )
    assert sorted(property_bitmaps.bitmaps) == [0, 1, 2]


# m > n for a list and a mapping
def test_bisc_reads_the_lengths_up_to_m_of_a_list_or_a_mapping_past_n():
    good = good_by_length(Perm.stack_sortable, 6)
    avoiding_231 = {
        perm: [set()] for perm in Perm.of_length(4) if perm.avoids(Perm((1, 2, 0)))
    }
    # no good permutation of length 4 in a list that ends at length 3: all of
    # the length-4 permutations that avoid 231 are minimal forbidden patterns
    assert bisc(listed(good_by_length(Perm.stack_sortable, 3)), 4) == {
        **BASIS_231,
        4: avoiding_231,
    }
    # the lengths up to m = 5 of a longer list or mapping are read, though only
    # perms up to n = 3 are mined
    expected = {**BASIS_231, 4: {}, 5: {}}
    assert bisc(listed(good), 5, 3) == expected
    assert bisc(good, 5, 3) == expected


# Lengths 0 and 1, m = 0, n = 0, and the empty input
def test_bisc_of_the_empty_set_forbids_the_empty_permutation():
    assert bisc([], 3, 5) == {0: {Perm(()): [set()]}, 1: {}, 2: {}, 3: {}}
    assert bisc(lambda perm: False, 3, 5) == {
        0: {Perm(()): [set()]},
        1: {},
        2: {},
        3: {},
    }
    with pytest.raises(ValueError):
        bisc([], 3)  # no n, and no longest length
    with pytest.raises(ValueError):
        bisc({}, 3)


def test_bisc_with_m_or_n_zero():
    # the empty permutation alone: the class {empty}, whose basis is 1
    assert bisc(Perm.stack_sortable, 3, 0) == {1: {Perm((0,)): [set()]}, 2: {}, 3: {}}
    assert bisc([Perm(())], 3, 0) == {1: {Perm((0,)): [set()]}, 2: {}, 3: {}}
    # patterns of length 0 only: every length-0 permutation is good, "search for
    # longer patterns", {}
    for A in (Perm.stack_sortable, [Perm(())], {0: [Perm(())]}):
        assert run(bisc, A, 0, 0) == ({}, "You need to search for longer patterns\n")


# report=True, byte for byte
def test_bisc_report_prints_the_progress_and_the_same_for_each_input_kind():
    good = good_by_length(Perm.stack_sortable, 5)
    answer, printed = run(bisc, Perm.stack_sortable, 3, 5, True)
    assert answer == BASIS_231
    assert "Starting search for allowed patterns of lengths 0, ..., 3" in printed
    assert "Starting search for minimal forbidden patterns" in printed
    assert run(bisc, Perm.stack_sortable, 3, 5, False)[1] == ""
    for A in (listed(good), good, PropertyBitmaps(bitmaps=bitmaps_of(good))):
        assert run(bisc, A, 3, 5, True) == (answer, printed)


# What auto_bisc prints, for each input kind
def test_auto_bisc_prints_the_same_for_each_input_kind():
    good, bad = create_bisc_input(8, Perm.stack_sortable)
    answer, printed = run(auto_bisc, Perm.stack_sortable)
    assert answer == BASIS_231
    # the bitmaps and the pair of dictionaries print what the property prints
    assert run(auto_bisc, (good, bad)) == (answer, printed)
    assert run(auto_bisc, PropertyBitmaps(bitmaps=bitmaps_of(good))) == (
        answer,
        printed,
    )
    # a list prints a line for the bad permutations of length 8 it populates
    populating = "Populating the dictionary of bad perms of length  8\n"
    assert run(auto_bisc, listed(good)) == (answer, populating + printed)
    # a stored set prints the line that says so first
    smooth_answer, smooth_printed = run(auto_bisc, smooth)
    assert run(auto_bisc, "smooth") == (
        smooth_answer,
        "Attempting to read perms from permsets\n" + smooth_printed,
    )


# Where auto_bisc stops: a list, a tuple, a stored set
def derangement_in_av_213_231_312(perm):
    return perm.avoids(Perm((1, 0, 2)), Perm((1, 2, 0)), Perm((2, 0, 1))) and all(
        value != index for index, value in enumerate(perm)
    )


def test_auto_bisc_stops_when_a_list_or_a_tuple_is_too_short():
    good, bad = create_bisc_input(8, derangement_in_av_213_231_312)
    result, printed = run(auto_bisc, listed(good))
    assert result is None
    assert printed.endswith("You need to input a longer list of permutations\n")
    result, printed = run(auto_bisc, (good, bad))
    assert result is None
    assert printed.endswith("You need to add longer permutations to the dictionaries\n")
    # a bad dictionary that stops at length 7 stops it, though the good one reaches 8
    short_bad = {length: perms for length, perms in bad.items() if length < 8}
    result, printed = run(auto_bisc, (good, short_bad))
    assert result is None
    assert printed.endswith("You need to add longer permutations to the dictionaries\n")
    # one that stops at length 6 stops it at once: auto_bisc learns from the
    # permutations up to length 7 before its sanity checks reach length 8
    shorter_bad = {length: perms for length, perms in bad.items() if length < 7}
    assert run(auto_bisc, (good, shorter_bad)) == (
        None,
        "You need to add longer permutations to the dictionaries\n",
    )


@pytest.mark.parametrize("short", ["list", "tuple"])
def test_auto_bisc_wants_permutations_up_to_length_8(short):
    good, bad = create_bisc_input(7, Perm.stack_sortable)
    given = listed(good) if short == "list" else (good, bad)
    assert run(auto_bisc, given) == (
        None,
        "You should have permutations up to length at least 8\n",
    )
    assert run(auto_bisc, []) == (
        None,
        "You should have permutations up to length at least 8\n",
    )
    assert run(auto_bisc, ({}, {})) == (
        None,
        "You should have permutations up to length at least 8\n",
    )


def test_auto_bisc_of_a_stored_set_that_does_not_exist_or_runs_out():
    assert run(auto_bisc, "nosuchset") == (
        None,
        "Attempting to read perms from permsets\nThe required files do not exist\n",
    )
    # meander is stored to length 8: auto_bisc learns from perms of length 7, and
    # asks for the files again, for length 9
    result, printed = run(auto_bisc, "meander")
    assert result is None
    assert printed.endswith(
        "Attempting to read perms from permsets\nThe required files do not exist\n"
    )
    assert printed.count("Attempting to read perms from permsets") == 2


def test_auto_bisc_finds_a_stored_set_whose_name_holds_underscores(monkeypatch):
    # The files are <name>_<good or bad>_len<length>.json, and eight of the
    # thirteen stored sets have underscores in their names, as stack_sortable has
    answer, printed = run(auto_bisc, "stack_sortable")
    assert answer == BASIS_231
    assert printed.startswith("Attempting to read perms from permsets\n")
    read_files = []

    def recording_read(path):
        read_files.append(os.path.basename(path))
        return {}

    monkeypatch.setattr(bisc_module, "read_bisc_file", recording_read)
    for name, min_length, lengths in (
        ("stack_sortable", 8, {"len8"}),
        ("West_2_stack_sortable", 8, {"len8"}),
        ("av_231_and_mesh", 8, {"len8", "len9"}),
        ("av_231_and_mesh", 9, {"len9"}),
        ("smooth", 8, {"len8"}),
    ):
        read_files.clear()
        assert bisc_module._read_stored_set(name, min_length) == ({}, {})
        good_file, bad_file = read_files
        assert good_file.rsplit("_", 2)[:2] == [name, "good"]
        assert bad_file.rsplit("_", 2)[:2] == [name, "bad"]
        assert {good_file.rsplit("_", 1)[1], bad_file.rsplit("_", 1)[1]} <= lengths
    # a part of a name is no name
    for part in ("stack", "sortable", "West_2", "av_231_and"):
        assert bisc_module._read_stored_set(part, 8) is None


class StandInFolder:
    """Stands in for os.scandir's result: the entries of a folder, by name."""

    def __init__(self, names):
        self.entries = [type("Entry", (), {"name": name}) for name in names]

    def __enter__(self):
        return iter(self.entries)

    def __exit__(self, *exception):
        return False


def stand_in_stored_sets(monkeypatch, names):
    """Stands in a folder of files with these names for the stored sets', and
    returns the list of the files that reading a set then reads."""
    monkeypatch.setattr(os, "scandir", lambda path: StandInFolder(names))
    read_files = []

    def recording_read(path):
        read_files.append(os.path.basename(path))
        return {}

    monkeypatch.setattr(bisc_module, "read_bisc_file", recording_read)
    return read_files


def test_a_file_that_is_not_a_stored_sets_is_passed_over(monkeypatch):
    # the folder holds only sets' files, so the others are stood in for. The
    # first two come before the set's own: the first would be read as its good
    # one if a name were matched only from its start, and the second would
    # raise if a length could be no digits
    read_files = stand_in_stored_sets(
        monkeypatch,
        [
            "stack_good_len8.json.bak",
            "stack_good_len.json",
            "README",
            "stack_good_lenX.json",
            "stack_good_len8.txt",
            "stack_bad.json",
            "good_len8.json",
            "stack_good_len8.json",
            "stack_bad_len8.json",
        ],
    )
    assert bisc_module._read_stored_set("stack", 8) == ({}, {})
    assert read_files == ["stack_good_len8", "stack_bad_len8"]
    assert bisc_module._read_stored_set("stack", 9) is None


def test_a_set_is_read_only_if_both_kinds_go_far_enough(monkeypatch):
    # its good permutations go to length 9, and its bad ones to 8
    read_files = stand_in_stored_sets(
        monkeypatch, ["stack_good_len9.json", "stack_bad_len8.json"]
    )
    assert bisc_module._read_stored_set("stack", 9) is None
    assert read_files == []
    assert bisc_module._read_stored_set("stack", 8) == ({}, {})
    assert read_files == ["stack_good_len9", "stack_bad_len8"]


def test_auto_bisc_reads_a_stored_set_again_for_a_longer_length(monkeypatch):
    # No stored set that auto_bisc can name is longer than 8 and learned from perms
    # of length 8 or more, so the files are faked: the increasing permutations of
    # even length are no class (the bad (0) avoids their basis, 21), so auto_bisc
    # keeps growing n and reading
    def cycle(perm):
        return len(perm) % 2 == 0 and perm.is_increasing()

    reads = []

    def fake_read_stored_set(name, min_length):
        reads.append(min_length)
        return (
            create_bisc_input(8, cycle)
            if min_length <= 8
            else (create_bisc_input(9, cycle) if min_length == 9 else None)
        )

    monkeypatch.setattr(bisc_module, "_read_stored_set", fake_read_stored_set)
    # the sanity check of the learned patterns must see the longer set it was read
    # again for: the bad permutations of length L, where L is the length asked
    real_check = bisc_module.patterns_suffice_for_bad
    checks = []

    def recording_check(patterns, length, bad, stop_on_failure=False):
        checks.append((length, max(bad.keys())))
        return real_check(patterns, length, bad, stop_on_failure=stop_on_failure)

    monkeypatch.setattr(bisc_module, "patterns_suffice_for_bad", recording_check)
    result, printed = run(auto_bisc, "cycles")
    assert result is None
    assert reads == [8, 9, 10]
    assert (9, 9) in checks and all(longest >= length for length, longest in checks)
    assert printed.endswith(
        "Attempting to read perms from permsets\nThe required files do not exist\n"
    )


# Growth does not replace the bitmaps auto_bisc was given
class ReachedLength10(Exception):
    pass


def test_auto_bisc_growth_does_not_label_a_length_it_was_given():
    labeled_lengths = []

    def prop(perm):
        if len(perm) == 10:
            raise ReachedLength10
        labeled_lengths.append(len(perm))
        return derangement_in_av_213_231_312(perm)

    bitmaps = bitmaps_of(good_by_length(derangement_in_av_213_231_312, 8))
    # length 9: deliberately given as all bad, and not asked of the property
    bitmaps[9] = bytes(45360)
    property_bitmaps = PropertyBitmaps(prop, bitmaps=bitmaps)
    try:
        run(auto_bisc, property_bitmaps)
    except ReachedLength10:
        pass
    assert 9 not in labeled_lengths
    assert property_bitmaps.bitmaps[9] == bytes(45360)


# A permutation given twice on one side counts once, for auto_bisc too
def test_a_permutation_given_twice_counts_once_in_auto_bisc():
    good, bad = create_bisc_input(8, Perm.stack_sortable)
    answer, printed = run(auto_bisc, Perm.stack_sortable)
    twice = {**good, 5: good[5] + good[5][:3]}
    assert run(auto_bisc, (twice, bad)) == (answer, printed)
    assert run(auto_bisc, listed(twice)) == (
        answer,
        "Populating the dictionary of bad perms of length  8\n" + printed,
    )
    also_bad_twice = {**bad, 6: bad[6] + bad[6][:2]}
    assert run(auto_bisc, (good, also_bad_twice)) == (answer, printed)


# A dictionary of the pair may lack a length it has no permutation of
def test_a_tuple_may_lack_a_length_with_no_bad_permutations():
    good, bad = create_bisc_input(8, Perm.stack_sortable)
    # every permutation of length 0, 1 and 2 is stack-sortable: no bad ones
    bad = {length: perms for length, perms in bad.items() if perms}
    assert sorted(bad) == [3, 4, 5, 6, 7, 8]
    assert auto_bisc((good, bad)) == BASIS_231


# A bytearray given as a bitmap is copied
def test_a_bytearray_bitmap_is_copied():
    raw = bytearray(b"\x3f")
    property_bitmaps = PropertyBitmaps(bitmaps={3: raw})
    raw[0] = 0
    assert len(property_bitmaps.good[3]) == 6
    assert len(list(property_bitmaps.good[3])) == 6


# The views follow the PropertyBitmaps as lengths are added
def test_the_views_follow_added_lengths():
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable)
    good, bad = property_bitmaps.good, property_bitmaps.bad
    assert 4 not in good and len(good) == 0
    property_bitmaps.add_length(4)
    assert 4 in good and 4 in bad and list(good) == [4]
    assert len(good[4]) == 14 and len(bad[4]) == 10


# add_length replaces a bitmap it was given
def test_add_length_replaces_the_bitmap_of_a_length():
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable, bitmaps={3: bytes(1)})
    assert len(property_bitmaps.good[3]) == 0
    property_bitmaps.add_length(3)
    assert len(property_bitmaps.good[3]) == 5 and len(property_bitmaps.bad[3]) == 1
    assert list(property_bitmaps.bad[3]) == [Perm((1, 2, 0))]


# A PropertyBitmaps with only a property is labeled up to length 8 at the start
class ReachedLength9(Exception):
    pass


def test_auto_bisc_of_a_property_only_input_labels_the_lengths_up_to_8():
    def prop(perm):
        if len(perm) > 8:
            raise ReachedLength9
        return perm.stack_sortable()

    property_bitmaps = PropertyBitmaps(prop)
    assert auto_bisc(property_bitmaps) == BASIS_231
    assert sorted(property_bitmaps.bitmaps) == list(range(9))


# The tuple, the list and the bitmaps without a property stop at the same point
def test_auto_bisc_stops_at_the_same_point_for_each_input_kind():
    good, bad = create_bisc_input(8, derangement_in_av_213_231_312)
    bitmaps_message = "You need to add bitmaps of longer permutations\n"
    bitmaps_printed = run(auto_bisc, PropertyBitmaps(bitmaps=bitmaps_of(good)))[1]
    assert bitmaps_printed.endswith(bitmaps_message)
    body = bitmaps_printed[: -len(bitmaps_message)]
    result, printed = run(auto_bisc, (good, bad))
    assert result is None
    assert printed == body + "You need to add longer permutations to the dictionaries\n"
    result, printed = run(auto_bisc, listed(good))
    assert result is None
    assert printed == (
        "Populating the dictionary of bad perms of length  8\n"
        + body
        + "You need to input a longer list of permutations\n"
    )


# A view unranks when at most one in 16 is wanted, on both sides of the edge
@pytest.mark.parametrize("good", [True, False])
def test_a_view_unranks_exactly_when_at_most_one_in_16_is_wanted(monkeypatch, good):
    unranked = []
    real_unrank = Perm.unrank

    def counting_unrank(index, length):
        unranked.append(index)
        return real_unrank(index, length)

    monkeypatch.setattr(Perm, "unrank", staticmethod(counting_unrank))
    # length 6 has 720 permutations: 45 is one in 16, 46 is more
    for wanted, expect_unranking in ((45, True), (46, False)):
        label_bits = (1 << wanted) - 1  # the first `wanted` permutations
        if not good:
            label_bits = ((1 << 720) - 1) ^ label_bits
        view = PropertyBitmaps(bitmaps={6: label_bits.to_bytes(90, "little")})
        view = view.good[6] if good else view.bad[6]
        unranked.clear()
        assert len(list(view)) == wanted
        assert bool(unranked) == expect_unranking
