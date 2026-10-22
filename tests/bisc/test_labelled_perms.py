import contextlib
import io
from math import factorial

import pytest

from permuta.bisc.bisc import LabelledPerms, auto_bisc, bisc
from permuta.patterns.perm import Perm

BASIS_231 = {3: {Perm((1, 2, 0)): [set()]}}


def labelled_up_to(prop, max_length):
    labelled_perms = LabelledPerms(prop)
    for length in range(max_length + 1):
        labelled_perms.add_length(length)
    return labelled_perms


def test_views_match_lists():
    labelled_perms = labelled_up_to(Perm.stack_sortable, 6)
    for length in range(7):
        good = [perm for perm in Perm.of_length(length) if perm.stack_sortable()]
        bad = [perm for perm in Perm.of_length(length) if not perm.stack_sortable()]
        assert list(labelled_perms.good[length]) == good
        assert list(labelled_perms.bad[length]) == bad
        assert len(labelled_perms.good[length]) == len(good)
        assert len(labelled_perms.bad[length]) == len(bad)
        assert bool(labelled_perms.bad[length]) == bool(bad)
    assert sorted(labelled_perms.good.keys()) == list(range(7))
    assert 6 in labelled_perms.bad and 7 not in labelled_perms.bad
    with pytest.raises(KeyError):
        _ = labelled_perms.good[7]


def test_bit_order_is_perm_unrank():
    # Bit i of a length's bitmap is the label of Perm.unrank(i, length), and the
    # permutation perm is at bit perm.rank() minus the number of shorter
    # permutations
    labelled_perms = labelled_up_to(Perm.stack_sortable, 6)
    shorter_count = 0
    for length in range(7):
        bitmap = labelled_perms.bitmaps[length]
        for i in range(factorial(length)):
            perm = Perm.unrank(i, length)
            assert perm.rank() - shorter_count == i
            assert bool(bitmap[i >> 3] >> (i & 7) & 1) == perm.stack_sortable()
        shorter_count += factorial(length)


def test_bitmaps_round_trip():
    labelled_perms = labelled_up_to(Perm.stack_sortable, 6)
    round_trip = LabelledPerms(bitmaps=labelled_perms.bitmaps)
    for length in range(7):
        assert list(round_trip.good[length]) == list(labelled_perms.good[length])
        assert list(round_trip.bad[length]) == list(labelled_perms.bad[length])
    with pytest.raises(ValueError):
        LabelledPerms(bitmaps={3: b"\x00\x00"})  # 3! bits fit in one byte


@pytest.mark.parametrize(
    "length, bitmap",
    [(0, b"\x03"), (1, b"\x81"), (2, b"\x04"), (3, b"\xff"), (3, b"\x40")],
)
def test_set_padding_bits_are_rejected(length, bitmap):
    with pytest.raises(ValueError):
        LabelledPerms(bitmaps={length: bitmap})


@pytest.mark.parametrize("length, bitmap", [(0, 1), (3, 1), (4, 3), (5, 15)])
def test_an_int_is_not_a_bitmap(length, bitmap):
    with pytest.raises(TypeError):
        LabelledPerms(bitmaps={length: bitmap})


def test_bitmaps_may_be_any_bytes_like():
    # All six permutations of length 3 are good, and the first of length 2
    for bitmap in (b"\x3f", bytearray(b"\x3f"), memoryview(b"\x3f")):
        labelled_perms = LabelledPerms(bitmaps={3: bitmap, 2: b"\x01"})
        assert len(labelled_perms.good[3]) == 6 and not labelled_perms.bad[3]
        assert list(labelled_perms.good[2]) == [Perm((0, 1))]
        assert isinstance(labelled_perms.bitmaps[3], bytes)


def test_bisc_accepts_labelled_perms():
    assert bisc(Perm.stack_sortable, 3, 5) == BASIS_231
    assert bisc(labelled_up_to(Perm.stack_sortable, 5), 3, 5) == BASIS_231


def test_auto_bisc_labels_option():
    assert auto_bisc(Perm.stack_sortable) == BASIS_231
    assert auto_bisc(Perm.stack_sortable, labels="lists") == BASIS_231
    assert auto_bisc(Perm.stack_sortable, labels="bitmaps") == BASIS_231
    with pytest.raises(ValueError):
        auto_bisc(Perm.stack_sortable, labels="sets")


def test_labels_option_selects_the_representation(monkeypatch):
    # The results are the same either way, so record which lengths are kept as
    # bitmaps: none for lists, every length checked for bitmaps
    added_lengths = []
    real_add_length = LabelledPerms.add_length

    def recording_add_length(self, length):
        added_lengths.append(length)
        return real_add_length(self, length)

    monkeypatch.setattr(LabelledPerms, "add_length", recording_add_length)
    assert auto_bisc(Perm.stack_sortable) == BASIS_231
    assert auto_bisc(Perm.stack_sortable, labels="lists") == BASIS_231
    assert added_lengths == []
    assert auto_bisc(Perm.stack_sortable, labels="bitmaps") == BASIS_231
    assert added_lengths == list(range(9))


def test_auto_bisc_labelled_perms_input():
    assert auto_bisc(labelled_up_to(Perm.stack_sortable, 8)) == BASIS_231
    # Given bitmaps and no property: the lengths auto_bisc needs must be there
    bitmaps = labelled_up_to(Perm.stack_sortable, 8).bitmaps
    assert auto_bisc(LabelledPerms(bitmaps=bitmaps)) == BASIS_231
    too_short = {length: bitmaps[length] for length in range(6)}
    assert auto_bisc(LabelledPerms(bitmaps=too_short)) is None


def encode(prop, length):
    """A length's bitmap made without LabelledPerms: bit i of the little-endian
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
    labelled_perms = LabelledPerms(
        prop,
        bitmaps={
            length: encode(Perm.stack_sortable, length) for length in given_lengths
        },
    )
    assert auto_bisc(labelled_perms) == BASIS_231
    assert set(labelled_lengths) == {4, 6, 7}
    assert sorted(labelled_perms.bitmaps) == list(range(9))


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
    bitmaps = labelled_up_to(derangement_in_av_213_231_312, 8).bitmaps
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        assert auto_bisc(LabelledPerms(bitmaps=bitmaps)) is None
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
