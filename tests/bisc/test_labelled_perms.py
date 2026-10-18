import pytest

from permuta.bisc.bisc import LabelledPerms, auto_bisc, bisc
from permuta.patterns.perm import Perm


def stack_sortable(perm):
    return perm.avoids(Perm((1, 2, 0)))


def labelled(prop, top):
    labels = LabelledPerms(prop)
    for n in range(top + 1):
        labels.add_length(n)
    return labels


def test_views_match_lists():
    labels = labelled(stack_sortable, 6)
    for n in range(7):
        good = [perm for perm in Perm.of_length(n) if stack_sortable(perm)]
        bad = [perm for perm in Perm.of_length(n) if not stack_sortable(perm)]
        assert list(labels.good[n]) == good
        assert list(labels.bad[n]) == bad
        assert len(labels.good[n]) == len(good)
        assert len(labels.bad[n]) == len(bad)
        assert bool(labels.bad[n]) == bool(bad)
    assert sorted(labels.good.keys()) == list(range(7))
    assert 6 in labels.bad and 7 not in labels.bad
    with pytest.raises(KeyError):
        _ = labels.good[7]


def test_bitmaps_round_trip():
    labels = labelled(stack_sortable, 6)
    again = LabelledPerms(bitmaps=labels.bits)
    for n in range(7):
        assert list(again.good[n]) == list(labels.good[n])
        assert list(again.bad[n]) == list(labels.bad[n])
    with pytest.raises(ValueError):
        LabelledPerms(bitmaps={3: b"\x00\x00"})  # 3! bits fit in one byte


def test_bisc_accepts_labelled_perms():
    expected = {3: {Perm((1, 2, 0)): [set()]}}
    assert bisc(stack_sortable, 3, 5) == expected
    assert bisc(labelled(stack_sortable, 5), 3, 5) == expected


def test_auto_bisc_labels_option():
    expected = {3: {Perm((1, 2, 0)): [set()]}}
    assert auto_bisc(stack_sortable) == expected
    assert auto_bisc(stack_sortable, labels="lists") == expected
    assert auto_bisc(stack_sortable, labels="bitmaps") == expected
    with pytest.raises(ValueError):
        auto_bisc(stack_sortable, labels="sets")


def test_auto_bisc_labelled_perms_input():
    expected = {3: {Perm((1, 2, 0)): [set()]}}
    assert auto_bisc(labelled(stack_sortable, 8)) == expected
    # Given bitmaps and no property: the lengths auto_bisc needs must be there
    bits = labelled(stack_sortable, 8).bits
    assert auto_bisc(LabelledPerms(bitmaps=bits)) == expected
    short = {n: bits[n] for n in range(6)}
    assert auto_bisc(LabelledPerms(bitmaps=short)) is None


def test_west_2_stack_sortable_same_as_lists():
    def west_2(perm):
        def stack_sort(word):
            out, stack = [], []
            for x in word:
                while stack and stack[-1] < x:
                    out.append(stack.pop())
                stack.append(x)
            return out + stack[::-1]

        return stack_sort(stack_sort(list(perm))) == sorted(perm)

    assert auto_bisc(west_2, labels="bitmaps") == auto_bisc(west_2)
