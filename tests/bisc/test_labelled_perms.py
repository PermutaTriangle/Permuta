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


def test_bisc_accepts_labelled_perms():
    assert bisc(Perm.stack_sortable, 3, 5) == BASIS_231
    assert bisc(labelled_up_to(Perm.stack_sortable, 5), 3, 5) == BASIS_231


def test_auto_bisc_labels_option():
    assert auto_bisc(Perm.stack_sortable) == BASIS_231
    assert auto_bisc(Perm.stack_sortable, labels="lists") == BASIS_231
    assert auto_bisc(Perm.stack_sortable, labels="bitmaps") == BASIS_231
    with pytest.raises(ValueError):
        auto_bisc(Perm.stack_sortable, labels="sets")


def test_auto_bisc_labelled_perms_input():
    assert auto_bisc(labelled_up_to(Perm.stack_sortable, 8)) == BASIS_231
    # Given bitmaps and no property: the lengths auto_bisc needs must be there
    bitmaps = labelled_up_to(Perm.stack_sortable, 8).bitmaps
    assert auto_bisc(LabelledPerms(bitmaps=bitmaps)) == BASIS_231
    too_short = {length: bitmaps[length] for length in range(6)}
    assert auto_bisc(LabelledPerms(bitmaps=too_short)) is None


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
