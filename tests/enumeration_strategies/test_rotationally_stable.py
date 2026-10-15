from itertools import combinations

import pytest

from permuta import Av, CyclicPerm, Perm
from permuta.enumeration_strategies import find_strategies
from permuta.enumeration_strategies.rotationally_stable import (
    RotationallyStableStrategy,
    is_rotationally_stable,
    max_cut,
    min_cut,
)
from permuta.perm_sets.basis import Basis
from permuta.permutils.symmetry import inverse_set

r123 = Basis.from_string("123_231_312")
r132 = Basis.from_string("132_213_321")
s3 = Basis.from_string("123_132_213_231_312_321")
r1234 = Basis.from_string("1234_2341_3412_4123")
r1324 = Basis.from_string("1324_3241_2413_4132")
r1243 = Basis.from_string("1243_2431_4312_3124")
r1243_inverse = Basis.from_string("1243_2314_3421_4132")


def lift(basis):
    """The rotations of the patterns 1 + p for p in the basis."""
    return Basis(
        *(
            Perm((0,)).direct_sum(patt).shift_left(i)
            for patt in basis
            for i in range(len(patt) + 1)
        )
    )


def cyclic_count(patts, n):
    """The number of cyclic permutations of length n avoiding the patterns."""
    return sum(1 for perm in CyclicPerm.of_length(n) if perm.avoids_set(patts))


def test_is_rotationally_stable():
    assert is_rotationally_stable(r123)
    assert is_rotationally_stable(r132)
    assert is_rotationally_stable(s3)
    assert is_rotationally_stable(r1234)
    assert is_rotationally_stable(lift(r1234))
    assert not is_rotationally_stable(Basis.from_string("123"))
    assert not is_rotationally_stable(Basis.from_string("123_3412"))
    assert not is_rotationally_stable(r1243_inverse)
    # the basis of the class is tested, not the patterns as given
    assert is_rotationally_stable([*r123, Perm((0, 1, 2, 3))])


def test_applies_to_subsets_of_s3():
    applies = {
        frozenset(basis)
        for k in range(1, 7)
        for basis in combinations(s3, k)
        if RotationallyStableStrategy(basis).applies()
    }
    assert applies == {frozenset(r123), frozenset(r132), frozenset(s3)}


def test_applies_to_a_symmetry():
    # closed under rotating the values, so its inverse is closed under rotation
    assert is_rotationally_stable(inverse_set(r1243_inverse))
    assert RotationallyStableStrategy(r1243_inverse).applies()


def test_does_not_apply():
    assert not RotationallyStableStrategy(Basis.from_string("123_3412")).applies()
    assert not RotationallyStableStrategy([]).applies()
    assert not RotationallyStableStrategy([Perm()]).applies()


def test_cuts():
    assert min_cut(r123) == max_cut(r123) == Basis(Perm((0, 1)))
    assert min_cut(r1234) == max_cut(r1234) == Basis.from_string("123_3412")
    assert min_cut(r1324) == Basis.from_string("213_4132")
    assert max_cut(r1324) == Basis.from_string("132_3241")
    assert min_cut(r1243) == Basis.from_string("132_3124_4312")
    assert min_cut(lift(r123)) == r123
    assert min_cut([Perm((0,))]) == Basis(Perm())


def test_chain():
    assert RotationallyStableStrategy(lift(lift(r123))).chain() == [
        lift(lift(r123)),
        lift(r123),
        r123,
        Basis(Perm((0, 1))),
    ]
    assert RotationallyStableStrategy(lift(r1234)).chain() == [
        lift(r1234),
        r1234,
        Basis.from_string("123_3412"),
    ]
    assert RotationallyStableStrategy(r1243_inverse).chain() == [
        r1243,
        Basis.from_string("132_3124_4312"),
    ]
    assert RotationallyStableStrategy([Perm((0,))]).chain() == [
        Basis(Perm((0,))),
        Basis(Perm()),
    ]
    basis = Basis.from_string("123_3412")
    assert RotationallyStableStrategy(basis).chain() == [basis]


@pytest.mark.parametrize(
    "basis",
    [
        r123,
        s3,
        r1234,
        r1324,
        r1243,
        r1243_inverse,
        lift(r123),
        lift(lift(r123)),
        lift(r1234),
        Basis(Perm((0,))),
        Basis.from_string("123_3412"),
    ],
)
def test_count(basis):
    strategy = RotationallyStableStrategy(basis)
    assert [strategy.count(n) for n in range(9)] == Av(basis).enumeration(8)


def test_count_is_n_times_the_cyclic_count():
    # all rotations of some cyclic patterns are a rotationally stable basis, whose
    # class has n times as many permutations of length n as there are cyclic
    # permutations of length n avoiding the patterns
    cases = [[patt] for k in (4, 5) for patt in CyclicPerm.of_length(k)]
    cases.extend(list(pair) for pair in combinations(CyclicPerm.of_length(4), 2))
    for patts in cases:
        basis = Basis(*(rotation for patt in patts for rotation in patt.rotations()))
        strategy = RotationallyStableStrategy(basis)
        assert strategy.applies()
        for n in range(1, 8):
            assert strategy.count(n) == n * cyclic_count(patts, n)


def test_counts_from_either_cut():
    for basis in (r123, r1234, r1324, r1243, lift(r123)):
        counts = Av(basis).enumeration(8)
        for cut in (min_cut(basis), max_cut(basis)):
            assert counts[1:] == [n * Av(cut).count(n - 1) for n in range(1, 9)]


def test_find_strategies():
    assert any(
        isinstance(strategy, RotationallyStableStrategy)
        for strategy in find_strategies(r1234, long_runnning=False)
    )
    assert not any(
        isinstance(strategy, RotationallyStableStrategy)
        for strategy in find_strategies(Basis.from_string("123_3412"), False)
    )
