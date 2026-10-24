"""The two forms in which a PropertyBitmaps keeps a length's labels: its bitmap,
or the sorted indices of its good permutations when fewer than one in
_SPARSE_WHEN_ONE_IN is good. Each way in chooses the form by the number of good
permutations, and every view reads both forms."""

import importlib
import random
from array import array
from math import factorial

import pytest

from permuta.bisc.bisc import PropertyBitmaps, bisc
from permuta.patterns.perm import Perm

# The module, which permuta.bisc's function bisc hides
bisc_module = importlib.import_module("permuta.bisc.bisc")

MAX_LENGTH = 8


def expected_bitmap(length, good_set):
    """A length's bitmap with the bits of the permutations in good_set set, made
    without PropertyBitmaps."""
    label_bits = sum(
        1 << index
        for index, perm in enumerate(Perm.of_length(length))
        if perm in good_set
    )
    return label_bits.to_bytes((factorial(length) + 7) // 8, "little")


def is_kept_as_indices(property_bitmaps, length):
    return isinstance(property_bitmaps._labels[length], (array, list))


def assert_views_match(property_bitmaps, length, good_set, bitmap=None):
    """Every view of a length against brute force: iteration and its order,
    len(), in, the bad view, the count and the bitmap."""
    perms = list(Perm.of_length(length))
    good = [perm for perm in perms if perm in good_set]
    bad = [perm for perm in perms if perm not in good_set]
    good_view, bad_view = property_bitmaps.good[length], property_bitmaps.bad[length]
    assert list(good_view) == good
    assert list(bad_view) == bad
    assert len(good_view) == len(good) and len(bad_view) == len(bad)
    # in, for every permutation up to length 6, and for every seventh good and
    # bad one at lengths 7 and 8
    step = 1 if length < 7 else 7
    for perm in good[::step] + bad[::step]:
        assert (perm in good_view) == (perm in good_set)
        assert (perm in bad_view) == (perm not in good_set)
    assert property_bitmaps.good_counts[length] == len(good)
    if bitmap is None:
        bitmap = expected_bitmap(length, good_set)
    assert property_bitmaps.bitmaps[length] == bitmap


def each_way_in(good_sets, bitmaps, randomness):
    """A PropertyBitmaps made from good_sets in each way that bisc and auto_bisc
    make one, with its name: a list or a mapping (whose good permutations come
    shuffled, with some twice), a tuple of the good and the bad, bitmaps, and a
    property."""
    lengths = range(MAX_LENGTH + 1)
    good_lists, bad_lists = {}, {}
    for length in lengths:
        good_lists[length] = sorted(good_sets[length])
        randomness.shuffle(good_lists[length])
        bad_lists[length] = [
            perm for perm in Perm.of_length(length) if perm not in good_sets[length]
        ]
    listed_twice = {
        length: good_lists[length] + good_lists[length][:3] for length in lengths
    }
    yield "list or mapping", bisc_module._from_perms_by_length(listed_twice)
    yield "tuple", bisc_module._from_good_and_bad(good_lists, bad_lists)
    yield "bitmaps", PropertyBitmaps(bitmaps=bitmaps)
    by_property = PropertyBitmaps(lambda perm: perm in good_sets[len(perm)])
    for length in lengths:
        by_property.add_length(length)
    yield "property", by_property


def first_dense_count(length, sparse_when_one_in):
    """The fewest good permutations of a length that are kept as a bitmap."""
    return -(-factorial(length) // sparse_when_one_in)


SIZE_KINDS = (
    "none",
    "just under the threshold",
    "at the threshold",
    "all",
    "random under",
    "random over",
)


def good_count_of(size_kind, length, sparse_when_one_in, randomness):
    first_dense = min(first_dense_count(length, sparse_when_one_in), factorial(length))
    return {
        "none": 0,
        "just under the threshold": max(first_dense - 1, 0),
        "at the threshold": first_dense,
        "all": factorial(length),
        "random under": randomness.randint(0, max(first_dense - 1, 0)),
        "random over": randomness.randint(first_dense, factorial(length)),
    }[size_kind]


# Both forms against brute force, for every view and every way in, at lengths 0
# to 8. With one in 2, both forms occur at every length from 2 on; with one in
# 64, the default, from 5 on. The bitmaps are read seven bytes at a time, so that
# counting them takes several chunks
@pytest.mark.parametrize("sparse_when_one_in", [2, 64])
@pytest.mark.parametrize("size_kind", SIZE_KINDS)
def test_both_forms_read_as_brute_force(monkeypatch, sparse_when_one_in, size_kind):
    monkeypatch.setattr(bisc_module, "_SPARSE_WHEN_ONE_IN", sparse_when_one_in)
    monkeypatch.setattr(bisc_module, "_CHUNK_BYTES", 7)
    randomness = random.Random(f"{sparse_when_one_in} {size_kind}")
    good_sets, bitmaps = {}, {}
    for length in range(MAX_LENGTH + 1):
        good_count = good_count_of(size_kind, length, sparse_when_one_in, randomness)
        perms = list(Perm.of_length(length))
        good_sets[length] = set(randomness.sample(perms, good_count))
        bitmaps[length] = expected_bitmap(length, good_sets[length])
    for way, property_bitmaps in each_way_in(good_sets, bitmaps, randomness):
        for length in range(MAX_LENGTH + 1):
            good_count = len(good_sets[length])
            kept_as_indices = good_count * sparse_when_one_in < factorial(length)
            assert is_kept_as_indices(property_bitmaps, length) == kept_as_indices, (
                way,
                length,
            )
            assert_views_match(
                property_bitmaps, length, good_sets[length], bitmaps[length]
            )


# add_length keeps the indices while they are few, and switches to a bitmap in
# the middle of a length once they would take as much space. Length 7 has 5040
# permutations, so its 79th good one makes them as many as one in 64
@pytest.mark.parametrize(
    "good_indices",
    [
        range(5040),  # all, the switch at the 79th
        range(4800, 5040),  # good from a point on, the switch late in the length
        range(4961, 5040),  # 79 good, the switch at the last permutation
        range(4962, 5040),  # 78 good, kept as indices
        range(0, 5040, 50),  # 101 spread out, the switch at index 3900
        range(5039, 5040),  # one good
        range(0),  # none
    ],
)
def test_add_length_switches_to_a_bitmap_when_the_good_become_many(good_indices):
    length = 7
    perms = list(Perm.of_length(length))
    good_set = {perms[index] for index in good_indices}
    property_bitmaps = PropertyBitmaps(lambda perm: perm in good_set)
    property_bitmaps.add_length(length)
    kept_as_indices = len(good_set) * 64 < factorial(length)
    assert is_kept_as_indices(property_bitmaps, length) == kept_as_indices
    assert_views_match(property_bitmaps, length, good_set)


# A permutation listed many times counts once, for the form too
def test_a_permutation_listed_many_times_is_kept_as_one_index():
    # Five copies of one permutation of length 5 look like 5 of its 120, which a
    # bitmap would keep at one in 64, but they are one good permutation
    perm = Perm((1, 0, 2, 3, 4))
    property_bitmaps = bisc_module._from_perms_by_length({5: [perm] * 5})
    assert is_kept_as_indices(property_bitmaps, 5)
    assert_views_match(property_bitmaps, 5, {perm})


def tuple_of(good_8, bad_8):
    """A tuple of the good and the bad permutations: every permutation shorter
    than 8 good, and those given at length 8."""
    good = {length: list(Perm.of_length(length)) for length in range(8)}
    bad = {length: [] for length in range(8)}
    return {**good, 8: good_8}, {**bad, 8: bad_8}


# The good and the bad permutations of a tuple are checked in every pair of
# forms: the good kept as indices or as a bitmap, and the bad as well
@pytest.mark.parametrize(
    "good_8, bad_8, in_both, in_neither",
    [
        (slice(0, 5), slice(3, None), 2, 0),  # indices, bitmap
        (slice(0, 40000), slice(39990, 40010), 10, 310),  # bitmap, indices
        (slice(0, 20000), slice(19990, None), 10, 0),  # bitmap, bitmap
        (slice(0, 5), slice(3, 8), 2, 40312),  # indices, indices
    ],
)
def test_a_tuple_is_checked_in_every_pair_of_forms(
    monkeypatch, good_8, bad_8, in_both, in_neither
):
    monkeypatch.setattr(bisc_module, "_CHUNK_BYTES", 7)
    perms = list(Perm.of_length(8))
    good, bad = tuple_of(perms[good_8], perms[bad_8])
    with pytest.raises(
        ValueError,
        match=r"length 8 .* \(in both: {}, in neither: {}\)".format(
            in_both, in_neither
        ),
    ):
        bisc_module._from_good_and_bad(good, bad)


# Asking whether a length is there, or reading its good permutations, does not
# build the bitmap of a length kept as indices
def test_a_length_kept_as_indices_builds_no_bitmap_unless_asked(monkeypatch):
    identity = Perm(range(10))
    property_bitmaps = bisc_module._from_perms_by_length({10: [identity]})
    built = []
    real_bitmap_from_indices = bisc_module._bitmap_from_indices

    def recording_bitmap_from_indices(length, indices):
        built.append(length)
        return real_bitmap_from_indices(length, indices)

    monkeypatch.setattr(
        bisc_module, "_bitmap_from_indices", recording_bitmap_from_indices
    )
    assert 10 in property_bitmaps.bitmaps and 9 not in property_bitmaps.bitmaps
    assert list(property_bitmaps.bitmaps) == [10] and len(property_bitmaps.bitmaps) == 1
    assert list(property_bitmaps.good[10]) == [identity]
    assert identity in property_bitmaps.good[10]
    assert Perm(range(9, -1, -1)) in property_bitmaps.bad[10]
    assert len(property_bitmaps.bad[10]) == factorial(10) - 1
    assert built == []
    assert property_bitmaps.bitmaps[10] == b"\x01" + bytes(453599)
    assert built == [10]


THREE_OF_LENGTH_14 = [
    Perm((1, 9, 11, 10, 8, 3, 4, 5, 2, 6, 0, 7, 13, 12)),
    Perm((7, 10, 6, 11, 1, 4, 3, 12, 2, 5, 8, 9, 0, 13)),
    Perm((8, 10, 12, 4, 2, 0, 1, 13, 11, 9, 6, 3, 7, 5)),
]
# bisc(THREE_OF_LENGTH_14, 2, 14) on develop, before PropertyBitmaps
DEVELOP_ANSWER_14 = {
    0: {Perm(()): [{(0, 0)}]},
    1: {Perm((0,)): [{(0, 1), (1, 0), (0, 0)}, {(1, 1), (0, 0)}]},
    2: {
        Perm((0, 1)): [
            {(0, 1), (0, 2), (1, 2), (2, 1), (0, 0), (1, 1)},
            {(0, 1), (0, 2), (1, 2), (2, 1), (1, 0)},
            {(0, 1), (1, 2), (2, 2), (0, 0), (1, 1)},
            {(0, 1), (0, 2), (0, 0), (1, 1), (2, 0)},
            {(0, 1), (1, 0), (0, 2), (2, 0)},
            {(0, 1), (1, 0), (2, 2)},
        ],
        Perm((1, 0)): [
            {(0, 1), (1, 2), (2, 1), (0, 0), (1, 0)},
            {(0, 2), (1, 2), (0, 0), (1, 1), (2, 0)},
            {(0, 2), (1, 2), (2, 1), (0, 0), (1, 1)},
            {(0, 1), (0, 2), (1, 2), (0, 0)},
            {(2, 0), (1, 1), (2, 2), (0, 0)},
            {(1, 0), (2, 2), (0, 0)},
            {(1, 2), (2, 2), (0, 0)},
        ],
    },
}


def shadings_as_sets(answer):
    """bisc's answer with each pattern's shadings as a set, whose order the
    Python may change."""
    return {
        length: {
            pattern: {frozenset(shading) for shading in shadings}
            for pattern, shadings in patterns.items()
        }
        for length, patterns in answer.items()
    }


# Three permutations of length 14 run in megabytes: each length up to 14 is kept
# as indices, where the bitmap of length 14 alone would take 10.9 GB
def test_three_permutations_of_length_14_take_little_memory():
    # tracemalloc is CPython's
    tracemalloc = pytest.importorskip("tracemalloc")
    tracemalloc.start()
    try:
        answer = bisc(THREE_OF_LENGTH_14, 2, 14)
        peak_bytes = tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()
    assert peak_bytes < 2**20
    assert shadings_as_sets(answer) == shadings_as_sets(DEVELOP_ANSWER_14)


@pytest.mark.parametrize("length", [20, 21, 25])
def test_the_last_permutation_of_a_long_length_can_be_listed(length):
    """The decreasing permutation of a length, whose index is its largest. 21! is
    above 2**64, so past length 20 the indices are kept in a list."""
    last = Perm(range(length - 1, -1, -1))
    property_bitmaps = bisc_module._from_perms_by_length({length: [last]})
    assert list(property_bitmaps.good[length]) == [last]
    assert last in property_bitmaps.good[length]
    assert last not in property_bitmaps.bad[length]
    assert property_bitmaps.good_counts[length] == 1
    kept_in = array if length <= 20 else list
    assert isinstance(property_bitmaps._labels[length], kept_in)


def test_a_permutation_of_length_21_whose_index_needs_the_top_bit():
    """An index from 2**63 to 2**64, which an unsigned 64-bit integer holds and
    a signed one does not."""
    perm = Perm.unrank(2**63 + 5, 21)
    assert perm.rank() - bisc_module._shorter_count(21) == 2**63 + 5
    property_bitmaps = bisc_module._from_perms_by_length({21: [perm]})
    assert list(property_bitmaps.good[21]) == [perm]
    assert perm in property_bitmaps.good[21]


# bisc([the decreasing permutation of length 21], 2, 21) on develop, before
# PropertyBitmaps, and the same at length 25
DEVELOP_ANSWER_LONG = {
    0: {Perm(()): [{(0, 0)}]},
    1: {Perm((0,)): [{(0, 1), (1, 0)}]},
    2: {Perm((0, 1)): [set()], Perm((1, 0)): [{(0, 2), (1, 1), (2, 0)}]},
}


@pytest.mark.parametrize("length", [21, 25])
def test_bisc_of_one_long_permutation_is_as_before(length):
    """bisc mines one listed permutation of length 21 or more, as it did before
    PropertyBitmaps."""
    last = Perm(range(length - 1, -1, -1))
    answer = bisc([last], 2, length)
    assert shadings_as_sets(answer) == shadings_as_sets(DEVELOP_ANSWER_LONG)


def test_a_dense_length_is_kept_as_bytes_and_read_without_a_copy():
    """A length kept as a bitmap keeps bytes, however it came in, so that
    bitmaps gives the same object on every read."""
    length = 6
    good_set = {
        perm for index, perm in enumerate(Perm.of_length(length)) if index % 3 == 0
    }
    by_property = PropertyBitmaps(lambda perm: perm in good_set)
    by_property.add_length(length)
    from_list = bisc_module._from_perms_by_length({length: sorted(good_set)})
    given = PropertyBitmaps(
        bitmaps={length: bytearray(expected_bitmap(length, good_set))}
    )
    for property_bitmaps in (by_property, from_list, given):
        assert type(property_bitmaps._labels[length]) is bytes
        assert property_bitmaps.bitmaps[length] is property_bitmaps.bitmaps[length]
        assert property_bitmaps.bitmaps[length] == expected_bitmap(length, good_set)


LENGTH_6 = list(Perm.of_length(6))  # 720 permutations: kept as indices below 12 good
SPARSE_6 = {LENGTH_6[index] for index in (0, 5, 100, 719)}
DENSE_6 = {perm for index, perm in enumerate(LENGTH_6) if index % 3 == 0}


@pytest.mark.parametrize("good_set", [SPARSE_6, DENSE_6], ids=["sparse", "dense"])
@pytest.mark.parametrize("wrap", [bytearray, lambda raw: memoryview(bytearray(raw))])
def test_a_buffer_given_and_changed_afterwards_changes_nothing(good_set, wrap):
    """A bitmap given is copied, whatever its form: changing the caller's
    bytearray, or the one under a memoryview, afterwards changes nothing."""
    buffer = wrap(expected_bitmap(6, good_set))
    underlying = buffer.obj if isinstance(buffer, memoryview) else buffer
    property_bitmaps = PropertyBitmaps(bitmaps={6: buffer})
    assert is_kept_as_indices(property_bitmaps, 6) == (good_set is SPARSE_6)
    underlying[:] = b"\xff" * len(underlying)  # every permutation good
    assert_views_match(property_bitmaps, 6, good_set)
    underlying[:] = bytes(len(underlying))  # none good
    assert_views_match(property_bitmaps, 6, good_set)


@pytest.mark.parametrize("good_set", [SPARSE_6, DENSE_6], ids=["sparse", "dense"])
def test_a_memoryview_of_another_format_is_read_as_bytes(good_set):
    """A memoryview of another format, shape or stride is read as its bytes."""
    raw = expected_bitmap(6, good_set)  # 90 bytes
    views = {
        "2-byte items": memoryview(raw).cast("H"),  # 45 items of 2 bytes
        "3 x 30": memoryview(raw).cast("B", shape=[3, 30]),
        "every other byte": memoryview(b"".join(bytes((byte, 0)) for byte in raw))[::2],
        "signed": memoryview(raw).cast("b"),
    }
    for name, view in views.items():
        property_bitmaps = PropertyBitmaps(bitmaps={6: view})
        assert is_kept_as_indices(property_bitmaps, 6) == (good_set is SPARSE_6), name
        assert_views_match(property_bitmaps, 6, good_set)


def test_bitmaps_give_bytes_that_are_equal_on_every_read():
    """bitmaps gives a length's bitmap as bytes, whatever form the length is
    kept in, and the same on every read."""
    by_property = PropertyBitmaps(lambda perm: perm in DENSE_6 or perm in SPARSE_6)
    by_property.add_length(6)
    sparse_by_property = PropertyBitmaps(lambda perm: perm in SPARSE_6)
    sparse_by_property.add_length(6)
    from_list = bisc_module._from_perms_by_length({6: sorted(DENSE_6)})
    from_sparse_list = bisc_module._from_perms_by_length({6: sorted(SPARSE_6)})
    for property_bitmaps in (
        by_property,
        sparse_by_property,
        from_list,
        from_sparse_list,
    ):
        first = property_bitmaps.bitmaps[6]
        assert type(first) is bytes
        assert property_bitmaps.bitmaps[6] == first
        assert len(first) == 90


def extremes(length):
    """The first and the last permutation of a length: one for lengths 0 and 1."""
    return {Perm(range(length)), Perm(range(length - 1, -1, -1))}


def test_bitmaps_round_trip_with_lengths_kept_as_indices():
    """A PropertyBitmaps made from another's bitmaps keeps each length in the
    same form, with the same labels."""
    property_bitmaps = PropertyBitmaps(lambda perm: perm in extremes(len(perm)))
    for length in range(9):
        property_bitmaps.add_length(length)
    assert [is_kept_as_indices(property_bitmaps, length) for length in range(9)] == [
        False,
        False,
        False,
        False,
        False,
        False,
        True,
        True,
        True,
    ]
    round_trip = PropertyBitmaps(bitmaps=property_bitmaps.bitmaps)
    for length in range(9):
        assert is_kept_as_indices(round_trip, length) == is_kept_as_indices(
            property_bitmaps, length
        )
        assert round_trip.good_counts[length] == property_bitmaps.good_counts[length]
        assert round_trip.bitmaps[length] == property_bitmaps.bitmaps[length]
        assert list(round_trip.good[length]) == list(property_bitmaps.good[length])
        assert list(round_trip.bad[length]) == list(property_bitmaps.bad[length])


LENGTH_8 = list(Perm.of_length(8))
SPARSE_8 = {LENGTH_8[0], LENGTH_8[-1]}  # the first and the last permutation


def test_the_first_and_the_last_permutation_of_a_sparse_length():
    """The first and the last permutation of a length kept as indices, in
    either view, good or bad; and, with the good ones in between, a bitmap."""
    first, last = LENGTH_8[0], LENGTH_8[-1]
    for good_set in (SPARSE_8, {first}, {last}):
        property_bitmaps = bisc_module._from_perms_by_length({8: sorted(good_set)})
        assert is_kept_as_indices(property_bitmaps, 8)
        good, bad = property_bitmaps.good[8], property_bitmaps.bad[8]
        for perm in (first, last):
            assert (perm in good) == (perm in good_set)
            assert (perm in bad) == (perm not in good_set)
        assert list(good) == sorted(good_set)
        bad_perms = list(bad)
        assert len(bad_perms) == len(bad) == factorial(8) - len(good_set)
        assert bad_perms == [perm for perm in LENGTH_8 if perm not in good_set]
    in_between = set(LENGTH_8[1:-1])
    property_bitmaps = bisc_module._from_perms_by_length({8: sorted(in_between)})
    assert not is_kept_as_indices(property_bitmaps, 8)
    assert list(property_bitmaps.bad[8]) == [first, last]


class PropertyFailed(Exception):
    pass


@pytest.mark.parametrize("fail_after", [10, 1000, 5039])
def test_a_property_that_raises_midway_through_add_length_keeps_nothing(fail_after):
    """A property that raises in the middle of add_length, while the indices
    are kept or after the switch to the bitmap, leaves nothing of that call,
    and a length labeled before keeps its labels."""
    perms = list(Perm.of_length(7))  # 5040; all good makes the switch at the 79th
    calls = []

    def all_good_but_fails_once_asked(perm):
        calls.append(perm)
        if len(calls) == fail_after + 1:
            raise PropertyFailed
        return True

    property_bitmaps = PropertyBitmaps(all_good_but_fails_once_asked)
    with pytest.raises(PropertyFailed):
        property_bitmaps.add_length(7)
    assert 7 not in property_bitmaps.bitmaps and 7 not in property_bitmaps.good_counts
    assert 7 not in property_bitmaps.good and 7 not in property_bitmaps.bad
    property_bitmaps.prop = lambda perm: perm == perms[3]
    property_bitmaps.add_length(7)
    property_bitmaps.prop = all_good_but_fails_once_asked
    calls.clear()
    with pytest.raises(PropertyFailed):
        property_bitmaps.add_length(7)
    assert_views_match(property_bitmaps, 7, {perms[3]})
    # A call that succeeds replaces the labels
    property_bitmaps.prop = lambda perm: True
    property_bitmaps.add_length(7)
    assert_views_match(property_bitmaps, 7, set(perms))
    assert not is_kept_as_indices(property_bitmaps, 7)


def test_add_length_replaces_labels_between_the_forms():
    """add_length replaces a length's labels, from indices to a bitmap and
    back."""
    property_bitmaps = PropertyBitmaps(lambda perm: perm in SPARSE_6)
    property_bitmaps.add_length(6)
    assert is_kept_as_indices(property_bitmaps, 6)
    property_bitmaps.prop = lambda perm: perm in DENSE_6
    property_bitmaps.add_length(6)
    assert not is_kept_as_indices(property_bitmaps, 6)
    assert_views_match(property_bitmaps, 6, DENSE_6)
    property_bitmaps.prop = lambda perm: perm in SPARSE_6
    property_bitmaps.add_length(6)
    assert is_kept_as_indices(property_bitmaps, 6)
    assert_views_match(property_bitmaps, 6, SPARSE_6)


def test_lengths_past_n_have_a_count_of_zero(monkeypatch):
    """With m > n, the lengths past n are counted as empty, not only holding no
    bits: mine() takes a length for complete when its count is the length's
    factorial, and with a count of 1 it would take length 1 for complete."""
    seen = []
    real_mine = bisc_module.mine

    def recording_mine(goodperms, M, N=None, report=False):
        property_bitmaps = goodperms.property_bitmaps
        seen.append(
            {
                length: (
                    property_bitmaps.good_counts[length],
                    len(goodperms[length]),
                    list(goodperms[length]),
                    len(property_bitmaps.bad[length]),
                )
                for length in goodperms
            }
        )
        return real_mine(goodperms, M, N, report)

    monkeypatch.setattr(bisc_module, "mine", recording_mine)
    bisc(lambda perm: True, 3, 0)
    assert seen[0] == {
        0: (1, 1, [Perm(())], 0),
        1: (0, 0, [], 1),
        2: (0, 0, [], 2),
        3: (0, 0, [], 6),
    }


def test_a_sparse_view_iterates_independently():
    """The same view of a length kept as indices, iterated twice or in step
    with itself, gives the same permutations."""
    property_bitmaps = bisc_module._from_perms_by_length({6: sorted(SPARSE_6)})
    for view in (property_bitmaps.good[6], property_bitmaps.bad[6]):
        once = list(view)
        assert list(view) == once
        assert list(zip(view, view)) == [(perm, perm) for perm in once]


def test_bisc_takes_the_view_of_a_sparse_length():
    """bisc given the good view of a PropertyBitmaps, a Mapping, mines what it
    mines from the list it was made from."""
    perms = [Perm(range(length)) for length in range(7)] + [Perm(range(6, -1, -1))]
    property_bitmaps = bisc_module._from_perms_by_length(
        {length: [perm for perm in perms if len(perm) == length] for length in range(8)}
    )
    assert is_kept_as_indices(property_bitmaps, 7)
    assert bisc(property_bitmaps.good, 2, 7) == bisc(perms, 2, 7)


def test_a_sparse_length_14_never_sizes_a_bitmap(monkeypatch):
    """No bitmap is sized for a length kept as indices: length 14's would take
    10.9 GB. A check of the structure, so that it runs on PyPy too, which has no
    tracemalloc."""
    real_bitmap_size = bisc_module._bitmap_size

    def guarded_bitmap_size(length):
        assert length <= 10, "a bitmap of length {} was sized".format(length)
        return real_bitmap_size(length)

    monkeypatch.setattr(bisc_module, "_bitmap_size", guarded_bitmap_size)
    by_length = {length: [] for length in range(15)}
    by_length[14] = THREE_OF_LENGTH_14
    by_length[13] = [Perm(range(13))]
    by_length[12] = [Perm(range(12))]
    by_length[11] = [Perm(range(11))]
    property_bitmaps = bisc_module._from_perms_by_length(by_length)
    for length in (11, 12, 13, 14):
        labels = property_bitmaps._labels[length]
        assert isinstance(labels, array) and len(labels) == len(by_length[length])
    assert list(property_bitmaps.good[14]) == sorted(THREE_OF_LENGTH_14)
    assert len(property_bitmaps.bad[14]) == factorial(14) - 3
    for perm in THREE_OF_LENGTH_14:
        assert perm in property_bitmaps.good[14]
        assert perm not in property_bitmaps.bad[14]
    assert Perm(range(14)) in property_bitmaps.bad[14]
    assert 14 in property_bitmaps.bitmaps and len(property_bitmaps.bitmaps) == 15


class MineStopped(Exception):
    pass


def test_lengths_past_n_are_kept_as_empty_indices_and_size_no_bitmap(monkeypatch):
    """With m > n, a length past n is kept as no indices, not as a bitmap: m = 14
    would size one of 10.9 GB. The lengths up to n are labeled."""
    real_bitmap_size = bisc_module._bitmap_size
    kept = {}

    def guarded_bitmap_size(length):
        assert length <= 10, "a bitmap of length {} was sized".format(length)
        return real_bitmap_size(length)

    def stopped_mine(goodperms, M, N=None, report=False):
        property_bitmaps = goodperms.property_bitmaps
        kept.update(property_bitmaps._labels)
        raise MineStopped

    monkeypatch.setattr(bisc_module, "_bitmap_size", guarded_bitmap_size)
    monkeypatch.setattr(bisc_module, "mine", stopped_mine)
    with pytest.raises(MineStopped):
        bisc(lambda perm: perm.is_increasing(), 14, 2)
    assert sorted(kept) == list(range(15))
    for length in range(3, 15):
        assert isinstance(kept[length], array) and len(kept[length]) == 0


def test_a_sparse_list_with_repeats_counts_each_permutation_once():
    """A list that looks sparse before it is counted, with a permutation
    repeated, counts it once."""
    first, second = LENGTH_8[7], LENGTH_8[100]
    property_bitmaps = bisc_module._from_perms_by_length(
        {8: [second, first, first, first]}
    )
    assert is_kept_as_indices(property_bitmaps, 8)
    assert property_bitmaps.good_counts[8] == 2
    assert len(property_bitmaps.good[8]) == 2
    assert len(property_bitmaps.bad[8]) == factorial(8) - 2
    assert list(property_bitmaps.good[8]) == [first, second]
