import contextlib
import importlib
import io
import os
from collections.abc import Collection, Mapping
from math import factorial

import pytest

from permuta.bisc.bisc import (
    PropertyBitmaps,
    auto_bisc,
    bisc,
    create_bisc_input,
    read_bisc_file,
)
from permuta.bisc.perm_properties import smooth
from permuta.patterns.perm import Perm

BASIS_231 = {3: {Perm((1, 2, 0)): [set()]}}
BASIS_WEST_2 = {4: {Perm((1, 2, 3, 0)): [set()], Perm((2, 1, 3, 0)): [{(1, 4)}]}}
# The module, which permuta.bisc's function bisc hides, and its mine()
bisc_module = importlib.import_module("permuta.bisc.bisc")
REAL_MINE = bisc_module.mine


def property_bitmaps_up_to(prop, max_length):
    property_bitmaps = PropertyBitmaps(prop)
    for length in range(max_length + 1):
        property_bitmaps.add_length(length)
    return property_bitmaps


def test_views_match_lists():
    property_bitmaps = property_bitmaps_up_to(Perm.stack_sortable, 6)
    for length in range(7):
        good = [perm for perm in Perm.of_length(length) if perm.stack_sortable()]
        bad = [perm for perm in Perm.of_length(length) if not perm.stack_sortable()]
        assert list(property_bitmaps.good[length]) == good
        assert list(property_bitmaps.bad[length]) == bad
        assert len(property_bitmaps.good[length]) == len(good)
        assert len(property_bitmaps.bad[length]) == len(bad)
        assert bool(property_bitmaps.bad[length]) == bool(bad)
    assert sorted(property_bitmaps.good.keys()) == list(range(7))
    assert 6 in property_bitmaps.bad and 7 not in property_bitmaps.bad
    with pytest.raises(KeyError, match="7"):
        _ = property_bitmaps.good[7]


def test_views_are_a_mapping_of_collections():
    property_bitmaps = property_bitmaps_up_to(Perm.stack_sortable, 6)
    for view in (property_bitmaps.good, property_bitmaps.bad):
        assert isinstance(view, Mapping)
        assert list(view) == list(range(7)) and len(view) == 7
        assert view.get(7) is None
        assert all(isinstance(view[length], Collection) for length in view)
    for length in range(7):
        good, bad = property_bitmaps.good[length], property_bitmaps.bad[length]
        for perm in Perm.of_length(length):
            assert (perm in good) == perm.stack_sortable()
            assert (perm in bad) == (not perm.stack_sortable())
    # A permutation of another length is in neither view of a length
    assert Perm((0, 1)) not in property_bitmaps.good[3]
    assert Perm((0, 1, 2, 3)) not in property_bitmaps.bad[3]
    # Any sequence that is a permutation of the length is read as one, and
    # nothing else is in a view
    assert (0, 1, 2) in property_bitmaps.good[3] and [1, 2, 0] in property_bitmaps.bad[
        3
    ]
    for not_a_perm_of_3 in (Perm((1, 2, 3)), Perm((5, 5, 5)), (0, 0, 1), "012", 3):
        assert not_a_perm_of_3 not in property_bitmaps.good[3]
        assert not_a_perm_of_3 not in property_bitmaps.bad[3]


def test_views_unrank_a_length_with_few_wanted():
    # A length where at most one permutation in 16 is wanted is read by
    # unranking those, in the order of Perm.of_length: the good permutations at
    # length 8 here (1430 of 40320), and every bad one of a set of all but the
    # identity; length 7 (429 good of 5040) is read by generating the length
    property_bitmaps = property_bitmaps_up_to(Perm.stack_sortable, 8)
    for length in (7, 8):
        good = [perm for perm in Perm.of_length(length) if perm.stack_sortable()]
        assert list(property_bitmaps.good[length]) == good
    not_increasing = property_bitmaps_up_to(lambda perm: not perm.is_increasing(), 6)
    for length in range(7):
        assert list(not_increasing.bad[length]) == [Perm(range(length))]
        assert list(not_increasing.good[length]) == list(Perm.of_length(length))[1:]
    # The first eight permutations of length 6 bad, a byte of zeros
    first_eight_bad = PropertyBitmaps(bitmaps={6: b"\x00" + b"\xff" * 89})
    assert list(first_eight_bad.bad[6]) == list(Perm.of_length(6))[:8]
    # No bad permutation of length 3: the spare bits of its byte are not read
    assert list(PropertyBitmaps(bitmaps={3: b"\x3f"}).bad[3]) == []


def test_views_unrank_a_byte_of_good_permutations():
    # The first eight permutations of length 6 good, a byte of ones: 8 of 720,
    # read by unranking, and the byte must not be skipped
    first_eight_good = PropertyBitmaps(bitmaps={6: b"\xff" + b"\x00" * 89})
    assert list(first_eight_good.good[6]) == list(Perm.of_length(6))[:8]
    # A property that holds on a lexicographic block: the 120 permutations of
    # length 7 that start with 0, 1 fill fifteen bytes
    starts_0_1 = property_bitmaps_up_to(
        lambda perm: len(perm) < 2 or (perm[0] == 0 and perm[1] == 1), 7
    )
    assert list(starts_0_1.good[7]) == [
        perm for perm in Perm.of_length(7) if perm[0] == 0 and perm[1] == 1
    ]


def test_bit_order_is_perm_unrank():
    # Bit i of a length's bitmap is the label of Perm.unrank(i, length), and the
    # permutation perm is at bit perm.rank() minus the number of shorter
    # permutations
    property_bitmaps = property_bitmaps_up_to(Perm.stack_sortable, 6)
    shorter_count = 0
    for length in range(7):
        bitmap = property_bitmaps.bitmaps[length]
        for i in range(factorial(length)):
            perm = Perm.unrank(i, length)
            assert perm.rank() - shorter_count == i
            assert bool(bitmap[i >> 3] >> (i & 7) & 1) == perm.stack_sortable()
        shorter_count += factorial(length)


def test_bitmaps_round_trip():
    property_bitmaps = property_bitmaps_up_to(Perm.stack_sortable, 6)
    round_trip = PropertyBitmaps(bitmaps=property_bitmaps.bitmaps)
    for length in range(7):
        assert list(round_trip.good[length]) == list(property_bitmaps.good[length])
        assert list(round_trip.bad[length]) == list(property_bitmaps.bad[length])
    # 3! bits fit in one byte
    with pytest.raises(ValueError, match="length 3 has 2 bytes, and must have 1"):
        PropertyBitmaps(bitmaps={3: b"\x00\x00"})
    with pytest.raises(ValueError, match="length 3 has 0 bytes, and must have 1"):
        PropertyBitmaps(bitmaps={3: b""})


def test_lengths_0_and_1_labeled_bad():
    property_bitmaps = PropertyBitmaps(bitmaps={0: b"\x00", 1: b"\x00"})
    for length in (0, 1):
        assert list(property_bitmaps.good[length]) == []
        assert list(property_bitmaps.bad[length]) == [Perm(range(length))]
        assert len(property_bitmaps.good[length]) == 0
        assert len(property_bitmaps.bad[length]) == 1


@pytest.mark.parametrize(
    "length, bitmap",
    [(0, b"\x03"), (1, b"\x81"), (2, b"\x04"), (3, b"\xff"), (3, b"\x40")],
)
def test_set_padding_bits_are_rejected(length, bitmap):
    with pytest.raises(ValueError, match="bits set past"):
        PropertyBitmaps(bitmaps={length: bitmap})


@pytest.mark.parametrize("length, bitmap", [(0, 1), (3, 1), (4, 3), (5, 15)])
def test_an_int_is_not_a_bitmap(length, bitmap):
    with pytest.raises(TypeError, match="must be bytes"):
        PropertyBitmaps(bitmaps={length: bitmap})


def test_bitmaps_may_be_any_bytes_like():
    # All six permutations of length 3 are good, and the first of length 2
    for bitmap in (b"\x3f", bytearray(b"\x3f"), memoryview(b"\x3f")):
        property_bitmaps = PropertyBitmaps(bitmaps={3: bitmap, 2: b"\x01"})
        assert len(property_bitmaps.good[3]) == 6 and not property_bitmaps.bad[3]
        assert list(property_bitmaps.good[2]) == [Perm((0, 1))]
        assert isinstance(property_bitmaps.bitmaps[3], bytes)


def test_bisc_accepts_property_bitmaps():
    assert bisc(Perm.stack_sortable, 3, 5) == BASIS_231
    assert bisc(property_bitmaps_up_to(Perm.stack_sortable, 5), 3, 5) == BASIS_231


def mined_bitmaps(monkeypatch, A, m, n=None):
    """bisc's answer for A, and the bitmaps of the good permutations it gave
    mine()."""
    mined = {}

    def recording_mine(goodperms, M, N=None, report=False):
        mined.update(goodperms.property_bitmaps.bitmaps)
        return REAL_MINE(goodperms, M, N, report)

    monkeypatch.setattr(bisc_module, "mine", recording_mine)
    return bisc(A, m, n), mined


def test_bisc_turns_each_input_into_bitmaps(monkeypatch):
    bitmaps = {length: encode(Perm.stack_sortable, length) for length in range(6)}
    good_lists = {
        length: [perm for perm in Perm.of_length(length) if perm.stack_sortable()]
        for length in range(6)
    }
    listed = [perm for length in range(6) for perm in good_lists[length]]
    for A in (
        Perm.stack_sortable,
        listed,
        good_lists,
        property_bitmaps_up_to(Perm.stack_sortable, 5),
    ):
        assert mined_bitmaps(monkeypatch, A, 3, 5) == (BASIS_231, bitmaps)
    # A Mapping must have each length up to max(m, n)
    with pytest.raises(KeyError):
        bisc({length: good_lists[length] for length in (0, 1, 3)}, 3)


def test_a_list_sets_the_bits_of_the_permutations_it_lists(monkeypatch):
    # A length with none listed is empty
    _, mined = mined_bitmaps(monkeypatch, [Perm((0,)), Perm((0, 1, 2))], 2, 3)
    assert mined == {0: b"\x00", 1: b"\x01", 2: b"\x00", 3: b"\x01"}
    # A permutation listed twice sets one bit, so (0, 1) is not taken for both
    # permutations of length 2, and the increasing permutations avoid 10
    increasing = [Perm(()), Perm((0,)), Perm((0, 1)), Perm((0, 1)), Perm((0, 1, 2))]
    answer, mined = mined_bitmaps(monkeypatch, increasing, 2, 3)
    assert mined == {0: b"\x01", 1: b"\x01", 2: b"\x01", 3: b"\x01"}
    assert answer == {2: {Perm((1, 0)): [set()]}}


def test_a_property_leaves_the_lengths_past_n_empty(monkeypatch):
    # mine() reads the lengths up to m, and a property labels those up to n; the
    # others are read as empty
    answer, mined = mined_bitmaps(monkeypatch, Perm.stack_sortable, 4, 2)
    assert mined == {
        **{length: encode(Perm.stack_sortable, length) for length in range(3)},
        3: bytes(1),
        4: bytes(3),
    }
    assert answer == {3: {perm: [set()] for perm in Perm.of_length(3)}, 4: {}}


def first_mined_bitmaps(monkeypatch, prop):
    """auto_bisc's answer for prop, and the bitmaps of the good permutations it
    first gave mine()."""
    mined = []

    def recording_mine(goodperms, M, N=None, report=False):
        mined.append(dict(goodperms.property_bitmaps.bitmaps))
        return REAL_MINE(goodperms, M, N, report)

    monkeypatch.setattr(bisc_module, "mine", recording_mine)
    return auto_bisc(prop), mined[0]


def test_auto_bisc_turns_each_input_into_bitmaps(monkeypatch):
    bitmaps = {length: encode(Perm.stack_sortable, length) for length in range(9)}
    good, bad = create_bisc_input(8, Perm.stack_sortable)
    listed = [perm for length in range(9) for perm in good[length]]
    for prop in (
        Perm.stack_sortable,
        listed,
        (good, bad),
        PropertyBitmaps(bitmaps=bitmaps),
    ):
        assert first_mined_bitmaps(monkeypatch, prop) == (BASIS_231, bitmaps)
    answer, mined = first_mined_bitmaps(monkeypatch, "smooth")
    assert answer == {4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [set()]}}
    assert mined == {length: encode(smooth, length) for length in range(9)}


def test_auto_bisc_labels_each_length_of_a_property(monkeypatch):
    added_lengths = []
    real_add_length = PropertyBitmaps.add_length

    def recording_add_length(self, length):
        added_lengths.append(length)
        return real_add_length(self, length)

    monkeypatch.setattr(PropertyBitmaps, "add_length", recording_add_length)
    assert auto_bisc(Perm.stack_sortable) == BASIS_231
    assert added_lengths == list(range(9))


def test_the_good_and_bad_of_a_tuple_must_split_each_length():
    good, bad = create_bisc_input(8, Perm.stack_sortable)
    missing_one = {**bad, 5: bad[5][1:]}
    with pytest.raises(ValueError, match=r"length 5 .* \(in both: 0, in neither: 1\)"):
        auto_bisc((good, missing_one))
    in_both = {**bad, 4: bad[4] + good[4][:1]}
    with pytest.raises(ValueError, match=r"length 4 .* \(in both: 1, in neither: 0\)"):
        auto_bisc((good, in_both))


def test_the_stored_sets_give_each_permutation_once():
    folder = "permuta/resources/bisc/"
    for file_name in sorted(os.listdir(folder)):
        if "_good_len" in file_name:
            good_name = file_name[: -len(".json")]
            good = read_bisc_file(folder + good_name)
            bad = read_bisc_file(folder + good_name.replace("_good_", "_bad_"))
            property_bitmaps = bisc_module._from_good_and_bad(good, bad)
            longest_length = int(good_name.rsplit("len", 1)[1])
            assert sorted(property_bitmaps.bitmaps) == list(range(longest_length + 1))


def test_auto_bisc_property_bitmaps_input():
    assert auto_bisc(property_bitmaps_up_to(Perm.stack_sortable, 8)) == BASIS_231
    # Given bitmaps and no property: the lengths auto_bisc needs must be there
    bitmaps = property_bitmaps_up_to(Perm.stack_sortable, 8).bitmaps
    assert auto_bisc(PropertyBitmaps(bitmaps=bitmaps)) == BASIS_231
    too_short = {length: bitmaps[length] for length in range(6)}
    assert auto_bisc(PropertyBitmaps(bitmaps=too_short)) is None


def encode(prop, length):
    """A length's bitmap made without PropertyBitmaps: bit i of the little-endian
    integer is the label of Perm.unrank(i, length)."""
    label_bits = sum(
        1 << i for i in range(factorial(length)) if prop(Perm.unrank(i, length))
    )
    return label_bits.to_bytes((factorial(length) + 7) // 8, "little")


def test_auto_bisc_labels_only_missing_lengths_with_the_property():
    labeled_lengths = []

    def prop(perm):
        labeled_lengths.append(len(perm))
        return perm.stack_sortable()

    given_lengths = (0, 1, 2, 3, 5, 8)
    property_bitmaps = PropertyBitmaps(
        prop,
        bitmaps={
            length: encode(Perm.stack_sortable, length) for length in given_lengths
        },
    )
    assert auto_bisc(property_bitmaps) == BASIS_231
    assert set(labeled_lengths) == {4, 6, 7}
    assert sorted(property_bitmaps.bitmaps) == list(range(9))


def test_bisc_labels_missing_lengths_with_the_property():
    # Without n, bisc uses the longest length labeled, or 7 when there is none
    assert bisc(property_bitmaps_up_to(Perm.stack_sortable, 5), 3) == BASIS_231
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable)
    assert bisc(property_bitmaps, 3, 5) == BASIS_231
    assert sorted(property_bitmaps.bitmaps) == list(range(6))
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable)
    assert bisc(property_bitmaps, 3) == BASIS_231
    assert sorted(property_bitmaps.bitmaps) == list(range(8))


def test_bisc_needs_bitmaps_or_a_property():
    bitmaps = {length: encode(Perm.stack_sortable, length) for length in range(4)}
    with pytest.raises(ValueError, match="none of length 4 and no property"):
        bisc(PropertyBitmaps(bitmaps=bitmaps), 3, 5)
    with pytest.raises(ValueError, match="no bitmaps and no property"):
        bisc(PropertyBitmaps(), 3)


def test_add_length_needs_a_property():
    property_bitmaps = PropertyBitmaps(bitmaps={0: b"\x01"})
    with pytest.raises(ValueError, match="no property to label length 3 with"):
        property_bitmaps.add_length(3)
    assert sorted(property_bitmaps.bitmaps) == [0]


def test_bisc_without_n_uses_the_longest_labeled_length_with_no_property():
    bitmaps = {length: encode(Perm.stack_sortable, length) for length in range(6)}
    assert bisc(PropertyBitmaps(bitmaps=bitmaps), 3) == BASIS_231


def test_bisc_labels_only_the_missing_lengths():
    labeled_lengths = []

    def prop(perm):
        labeled_lengths.append(len(perm))
        return perm.stack_sortable()

    given_lengths = (0, 1, 2, 3, 5)
    property_bitmaps = PropertyBitmaps(
        prop,
        bitmaps={
            length: encode(Perm.stack_sortable, length) for length in given_lengths
        },
    )
    assert bisc(property_bitmaps, 3) == BASIS_231
    assert labeled_lengths == [4] * factorial(4)
    assert sorted(property_bitmaps.bitmaps) == list(range(6))
    assert bisc(property_bitmaps, 3, 5) == BASIS_231
    assert labeled_lengths == [4] * factorial(4)


def test_bisc_labels_up_to_the_pattern_length():
    # mine() reads the lengths up to m, so bisc labels up to m when n < m
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable)
    bisc(property_bitmaps, 3, 0)
    assert sorted(property_bitmaps.bitmaps) == [0, 1, 2, 3]
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable, bitmaps={0: b"\x01"})
    bisc(property_bitmaps, 3)
    assert sorted(property_bitmaps.bitmaps) == [0, 1, 2, 3]
    with pytest.raises(ValueError, match="none of length 1 and no property"):
        bisc(PropertyBitmaps(bitmaps={0: b"\x01"}), 3)


def test_bisc_accepts_the_views():
    assert bisc(property_bitmaps_up_to(Perm.stack_sortable, 5).good, 3) == BASIS_231


def test_west_2_stack_sortable():
    assert auto_bisc(Perm.west_2_stack_sortable) == BASIS_WEST_2


def derangement_in_av_213_231_312(perm):
    """One member at each even length, none at odd: auto_bisc keeps learning longer
    patterns while each step stays cheap, so it soon needs more labels."""
    return perm.avoids(Perm((1, 0, 2)), Perm((1, 2, 0)), Perm((2, 0, 1))) and all(
        value != index for index, value in enumerate(perm)
    )


def test_auto_bisc_stops_without_bitmaps_it_needs():
    # Bitmaps up to length 8 and no property: auto_bisc needs length 9 and stops
    bitmaps = property_bitmaps_up_to(derangement_in_av_213_231_312, 8).bitmaps
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        assert auto_bisc(PropertyBitmaps(bitmaps=bitmaps)) is None
    assert "You need to add bitmaps of longer permutations" in output.getvalue()


class ReachedLength9(Exception):
    pass


def test_auto_bisc_labels_new_lengths_from_the_property():
    # When auto_bisc grows past the labeled lengths, it labels the new ones with
    # the property: here it is stopped at the first permutation of length 9
    def prop(perm):
        if len(perm) == 9:
            raise ReachedLength9
        return derangement_in_av_213_231_312(perm)

    output = io.StringIO()
    with contextlib.redirect_stdout(output), pytest.raises(ReachedLength9):
        auto_bisc(prop)
    assert "Adding perms of length 9" in output.getvalue()


def test_a_list_of_tuples_is_read_as_permutations():
    # Tuples are read as the permutations they are, as they always were
    perms = [
        perm
        for length in range(6)
        for perm in Perm.of_length(length)
        if perm.stack_sortable()
    ]
    assert bisc([tuple(perm) for perm in perms], 3, 5) == bisc(perms, 3, 5)


def test_a_permutation_under_the_wrong_length_is_refused():
    with pytest.raises(ValueError, match="length 3 is given as one of length 2"):
        bisc({0: [Perm(())], 1: [Perm((0,))], 2: [Perm((0, 1, 2))]}, 2)


def test_a_tuple_may_lack_a_length_in_one_dictionary(monkeypatch):
    # A length one dictionary lacks is empty in it: here no permutation of
    # length 0 is good
    good, bad = create_bisc_input(8, Perm.stack_sortable)
    good = {length: perms for length, perms in good.items() if perms}
    bad = dict(bad)
    bad[0] = bad.get(0, []) + good.pop(0, [])
    given = []

    class MineCalled(Exception):
        pass

    def recording_mine(goodperms, M, N=None, report=False):
        given.append({length: list(goodperms[length]) for length in goodperms})
        raise MineCalled

    monkeypatch.setattr(bisc_module, "mine", recording_mine)
    with pytest.raises(MineCalled):
        auto_bisc((good, bad))
    assert given[0][0] == []
    assert given[0][3] == [perm for perm in Perm.of_length(3) if perm.stack_sortable()]
