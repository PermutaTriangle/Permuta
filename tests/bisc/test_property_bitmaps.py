import contextlib
import io
from collections.abc import Collection, Mapping
from math import factorial

import pytest

from permuta.bisc.bisc import PropertyBitmaps, auto_bisc, bisc
from permuta.patterns.perm import Perm

BASIS_231 = {3: {Perm((1, 2, 0)): [set()]}}


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
    with pytest.raises(ValueError, match="wrong size"):
        PropertyBitmaps(bitmaps={3: b"\x00\x00"})  # 3! bits fit in one byte
    with pytest.raises(ValueError, match="wrong size"):
        PropertyBitmaps(bitmaps={3: b""})


def test_lengths_0_and_1_labelled_bad():
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


def test_auto_bisc_labels_option():
    assert auto_bisc(Perm.stack_sortable) == BASIS_231
    assert auto_bisc(Perm.stack_sortable, labels="lists") == BASIS_231
    assert auto_bisc(Perm.stack_sortable, labels="bitmaps") == BASIS_231
    with pytest.raises(ValueError, match="labels must be"):
        auto_bisc(Perm.stack_sortable, labels="sets")


def test_labels_option_selects_the_representation(monkeypatch):
    # The results are the same either way, so record which lengths are kept as
    # bitmaps: none for lists, every length checked for bitmaps
    added_lengths = []
    real_add_length = PropertyBitmaps.add_length

    def recording_add_length(self, length):
        added_lengths.append(length)
        return real_add_length(self, length)

    monkeypatch.setattr(PropertyBitmaps, "add_length", recording_add_length)
    assert auto_bisc(Perm.stack_sortable) == BASIS_231
    assert auto_bisc(Perm.stack_sortable, labels="lists") == BASIS_231
    assert added_lengths == []
    assert auto_bisc(Perm.stack_sortable, labels="bitmaps") == BASIS_231
    assert added_lengths == list(range(9))


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
    labelled_lengths = []

    def prop(perm):
        labelled_lengths.append(len(perm))
        return perm.stack_sortable()

    given_lengths = (0, 1, 2, 3, 5, 8)
    property_bitmaps = PropertyBitmaps(
        prop,
        bitmaps={
            length: encode(Perm.stack_sortable, length) for length in given_lengths
        },
    )
    assert auto_bisc(property_bitmaps) == BASIS_231
    assert set(labelled_lengths) == {4, 6, 7}
    assert sorted(property_bitmaps.bitmaps) == list(range(9))


def test_bisc_labels_missing_lengths_with_the_property():
    # Without n, bisc uses the longest length labelled, or 7 when there is none
    assert bisc(property_bitmaps_up_to(Perm.stack_sortable, 5), 3) == BASIS_231
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable)
    assert bisc(property_bitmaps, 3, 5) == BASIS_231
    assert sorted(property_bitmaps.bitmaps) == list(range(6))
    property_bitmaps = PropertyBitmaps(Perm.stack_sortable)
    assert bisc(property_bitmaps, 3) == BASIS_231
    assert sorted(property_bitmaps.bitmaps) == list(range(8))


def test_bisc_needs_labels_or_a_property():
    bitmaps = {length: encode(Perm.stack_sortable, length) for length in range(4)}
    with pytest.raises(ValueError, match="none of length 4 and no property"):
        bisc(PropertyBitmaps(bitmaps=bitmaps), 3, 5)
    with pytest.raises(ValueError, match="no labels and no property"):
        bisc(PropertyBitmaps(), 3)


def test_bisc_without_n_uses_the_longest_labelled_length_with_no_property():
    bitmaps = {length: encode(Perm.stack_sortable, length) for length in range(6)}
    assert bisc(PropertyBitmaps(bitmaps=bitmaps), 3) == BASIS_231


def test_bisc_labels_only_the_missing_lengths():
    labelled_lengths = []

    def prop(perm):
        labelled_lengths.append(len(perm))
        return perm.stack_sortable()

    given_lengths = (0, 1, 2, 3, 5)
    property_bitmaps = PropertyBitmaps(
        prop,
        bitmaps={
            length: encode(Perm.stack_sortable, length) for length in given_lengths
        },
    )
    assert bisc(property_bitmaps, 3) == BASIS_231
    assert labelled_lengths == [4] * factorial(4)
    assert sorted(property_bitmaps.bitmaps) == list(range(6))
    assert bisc(property_bitmaps, 3, 5) == BASIS_231
    assert labelled_lengths == [4] * factorial(4)


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


def test_bitmaps_need_a_property():
    for prop in ([Perm((0,))], ({}, {}), "yt_perm_avoids_22"):
        with pytest.raises(ValueError, match="needs a property"):
            auto_bisc(prop, labels="bitmaps")
    property_bitmaps = property_bitmaps_up_to(Perm.stack_sortable, 8)
    assert auto_bisc(property_bitmaps, labels="bitmaps") == BASIS_231


def test_west_2_stack_sortable_same_as_lists():
    assert auto_bisc(Perm.west_2_stack_sortable, labels="bitmaps") == auto_bisc(
        Perm.west_2_stack_sortable
    )


def derangement_in_av_213_231_312(perm):
    """One member at each even length, none at odd: auto_bisc keeps learning longer
    patterns while each step stays cheap, so it soon needs more labels."""
    return perm.avoids(Perm((1, 0, 2)), Perm((1, 2, 0)), Perm((2, 0, 1))) and all(
        value != index for index, value in enumerate(perm)
    )


def test_auto_bisc_stops_without_labels_it_needs():
    # Bitmaps up to length 8 and no property: auto_bisc needs length 9 and stops
    bitmaps = property_bitmaps_up_to(derangement_in_av_213_231_312, 8).bitmaps
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        assert auto_bisc(PropertyBitmaps(bitmaps=bitmaps)) is None
    assert "You need to add labels of longer permutations" in output.getvalue()


class ReachedLength9(Exception):
    pass


def test_auto_bisc_labels_new_lengths_from_the_property():
    # When auto_bisc grows past the labelled lengths, it labels the new ones with
    # the property; stopped at the first permutation of length 9, both approaches
    # have printed the same
    def prop(perm):
        if len(perm) == 9:
            raise ReachedLength9
        return derangement_in_av_213_231_312(perm)

    outputs = []
    for labels in ("lists", "bitmaps"):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), pytest.raises(ReachedLength9):
            auto_bisc(prop, labels=labels)
        outputs.append(output.getvalue())
    assert outputs[0] == outputs[1]
    assert "Adding perms of length 9" in outputs[1]
