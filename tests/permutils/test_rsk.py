import random
from collections import defaultdict
from itertools import combinations, permutations

import pytest

from permuta import Perm
from permuta.permutils.rsk import (
    evacuate_recording_tableau,
    evacuation,
    is_knuth_closed,
    is_shape_closed,
    rsk,
    rsk_inverse,
)


def shape(word):
    return tuple(len(row) for row in rsk(word)[0])


def perms(size):
    return (list(perm) for perm in permutations(range(size)))


@pytest.mark.parametrize("size", range(8))
def test_rsk_and_its_inverse(size):
    for perm in perms(size):
        insertion_tableau, recording_tableau = rsk(perm)
        assert [len(row) for row in insertion_tableau] == [
            len(row) for row in recording_tableau
        ]
        assert rsk_inverse(insertion_tableau, recording_tableau) == perm


def test_rsk_of_words_with_gaps():
    word = [7, 2, 9, 4]
    insertion_tableau, recording_tableau = rsk(word)
    assert insertion_tableau == [[2, 4], [7, 9]]
    assert recording_tableau == [[1, 3], [2, 4]]
    assert rsk_inverse(insertion_tableau, recording_tableau) == word


@pytest.mark.parametrize("size", range(8))
def test_evacuation_is_a_shape_preserving_involution(size):
    for perm in perms(size):
        recording_tableau = rsk(perm)[1]
        evacuated = evacuation(recording_tableau)
        assert [len(row) for row in evacuated] == [
            len(row) for row in recording_tableau
        ]
        assert evacuation(evacuated) == recording_tableau


@pytest.mark.parametrize("size", range(8))
def test_evacuation_records_the_reverse_complement(size):
    """Schutzenberger: Q(w^#) = evac(Q(w)) for the reverse-complement w^#."""
    for perm in perms(size):
        reverse_complement = [size - 1 - value for value in reversed(perm)]
        assert rsk(reverse_complement)[1] == evacuation(rsk(perm)[1])


@pytest.mark.parametrize("size", range(8))
def test_evacuating_the_recording_tableau(size):
    """It keeps the insertion tableau, gives every factor the shape of the mirrored
    factor of the word, and is an involution."""
    for perm in perms(size):
        image = evacuate_recording_tableau(perm)
        assert rsk(image)[0] == rsk(perm)[0]
        assert evacuate_recording_tableau(image) == perm
        for i in range(size):
            for j in range(i, size):
                assert shape(image[size - 1 - j : size - i]) == shape(perm[i : j + 1])


def test_the_knuth_class_is_kept_on_every_window_of_values():
    for perm in perms(6):
        image = evacuate_recording_tableau(perm)
        for low in range(6):
            for high in range(low, 6):
                window = [value for value in perm if low <= value <= high]
                image_window = [value for value in image if low <= value <= high]
                assert rsk(window)[0] == rsk(image_window)[0]


def brute_force_knuth_closed(patterns, length):
    for size in range(length + 1):
        classes = defaultdict(list)
        for perm in permutations(range(size)):
            classes[tuple(map(tuple, rsk(perm)[0]))].append(Perm(perm))
        for knuth_class in classes.values():
            if len({perm.avoids(*patterns) for perm in knuth_class}) > 1:
                return False
    return True


def test_knuth_closure_against_brute_force():
    """Any failure of closure shows on permutations at most one entry longer than
    the longest pattern, so the brute force to that length decides it."""
    perms_of_length_3 = [Perm(perm) for perm in permutations(range(3))]
    perms_of_length_4 = [Perm(perm) for perm in permutations(range(4))]
    generator = random.Random(2026)
    bases = [
        list(chosen)
        for size in range(1, 7)
        for chosen in combinations(perms_of_length_3, size)
    ]
    bases += [
        generator.sample(perms_of_length_4, generator.randint(1, 6)) for _ in range(40)
    ]
    bases += [
        generator.sample(perms_of_length_3, 1)
        + generator.sample(perms_of_length_4, generator.randint(1, 3))
        for _ in range(20)
    ]
    for basis in bases:
        length = max(len(pattern) for pattern in basis) + 1
        assert is_knuth_closed(frozenset(basis)) == brute_force_knuth_closed(
            basis, length
        ), basis


def test_shape_closure():
    def basis(*patterns):
        return frozenset(Perm.to_standard(pattern) for pattern in patterns)

    for size in range(1, 6):
        assert is_shape_closed(frozenset([Perm(range(size))]))
        assert is_shape_closed(frozenset([Perm(range(size - 1, -1, -1))]))
    shape_31 = frozenset(
        Perm(perm) for perm in permutations(range(4)) if shape(list(perm)) == (3, 1)
    )
    assert len(shape_31) == 9 and is_shape_closed(shape_31)
    # Henning's stable Knuth class: Knuth-closed, but not determined by the shape
    stable_knuth_class = basis("1243", "1423", "4123")
    assert is_knuth_closed(stable_knuth_class) and not is_shape_closed(
        stable_knuth_class
    )
    assert not is_knuth_closed(basis("132"))
    assert is_knuth_closed(basis("132", "312"))
    assert not is_shape_closed(basis("132", "312"))
    assert is_knuth_closed(frozenset()) and is_shape_closed(frozenset())


def knuth_class_moves(word):
    """The words one elementary Knuth move from word, as Knuth stated them: for
    x < y < z, y z x <-> y x z and x z y <-> z x y. Written from that statement, not
    from the module under test."""
    for i in range(len(word) - 2):
        triple = tuple(word[i : i + 3])
        low, middle, high = sorted(triple)
        for one, other in [
            ((middle, high, low), (middle, low, high)),
            ((low, high, middle), (high, low, middle)),
        ]:
            for before, after in [(one, other), (other, one)]:
                if triple == before:
                    yield tuple(word[:i]) + after + tuple(word[i + 3 :])


@pytest.mark.parametrize("size", range(8))
def test_the_insertion_tableau_identifies_the_knuth_classes(size):
    """Knuth's theorem: two permutations are Knuth equivalent exactly when their
    insertion tableaux are equal. The classes are found here by the moves alone, and
    compared with the fibers of rsk's first tableau."""
    by_tableau = defaultdict(set)
    for perm in permutations(range(size)):
        by_tableau[tuple(map(tuple, rsk(perm)[0]))].add(perm)
    seen = set()
    for start in permutations(range(size)):
        if start in seen:
            continue
        component, frontier = {start}, [start]
        while frontier:
            for neighbor in knuth_class_moves(frontier.pop()):
                if neighbor not in component:
                    component.add(neighbor)
                    frontier.append(neighbor)
        seen |= component
        assert component == by_tableau[tuple(map(tuple, rsk(start)[0]))]


def test_knuth_closure_of_unions_of_knuth_classes():
    """Most sets of patterns are not closed, so the brute force above mostly agrees on
    the answer False for patterns of four letters. Unions of Knuth classes are often
    closed: the answers True are compared too."""
    classes = {}
    for size in (3, 4):
        by_tableau = defaultdict(list)
        for perm in permutations(range(size)):
            by_tableau[tuple(map(tuple, rsk(perm)[0]))].append(Perm(perm))
        classes[size] = list(by_tableau.values())
    generator = random.Random(2027)
    closed = 0
    for _ in range(60):
        basis = [
            perm
            for size in (3, 4)
            for knuth_class in generator.sample(classes[size], generator.randint(0, 2))
            for perm in knuth_class
        ]
        if not basis:
            continue
        length = max(len(pattern) for pattern in basis) + 1
        expected = brute_force_knuth_closed(basis, length)
        assert is_knuth_closed(frozenset(basis)) == expected, basis
        closed += expected
    assert closed >= 10


def test_the_insertion_tableaux():
    """The insertion tableaux of the permutations of each length are the standard
    Young tableaux of that size, as many as the involutions; and some examples."""
    tableaux = {length: set() for length in range(8)}
    for length in range(8):
        for perm in Perm.of_length(length):
            tableaux[length].add(tuple(map(tuple, rsk(perm)[0])))
    expected = [1, 1, 2, 4, 10, 26, 76, 232]
    for length in range(8):
        assert len(tableaux[length]) == expected[length]
    assert rsk(Perm((1, 0)))[0] == [[0], [1]]
    assert rsk(Perm((1, 0, 3, 5, 2, 4)))[0] == [[0, 2, 4], [1, 3, 5]]
    assert rsk(Perm((1, 0, 2, 3)))[0] == [[0, 2, 3], [1]]
    assert rsk(Perm((3, 1, 4, 0, 2)))[0] == [[0, 2], [1, 4], [3]]
    assert rsk(Perm((5, 4, 1, 0, 3, 2)))[0] == [[0, 2], [1, 3], [4], [5]]
    assert rsk(Perm((0, 1)))[0] == [[0, 1]]
    assert rsk(Perm((0,)))[0] == [[0]]
    assert rsk(Perm((2, 3, 0, 1)))[0] == [[0, 1], [2, 3]]
    assert rsk(Perm((1, 2, 3, 0)))[0] == [[0, 2, 3], [1]]
    assert rsk(Perm((4, 0, 1, 2, 5, 3)))[0] == [[0, 1, 2, 3], [4, 5]]


def test_the_empty_word_and_a_single_letter():
    assert rsk([]) == ([], [])
    assert rsk([5]) == ([[5]], [[1]])
    assert rsk_inverse([], []) == []
    assert rsk_inverse([[5]], [[1]]) == [5]
    assert evacuation([]) == []
    assert evacuation([[1]]) == [[1]]
    assert evacuate_recording_tableau([]) == []
    assert evacuate_recording_tableau([5]) == [5]


@pytest.mark.parametrize("size", range(7))
def test_only_the_order_of_the_letters_matters(size):
    """A word of distinct letters that are not 0, 1, ...: relabeling the letters of a
    permutation by an increasing map relabels its insertion tableau and the evacuated
    word, and leaves the recording tableau alone."""

    def relabel(letters):
        return [3 * letter - 4 for letter in letters]

    for perm in perms(size):
        word = relabel(perm)
        insertion_tableau, recording_tableau = rsk(word)
        standard_insertion, standard_recording = rsk(perm)
        assert insertion_tableau == [relabel(row) for row in standard_insertion]
        assert recording_tableau == standard_recording
        assert rsk_inverse(insertion_tableau, recording_tableau) == word
        assert evacuate_recording_tableau(word) == relabel(
            evacuate_recording_tableau(perm)
        )


def test_the_tableaux_given_are_not_changed_and_may_be_tuples():
    for perm in perms(5):
        insertion_tableau, recording_tableau = rsk(perm)
        copies = (
            [list(row) for row in insertion_tableau],
            [list(row) for row in recording_tableau],
        )
        assert rsk_inverse(insertion_tableau, recording_tableau) == perm
        evacuated = evacuation(recording_tableau)
        assert (insertion_tableau, recording_tableau) == copies
        insertion_tuples = tuple(map(tuple, insertion_tableau))
        recording_tuples = tuple(map(tuple, recording_tableau))
        assert rsk_inverse(insertion_tuples, recording_tuples) == perm
        assert evacuation(recording_tuples) == evacuated


@pytest.mark.parametrize(
    "convert",
    [
        list,
        tuple,
        set,
        frozenset,
        iter,
        lambda patterns: (pattern for pattern in patterns),
    ],
    ids=["list", "tuple", "set", "frozenset", "iterator", "generator"],
)
def test_the_closure_tests_take_any_iterable_of_patterns(convert):
    def patterns(*perms_):
        return convert([Perm(perm) for perm in perms_])

    # Knuth closed, but not determined by the shape
    assert is_knuth_closed(patterns((0, 2, 1), (2, 0, 1))) is True
    assert is_shape_closed(patterns((0, 2, 1), (2, 0, 1))) is False
    # neither
    assert is_knuth_closed(patterns((0, 2, 1))) is False
    assert is_shape_closed(patterns((0, 2, 1))) is False
    # both
    assert is_knuth_closed(patterns((2, 1, 0))) is True
    assert is_shape_closed(patterns((2, 1, 0))) is True
    # the empty basis: everything avoids it
    assert is_knuth_closed(patterns()) is True
    assert is_shape_closed(patterns()) is True


def test_the_closure_tests_ignore_the_order_and_the_duplicates_of_the_patterns():
    pair = [Perm((0, 2, 1)), Perm((2, 0, 1))]
    for patterns in (
        pair,
        pair[::-1],
        pair + pair,
        [pair[0], pair[1], pair[0], pair[1], pair[0]],
    ):
        assert is_knuth_closed(patterns) is True
        assert is_shape_closed(patterns) is False
    assert is_knuth_closed([pair[0]] * 3) is False
    assert is_shape_closed([pair[1]] * 3) is False


def brute_force_shape_closed(patterns, length):
    for size in range(length + 1):
        classes = defaultdict(list)
        for perm in permutations(range(size)):
            classes[shape(perm)].append(Perm(perm))
        for shape_class in classes.values():
            if len({perm.avoids(*patterns) for perm in shape_class}) > 1:
                return False
    return True


@pytest.mark.parametrize(
    "basis",
    [
        [Perm()],
        [Perm(), Perm((0, 2, 1))],
        [Perm((0,))],
        [Perm((0,)), Perm((0, 2, 1))],
        [Perm((0, 1))],
        [Perm((1, 0))],
        [Perm((0, 1)), Perm((1, 0))],
        [Perm((0, 1)), Perm((0, 2, 1))],
        [Perm((1, 0)), Perm((1, 2, 0)), Perm((2, 0, 1, 3))],
    ],
)
def test_a_pattern_of_length_at_most_2_closes_the_basis(basis):
    """Its avoiders are decreasing, or increasing, or the empty permutation alone, and
    Knuth moves and their duals leave these alone: every such basis is closed, and the
    empty permutation as a pattern, which nothing avoids, is too."""
    length = max(len(pattern) for pattern in basis) + 1
    assert is_knuth_closed(basis) == brute_force_knuth_closed(basis, length)
    assert is_shape_closed(basis) == brute_force_shape_closed(basis, length)


def test_shape_closure_against_brute_force():
    """Whether the avoiders are determined by the shape, to one entry beyond the
    longest pattern, and so for every length."""
    perms_of_length_3 = [Perm(perm) for perm in permutations(range(3))]
    perms_of_length_4 = [Perm(perm) for perm in permutations(range(4))]
    generator = random.Random(2028)
    bases = [
        list(chosen)
        for size in range(1, 4)
        for chosen in combinations(perms_of_length_3, size)
    ]
    bases += [
        generator.sample(perms_of_length_4, generator.randint(1, 8)) for _ in range(30)
    ]
    bases += [
        generator.sample(perms_of_length_3, 1)
        + generator.sample(perms_of_length_4, generator.randint(1, 3))
        for _ in range(15)
    ]
    closed = 0
    for basis in bases:
        length = max(len(pattern) for pattern in basis) + 1
        expected = brute_force_shape_closed(basis, length)
        assert is_shape_closed(basis) == expected, basis
        closed += expected
    assert closed >= 5


def test_a_basis_with_redundant_patterns_is_closed_as_its_minimal_basis_is():
    """The avoiders of a basis do not change when the patterns that contain another
    pattern of it are added."""
    perms_of_length_3 = [Perm(perm) for perm in permutations(range(3))]
    perms_of_length_4 = [Perm(perm) for perm in permutations(range(4))]
    bases = [
        list(chosen)
        for size in (1, 2)
        for chosen in combinations(perms_of_length_3, size)
    ]
    bases += [[Perm((0, 1))], [Perm((1, 0))], [Perm((0,))]]
    for minimal in bases:
        redundant = [
            perm
            for perm in perms_of_length_3 + perms_of_length_4
            if perm not in minimal and not perm.avoids(*minimal)
        ]
        assert redundant
        for extended in (minimal + redundant, redundant[::-1] + minimal):
            assert is_knuth_closed(extended) == is_knuth_closed(minimal), extended
            assert is_shape_closed(extended) == is_shape_closed(minimal), extended
