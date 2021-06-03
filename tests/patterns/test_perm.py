import itertools
import random
from collections import deque

import pytest

from permuta import Perm


def test_from_iterable_validated():
    with pytest.raises(ValueError):
        Perm.from_iterable_validated([0, 1, 1])
    with pytest.raises(ValueError):
        Perm.from_iterable_validated([1, 0, 1])
    with pytest.raises(ValueError):
        Perm.from_iterable_validated([0, 0])
    with pytest.raises(ValueError):
        Perm.from_iterable_validated([1])
    with pytest.raises(ValueError):
        Perm.from_iterable_validated((1,))
    with pytest.raises(TypeError):
        Perm.from_iterable_validated(101)
    with pytest.raises(TypeError):
        Perm.from_iterable_validated(-234)
    with pytest.raises(TypeError):
        Perm.from_iterable_validated(None)
    with pytest.raises(TypeError):
        Perm.from_iterable_validated([0.1, 0.2, 0.3])
    with pytest.raises(ValueError):
        Perm.from_iterable_validated("132")
    with pytest.raises(ValueError):
        Perm.from_iterable_validated("134")
    with pytest.raises(ValueError):
        Perm.from_iterable_validated("112")
    with pytest.raises(ValueError):
        Perm.from_iterable_validated("5")
    try:
        Perm.from_iterable_validated(())
        Perm.from_iterable_validated((1, 0))
        Perm.from_iterable_validated([5, 1, 0, 2, 4, 3])
        Perm.from_iterable_validated("1302")
    except (ValueError, TypeError):
        pytest.fail("Exception raised when it shouldn't")


def test_to_standard():
    def gen(perm):
        res = list(perm)
        add = 0
        for i in perm.inverse():
            add += random.randint(0, 10)
            res[i] += add
        return Perm(res)

    perm = Perm.to_standard(x for x in range(10))
    Perm.to_standard(x for x in range(3, 10))

    for _ in range(100):
        perm = Perm.random(random.randint(0, 20))
        assert perm == Perm.to_standard(perm)
        assert perm == Perm.to_standard(gen(perm))

    assert Perm.to_standard("aaa") == Perm((0, 1, 2))
    assert Perm.to_standard("cba") == Perm((2, 1, 0))


def test_from_integer():
    assert Perm.from_integer(123) == Perm((0, 1, 2))
    assert Perm.from_integer(321) == Perm((2, 1, 0))
    assert Perm.from_integer(201) == Perm((2, 0, 1))
    assert Perm.from_integer(0) == Perm((0,))
    assert Perm.from_integer(1) == Perm((0,))
    assert Perm.from_integer(123456789) == Perm((0, 1, 2, 3, 4, 5, 6, 7, 8))
    assert Perm.from_integer(9876543210) == Perm((9, 8, 7, 6, 5, 4, 3, 2, 1, 0))


def test_from_string():
    assert Perm.from_string("203451") == Perm((2, 0, 3, 4, 5, 1))
    assert Perm.from_string("40132") == Perm((4, 0, 1, 3, 2))
    assert Perm.from_string("0") == Perm((0,))

    for _ in range(100):
        perm = Perm.random(random.randint(0, 10))
        assert perm == Perm.from_string("".join(map(str, perm)))


def test_str_representation():
    assert str(Perm((0, 2, 1))) == "021"
    assert (
        str(Perm((0, 11, 1, 10, 2, 9, 3, 8, 4, 7, 5, 6)))
        == "(0)(11)(1)(10)(2)(9)(3)(8)(4)(7)(5)(6)"
    )
    assert str(Perm(())) == "\u03B5"


def test_of_length():
    assert list(Perm.of_length(3)) == [
        Perm((0, 1, 2)),
        Perm((0, 2, 1)),
        Perm((1, 0, 2)),
        Perm((1, 2, 0)),
        Perm((2, 0, 1)),
        Perm((2, 1, 0)),
    ]
    assert list(Perm.of_length(0)) == [Perm(())]
    assert list(Perm.of_length(1)) == [Perm((0,))]


def test_first():
    assert list(Perm.first(3)) == [Perm(()), Perm((0,)), Perm((0, 1))]
    assert list(Perm.first(0)) == []
    assert list(Perm.first(1)) == [Perm(())]
    assert list(Perm.first(11)) == [
        Perm(()),
        Perm((0,)),
        Perm((0, 1)),
        Perm((1, 0)),
        Perm((0, 1, 2)),
        Perm((0, 2, 1)),
        Perm((1, 0, 2)),
        Perm((1, 2, 0)),
        Perm((2, 0, 1)),
        Perm((2, 1, 0)),
        Perm((0, 1, 2, 3)),
    ]


def test_one_based():
    assert Perm.one_based((4, 1, 3, 2)) == Perm((3, 0, 2, 1))
    assert Perm.one_based((1,)) == Perm((0,))
    assert Perm.one_based(()) == Perm()

    for _ in range(100):
        p = list(range(1, random.randint(2, 20)))
        random.shuffle(p)
        assert Perm.one_based(p) == Perm([i - 1 for i in p])


def test_identity():
    for length in range(11):
        assert Perm.identity(length) == Perm(range(length))


def test_random():
    for length in range(11):
        for _ in range(10):
            perm = Perm.random(length)
            assert len(perm) == length
            assert set(perm) == set(range(length))


def test_monotone_decreasing():
    for length in range(11):
        assert Perm.monotone_decreasing(length) == Perm(range(length - 1, -1, -1))


def test_unrank():
    counter = 0
    for n in range(8):
        for i, perm in enumerate(itertools.permutations(range(n))):
            assert Perm(perm) == Perm.unrank(i, n) == Perm.unrank(counter)
            counter += 1
    with pytest.raises(AssertionError):
        Perm.unrank(-1)
    with pytest.raises(AssertionError):
        Perm.unrank(6, 3)


def test_contained_in():
    def generate_contained(n, perm):
        for i in range(len(perm), n):
            r = random.randint(1, len(perm) + 1)
            for i in range(len(perm)):
                if perm[i] >= r:
                    perm[i] += 1
            x = random.randint(0, len(perm))
            perm = perm[:x] + [r] + perm[x:]
        return Perm(perm)

    assert Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]).contained_in(
        Perm([3, 7, 0, 8, 1, 6, 5, 2, 4])
    )
    assert Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]).contains(Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]))
    assert Perm([]).contained_in(Perm([]))
    assert Perm([]).contained_in(Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]))
    assert Perm([0]).contained_in(Perm([0]))
    assert not Perm([7, 3, 0, 8, 1, 6, 5, 2, 4]).contained_in(
        Perm([3, 7, 0, 8, 1, 6, 5, 2, 4])
    )

    for i in range(100):
        n = random.randint(0, 4)
        patt = Perm.random(n)
        perm = generate_contained(random.randint(n, 8), list(patt))
        assert patt.contained_in(perm)
        assert perm.contains(patt)

    assert not Perm([0]).contained_in(Perm([]))
    assert not Perm([0, 1]).contained_in(Perm([]))
    assert not Perm([0, 1]).contained_in(Perm([0]))
    assert not Perm([1, 0]).contained_in(Perm([0, 1]))
    assert not Perm([0, 1, 2]).contained_in(Perm([0, 1]))
    assert not Perm([1, 0, 2]).contained_in(Perm([0, 1, 3, 4, 2]))
    assert not Perm([0, 1, 2]).contained_in(Perm([2, 1, 3, 0]))
    assert not Perm([2, 1, 3, 0]).contained_in(Perm([2, 0, 3, 1]))
    assert not Perm([0, 2, 1]).contained_in(Perm([2, 0, 1, 3]))
    assert not Perm([2, 0, 1, 3]).contained_in(Perm([5, 3, 2, 7, 1, 0, 6, 4]))
    assert not Perm([0, 1, 2, 3]).contained_in(Perm([4, 7, 5, 1, 6, 2, 3, 0]))


def test_left_floor_and_ceiling():
    iterable = Perm([4, 5, 1, 2, 3, 6])
    expected = [
        (-1, -1),  # 4
        (0, -1),  # 5
        (-1, 0),  # 1
        (2, 0),  # 2
        (3, 0),  # 3
        (1, -1),  # 6
    ]
    index = 0
    for fac in iterable.left_floor_and_ceiling():
        assert fac == expected[index]
        index += 1

    iterable = Perm([4, 1, 2, 5, 3])
    expected = [(-1, -1), (-1, 0), (1, 0), (0, -1), (2, 0)]  # 4  # 1  # 2  # 5  # 3
    index = 0
    for fac in iterable.left_floor_and_ceiling():
        assert fac == expected[index]
        index += 1

    iterable = Perm([1, 2, 3])
    expected = [(-1, -1), (0, -1), (1, -1)]  # 1  # 2  # 3
    index = 0
    for fac in iterable.left_floor_and_ceiling():
        assert fac == expected[index]
        index += 1

    iterable = Perm([3, 2, 1])
    expected = [(-1, -1), (-1, 0), (-1, 1)]  # 3  # 2  # 1
    index = 0
    for fac in iterable.left_floor_and_ceiling():
        assert fac == expected[index]
        index += 1
    assert list(Perm(()).left_floor_and_ceiling()) == []
    assert list(Perm((0,)).left_floor_and_ceiling()) == [(-1, -1)]
    assert list(Perm((0, 1)).left_floor_and_ceiling()) == [(-1, -1), (0, -1)]
    assert list(Perm((1, 0)).left_floor_and_ceiling()) == [(-1, -1), (-1, 0)]
    assert list(Perm((2, 1, 0, 3)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
    ]
    assert list(Perm((3, 2, 0, 1)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (2, 1),
    ]
    assert list(Perm((0, 4, 1, 2, 3)).left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (0, 1),
        (2, 1),
        (3, 1),
    ]
    assert list(Perm((1, 2, 4, 3, 0)).left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 2),
        (-1, 0),
    ]
    assert list(Perm((3, 0, 2, 5, 1, 4)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (0, -1),
        (1, 2),
        (0, 3),
    ]
    assert list(Perm((2, 5, 0, 3, 4, 1)).left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (-1, 0),
        (0, 1),
        (3, 1),
        (2, 0),
    ]
    assert list(Perm((6, 5, 0, 2, 1, 3, 4)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (2, 1),
        (2, 3),
        (3, 1),
        (5, 1),
    ]
    assert list(Perm((0, 2, 6, 5, 4, 1, 3)).left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 2),
        (1, 3),
        (0, 1),
        (1, 4),
    ]
    assert list(Perm((3, 6, 2, 7, 5, 0, 1, 4)).left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (-1, 0),
        (1, -1),
        (0, 1),
        (-1, 2),
        (5, 2),
        (0, 4),
    ]
    assert list(Perm((2, 0, 5, 6, 1, 7, 4, 3)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (0, -1),
        (2, -1),
        (1, 0),
        (3, -1),
        (0, 2),
        (0, 6),
    ]
    assert list(Perm((8, 5, 0, 7, 1, 2, 4, 6, 3)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (1, 0),
        (2, 1),
        (4, 1),
        (5, 1),
        (1, 3),
        (5, 6),
    ]
    assert list(Perm((0, 3, 7, 8, 2, 6, 4, 5, 1)).left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (2, -1),
        (0, 1),
        (1, 2),
        (1, 5),
        (6, 5),
        (0, 4),
    ]
    assert list(Perm((5, 3, 4, 1, 7, 9, 0, 6, 8, 2)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, -1),
        (4, -1),
        (-1, 3),
        (0, 4),
        (4, 5),
        (3, 1),
    ]
    assert list(Perm((9, 2, 0, 5, 3, 6, 1, 8, 7, 4)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (1, 0),
        (1, 3),
        (3, 0),
        (2, 1),
        (5, 0),
        (5, 7),
        (4, 3),
    ]
    assert list(Perm((9, 0, 6, 2, 3, 1, 4, 5, 7, 8, 10)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (1, 2),
        (3, 2),
        (1, 3),
        (4, 2),
        (6, 2),
        (2, 0),
        (8, 0),
        (0, -1),
    ]
    assert list(Perm((10, 0, 1, 2, 3, 5, 7, 6, 4, 8, 9)).left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 0),
        (5, 6),
        (4, 5),
        (6, 0),
        (9, 0),
    ]
    assert list(
        Perm((4, 10, 11, 3, 9, 7, 2, 8, 6, 1, 5, 0)).left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (0, 1),
        (0, 4),
        (-1, 3),
        (5, 4),
        (0, 5),
        (-1, 6),
        (0, 8),
        (-1, 9),
    ]
    assert list(
        Perm((3, 4, 11, 8, 9, 10, 0, 2, 5, 1, 7, 6)).left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 2),
        (3, 2),
        (4, 2),
        (-1, 0),
        (6, 0),
        (1, 3),
        (6, 7),
        (8, 3),
        (8, 10),
    ]
    assert list(
        Perm((2, 9, 8, 4, 1, 5, 10, 12, 7, 3, 11, 0, 6)).left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (0, 1),
        (0, 2),
        (-1, 0),
        (3, 2),
        (1, -1),
        (6, -1),
        (5, 2),
        (0, 3),
        (6, 7),
        (-1, 4),
        (5, 8),
    ]
    assert list(
        Perm((7, 9, 6, 3, 0, 2, 4, 12, 1, 5, 11, 10, 8)).left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (-1, 0),
        (-1, 2),
        (-1, 3),
        (4, 3),
        (3, 2),
        (1, -1),
        (4, 5),
        (6, 2),
        (1, 7),
        (1, 10),
        (0, 1),
    ]
    assert list(
        Perm((8, 3, 4, 12, 5, 13, 2, 6, 1, 7, 9, 10, 11, 0)).left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (0, -1),
        (2, 0),
        (3, -1),
        (-1, 1),
        (4, 0),
        (-1, 6),
        (7, 0),
        (0, 3),
        (10, 3),
        (11, 3),
        (-1, 8),
    ]
    assert list(
        Perm((9, 12, 8, 11, 6, 13, 1, 5, 4, 3, 10, 2, 0, 7)).left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (-1, 0),
        (0, 1),
        (-1, 2),
        (1, -1),
        (-1, 4),
        (6, 4),
        (6, 7),
        (6, 8),
        (0, 3),
        (6, 9),
        (-1, 6),
        (4, 2),
    ]
    assert list(
        Perm(
            (11, 4, 12, 1, 8, 9, 10, 14, 3, 2, 13, 0, 5, 6, 7)
        ).left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (0, -1),
        (-1, 1),
        (1, 0),
        (4, 0),
        (5, 0),
        (2, -1),
        (3, 1),
        (3, 8),
        (2, 7),
        (-1, 3),
        (1, 4),
        (12, 4),
        (13, 4),
    ]
    assert list(
        Perm(
            (8, 3, 16, 0, 17, 5, 9, 10, 6, 19, 18, 2, 11, 14, 12, 13, 15, 4, 7, 1)
        ).left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (0, -1),
        (-1, 1),
        (2, -1),
        (1, 0),
        (0, 2),
        (6, 2),
        (5, 0),
        (4, -1),
        (4, 9),
        (3, 1),
        (7, 2),
        (12, 2),
        (12, 13),
        (14, 13),
        (13, 2),
        (1, 5),
        (8, 0),
        (3, 11),
    ]


def test_count_occurrences_in():
    assert Perm([]).count_occurrences_in(Perm([4, 1, 2, 3, 0])) == 1
    assert Perm([0]).count_occurrences_in(Perm([4, 1, 2, 3, 0])) == 5
    assert Perm([0, 1]).count_occurrences_in(Perm([4, 1, 2, 3, 0])) == 3
    assert Perm([1, 0]).count_occurrences_in(Perm([4, 1, 2, 3, 0])) == 7
    assert Perm([4, 1, 2, 3, 0]).count_occurrences_in(Perm([])) == 0
    assert Perm([4, 1, 2, 3, 0]).count_occurrences_in(Perm([1, 0])) == 0


def test_count_occurrences_of():
    assert Perm([4, 1, 2, 3, 0]).count_occurrences_of(Perm([1, 0])) == 7
    assert Perm([4, 1, 2, 3, 0]).count_occurrences_of(Perm([0, 1])) == 3
    assert Perm((1, 3, 4, 0, 2, 5)).count_occurrences_of(Perm((0, 2, 1))) == 2
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        for key, val in perm.threepats().items():
            assert perm.count_occurrences_of(key) == val
        for key, val in perm.fourpats().items():
            assert perm.count_occurrences_of(key) == val


def test_occurrences_in():
    assert list(Perm([]).occurrences_in(Perm([4, 1, 2, 3, 0]))) == [()]
    assert sorted(Perm([0]).occurrences_in(Perm([4, 1, 2, 3, 0]))) == [
        (0,),
        (1,),
        (2,),
        (3,),
        (4,),
    ]
    assert sorted(Perm([0, 1]).occurrences_in(Perm([4, 1, 2, 3, 0]))) == [
        (1, 2),
        (1, 3),
        (2, 3),
    ]
    assert sorted(Perm([1, 0]).occurrences_in(Perm([4, 1, 2, 3, 0]))) == [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
    ]
    assert list(Perm([4, 1, 2, 3, 0]).occurrences_in(Perm([]))) == []
    assert list(Perm([4, 1, 2, 3, 0]).occurrences_in(Perm([1, 0]))) == []
    # Test with colours
    assert sorted(
        Perm([0]).occurrences_in(Perm([4, 1, 2, 3, 0]), [1], [0, 0, 1, 1, 0])
    ) == [(2,), (3,)]
    assert sorted(
        Perm([1, 0]).occurrences_in(Perm([4, 1, 2, 3, 0]), [1, 0], [1, 0, 1, 2, 0])
    ) == [(0, 1), (0, 4), (2, 4)]


def test_apply():
    with pytest.raises(AssertionError):
        Perm((1, 2, 4, 0, 3, 5)).apply(Perm((0, 2, 1, 3)))
    with pytest.raises(AssertionError):
        Perm().apply(Perm((0,)))

    for i in range(100):
        n = random.randint(0, 20)
        lst = [random.randint(0, 10000) for _ in range(n)]
        perm = Perm.random(n)
        res = list(perm.apply(lst))
        for j, k in enumerate(perm.inverse()):
            assert lst[j] == res[k]


def test_direct_sum():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((0, 4, 2, 1, 3))
    p3 = Perm((2, 0, 1))
    p4 = Perm((0,))
    p5 = Perm()
    # All together
    result = p1 + p2 + p3 + p4 + p5
    expected = Perm((0, 1, 3, 2, 4, 8, 6, 5, 7, 11, 9, 10, 12))
    assert result == expected
    # Two
    result = p1 + p3
    expected = Perm((0, 1, 3, 2, 6, 4, 5))
    assert result == expected
    # None
    assert p1.direct_sum() == p1
    # Arguments not a permutation
    with pytest.raises(TypeError):
        p1 + None
    with pytest.raises(TypeError):
        p1.direct_sum(p2, None)
    with pytest.raises(TypeError):
        p1.direct_sum(1237)
    with pytest.raises(TypeError):
        p5 + "hahaha"


def test_skew_sum():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((0, 4, 2, 1, 3))
    p3 = Perm((2, 0, 1))
    p4 = Perm((0,))
    p5 = Perm()
    # All together
    result = p1.skew_sum(p2, p3, p4, p5)
    expected = Perm((9, 10, 12, 11, 4, 8, 6, 5, 7, 3, 1, 2, 0))
    assert result == expected
    # Two
    result = p1 - p3
    expected = Perm((3, 4, 6, 5, 2, 0, 1))
    assert result == expected
    # None
    assert p1.skew_sum(), p1

    with pytest.raises(TypeError):
        p1 - None
    with pytest.raises(TypeError):
        p2.skew_sum(p2, None)
    with pytest.raises(TypeError):
        p3.skew_sum(1237)
    with pytest.raises(TypeError):
        p5 - "hahaha"


def test_maximal_decreasing_run():
    assert Perm((1, 3, 2, 5, 0, 4)).maximal_decreasing_run() == 2
    assert Perm((0, 1)).maximal_decreasing_run() == 1
    assert Perm((3, 1, 0, 4, 2, 5)).maximal_decreasing_run() == 1
    assert Perm((0,)).maximal_decreasing_run() == 1
    assert Perm((1, 2, 4, 0, 3, 5)).maximal_decreasing_run() == 1
    assert Perm((2, 1, 0)).maximal_decreasing_run() == 3
    assert Perm((5, 2, 4, 1, 0, 3)).maximal_decreasing_run() == 3
    assert Perm((5, 3, 2, 4, 0, 1)).maximal_decreasing_run() == 2
    assert Perm((5, 0, 4, 1, 3, 2)).maximal_decreasing_run() == 4
    assert Perm((2, 0, 5, 4, 1, 3)).maximal_decreasing_run() == 3
    assert Perm((1, 2, 0)).maximal_decreasing_run() == 1
    assert Perm((1, 0)).maximal_decreasing_run() == 2
    assert Perm((2, 0, 1)).maximal_decreasing_run() == 2
    assert Perm((0, 3, 4, 1, 2)).maximal_decreasing_run() == 1
    assert Perm(()).maximal_decreasing_run() == 0
    assert Perm((0, 3, 5, 4, 1, 2)).maximal_decreasing_run() == 2
    assert Perm((0, 1, 2)).maximal_decreasing_run() == 1
    assert Perm((4, 3, 5, 2, 1, 0)).maximal_decreasing_run() == 1
    assert Perm((1, 0, 2)).maximal_decreasing_run() == 1
    assert Perm((0, 2, 1)).maximal_decreasing_run() == 2
    for i in range(1, 100):
        assert Perm.monotone_increasing(i).maximal_decreasing_run() == 1
        assert Perm.monotone_decreasing(i).maximal_decreasing_run() == i


def test_compose():
    p0 = Perm()

    p1 = Perm((0, 3, 1, 2))
    p2 = Perm((2, 1, 0, 3))
    p3 = Perm((1, 3, 0, 2))

    p4 = Perm((1, 0, 2))
    p5 = Perm((0, 1, 2))
    p6 = Perm((2, 1, 0))
    p7 = Perm((2, 0, 1))

    assert p0.compose() == p0
    assert p1.compose() == p1
    assert p4.compose() == p4

    assert p1 * p2 == p3
    assert p1 * p3 == Perm((3, 2, 0, 1))
    assert p2 * p1 == Perm((2, 3, 1, 0))

    assert p4 * p5 * p6 == p7
    assert p5 * p6 * p7 * p4 == p7

    with pytest.raises(AssertionError):
        p1.compose(None)
    with pytest.raises(TypeError):
        p1 * None
    with pytest.raises(AssertionError):
        p2.compose(p2, None)
    with pytest.raises(AssertionError):
        p3.compose(1237)
    with pytest.raises(TypeError):
        p5 * ("hahaha")
    with pytest.raises(TypeError):
        p5 * (p1,)

    with pytest.raises(AssertionError):
        p1.compose(p0)
    with pytest.raises(AssertionError):
        p0.compose(p5)
    with pytest.raises(AssertionError):
        p2.compose(p3, p0)
    with pytest.raises(AssertionError):
        p4.compose(p5, p6, p1)


def test_insert():
    assert Perm(()).insert() == Perm((0,))
    assert Perm(()).insert(0) == Perm((0,))
    assert Perm((0, 1)).insert() == Perm((0, 1, 2))
    assert Perm((0, 1)).insert(0) == Perm((2, 0, 1))
    assert Perm((0, 1)).insert(1) == Perm((0, 2, 1))
    assert Perm((0, 1)).insert(2) == Perm((0, 1, 2))

    assert Perm((2, 0, 1)).insert(2, 1) == Perm((3, 0, 1, 2))
    assert Perm((0, 3, 1, 2)).insert(3, 4) == Perm((0, 3, 1, 4, 2))
    assert Perm((0, 3, 1, 2)).insert(3, 3) == Perm((0, 4, 1, 3, 2))
    assert Perm((0, 3, 1, 2)).insert(1, 0) == Perm((1, 0, 4, 2, 3))

    with pytest.raises(AssertionError):
        Perm((2, 1, 0, 3)).insert(2, 100)
    with pytest.raises(AssertionError):
        Perm((2, 1, 0, 3)).insert(0, 5)
    with pytest.raises(AssertionError):
        Perm((2, 1, 0, 3)).insert(3, -3)


def test_remove():
    assert Perm().remove() == Perm()
    assert Perm((2, 0, 1)).remove() == Perm((0, 1))
    assert Perm((3, 0, 1, 2)).remove(0) == Perm((0, 1, 2))
    assert Perm((2, 0, 1)).remove(2) == Perm((1, 0))
    assert Perm((0,)).remove(0) == Perm()
    assert Perm((3, 0, 1, 2)).remove(3) == Perm((2, 0, 1))
    assert Perm((0, 3, 1, 4, 2)).remove(3) == Perm((0, 3, 1, 2))
    assert Perm((0, 4, 1, 3, 2)).remove(4) == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 4, 2, 3)).remove(0) == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 4, 2, 3)).remove() == Perm((1, 0, 2, 3))
    assert Perm((0, 4, 1, 3, 2)).remove() == Perm((0, 1, 3, 2))
    with pytest.raises(IndexError):
        assert Perm((0, 5, 4, 3, 2, 1)).remove(100)


def test_remove_element():
    assert Perm().remove() == Perm()
    assert Perm((3, 0, 1, 2)).remove_element() == Perm((0, 1, 2))
    assert Perm((3, 0, 2, 1)).remove_element(0) == Perm((2, 1, 0))
    assert Perm((3, 0, 1, 2)).remove_element(1) == Perm((2, 0, 1))
    assert Perm((0, 3, 1, 4, 2)).remove_element(4) == Perm((0, 3, 1, 2))
    assert Perm((0, 4, 1, 3, 2)).remove_element(2) == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 4, 2, 3)).remove_element(1) == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 4, 2, 3)).remove_element() == Perm((1, 0, 2, 3))
    assert Perm((0, 4, 1, 3, 2)).remove_element() == Perm((0, 1, 3, 2))

    with pytest.raises(AssertionError):
        Perm((1, 0, 4, 2, 3)).remove_element(5)
    with pytest.raises(AssertionError):
        Perm((1, 0, 4, 2, 3)).remove_element(51)
    with pytest.raises(AssertionError):
        Perm((1, 0, 4, 2, 3)).remove_element(-5)


def test_inflate():
    assert Perm((0, 1)).inflate([Perm((1, 0)), Perm((2, 1, 0))]) == Perm(
        (1, 0, 4, 3, 2)
    )
    assert Perm((1, 0, 2)).inflate([None, Perm((0, 1)), Perm((0, 1))]) == Perm(
        (2, 0, 1, 3, 4)
    )
    assert Perm((0, 1)).inflate([Perm(), Perm()]) == Perm()


def test_contract_inc_bonds():
    assert Perm().contract_inc_bonds() == Perm()
    assert Perm((0,)).contract_inc_bonds() == Perm((0,))
    assert Perm((0, 1)).contract_inc_bonds() == Perm((0,))
    assert Perm((0, 1, 2)).contract_inc_bonds() == Perm((0,))
    assert Perm((2, 1, 0)).contract_inc_bonds() == Perm((2, 1, 0))
    assert Perm((0, 3, 1, 4, 2)).contract_inc_bonds() == Perm((0, 3, 1, 4, 2))
    assert Perm((1, 0, 4, 2, 3)).contract_inc_bonds() == Perm((1, 0, 3, 2))
    assert Perm((1, 0, 2, 3, 4)).contract_inc_bonds() == Perm((1, 0, 2))
    assert Perm((0, 4, 1, 2, 3)).contract_inc_bonds() == Perm((0, 2, 1))


def test_contract_dec_bonds():
    assert Perm().contract_dec_bonds() == Perm()
    assert Perm((0,)).contract_dec_bonds() == Perm((0,))
    assert Perm((2, 1)).contract_dec_bonds() == Perm((0,))
    assert Perm((2, 1, 0)).contract_dec_bonds() == Perm((0,))
    assert Perm((0, 1, 2)).contract_dec_bonds() == Perm((0, 1, 2))
    assert Perm((0, 3, 1, 4, 2)).contract_dec_bonds() == Perm((0, 3, 1, 4, 2))
    assert Perm((0, 4, 3, 2, 1)).contract_dec_bonds() == Perm((0, 1))
    assert Perm((1, 0, 4, 2, 3)).contract_dec_bonds() == Perm((0, 3, 1, 2))
    assert Perm((0, 4, 1, 3, 2)).contract_dec_bonds() == Perm((0, 3, 1, 2))


def test_contract_bonds():
    assert Perm().contract_bonds() == Perm()
    assert Perm((0,)).contract_bonds() == Perm((0,))
    assert Perm((1, 0)).contract_bonds() == Perm((0,))
    assert Perm((0, 1)).contract_bonds() == Perm((0,))
    assert Perm((2, 1, 0)).contract_bonds() == Perm((0,))
    assert Perm((0, 1, 2)).contract_bonds() == Perm((0,))
    assert Perm((0, 3, 1, 4, 2)).contract_bonds() == Perm((0, 3, 1, 4, 2))
    assert Perm((0, 4, 3, 2, 1)).contract_bonds() == Perm((0, 1))
    assert Perm((1, 0, 4, 2, 3)).contract_bonds() == Perm((0, 2, 1))
    assert Perm((0, 4, 1, 3, 2)).contract_bonds() == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 2, 3, 4)).contract_bonds() == Perm((0, 1))


def test_inverse():
    for i in range(10):
        assert Perm(range(i)) == Perm(range(i)).inverse()
    assert Perm([2, 1, 3, 0]) == Perm([3, 1, 0, 2]).inverse()
    assert Perm((1, 2, 5, 0, 3, 4)).inverse() == Perm((3, 0, 1, 4, 5, 2))
    assert (
        Perm([4, 3, 1, 6, 5, 7, 8, 0, 2]) == Perm([7, 2, 8, 1, 0, 4, 3, 5, 6]).inverse()
    )


def test_reverse():
    assert Perm([5, 2, 3, 0, 4, 6, 1]) == Perm([1, 6, 4, 0, 3, 2, 5]).reverse()
    assert Perm([7, 1, 0, 2, 4, 6, 3, 5]) == Perm([5, 3, 6, 4, 2, 0, 1, 7]).reverse()


def test_complement():
    assert Perm().complement() == Perm()
    assert Perm((0,)).complement() == Perm((0,))
    assert Perm((1, 2, 3, 0, 4)).complement() == Perm((3, 2, 1, 4, 0))
    assert Perm((2, 0, 1)).complement() == Perm((0, 2, 1))
    assert Perm([6, 4, 2, 3, 1, 0, 5]).complement() == Perm([0, 2, 4, 3, 5, 6, 1])
    assert Perm([2, 5, 6, 3, 7, 4, 0, 1]).complement() == Perm([5, 2, 1, 4, 0, 3, 7, 6])


def test_reverse_complement():
    for _ in range(100):
        perm = Perm.random(random.randint(0, 20))
        assert perm.reverse_complement() == perm.rotate().rotate()


def test_rotate_right():
    for i in range(10):
        assert Perm(range(i - 1, -1, -1)) == Perm(range(i)).rotate()
    assert Perm([2, 1, 3, 4, 0, 5, 6]) == Perm([6, 5, 3, 2, 0, 1, 4]).rotate()
    assert Perm([4, 5, 3, 1, 7, 0, 2, 6]) == Perm([4, 7, 1, 0, 2, 6, 3, 5]).rotate()
    assert Perm([0, 1, 2]) == Perm([2, 1, 0]).rotate(5)
    assert Perm([4, 5, 3, 1, 0, 2]) == Perm([4, 5, 3, 1, 0, 2]).rotate(4)


def test_rotate_left():
    for i in range(10):
        assert Perm(list(range(i - 1, -1, -1))) == Perm(range(i)).rotate()
    assert Perm([6, 5, 3, 2, 0, 1, 4]).rotate(-1) == Perm([6, 5, 3, 2, 0, 1, 4]).rotate(
        3
    )
    assert Perm([4, 7, 1, 0, 2, 6, 3, 5]).rotate(-1) == Perm(
        [4, 7, 1, 0, 2, 6, 3, 5]
    ).rotate(7)
    assert Perm([]).rotate(-1) == Perm([]).rotate(-123)


def test_shift_left():
    assert Perm([]) == Perm([]).shift_left()
    assert Perm([0]) == Perm([0]).shift_left()
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([0, 1, 2, 3, 4, 5, 6, 7]).shift_left(
        0
    )
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([5, 6, 7, 0, 1, 2, 3, 4]).shift_left(
        3
    )
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([0, 1, 2, 3, 4, 5, 6, 7]).shift_left(
        800
    )
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([5, 6, 7, 0, 1, 2, 3, 4]).shift_left(
        403
    )
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([0, 1, 2, 3, 4, 5, 6, 7]).shift_left(
        -8
    )
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([5, 6, 7, 0, 1, 2, 3, 4]).shift_left(
        -5
    )


def test_shift_down():
    assert Perm([]) == Perm([]).shift_down(1000)
    assert Perm([0]) == Perm([0]).shift_down(10)
    assert Perm([1, 0, 4, 2, 3, 5]) == Perm([2, 1, 5, 3, 4, 0]).shift_down()
    assert Perm([1, 0, 4, 2, 3, 5]) == Perm([2, 1, 5, 3, 4, 0]).shift_down(13)
    assert Perm([1, 0, 4, 2, 3, 5]) == Perm([5, 4, 2, 0, 1, 3]).shift_down(-2)
    assert Perm([1, 0, 4, 2, 3, 5]) == Perm([5, 4, 2, 0, 1, 3]).shift_down(-8)


def test_flip_horizontal():
    assert Perm().flip_horizontal() == Perm()
    assert Perm((0,)).flip_horizontal() == Perm((0,))
    assert Perm((1, 2, 3, 0, 4)).flip_horizontal() == Perm((3, 2, 1, 4, 0))
    assert Perm((2, 0, 1)).flip_horizontal() == Perm((0, 2, 1))
    assert Perm([6, 4, 2, 3, 1, 0, 5]).flip_horizontal() == Perm([0, 2, 4, 3, 5, 6, 1])
    assert Perm([2, 5, 6, 3, 7, 4, 0, 1]).flip_horizontal() == Perm(
        [5, 2, 1, 4, 0, 3, 7, 6]
    )


def test_flip_vertical():
    assert Perm().flip_vertical() == Perm()
    assert Perm((0,)).flip_vertical() == Perm((0,))
    assert Perm((0, 1)).flip_vertical() == Perm((1, 0))
    assert Perm((1, 2, 5, 0, 3, 4)).flip_vertical() == Perm((4, 3, 0, 5, 2, 1))
    assert Perm([5, 2, 3, 0, 4, 6, 1]).reverse() == Perm([1, 6, 4, 0, 3, 2, 5])
    assert Perm([7, 1, 0, 2, 4, 6, 3, 5]).reverse() == Perm([5, 3, 6, 4, 2, 0, 1, 7])


def test_flip_diagonal():
    for i in range(10):
        assert Perm(range(i)) == Perm(range(i)).flip_diagonal()
    assert Perm([2, 1, 3, 0]) == Perm([3, 1, 0, 2]).flip_diagonal()
    assert Perm((1, 2, 5, 0, 3, 4)).flip_diagonal() == Perm((3, 0, 1, 4, 5, 2))
    assert (
        Perm([4, 3, 1, 6, 5, 7, 8, 0, 2])
        == Perm([7, 2, 8, 1, 0, 4, 3, 5, 6]).flip_diagonal()
    )


def test_flip_antidiagonal():
    for i in range(100):
        perm = Perm.random(random.randint(0, 20))
        assert perm.reverse().complement().inverse() == perm.flip_antidiagonal()


def test_rotate_180():
    for _ in range(100):
        perm = Perm.random(random.randint(0, 20))
        assert perm.rotate(times=2) == perm.rotate().rotate()


def test_all_syms():
    assert list(sorted(Perm((0,)).all_syms())) == [Perm((0,))]
    assert list(sorted(Perm((0, 2, 1)).all_syms())) == [
        Perm((0, 2, 1)),
        Perm((1, 0, 2)),
        Perm((1, 2, 0)),
        Perm((2, 0, 1)),
    ]
    assert set(Perm((2, 1, 5, 3, 4, 0)).all_syms()) == {
        Perm((3, 4, 0, 2, 1, 5)),
        Perm((0, 4, 5, 2, 1, 3)),
        Perm((2, 4, 3, 0, 1, 5)),
        Perm((5, 1, 0, 3, 4, 2)),
        Perm((0, 4, 3, 5, 1, 2)),
        Perm((3, 1, 2, 5, 4, 0)),
        Perm((2, 1, 5, 3, 4, 0)),
        Perm((5, 1, 2, 0, 4, 3)),
    }
    assert set(Perm((1, 3, 4, 0, 2)).all_syms()) == {
        Perm((3, 1, 0, 4, 2)),
        Perm((1, 4, 0, 3, 2)),
        Perm((1, 3, 4, 0, 2)),
        Perm((2, 3, 0, 4, 1)),
        Perm((2, 0, 4, 3, 1)),
        Perm((2, 1, 4, 0, 3)),
        Perm((2, 4, 0, 1, 3)),
        Perm((3, 0, 4, 1, 2)),
    }
    assert set(Perm((2, 1, 0)).all_syms()) == {Perm((2, 1, 0)), Perm((0, 1, 2))}
    assert set(Perm((0, 2, 1, 3, 4)).all_syms()) == {
        Perm((4, 2, 3, 1, 0)),
        Perm((0, 1, 3, 2, 4)),
        Perm((0, 2, 1, 3, 4)),
        Perm((4, 3, 1, 2, 0)),
    }
    assert set(Perm((2, 1, 0)).all_syms()) == {Perm((2, 1, 0)), Perm((0, 1, 2))}
    assert set(Perm(()).all_syms()) == {Perm(())}
    assert set(Perm((0,)).all_syms()) == {Perm((0,))}
    assert set(Perm((3, 1, 6, 8, 5, 7, 4, 0, 2)).all_syms()) == {
        Perm((5, 7, 2, 0, 3, 1, 4, 8, 6)),
        Perm((2, 0, 4, 7, 5, 8, 6, 1, 3)),
        Perm((3, 5, 2, 4, 6, 0, 8, 1, 7)),
        Perm((6, 8, 4, 1, 3, 0, 2, 7, 5)),
        Perm((3, 1, 6, 8, 5, 7, 4, 0, 2)),
        Perm((5, 3, 6, 4, 2, 8, 0, 7, 1)),
        Perm((7, 1, 8, 0, 6, 4, 2, 5, 3)),
        Perm((1, 7, 0, 8, 2, 4, 6, 3, 5)),
    }
    assert set(Perm((6, 1, 3, 2, 5, 0, 4)).all_syms()) == {
        Perm((4, 0, 5, 2, 3, 1, 6)),
        Perm((6, 2, 0, 4, 3, 5, 1)),
        Perm((2, 6, 1, 4, 3, 5, 0)),
        Perm((0, 4, 6, 2, 3, 1, 5)),
        Perm((6, 1, 3, 2, 5, 0, 4)),
        Perm((1, 5, 3, 4, 0, 2, 6)),
        Perm((0, 5, 3, 4, 1, 6, 2)),
        Perm((5, 1, 3, 2, 6, 4, 0)),
    }
    assert set(Perm((1, 0)).all_syms()) == {Perm((1, 0)), Perm((0, 1))}


def test_fixed_points():
    assert list(Perm().fixed_points()) == []
    assert list(Perm((0, 2, 1)).fixed_points()) == [0]
    assert list(Perm((5, 4, 3, 2, 1, 0)).fixed_points()) == []
    assert list(Perm((4, 1, 0, 3, 2, 5)).fixed_points()) == [1, 3, 5]
    assert list(Perm((0, 1, 2, 3, 4, 5)).fixed_points()) == [0, 1, 2, 3, 4, 5]


def test_strong_fixed_points():
    assert list(Perm().strong_fixed_points()) == []
    assert list(Perm((5, 4, 3, 2, 1, 0)).strong_fixed_points()) == []
    assert list(Perm((4, 1, 0, 3, 2, 5)).strong_fixed_points()) == [5]
    assert list(Perm((0, 1, 2, 3, 4, 5)).strong_fixed_points()) == [0, 1, 2, 3, 4, 5]
    assert list(Perm((0, 1)).strong_fixed_points()) == [0, 1]
    assert list(Perm((0,)).strong_fixed_points()) == [0]
    assert list(Perm((2, 1, 0)).strong_fixed_points()) == []
    assert list(Perm((2, 0, 7, 4, 1, 5, 3, 6)).strong_fixed_points()) == []
    assert list(Perm((6, 4, 5, 3, 2, 0, 1)).strong_fixed_points()) == []
    assert list(Perm((4, 7, 2, 6, 0, 1, 5, 3)).strong_fixed_points()) == []
    assert list(Perm((0, 1, 2)).strong_fixed_points()) == [0, 1, 2]
    assert list(Perm((1, 6, 4, 3, 2, 0, 7, 5)).strong_fixed_points()) == []
    assert list(Perm((4, 1, 2, 6, 3, 5, 0)).strong_fixed_points()) == []
    assert list(Perm((5, 1, 0, 7, 4, 2, 3, 6)).strong_fixed_points()) == []
    assert list(Perm((0, 6, 5, 4, 3, 2, 1, 7)).strong_fixed_points()) == [0, 7]
    assert list(Perm((1, 4, 6, 2, 3, 5, 7, 0)).strong_fixed_points()) == []
    assert list(Perm((1, 3, 2, 0, 4, 6, 7, 5)).strong_fixed_points()) == [4]
    assert list(Perm((0, 1, 5, 4, 6, 3, 2, 7)).strong_fixed_points()) == [0, 1, 7]
    assert list(Perm((5, 6, 0, 2, 4, 3, 7, 1)).strong_fixed_points()) == []
    assert list(Perm((3, 6, 2, 5, 1, 4, 7, 0)).strong_fixed_points()) == []
    assert list(Perm((7, 6, 2, 3, 0, 1, 4, 5)).strong_fixed_points()) == []
    assert list(Perm((0, 2, 1)).strong_fixed_points()) == [0]
    assert list(Perm((7, 3, 2, 4, 5, 1, 6, 0)).strong_fixed_points()) == []
    assert list(Perm((1, 0, 2)).strong_fixed_points()) == [2]
    assert list(Perm((5, 3, 0, 6, 1, 4, 2, 7)).strong_fixed_points()) == [7]
    assert list(Perm((7, 1, 2, 3, 4, 5, 6, 0)).strong_fixed_points()) == []
    assert list(Perm((1, 0, 2, 4, 3, 5, 7, 6)).strong_fixed_points()) == [2, 5]


def test_count_fixed_points():
    assert Perm().count_fixed_points() == 0
    assert Perm((0, 2, 1)).count_fixed_points() == 1
    assert Perm((5, 4, 3, 2, 1, 0)).count_fixed_points() == 0
    assert Perm((4, 1, 0, 3, 2, 5)).count_fixed_points() == 3
    assert Perm((0, 1, 2, 3, 4, 5)).count_fixed_points() == 6


def test_is_skew_decomposable():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((0, 4, 2, 1, 3))
    p3 = Perm((2, 0, 1))
    p4 = Perm((0,))
    p5 = Perm()

    assert p1.skew_sum(p2).is_skew_decomposable()
    assert p1.skew_sum(p2, p3).is_skew_decomposable()
    assert p1.skew_sum(p2, p3, p4).is_skew_decomposable()
    assert p2.skew_sum(p3, p4).is_skew_decomposable()
    assert not p5.is_skew_decomposable()

    assert not Perm((0, 1, 2, 3, 4)).is_skew_decomposable()
    assert not Perm((0, 5, 4, 3, 2, 1)).is_skew_decomposable()


def test_skew_decomposition():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((0, 4, 2, 1, 3))
    p3 = Perm((2, 0, 1))
    p4 = Perm((0,))
    p5 = Perm()
    p6 = Perm((0, 1))

    assert p3.skew_decomposition() == [p4, p6]
    assert p1.skew_sum(p2).skew_decomposition() == [p1, p2]
    assert p1.skew_sum(p2, p3).skew_decomposition() == [p1, p2, p4, p6]
    assert p1.skew_sum(p2, p3, p4).skew_decomposition() == [p1, p2, p4, p6, p4]
    assert p5.skew_decomposition() == []
    assert p4.skew_decomposition() == [p4]
    assert p1.skew_decomposition() == [p1]
    assert Perm((0, 1, 2, 3, 4)).skew_decomposition() == [Perm((0, 1, 2, 3, 4))]
    assert Perm((0, 5, 4, 3, 2, 1)).skew_decomposition() == [Perm((0, 5, 4, 3, 2, 1))]


def test_is_sum_decomposable():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((4, 2, 1, 3, 0))
    p3 = Perm((2, 0, 1))
    p4 = Perm((0,))
    p5 = Perm()

    assert p1.is_sum_decomposable()
    assert p1.direct_sum(p2, p3).is_sum_decomposable()
    assert p1.direct_sum(p2, p3, p4).is_sum_decomposable()
    assert p1.direct_sum(p2, p3, p4, p5).is_sum_decomposable()

    assert not p2.is_sum_decomposable()
    assert not p3.is_sum_decomposable()
    assert not Perm((4, 3, 2, 1, 0)).is_sum_decomposable()


def test_sum_decomposition():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((4, 2, 1, 3, 0))
    p3 = Perm((2, 0, 1))
    p4 = Perm((0,))
    p5 = Perm()
    p6 = Perm((1, 0))

    assert p1.sum_decomposition() == [p4, p4, p6]
    assert p1.direct_sum(p2, p3).sum_decomposition() == [p4, p4, p6, p2, p3]
    assert p1.direct_sum(p2, p3, p4).sum_decomposition() == [
        p4,
        p4,
        p6,
        p2,
        p3,
        p4,
    ]
    assert p4.sum_decomposition() == [p4]
    assert p5.sum_decomposition() == []
    assert p2.sum_decomposition() == [p2]
    assert p3.sum_decomposition() == [p3]
    assert Perm((4, 3, 2, 1, 0)).sum_decomposition() == [Perm((4, 3, 2, 1, 0))]


def test_descent_set():
    assert Perm().descent_set() == []
    assert Perm().descent_set(step_size=2) == []

    assert Perm((0, 1, 2, 3)).descent_set() == []
    assert Perm((0, 1, 2, 3)).descent_set(step_size=2) == []

    assert Perm((3, 2, 1, 0)).descent_set() == [0, 1, 2]
    assert Perm((3, 2, 1, 0)).descent_set(step_size=1) == [0, 1, 2]
    assert Perm((3, 2, 1, 0)).descent_set(step_size=2) == []

    assert Perm((2, 1, 0, 4, 3, 5)).descent_set() == [0, 1, 3]
    assert Perm((2, 1, 0, 4, 3, 5)).descent_set(step_size=1) == [0, 1, 3]
    assert Perm((2, 1, 0, 4, 3, 5)).descent_set(step_size=2) == []

    assert Perm((1, 2, 3, 0, 6, 5, 4)).descent_set() == [2, 4, 5]
    assert Perm((1, 2, 3, 0, 6, 5, 4)).descent_set(step_size=1) == [4, 5]
    assert Perm((1, 2, 3, 0, 6, 5, 4)).descent_set(step_size=2) == []
    assert Perm((1, 2, 3, 0, 6, 5, 4)).descent_set(step_size=3) == [2]

    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).descent_set() == [0, 3, 5, 6]
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).descent_set(step_size=1) == [5]
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).descent_set(step_size=2) == [0]
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).descent_set(step_size=3) == []
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).descent_set(step_size=4) == [6]
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).descent_set(step_size=5) == [3]


def test_count_descents():
    assert Perm().count_descents() == 0
    assert Perm().count_descents(step_size=2) == 0

    assert Perm((0, 1, 2, 3)).count_descents() == 0
    assert Perm((0, 1, 2, 3)).count_descents(step_size=2) == 0

    assert Perm((3, 2, 1, 0)).count_descents() == 3
    assert Perm((3, 2, 1, 0)).count_descents(step_size=1) == 3
    assert Perm((3, 2, 1, 0)).count_descents(step_size=2) == 0

    assert Perm((2, 1, 0, 4, 3, 5)).count_descents() == 3
    assert Perm((2, 1, 0, 4, 3, 5)).count_descents(step_size=1) == 3
    assert Perm((2, 1, 0, 4, 3, 5)).count_descents(step_size=2) == 0

    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_descents() == 3
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_descents(step_size=1) == 2
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_descents(step_size=2) == 0
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_descents(step_size=3) == 1

    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_descents() == 4
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_descents(step_size=1) == 1
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_descents(step_size=2) == 1
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_descents(step_size=3) == 0
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_descents(step_size=4) == 1
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_descents(step_size=5) == 1


def test_ascent_set():
    assert Perm().ascent_set() == []
    assert Perm().ascent_set(step_size=2) == []

    assert Perm((0, 1, 2, 3)).ascent_set() == [0, 1, 2]
    assert Perm((0, 1, 2, 3)).ascent_set(step_size=1) == [0, 1, 2]
    assert Perm((0, 1, 2, 3)).ascent_set(step_size=2) == []

    assert Perm((3, 2, 1, 0)).ascent_set() == []
    assert Perm((3, 2, 1, 0)).ascent_set(step_size=2) == []

    assert Perm((2, 1, 0, 4, 3, 5)).ascent_set() == [2, 4]
    assert Perm((2, 1, 0, 4, 3, 5)).ascent_set(step_size=1) == []
    assert Perm((2, 1, 0, 4, 3, 5)).ascent_set(step_size=2) == [4]
    assert Perm((2, 1, 0, 4, 3, 5)).ascent_set(step_size=3) == []
    assert Perm((2, 1, 0, 4, 3, 5)).ascent_set(step_size=4) == [2]

    assert Perm((1, 2, 3, 0, 6, 5, 4)).ascent_set() == [0, 1, 3]
    assert Perm((1, 2, 3, 0, 6, 5, 4)).ascent_set(step_size=1) == [0, 1]
    assert Perm((1, 2, 3, 0, 6, 5, 4)).ascent_set(step_size=2) == []
    assert Perm((1, 2, 3, 0, 6, 5, 4)).ascent_set(step_size=3) == []
    assert Perm((1, 2, 3, 0, 6, 5, 4)).ascent_set(step_size=4) == []
    assert Perm((1, 2, 3, 0, 6, 5, 4)).ascent_set(step_size=5) == []
    assert Perm((1, 2, 3, 0, 6, 5, 4)).ascent_set(step_size=6) == [3]

    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).ascent_set() == [1, 2, 4]
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).ascent_set(step_size=1) == [2]
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).ascent_set(step_size=2) == []
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).ascent_set(step_size=3) == [1]
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).ascent_set(step_size=4) == []
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).ascent_set(step_size=5) == []
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).ascent_set(step_size=6) == []
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).ascent_set(step_size=7) == [4]


def test_count_ascents():
    assert Perm().count_ascents() == 0

    assert Perm((0, 1, 2, 3)).count_ascents() == 3
    assert Perm((0, 1, 2, 3)).count_ascents(step_size=1) == 3
    assert Perm((0, 1, 2, 3)).count_ascents(step_size=2) == 0

    assert Perm((3, 2, 1, 0)).count_ascents() == 0
    assert Perm((3, 2, 1, 0)).count_ascents(step_size=1) == 0
    assert Perm((3, 2, 1, 0)).count_ascents(step_size=2) == 0

    assert Perm((2, 1, 0, 4, 3, 5)).count_ascents() == 2
    assert Perm((2, 1, 0, 4, 3, 5)).count_ascents(step_size=1) == 0
    assert Perm((2, 1, 0, 4, 3, 5)).count_ascents(step_size=2) == 1
    assert Perm((2, 1, 0, 4, 3, 5)).count_ascents(step_size=3) == 0
    assert Perm((2, 1, 0, 4, 3, 5)).count_ascents(step_size=4) == 1

    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_ascents() == 3
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_ascents(step_size=1) == 2
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_ascents(step_size=2) == 0
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_ascents(step_size=3) == 0
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_ascents(step_size=4) == 0
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_ascents(step_size=5) == 0
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_ascents(step_size=6) == 1

    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_ascents() == 3
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_ascents(step_size=1) == 1
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_ascents(step_size=2) == 0
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_ascents(step_size=3) == 1
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_ascents(step_size=4) == 0
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_ascents(step_size=5) == 0
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_ascents(step_size=6) == 0
    assert Perm((3, 1, 4, 5, 0, 7, 6, 2)).count_ascents(step_size=7) == 1


def test_peaks():
    assert list(Perm().peaks()) == []
    assert list(Perm((0, 1, 2, 3)).peaks()) == []
    assert list(Perm((0, 1, 2, 4, 3)).peaks()) == [3]
    assert list(Perm((2, 1, 0, 4, 3, 5)).peaks()) == [3]
    assert list(Perm((1, 2, 3, 0, 6, 5, 4)).peaks()) == [2, 4]


def test_peak_list():
    assert Perm().peak_list() == []
    assert Perm((0, 1, 2, 3)).peak_list() == []
    assert Perm((0, 1, 2, 4, 3)).peak_list() == [3]
    assert Perm((2, 1, 0, 4, 3, 5)).peak_list() == [3]
    assert Perm((1, 2, 3, 0, 6, 5, 4)).peak_list() == [2, 4]


def test_count_peaks():
    assert Perm().count_peaks() == 0
    assert Perm((0, 1, 2, 3)).count_peaks() == 0
    assert Perm((2, 1, 0, 4, 3, 5)).count_peaks() == 1
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_peaks() == 2


def test_valleys():
    assert list(Perm().valleys()) == []
    assert list(Perm((0, 1, 2, 3)).valleys()) == []
    assert list(Perm((2, 1, 0, 4, 3, 5)).valleys()) == [2, 4]
    assert list(Perm((1, 2, 3, 0, 6, 5, 4)).valleys()) == [3]
    assert list(Perm((2, 1, 3, 0, 6, 4, 5)).valleys()) == [1, 3, 5]


def test_valley_list():
    assert Perm().valley_list() == []
    assert Perm((0, 1, 2, 3)).valley_list() == []
    assert Perm((2, 1, 0, 4, 3, 5)).valley_list() == [2, 4]
    assert Perm((1, 2, 3, 0, 6, 5, 4)).valley_list() == [3]
    assert Perm((2, 1, 3, 0, 6, 4, 5)).valley_list() == [1, 3, 5]


def test_count_valleys():
    assert Perm().count_valleys() == 0
    assert Perm((0, 1, 2, 3)).count_valleys() == 0
    assert Perm((2, 1, 0, 4, 3, 5)).count_valleys() == 2
    assert Perm((1, 2, 3, 0, 6, 5, 4)).count_valleys() == 1
    assert Perm((2, 1, 3, 0, 6, 4, 6)).count_valleys() == 3


def test_bends():
    assert list(Perm().bends()) == []
    assert list(Perm((0, 1)).bends()) == []
    assert list(Perm((2, 0, 1)).bends()) == [1]
    assert list(Perm((5, 3, 4, 0, 2, 1)).bends()) == [
        1,
        2,
        3,
        4,
    ]
    assert list(Perm((4, 3, 5, 7, 6, 9, 1, 2, 8, 0)).bends()) == [1, 3, 4, 5, 6, 8]
    assert list(Perm((6, 4, 3, 0, 1, 7, 2, 5, 8, 9)).bends()) == [3, 5, 6]


def test_bend_list():
    assert Perm().bend_list() == []
    assert Perm((0, 1)).bend_list() == []
    assert Perm((2, 0, 1)).bend_list() == [1]
    assert Perm((5, 3, 4, 0, 2, 1)).bend_list() == [
        1,
        2,
        3,
        4,
    ]
    assert Perm((4, 3, 5, 7, 6, 9, 1, 2, 8, 0)).bend_list() == [1, 3, 4, 5, 6, 8]
    assert Perm((6, 4, 3, 0, 1, 7, 2, 5, 8, 9)).bend_list() == [3, 5, 6]


def test_order():
    assert Perm().order() == 1
    assert Perm((0,)).order() == 1
    perm = Perm((4, 5, 2, 0, 6, 1, 3))
    args = tuple(perm for _ in range(perm.order() - 1))
    assert perm.compose(*args).is_identity()
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        args = tuple(perm for _ in range(perm.order() - 1))
        assert perm.compose(*args).is_identity()


def test_ltrmin():
    assert list(Perm().ltrmin()) == []
    assert list(Perm((0,)).ltrmin()) == [0]
    assert list(Perm((2, 4, 3, 0, 1)).ltrmin()) == [0, 3]
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        ltrmin_list = list(perm.ltrmin())
        assert ltrmin_list[0] == 0
        for i in range(len(ltrmin_list)):
            for j in range(ltrmin_list[i] + 1, len(perm)):
                if perm[j] < perm[ltrmin_list[i]]:
                    assert ltrmin_list[i + 1] == j
                    break


def test_rtlmin():
    assert list(Perm().rtlmin()) == []
    assert list(Perm((0,)).rtlmin()) == [0]
    assert list(Perm((2, 4, 3, 0, 1)).rtlmin()) == [3, 4]
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        rtlmin_list = list(perm.rtlmin())
        rtlmin_list.reverse()
        assert rtlmin_list[0] == len(perm) - 1
        for i in range(len(rtlmin_list)):
            for j in range(rtlmin_list[i] - 1, -1, -1):
                if perm[j] < perm[rtlmin_list[i]]:
                    assert rtlmin_list[i + 1] == j
                    break


def test_ltrmax():
    assert list(Perm().ltrmax()) == []
    assert list(Perm((0,)).ltrmax()) == [0]
    assert list(Perm((2, 0, 4, 1, 5, 3)).ltrmax()) == [0, 2, 4]
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        ltrmax_list = list(perm.ltrmax())
        assert ltrmax_list[0] == 0
        for i in range(len(ltrmax_list)):
            for j in range(ltrmax_list[i] + 1, len(perm)):
                if perm[j] > perm[ltrmax_list[i]]:
                    assert ltrmax_list[i + 1] == j
                    break


def test_rtlmax():
    assert list(Perm().rtlmax()) == []
    assert list(Perm((0,)).rtlmax()) == [0]
    assert list(Perm((2, 4, 3, 0, 1)).rtlmax()) == [1, 2, 4]
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        rtlmax_list = list(perm.rtlmax())
        rtlmax_list.reverse()
        assert rtlmax_list[0] == len(perm) - 1
        for i in range(len(rtlmax_list)):
            for j in range(rtlmax_list[i] - 1, -1, -1):
                if perm[j] > perm[rtlmax_list[i]]:
                    assert rtlmax_list[i + 1] == j
                    break


def test_count_ltrmin():
    assert Perm().count_ltrmin() == 0
    assert Perm((0,)).count_ltrmin() == 1
    assert Perm((0, 1)).count_ltrmin() == 1
    assert Perm((4, 0, 6, 3, 2, 1, 5, 8, 7, 9)).count_ltrmin() == 2
    assert Perm((5, 7, 3, 4, 6, 8, 2, 9, 0, 1)).count_ltrmin() == 4
    assert Perm((3, 1, 5, 9, 6, 4, 7, 8, 2, 0)).count_ltrmin() == 3


def test_inversions():
    assert list(Perm().inversions()) == []
    assert list(Perm((0,)).inversions()) == []
    assert list(Perm((0, 1)).inversions()) == []
    assert list(Perm((1, 0)).inversions()) == [(0, 1)]
    assert list(Perm((3, 0, 2, 1)).inversions()) == [(0, 1), (0, 2), (0, 3), (2, 3)]


def test_count_inversions():
    assert Perm().count_inversions() == 0
    assert Perm((0,)).count_inversions() == 0
    assert Perm((0, 1)).count_inversions() == 0
    assert Perm((1, 0)).count_inversions() == 1
    for _ in range(50):
        perm = Perm.random(random.randint(0, 20))
        invs = 0
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if perm[i] > perm[j]:
                    invs += 1
        assert perm.count_inversions() == invs


def test_non_inversions():
    assert list(Perm().non_inversions()) == []
    assert list(Perm((0,)).non_inversions()) == []
    assert list(Perm((0, 1)).non_inversions()) == [(0, 1)]
    assert list(Perm((1, 0)).non_inversions()) == []
    assert list(Perm((3, 0, 2, 1, 4)).non_inversions()) == [
        (0, 4),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 4),
        (3, 4),
    ]


def test_count_non_inversions():
    assert Perm().count_non_inversions() == 0
    assert Perm((0,)).count_non_inversions() == 0
    assert Perm((0, 1)).count_non_inversions() == 1
    assert Perm((1, 0)).count_non_inversions() == 0
    for _ in range(50):
        perm = Perm.random(random.randint(0, 20))
        invs = 0
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if perm[i] < perm[j]:
                    invs += 1
        assert perm.count_non_inversions() == invs


def test_all_bonds():
    assert list(Perm().all_bonds()) == []
    assert list(Perm((0, 1, 4, 2, 3)).all_bonds()) == [0, 3]
    assert list(Perm((0,)).all_bonds()) == []
    assert list(Perm.identity(10).all_bonds()) == list(range(9))
    assert list(Perm.monotone_decreasing(10).all_bonds()) == list(range(9))


def test_count_bonds():
    assert Perm().count_bonds() == 0
    assert Perm((0,)).count_bonds() == 0
    for _ in range(50):
        perm = Perm.random(random.randint(0, 20))
        bons = 0
        for i in range(len(perm) - 1):
            if perm[i] + 1 == perm[i + 1] or perm[i] == perm[i + 1] + 1:
                bons += 1
        assert bons == perm.count_bonds()


def test_inc_bonds():
    assert list(Perm().inc_bonds()) == []
    assert list(Perm((1, 0, 4, 2, 3)).inc_bonds()) == [3]
    assert list(Perm((0,)).inc_bonds()) == []
    assert list(Perm.identity(10).inc_bonds()) == list(range(9))
    assert list(Perm.monotone_decreasing(10).inc_bonds()) == []


def test_count_inc_bonds():
    assert Perm((0, 2, 3, 1)).count_inc_bonds() == 1
    assert Perm((2, 3, 4, 5, 0, 1)).count_inc_bonds() == 4


def test_dec_bonds():
    assert list(Perm().dec_bonds()) == []
    assert list(Perm((1, 0, 4, 2, 3)).dec_bonds()) == [0]
    assert list(Perm((0,)).dec_bonds()) == []
    assert list(Perm.identity(10).dec_bonds()) == []
    assert list(Perm.monotone_decreasing(10).dec_bonds()) == list(range(9))


def test_count_dec_bonds():
    assert Perm((2, 1, 0, 3)).count_dec_bonds() == 2
    assert Perm((1, 0, 3, 2, 5, 4)).count_dec_bonds() == 3


def test_major_index():
    assert Perm().major_index() == 0
    assert Perm((0,)).major_index() == 0
    assert Perm((0, 2, 1)).major_index() == 2
    assert Perm((3, 1, 2, 4, 0)).major_index() == 5
    assert Perm((3, 0, 7, 4, 1, 2, 5, 6)).major_index() == 8
    assert Perm((7, 0, 4, 3, 1, 5, 2, 6)).major_index() == 14


def test_depth():
    # From http://www.findstat.org/StatisticsDatabase/St000029/#
    Perm((0,)).depth() == 0
    Perm((0, 1)).depth() == 0
    Perm((1, 0)).depth() == 1
    Perm((0, 1, 2)).depth() == 0
    Perm((0, 2, 1)).depth() == 1
    Perm((1, 0, 2)).depth() == 1
    Perm((1, 2, 0)).depth() == 2
    Perm((2, 0, 1)).depth() == 2
    Perm((2, 1, 0)).depth() == 2
    Perm((0, 1, 2, 3)).depth() == 0
    Perm((0, 1, 3, 2)).depth() == 1
    Perm((0, 2, 1, 3)).depth() == 1
    Perm((0, 2, 3, 1)).depth() == 2
    Perm((0, 3, 1, 2)).depth() == 2
    Perm((0, 3, 2, 1)).depth() == 2
    Perm((1, 0, 2, 3)).depth() == 1
    Perm((1, 0, 3, 2)).depth() == 2
    Perm((1, 2, 0, 3)).depth() == 2
    Perm((1, 2, 3, 0)).depth() == 3
    Perm((1, 3, 0, 2)).depth() == 3
    Perm((1, 3, 2, 0)).depth() == 3
    Perm((2, 0, 1, 3)).depth() == 2
    Perm((2, 0, 3, 1)).depth() == 3
    Perm((2, 1, 0, 3)).depth() == 2
    Perm((2, 1, 3, 0)).depth() == 3
    Perm((2, 3, 0, 1)).depth() == 4
    Perm((2, 3, 1, 0)).depth() == 4
    Perm((3, 0, 1, 2)).depth() == 3
    Perm((3, 0, 2, 1)).depth() == 3
    Perm((3, 1, 0, 2)).depth() == 3
    Perm((3, 1, 2, 0)).depth() == 3
    Perm((3, 2, 0, 1)).depth() == 4
    Perm((3, 2, 1, 0)).depth() == 4
    Perm((0, 1, 2, 3, 4)).depth() == 0
    Perm((0, 1, 2, 4, 3)).depth() == 1
    Perm((0, 1, 3, 2, 4)).depth() == 1
    Perm((0, 1, 3, 4, 2)).depth() == 2
    Perm((0, 1, 4, 2, 3)).depth() == 2
    Perm((0, 1, 4, 3, 2)).depth() == 2
    Perm((0, 2, 1, 3, 4)).depth() == 1
    Perm((0, 2, 1, 4, 3)).depth() == 2
    Perm((0, 2, 3, 1, 4)).depth() == 2
    Perm((0, 2, 3, 4, 1)).depth() == 3
    Perm((0, 2, 4, 1, 3)).depth() == 3
    Perm((0, 2, 4, 3, 1)).depth() == 3
    Perm((0, 3, 1, 2, 4)).depth() == 2
    Perm((0, 3, 1, 4, 2)).depth() == 3
    Perm((0, 3, 2, 1, 4)).depth() == 2
    Perm((0, 3, 2, 4, 1)).depth() == 3
    Perm((0, 3, 4, 1, 2)).depth() == 4
    Perm((0, 3, 4, 2, 1)).depth() == 4
    Perm((0, 4, 1, 2, 3)).depth() == 3
    Perm((0, 4, 1, 3, 2)).depth() == 3
    Perm((0, 4, 2, 1, 3)).depth() == 3
    Perm((0, 4, 2, 3, 1)).depth() == 3
    Perm((0, 4, 3, 1, 2)).depth() == 4
    Perm((0, 4, 3, 2, 1)).depth() == 4
    Perm((1, 0, 2, 3, 4)).depth() == 1
    Perm((1, 0, 2, 4, 3)).depth() == 2
    Perm((1, 0, 3, 2, 4)).depth() == 2
    Perm((1, 0, 3, 4, 2)).depth() == 3
    Perm((1, 0, 4, 2, 3)).depth() == 3
    Perm((1, 0, 4, 3, 2)).depth() == 3
    Perm((1, 2, 0, 3, 4)).depth() == 2
    Perm((1, 2, 0, 4, 3)).depth() == 3
    Perm((1, 2, 3, 0, 4)).depth() == 3
    Perm((1, 2, 3, 4, 0)).depth() == 4
    Perm((1, 2, 4, 0, 3)).depth() == 4
    Perm((1, 2, 4, 3, 0)).depth() == 4
    Perm((1, 3, 0, 2, 4)).depth() == 3
    Perm((1, 3, 0, 4, 2)).depth() == 4
    Perm((1, 3, 2, 0, 4)).depth() == 3
    Perm((1, 3, 2, 4, 0)).depth() == 4
    Perm((1, 3, 4, 0, 2)).depth() == 5
    Perm((1, 3, 4, 2, 0)).depth() == 5
    Perm((1, 4, 0, 2, 3)).depth() == 4
    Perm((1, 4, 0, 3, 2)).depth() == 4
    Perm((1, 4, 2, 0, 3)).depth() == 4
    Perm((1, 4, 2, 3, 0)).depth() == 4
    Perm((1, 4, 3, 0, 2)).depth() == 5
    Perm((1, 4, 3, 2, 0)).depth() == 5
    Perm((2, 0, 1, 3, 4)).depth() == 2
    Perm((2, 0, 1, 4, 3)).depth() == 3
    Perm((2, 0, 3, 1, 4)).depth() == 3
    Perm((2, 0, 3, 4, 1)).depth() == 4
    Perm((2, 0, 4, 1, 3)).depth() == 4
    Perm((2, 0, 4, 3, 1)).depth() == 4
    Perm((2, 1, 0, 3, 4)).depth() == 2
    Perm((2, 1, 0, 4, 3)).depth() == 3
    Perm((2, 1, 3, 0, 4)).depth() == 3
    Perm((2, 1, 3, 4, 0)).depth() == 4
    Perm((2, 1, 4, 0, 3)).depth() == 4
    Perm((2, 1, 4, 3, 0)).depth() == 4
    Perm((2, 3, 0, 1, 4)).depth() == 4
    Perm((2, 3, 0, 4, 1)).depth() == 5
    Perm((2, 3, 1, 0, 4)).depth() == 4
    Perm((2, 3, 1, 4, 0)).depth() == 5
    Perm((2, 3, 4, 0, 1)).depth() == 6
    Perm((2, 3, 4, 1, 0)).depth() == 6
    Perm((2, 4, 0, 1, 3)).depth() == 5
    Perm((2, 4, 0, 3, 1)).depth() == 5
    Perm((2, 4, 1, 0, 3)).depth() == 5
    Perm((2, 4, 1, 3, 0)).depth() == 5
    Perm((2, 4, 3, 0, 1)).depth() == 6
    Perm((2, 4, 3, 1, 0)).depth() == 6
    Perm((3, 0, 1, 2, 4)).depth() == 3
    Perm((3, 0, 1, 4, 2)).depth() == 4
    Perm((3, 0, 2, 1, 4)).depth() == 3
    Perm((3, 0, 2, 4, 1)).depth() == 4
    Perm((3, 0, 4, 1, 2)).depth() == 5
    Perm((3, 0, 4, 2, 1)).depth() == 5
    Perm((3, 1, 0, 2, 4)).depth() == 3
    Perm((3, 1, 0, 4, 2)).depth() == 4
    Perm((3, 1, 2, 0, 4)).depth() == 3
    Perm((3, 1, 2, 4, 0)).depth() == 4
    Perm((3, 1, 4, 0, 2)).depth() == 5
    Perm((3, 1, 4, 2, 0)).depth() == 5
    Perm((3, 2, 0, 1, 4)).depth() == 4
    Perm((3, 2, 0, 4, 1)).depth() == 5
    Perm((3, 2, 1, 0, 4)).depth() == 4
    Perm((3, 2, 1, 4, 0)).depth() == 5
    Perm((3, 2, 4, 0, 1)).depth() == 6
    Perm((3, 2, 4, 1, 0)).depth() == 6
    Perm((3, 4, 0, 1, 2)).depth() == 6
    Perm((3, 4, 0, 2, 1)).depth() == 6
    Perm((3, 4, 1, 0, 2)).depth() == 6
    Perm((3, 4, 1, 2, 0)).depth() == 6
    Perm((3, 4, 2, 0, 1)).depth() == 6
    Perm((3, 4, 2, 1, 0)).depth() == 6
    Perm((4, 0, 1, 2, 3)).depth() == 4
    Perm((4, 0, 1, 3, 2)).depth() == 4
    Perm((4, 0, 2, 1, 3)).depth() == 4
    Perm((4, 0, 2, 3, 1)).depth() == 4
    Perm((4, 0, 3, 1, 2)).depth() == 5
    Perm((4, 0, 3, 2, 1)).depth() == 5
    Perm((4, 1, 0, 2, 3)).depth() == 4
    Perm((4, 1, 0, 3, 2)).depth() == 4
    Perm((4, 1, 2, 0, 3)).depth() == 4
    Perm((4, 1, 2, 3, 0)).depth() == 4
    Perm((4, 1, 3, 0, 2)).depth() == 5
    Perm((4, 1, 3, 2, 0)).depth() == 5
    Perm((4, 2, 0, 1, 3)).depth() == 5
    Perm((4, 2, 0, 3, 1)).depth() == 5
    Perm((4, 2, 1, 0, 3)).depth() == 5
    Perm((4, 2, 1, 3, 0)).depth() == 5
    Perm((4, 2, 3, 0, 1)).depth() == 6
    Perm((4, 2, 3, 1, 0)).depth() == 6
    Perm((4, 3, 0, 1, 2)).depth() == 6
    Perm((4, 3, 0, 2, 1)).depth() == 6
    Perm((4, 3, 1, 0, 2)).depth() == 6
    Perm((4, 3, 1, 2, 0)).depth() == 6
    Perm((4, 3, 2, 0, 1)).depth() == 6
    Perm((4, 3, 2, 1, 0)).depth() == 6


def test_minimum_gapsize():
    assert Perm((0, 1)).min_gapsize() == 2
    assert Perm((2, 0, 3, 1)).min_gapsize() == 3
    assert Perm((7, 2, 5, 3, 4, 1, 6, 0)).min_gapsize() == 2
    assert Perm((5, 2, 0, 3, 6, 4, 7, 1)).min_gapsize() == 3
    assert Perm((7, 2, 0, 4, 9, 5, 8, 1, 6, 3)).min_gapsize() == 3


def test_longestruns_descending():
    assert Perm().longestruns_descending() == (0, [])
    assert Perm((3, 2, 1, 0)).longestruns_descending() == (4, [0])
    assert Perm((0, 1, 2, 3, 4)).longestruns_descending() == (1, [0, 1, 2, 3, 4])
    assert Perm((3, 9, 7, 0, 2, 5, 8, 6, 4, 1)).longestruns_descending() == (4, [6])
    assert Perm((0, 3, 1, 4, 7, 2, 8, 5, 6, 9)).longestruns_descending() == (
        2,
        [1, 4, 6],
    )


def test_longestruns_ascending():
    assert Perm().longestruns_ascending() == (0, [])
    assert Perm((0, 1, 2, 3)).longestruns_ascending() == (4, [0])
    assert Perm((4, 3, 2, 1, 0)).longestruns_ascending() == (1, [0, 1, 2, 3, 4])
    assert Perm((8, 1, 7, 5, 6, 2, 9, 3, 0, 4)).longestruns_ascending() == (
        2,
        [1, 3, 5, 8],
    )
    assert Perm((1, 2, 3, 4, 6, 0, 9, 7, 8, 5)).longestruns_ascending() == (5, [0])


def test_length_of_longestrun_ascending():
    assert Perm().length_of_longestrun_ascending() == 0
    assert Perm((2, 1, 0)).length_of_longestrun_ascending() == 1
    assert Perm((0, 1, 2)).length_of_longestrun_ascending() == 3
    assert Perm((0, 1, 2, 3, 4, 5, 6, 7, 8, 9)).length_of_longestrun_ascending() == 10
    assert Perm((6, 0, 9, 1, 4, 7, 3, 8, 5, 2)).length_of_longestrun_ascending() == 3
    assert Perm((6, 1, 3, 7, 4, 5, 9, 8, 0, 2)).length_of_longestrun_ascending() == 3
    assert Perm((4, 0, 9, 5, 3, 7, 1, 6, 8, 2)).length_of_longestrun_ascending() == 3
    assert Perm((1, 9, 4, 6, 0, 8, 2, 7, 5, 3)).length_of_longestrun_ascending() == 2
    assert Perm((2, 5, 8, 6, 0, 1, 3, 7, 9, 4)).length_of_longestrun_ascending() == 5


def test_len():
    assert len(Perm()) == 0
    assert len(Perm((0,))) == 1
    assert len(Perm((1, 2, 0, 4, 3))) == 5


def test_length_of_longestrun_descending():
    assert Perm().length_of_longestrun_descending() == 0
    assert Perm((2, 1, 0)).length_of_longestrun_descending() == 3
    assert Perm((0, 1, 2)).length_of_longestrun_descending() == 1
    assert Perm((3, 5, 2, 7, 1, 8, 0, 6, 9, 4)).length_of_longestrun_descending() == 2
    assert Perm((5, 4, 8, 9, 7, 3, 2, 1, 0, 6)).length_of_longestrun_descending() == 6


def test_count_cycles():
    for i in range(10):
        assert Perm.identity(i).count_cycles() == i
    assert Perm((2, 0, 1)).count_cycles() == 1
    assert Perm((4, 2, 7, 0, 3, 1, 6, 5)).count_cycles() == 3
    assert Perm((5, 3, 8, 1, 0, 4, 2, 7, 6)).count_cycles() == 4


def test_is_involution():
    assert Perm().is_involution()
    assert Perm((0,)).is_involution()
    for _ in range(30):
        perm = Perm.random(random.randint(0, 20))
        cyclelist = perm.cycle_decomp()
        assert perm.is_involution() == all(map(lambda x: len(x) <= 2, cyclelist))


def test_cycle_decomp():
    assert Perm(()).cycle_decomp() == deque([])
    assert Perm((0,)).cycle_decomp() == deque([[0]])
    assert Perm((0, 1)).cycle_decomp() == deque([[0], [1]])
    assert Perm((0, 2, 1)).cycle_decomp() == deque([[0], [2, 1]])
    assert Perm((2, 3, 1, 0)).cycle_decomp() == deque([[3, 0, 2, 1]])
    assert Perm((0, 2, 4, 3, 1)).cycle_decomp() == deque([[0], [3], [4, 1, 2]])
    assert Perm((0, 1, 4, 3, 2, 5)).cycle_decomp() == deque(
        [[0], [1], [3], [4, 2], [5]]
    )
    assert Perm((0, 5, 4, 2, 1, 3, 6)).cycle_decomp() == deque(
        [[0], [5, 3, 2, 4, 1], [6]]
    )
    assert Perm((1, 7, 3, 5, 0, 2, 4, 6)).cycle_decomp() == deque(
        [[5, 2, 3], [7, 6, 4, 0, 1]]
    )
    assert Perm((0, 5, 1, 3, 2, 4, 6, 7, 8)).cycle_decomp() == deque(
        [[0], [3], [5, 4, 2, 1], [6], [7], [8]]
    )
    25
    assert Perm(
        (10, 0, 1, 3, 7, 11, 5, 2, 9, 13, 4, 8, 14, 6, 12)
    ).cycle_decomp() == deque(
        [[3], [10, 4, 7, 2, 1, 0], [13, 6, 5, 11, 8, 9], [14, 12]]
    )
    assert Perm(
        (13, 10, 4, 1, 6, 9, 2, 3, 8, 7, 5, 14, 12, 11, 0)
    ).cycle_decomp() == deque(
        [[6, 2, 4], [8], [10, 5, 9, 7, 3, 1], [12], [14, 0, 13, 11]]
    )
    assert Perm(
        (4, 1, 12, 14, 0, 5, 2, 7, 13, 3, 9, 6, 10, 8, 11)
    ).cycle_decomp() == deque(
        [[1], [4, 0], [5], [7], [13, 8], [14, 11, 6, 2, 12, 10, 9, 3]]
    )
    assert Perm(
        (6, 8, 5, 7, 0, 14, 2, 1, 3, 13, 12, 11, 4, 10, 9)
    ).cycle_decomp() == deque([[8, 3, 7, 1], [11], [14, 9, 13, 10, 12, 4, 0, 6, 2, 5]])
    assert Perm(
        (12, 6, 4, 0, 3, 2, 14, 13, 8, 1, 9, 7, 10, 11, 5)
    ).cycle_decomp() == deque([[8], [13, 11, 7], [14, 5, 2, 4, 3, 0, 12, 10, 9, 1, 6]])


def test_rank():
    for i, perm in enumerate(Perm.first(1000)):
        assert perm.rank() == i


def test_threepats():
    assert all(v == 0 for v in Perm().threepats().values())
    assert all(v == 0 for v in Perm((0,)).threepats().values())
    assert all(v == 0 for v in Perm((0, 1)).threepats().values())
    assert (
        lambda counter: all(
            (
                counter[Perm((0, 1, 2))] == 0,
                counter[Perm((0, 2, 1))] == 0,
                counter[Perm((1, 0, 2))] == 3,
                counter[Perm((1, 2, 0))] == 0,
                counter[Perm((2, 0, 1))] == 0,
                counter[Perm((2, 1, 0))] == 1,
            )
        )
    )(Perm((2, 1, 0, 3)).threepats())
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        threepatdict = perm.threepats()
        for key, val in threepatdict.items():
            assert key.count_occurrences_in(perm) == val


def test_fourpats():
    assert all(v == 0 for v in Perm().fourpats().values())
    assert all(v == 0 for v in Perm((0,)).fourpats().values())
    assert all(v == 0 for v in Perm((0, 1)).fourpats().values())
    assert (
        lambda counter: all(
            (
                counter[Perm((0, 1, 2, 3))] == 0,
                counter[Perm((0, 1, 3, 2))] == 2,
                counter[Perm((0, 2, 1, 3))] == 2,
                counter[Perm((0, 2, 3, 1))] == 2,
                counter[Perm((0, 3, 1, 2))] == 2,
                counter[Perm((0, 3, 2, 1))] == 0,
                counter[Perm((1, 0, 2, 3))] == 3,
                counter[Perm((1, 0, 3, 2))] == 3,
                counter[Perm((1, 2, 0, 3))] == 0,
                counter[Perm((1, 2, 3, 0))] == 0,
                counter[Perm((1, 3, 0, 2))] == 1,
                counter[Perm((1, 3, 2, 0))] == 0,
                counter[Perm((2, 0, 1, 3))] == 0,
                counter[Perm((2, 0, 3, 1))] == 0,
                counter[Perm((2, 1, 0, 3))] == 0,
                counter[Perm((2, 1, 3, 0))] == 0,
                counter[Perm((2, 3, 0, 1))] == 0,
                counter[Perm((2, 3, 1, 0))] == 0,
                counter[Perm((3, 0, 1, 2))] == 0,
                counter[Perm((3, 0, 2, 1))] == 0,
                counter[Perm((3, 1, 0, 2))] == 0,
                counter[Perm((3, 1, 2, 0))] == 0,
                counter[Perm((3, 2, 0, 1))] == 0,
                counter[Perm((3, 2, 1, 0))] == 0,
            )
        )
    )(Perm((1, 0, 3, 5, 2, 4)).fourpats())
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        fourpatdict = perm.fourpats()
        for key, val in fourpatdict.items():
            assert key.count_occurrences_in(perm) == val


def test_rank_encoding():
    assert Perm().rank_encoding() == []
    assert Perm((0,)).rank_encoding() == [0]
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        for index, val in enumerate(perm.rank_encoding()):
            invs = 0
            for i in range(index + 1, len(perm)):
                if perm[i] < perm[index]:
                    invs += 1
            assert invs == val


def test_block_decomposition():
    assert Perm().block_decomposition() == []
    assert Perm((0,)).block_decomposition() == [[]]
    assert Perm((5, 3, 0, 1, 2, 4, 7, 6)).block_decomposition() == [
        [],
        [],
        [2, 3, 6],
        [2],
        [1],
        [1],
        [0],
        [],
    ]
    assert set(Perm((4, 1, 0, 5, 2, 3)).block_decomposition_as_pattern()) == set(
        [Perm((0, 1)), Perm((1, 0))]
    )
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        blocks = perm.block_decomposition()
        patts = set(perm.block_decomposition_as_pattern())
        for length in range(len(blocks)):
            for start in blocks[length]:
                assert (
                    max(perm[start : start + length])
                    - min(perm[start : start + length])
                    == length - 1
                )
                assert Perm.to_standard(perm[start : start + length]) in patts


def test_count_rtlmax_ltrmin_layers():
    assert Perm((2, 1, 3, 0)).count_rtlmax_ltrmin_layers() == 1
    assert Perm((2, 0, 1, 3)).count_rtlmax_ltrmin_layers() == 2
    assert Perm((1, 3, 2, 7, 6, 5, 8, 0, 4)).count_rtlmax_ltrmin_layers() == 2
    assert Perm((0, 8, 2, 4, 5, 6, 3, 7, 1)).count_rtlmax_ltrmin_layers() == 4
    assert Perm((1, 0, 2)).count_rtlmax_ltrmin_layers() == 1
    assert Perm((1, 2, 0, 3)).count_rtlmax_ltrmin_layers() == 2
    assert Perm((3, 0, 2, 1)).count_rtlmax_ltrmin_layers() == 1
    assert Perm((2, 0, 1)).count_rtlmax_ltrmin_layers() == 1
    assert Perm((1, 3, 2, 0)).count_rtlmax_ltrmin_layers() == 1
    assert Perm(()).count_rtlmax_ltrmin_layers() == 0
    assert Perm((5, 3, 7, 4, 2, 0, 6, 1)).count_rtlmax_ltrmin_layers() == 2
    assert Perm((0, 2, 1, 6, 4, 3, 5, 7, 8)).count_rtlmax_ltrmin_layers() == 4
    assert Perm((2, 1, 0)).count_rtlmax_ltrmin_layers() == 1
    assert Perm((0, 2, 1)).count_rtlmax_ltrmin_layers() == 1
    assert Perm((0, 8, 3, 5, 7, 4, 2, 6, 1)).count_rtlmax_ltrmin_layers() == 2


def test_rtlmax_ltrmin_decomposition():
    assert list(Perm(()).rtlmax_ltrmin_decomposition()) == []
    assert list(Perm((0,)).rtlmax_ltrmin_decomposition()) == [[0]]
    assert list(Perm((2, 0, 3, 1)).rtlmax_ltrmin_decomposition()) == [[0, 1, 2, 3]]
    assert list(Perm((0, 1, 2, 3)).rtlmax_ltrmin_decomposition()) == [[0, 3], [0, 1]]
    assert list(Perm((1, 0, 2)).rtlmax_ltrmin_decomposition()) == [[0, 1, 2]]
    assert list(Perm((2, 1, 0)).rtlmax_ltrmin_decomposition()) == [[0, 1, 2]]
    assert list(Perm((0, 1)).rtlmax_ltrmin_decomposition()) == [[0, 1]]
    assert list(Perm((2, 1, 3, 0)).rtlmax_ltrmin_decomposition()) == [[0, 1, 2, 3]]
    assert list(Perm((0, 2, 1)).rtlmax_ltrmin_decomposition()) == [[0, 1, 2]]
    assert list(Perm((2, 3, 0, 1)).rtlmax_ltrmin_decomposition()) == [[0, 1, 2, 3]]
    assert list(Perm((1, 3, 0, 2)).rtlmax_ltrmin_decomposition()) == [[0, 1, 2, 3]]
    assert list(Perm((1, 2, 3, 0)).rtlmax_ltrmin_decomposition()) == [[0, 2, 3], [0]]
    assert list(Perm((0, 1, 6, 5, 4, 3, 2)).rtlmax_ltrmin_decomposition()) == [
        [0, 2, 3, 4, 5, 6],
        [0],
    ]
    assert list(Perm((0, 1, 4, 3, 2, 5)).rtlmax_ltrmin_decomposition()) == [
        [0, 5],
        [0, 1, 2, 3],
    ]
    assert list(Perm((2, 3, 0, 4, 1, 5)).rtlmax_ltrmin_decomposition()) == [
        [0, 2, 5],
        [1, 2],
        [0],
    ]
    assert list(Perm((4, 0, 2, 5, 3, 1)).rtlmax_ltrmin_decomposition()) == [
        [0, 1, 3, 4, 5],
        [0],
    ]
    assert list(Perm((1, 5, 0, 3, 2, 4)).rtlmax_ltrmin_decomposition()) == [
        [0, 1, 2, 5],
        [0, 1],
    ]


def test_monotone_block_decomposition():
    assert list(Perm().monotone_block_decomposition(True)) == []
    assert list(Perm((0,)).monotone_block_decomposition()) == []
    assert list(Perm((0,)).monotone_block_decomposition(True)) == [(0, 0)]
    assert list(Perm((6, 7, 5, 3, 0, 1, 2, 4)).monotone_block_decomposition()) == [
        (0, 1),
        (4, 6),
    ]
    assert list(Perm((0, 2, 1, 5, 6, 7, 4, 3)).monotone_block_decomposition()) == [
        (1, 2),
        (3, 5),
        (6, 7),
    ]
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        monblocks = perm.monotone_block_decomposition(True)
        last = -1
        for block in monblocks:
            assert block[0] == last + 1
            last = block[1]
            assert all(
                perm[i] - perm[i - 1] == perm[block[0] + 1] - perm[block[0]]
                for i in range(block[0] + 2, block[1])
            )


def test_monotone_block_decomposition_ascending():
    assert list(Perm().monotone_block_decomposition_ascending()) == []
    for i in range(1, 10):
        assert list(Perm.identity(i).monotone_block_decomposition_ascending(True)) == [
            (0, i - 1)
        ]
    assert list(
        Perm((0, 1, 3, 6, 5, 4, 2)).monotone_block_decomposition_ascending(True)
    ) == [(0, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
    assert list(
        Perm((0, 1, 5, 6, 3, 2, 4)).monotone_block_decomposition_ascending(False)
    ) == [(0, 1), (2, 3)]
    assert list(
        Perm((2, 3, 1, 4, 5, 0)).monotone_block_decomposition_ascending(False)
    ) == [(0, 1), (3, 4)]
    assert (
        list(Perm((3, 5, 1, 4, 0, 2)).monotone_block_decomposition_ascending(False))
        == []
    )
    assert list(
        Perm((5, 2, 4, 0, 3, 1)).monotone_block_decomposition_ascending(True)
    ) == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    assert list(
        Perm((3, 1, 2, 5, 4, 0)).monotone_block_decomposition_ascending(False)
    ) == [(1, 2)]
    assert (
        list(Perm((4, 0, 3, 2, 5, 1)).monotone_block_decomposition_ascending(False))
        == []
    )
    assert list(
        Perm((3, 2, 5, 4, 0, 1)).monotone_block_decomposition_ascending(True)
    ) == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5)]
    assert list(
        Perm((0, 1, 2, 4, 3, 5)).monotone_block_decomposition_ascending(False)
    ) == [(0, 2)]
    assert (
        list(Perm((3, 5, 1, 0, 4, 2)).monotone_block_decomposition_ascending(False))
        == []
    )


def test_test_monotone_block_decomposition_descending():
    assert list(Perm().monotone_block_decomposition_descending()) == []
    for i in range(1, 10):
        assert list(
            Perm.monotone_decreasing(i).monotone_block_decomposition_descending(True)
        ) == [(0, i - 1)]
    assert (
        list(Perm((5, 0, 3, 1, 2, 4)).monotone_block_decomposition_descending(False))
        == []
    )
    assert list(
        Perm((0, 5, 2, 3, 4, 1)).monotone_block_decomposition_descending(True)
    ) == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    assert list(
        Perm((5, 4, 2, 1, 0, 3)).monotone_block_decomposition_descending(False)
    ) == [(0, 1), (2, 4)]
    assert list(
        Perm((1, 3, 2, 0, 4)).monotone_block_decomposition_descending(True)
    ) == [(0, 0), (1, 2), (3, 3), (4, 4)]
    assert list(
        Perm((4, 5, 2, 3, 1, 0)).monotone_block_decomposition_descending(True)
    ) == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5)]
    assert list(
        Perm((2, 1, 3, 4, 0)).monotone_block_decomposition_descending(True)
    ) == [(0, 1), (2, 2), (3, 3), (4, 4)]
    assert list(
        Perm((0, 5, 1, 3, 2, 4)).monotone_block_decomposition_descending(True)
    ) == [(0, 0), (1, 1), (2, 2), (3, 4), (5, 5)]
    assert (
        list(Perm((2, 4, 0, 1, 5, 3)).monotone_block_decomposition_descending(False))
        == []
    )
    assert list(
        Perm((5, 4, 0, 1, 3, 2)).monotone_block_decomposition_descending(False)
    ) == [(0, 1), (4, 5)]
    assert list(
        Perm((5, 2, 1, 4, 3, 0)).monotone_block_decomposition_descending(True)
    ) == [(0, 0), (1, 2), (3, 4), (5, 5)]


def test_monotone_quotient():
    assert Perm().monotone_quotient() == Perm()
    assert Perm((0,)).monotone_quotient() == Perm((0,))
    assert Perm((0, 2, 1, 5, 6, 7, 4, 3)).monotone_quotient() == Perm((0, 1, 3, 2))
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        monblocks = tuple(
            start for (start, end) in perm.monotone_block_decomposition(True)
        )
        assert monblocks in list(perm.occurrences_of(perm.monotone_quotient()))


def test_maximum_block():
    assert Perm((0, 1, 2)).maximum_block() == (2, 0)
    assert Perm((0, 2, 1)).maximum_block() == (2, 1)
    assert Perm((1, 0, 2)).maximum_block() == (2, 0)
    assert Perm((1, 2, 0)).maximum_block() == (2, 0)
    assert Perm((2, 0, 1)).maximum_block() == (2, 1)
    assert Perm((2, 1, 0)).maximum_block() == (2, 0)
    assert Perm((4, 0, 6, 3, 5, 1, 2)).maximum_block() == (2, 5)
    assert Perm((1, 2, 7, 8, 6, 0, 3, 5, 4)).maximum_block() == (3, 2)


def test_simple_location():
    assert Perm().simple_location() == (0, 0)
    assert Perm((0,)).simple_location() == (0, 0)
    assert Perm((0, 2, 1, 5, 6, 7, 4, 3)).simple_location() == (7, 1)
    assert Perm((3, 4, 0, 7, 2, 6, 1, 5)).simple_location() == (2, 0)
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        length, start = perm.simple_location()
        if length != 0:
            assert (
                max(perm[start : start + length]) - min(perm[start : start + length])
                == length - 1
            )
        else:
            length = 2
        for bigger in range(length + 1, len(perm) - 1):
            for start in range(len(perm) - bigger - 1):
                assert (
                    max(perm[start : start + bigger])
                    - min(perm[start : start + bigger])
                    != bigger - 1
                )


def test_is_simple():
    assert Perm().is_simple()
    assert Perm((0,)).is_simple()
    assert not Perm((0, 1, 2)).is_simple()
    assert not Perm((0, 2, 1)).is_simple()
    assert not Perm((1, 0, 2)).is_simple()
    assert not Perm((1, 2, 0)).is_simple()
    assert not Perm((2, 0, 1)).is_simple()
    assert not Perm((2, 1, 0)).is_simple()
    assert Perm((2, 0, 3, 1)).is_simple()
    assert not Perm((3, 2, 0, 1)).is_simple()
    assert Perm((1, 3, 0, 2)).is_simple()
    assert Perm((3, 7, 2, 6, 1, 5, 0, 4)).is_simple()


def test_is_strongly_simple():
    assert Perm().is_strongly_simple()
    assert Perm((0,)).is_strongly_simple()
    assert not Perm((0, 1, 2)).is_strongly_simple()
    assert not Perm((0, 2, 1)).is_strongly_simple()
    assert not Perm((1, 0, 2)).is_strongly_simple()
    assert Perm((4, 1, 6, 3, 0, 7, 2, 5)).is_strongly_simple()


def test_coveredby():
    assert Perm().coveredby() == [Perm((0,))]
    assert sorted(Perm((0,)).coveredby()) == sorted([Perm((0, 1)), Perm((1, 0))])
    assert sorted(Perm((0, 1)).coveredby()) == sorted(
        [
            Perm((0, 2, 1)),
            Perm((1, 2, 0)),
            Perm((0, 1, 2)),
            Perm((2, 0, 1)),
            Perm((1, 0, 2)),
        ]
    )
    for _ in range(10):
        perm = Perm.random(random.randint(0, 12))
        for p in perm.coveredby():
            assert perm in p.children()


def test_children():
    assert Perm().children() == []
    assert Perm((0,)).children() == [Perm()]
    assert sorted(Perm((0, 4, 3, 1, 2)).children()) == [
        Perm((0, 3, 1, 2)),
        Perm((0, 3, 2, 1)),
        Perm((3, 2, 0, 1)),
    ]
    assert sorted(Perm((5, 0, 2, 4, 3, 1, 6)).children()) == [
        Perm((0, 2, 4, 3, 1, 5)),
        Perm((4, 0, 1, 3, 2, 5)),
        Perm((4, 0, 2, 3, 1, 5)),
        Perm((4, 0, 3, 2, 1, 5)),
        Perm((4, 1, 3, 2, 0, 5)),
        Perm((5, 0, 2, 4, 3, 1)),
    ]


def test_call_1():
    p = Perm((0, 1, 2, 3))
    for i in range(len(p)):
        assert p(i) == i
    with pytest.raises(AssertionError):
        p(-1)
    with pytest.raises(AssertionError):
        p(4)


def test_call_2():
    p = Perm((3, 4, 0, 2, 1))
    assert p(0) == 3
    assert p(1) == 4
    assert p(2) == 0
    assert p(3) == 2
    assert p(4) == 1
    with pytest.raises(AssertionError):
        p(-1)
    with pytest.raises(AssertionError):
        p(5)


def test_eq():
    assert Perm([]) == Perm([])
    assert Perm([0]) == Perm([0])
    assert Perm([]) != Perm([0])
    assert Perm([0]) != Perm([])
    assert not (Perm([]) != Perm([]))
    assert not (Perm([0]) != Perm([0]))
    assert not (Perm([]) == Perm([0]))
    assert not (Perm([0]) == Perm([]))
    for _ in range(100):
        a = Perm.random(random.randint(0, 10))
        b = Perm(a)
        c = Perm.random(random.randint(0, 10))
        if a == c:
            continue
        assert a == b
        assert a != c
        assert b == a
        assert c != a


def test_avoids():
    assert Perm([4, 0, 1, 2, 3]).avoids()
    assert not (Perm([4, 0, 1, 2, 3]).avoids(Perm([0, 1, 2])))
    assert not (Perm([4, 0, 1, 2, 3]).avoids(Perm([1, 0])))
    assert Perm([4, 0, 1, 2, 3]).avoids(Perm([2, 1, 0]))
    assert not (Perm([4, 0, 1, 2, 3]).avoids_set([Perm([2, 1, 0]), Perm([1, 0])]))
    assert Perm([4, 0, 1, 2, 3]).avoids_set([Perm([2, 1, 0]), Perm([1, 2, 0])])


def test_avoids_2():
    bound = 6

    def do_test(patts, expected):
        for i in range(min(len(expected), bound)):
            length = i + 1
            cnt = 0
            for p in Perm.of_length(length):
                ok = True
                for patt in patts:
                    if not p.avoids(Perm(patt)):
                        ok = False
                        break
                if ok:
                    cnt += 1
            assert expected[i] == cnt

    do_test([[0, 1, 2]], [1, 2, 5, 14, 42, 132, 429, 1430])
    do_test([[1, 2, 0]], [1, 2, 5, 14, 42, 132, 429, 1430])
    do_test([[0, 2, 3, 1]], [1, 2, 6, 23, 103, 512, 2740, 15485])
    do_test([[1, 3, 0, 2]], [1, 2, 6, 23, 103, 512, 2740, 15485])
    do_test([[0, 1, 2, 3]], [1, 2, 6, 23, 103, 513, 2761, 15767])
    do_test([[0, 3, 2, 1]], [1, 2, 6, 23, 103, 513, 2761, 15767])
    do_test([[1, 0, 3, 2]], [1, 2, 6, 23, 103, 513, 2761, 15767])
    do_test([[0, 2, 1, 3]], [1, 2, 6, 23, 103, 513, 2762, 15793])


def test_incr_decr():
    for i in range(100):
        assert Perm(range(i)).is_increasing()
        assert Perm(range(i - 1, -1, -1)).is_decreasing()

    assert not Perm([0, 2, 1]).is_increasing()
    assert not Perm([0, 2, 1]).is_decreasing()
    assert not Perm([1, 0, 2]).is_increasing()
    assert not Perm([1, 0, 2]).is_decreasing()


def test_lt():
    # TODO: No length testing is done here
    for _ in range(30):
        l1 = list(range(10))
        l2 = list(range(10))
        random.shuffle(l1)
        random.shuffle(l2)
        if l1 < l2:
            assert Perm(l1) < Perm(l2)
        else:
            assert not (Perm(l1) < Perm(l2))
        assert not (Perm(l1) < Perm(l1))
        assert not (Perm(l2) < Perm(l2))


def test_gt():
    # TODO: No length testing is done here
    for _ in range(30):
        l1 = list(range(10))
        l2 = list(range(10))
        random.shuffle(l1)
        random.shuffle(l2)
        if l1 > l2:
            assert Perm(l1) > Perm(l2)
        else:
            assert not (Perm(l1) > Perm(l2))
        assert not (Perm(l1) > Perm(l1))
        assert not (Perm(l2) > Perm(l2))


def test_ge():
    # TODO: No length testing is done here
    for _ in range(30):
        l1 = list(range(10))
        l2 = list(range(10))
        random.shuffle(l1)
        random.shuffle(l2)
        if l1 >= l2:
            assert Perm(l1) >= Perm(l2)
        else:
            assert not (Perm(l1) >= Perm(l2))
        assert Perm(l1) >= Perm(l1)
        assert Perm(l2) >= Perm(l2)


def test_bool():
    assert Perm([0, 1, 2, 3])
    assert Perm([0])
    assert not (Perm([]))
    assert not (Perm())


def test_ascii_plot():
    assert Perm().ascii_plot() == ""
    assert Perm((0,)).ascii_plot() == " |\n-\u25cf-\n |"
    assert (
        Perm((0, 1)).ascii_plot(cell_size=2) == "  |  |\n"
        "  |  |\n"
        "--+--●--\n"
        "  |  |\n"
        "  |  |\n"
        "--●--+--\n"
        "  |  |\n"
        "  |  |"
    )
    assert (
        Perm((1, 2, 4, 0, 3, 5)).ascii_plot() == " | | | | | |\n"
        "-+-+-+-+-+-●-\n"
        " | | | | | |\n"
        "-+-+-●-+-+-+-\n"
        " | | | | | |\n"
        "-+-+-+-+-●-+-\n"
        " | | | | | |\n"
        "-+-●-+-+-+-+-\n"
        " | | | | | |\n"
        "-●-+-+-+-+-+-\n"
        " | | | | | |\n"
        "-+-+-+-●-+-+-\n"
        " | | | | | |"
    )
    for _ in range(10):
        perm = Perm.random(random.randint(0, 20))
        plot = perm.ascii_plot(cell_size=0).split("\n")
        for i in range(len(perm)):
            assert plot[len(perm) - perm[i] - 1][2 * i] == "\u25cf"


def test_to_tikz():
    assert Perm((1, 0, 4, 2, 3)).to_tikz() == (
        "\\begin{tikzpicture}[scale=.3,baseline=(current bounding box.center)]\n\t\\"
        "foreach \\x in {1,...,5} {\n\t\t\\draw[ultra thin] (\\x,0)--(\\x,6); %vline\n"
        "\t\t\\draw[ultra thin] (0,\\x)--(6,\\x); %hline\n\t}\n\t\\draw[fill=black] (1,"
        "2) circle (5pt);\n\t\\draw[fill=black] (2,1) circle (5pt);\n\t\\draw[fill=blac"
        "k] (3,5) circle (5pt);\n\t\\draw[fill=black] (4,3) circle (5pt);\n\t\\draw[fil"
        "l=black] (5,4) circle (5pt);\n\\end{tikzpicture}".replace("\t", " " * 4)
    )


def test_cycle_notation():
    assert Perm().cycle_notation() == "( )"
    assert Perm((0,)).cycle_notation() == "( 0 )"
    assert Perm((0, 1)).cycle_notation() == "( 0 ) ( 1 )"
    assert Perm((7, 0, 1, 2, 5, 4, 3, 6)).cycle_notation() == "( 5 4 ) ( 7 6 3 2 1 0 )"


def test_count_bounces():
    assert Perm((0,)).count_bounces() == 0
    assert Perm((0, 1)).count_bounces() == 1
    assert Perm((1, 0)).count_bounces() == 0
    assert Perm((0, 1, 2)).count_bounces() == 3
    assert Perm((0, 2, 1)).count_bounces() == 2
    assert Perm((1, 0, 2)).count_bounces() == 1
    assert Perm((1, 2, 0)).count_bounces() == 0
    assert Perm((2, 0, 1)).count_bounces() == 1
    assert Perm((2, 1, 0)).count_bounces() == 0
    assert Perm((0, 3, 2, 1)).count_bounces() == 3
    assert Perm((2, 0, 1, 3)).count_bounces() == 3
    assert Perm((3, 0, 2, 1)).count_bounces() == 2
    assert Perm((0, 1, 3, 2, 4)).count_bounces() == 8
    assert Perm((0, 2, 3, 4, 1)).count_bounces() == 4
    assert Perm((0, 3, 4, 1, 2)).count_bounces() == 5
    assert Perm((0, 4, 3, 2, 1)).count_bounces() == 4
    assert Perm((1, 2, 0, 3, 4)).count_bounces() == 3
    assert Perm((1, 3, 0, 4, 2)).count_bounces() == 2
    assert Perm((1, 4, 2, 0, 3)).count_bounces() == 1
    assert Perm((2, 0, 3, 4, 1)).count_bounces() == 3
    assert Perm((2, 1, 4, 0, 3)).count_bounces() == 1
    assert Perm((4, 1, 3, 2, 0)).count_bounces() == 0
    assert Perm((4, 3, 0, 1, 2)).count_bounces() == 2
    assert Perm((0, 1, 2, 3, 5, 4)).count_bounces() == 14
    assert Perm((0, 1, 3, 4, 2, 5)).count_bounces() == 10
    assert Perm((0, 1, 4, 3, 5, 2)).count_bounces() == 9
    assert Perm((0, 1, 5, 4, 2, 3)).count_bounces() == 10
    assert Perm((0, 2, 1, 5, 4, 3)).count_bounces() == 8
    assert Perm((0, 2, 4, 1, 3, 5)).count_bounces() == 8
    assert Perm((0, 2, 5, 1, 4, 3)).count_bounces() == 7
    assert Perm((0, 3, 1, 4, 2, 5)).count_bounces() == 9
    assert Perm((0, 3, 2, 4, 5, 1)).count_bounces() == 5
    assert Perm((0, 3, 4, 5, 1, 2)).count_bounces() == 6
    assert Perm((0, 3, 5, 4, 2, 1)).count_bounces() == 5
    assert Perm((0, 4, 2, 1, 3, 5)).count_bounces() == 8
    assert Perm((0, 4, 3, 1, 5, 2)).count_bounces() == 7
    assert Perm((0, 4, 5, 2, 1, 3)).count_bounces() == 6
    assert Perm((0, 5, 1, 3, 4, 2)).count_bounces() == 8
    assert Perm((0, 5, 2, 4, 1, 3)).count_bounces() == 6
    assert Perm((0, 5, 3, 4, 2, 1)).count_bounces() == 5
    assert Perm((1, 0, 2, 3, 4, 5)).count_bounces() == 10
    assert Perm((1, 0, 3, 2, 5, 4)).count_bounces() == 6
    assert Perm((1, 0, 4, 3, 2, 5)).count_bounces() == 5
    assert Perm((1, 0, 5, 3, 4, 2)).count_bounces() == 4
    assert Perm((1, 2, 0, 5, 3, 4)).count_bounces() == 4
    assert Perm((1, 2, 3, 5, 4, 0)).count_bounces() == 0
    assert Perm((1, 2, 5, 0, 3, 4)).count_bounces() == 2
    assert Perm((1, 3, 0, 2, 5, 4)).count_bounces() == 5
    assert Perm((1, 3, 2, 4, 0, 5)).count_bounces() == 1
    assert Perm((1, 3, 4, 2, 5, 0)).count_bounces() == 0
    assert Perm((1, 3, 5, 4, 0, 2)).count_bounces() == 1
    assert Perm((1, 4, 0, 5, 3, 2)).count_bounces() == 3
    assert Perm((1, 4, 3, 0, 2, 5)).count_bounces() == 3
    assert Perm((1, 4, 5, 0, 3, 2)).count_bounces() == 2
    assert Perm((1, 5, 0, 3, 2, 4)).count_bounces() == 4
    assert Perm((1, 5, 2, 3, 4, 0)).count_bounces() == 0
    assert Perm((1, 5, 3, 4, 0, 2)).count_bounces() == 1
    assert Perm((1, 5, 4, 3, 2, 0)).count_bounces() == 0
    assert Perm((2, 0, 3, 1, 4, 5)).count_bounces() == 7
    assert Perm((2, 0, 4, 1, 5, 3)).count_bounces() == 6
    assert Perm((2, 0, 5, 3, 1, 4)).count_bounces() == 5
    assert Perm((2, 1, 0, 4, 5, 3)).count_bounces() == 3
    assert Perm((2, 1, 3, 5, 0, 4)).count_bounces() == 1
    assert Perm((2, 1, 4, 5, 3, 0)).count_bounces() == 0
    assert Perm((2, 3, 0, 1, 4, 5)).count_bounces() == 6
    assert Perm((2, 3, 1, 0, 5, 4)).count_bounces() == 2
    assert Perm((2, 3, 4, 1, 0, 5)).count_bounces() == 1
    assert Perm((2, 3, 5, 1, 4, 0)).count_bounces() == 0
    assert Perm((2, 4, 0, 5, 1, 3)).count_bounces() == 3
    assert Perm((2, 4, 1, 5, 3, 0)).count_bounces() == 0
    assert Perm((2, 4, 5, 0, 1, 3)).count_bounces() == 2
    assert Perm((2, 5, 0, 1, 4, 3)).count_bounces() == 3
    assert Perm((2, 5, 1, 3, 0, 4)).count_bounces() == 1
    assert Perm((2, 5, 3, 1, 4, 0)).count_bounces() == 0
    assert Perm((2, 5, 4, 3, 0, 1)).count_bounces() == 1
    assert Perm((3, 2, 5, 1, 0, 4)).count_bounces() == 1
    assert Perm((3, 4, 0, 2, 5, 1)).count_bounces() == 3
    assert Perm((3, 4, 1, 5, 0, 2)).count_bounces() == 1
    assert Perm((3, 4, 2, 5, 1, 0)).count_bounces() == 0
    assert Perm((3, 5, 0, 1, 2, 4)).count_bounces() == 4
    assert Perm((3, 5, 1, 0, 4, 2)).count_bounces() == 2
    assert Perm((3, 5, 2, 1, 0, 4)).count_bounces() == 1
    assert Perm((3, 5, 4, 1, 2, 0)).count_bounces() == 0
    assert Perm((4, 0, 1, 5, 2, 3)).count_bounces() == 5
    assert Perm((4, 0, 2, 5, 3, 1)).count_bounces() == 4
    assert Perm((4, 0, 5, 1, 2, 3)).count_bounces() == 5
    assert Perm((4, 1, 0, 2, 5, 3)).count_bounces() == 3
    assert Perm((4, 1, 2, 3, 0, 5)).count_bounces() == 1
    assert Perm((4, 1, 3, 2, 5, 0)).count_bounces() == 0
    assert Perm((4, 1, 5, 3, 0, 2)).count_bounces() == 1
    assert Perm((4, 3, 2, 5, 0, 1)).count_bounces() == 1
    assert Perm((4, 3, 5, 2, 1, 0)).count_bounces() == 0
    assert Perm((4, 5, 1, 0, 2, 3)).count_bounces() == 2
    assert Perm((4, 5, 2, 0, 3, 1)).count_bounces() == 2
    assert Perm((4, 5, 3, 1, 0, 2)).count_bounces() == 1
    assert Perm((5, 0, 1, 3, 4, 2)).count_bounces() == 4
