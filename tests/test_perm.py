import random
import pytest
from permuta import Perm, PermSet

def test_init():
    Perm.toggle_check()
    try:
        with pytest.raises(ValueError): Perm([0, 1, 1])
        with pytest.raises(ValueError): Perm([1, 0, 1])
        with pytest.raises(ValueError): Perm([0, 0])
        with pytest.raises(ValueError): Perm([1])
        with pytest.raises(ValueError): Perm((1))
        with pytest.raises(ValueError): Perm(101)
        with pytest.raises(ValueError): Perm(-234)
        with pytest.raises(TypeError): Perm(None)
        with pytest.raises(TypeError): Perm([0.1, 0.2, 0.3])
        Perm()
        Perm([])
        Perm(0)
        Perm([0])
        Perm([3, 0, 2, 1])
        Perm(set([0, 1, 2]))
        p = Perm(502134)
        assert p == Perm((5, 0, 2, 1, 3, 4))
    finally:
        Perm.toggle_check()

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

def test_from_string():
    assert Perm.from_string("203451") == Perm((2, 0, 3, 4, 5, 1))
    assert Perm.from_string("40132") == Perm((4, 0, 1, 3, 2))
    assert Perm.from_string("0") == Perm((0))

    for _ in range(100):
        perm = Perm.random(random.randint(0, 10))
        assert perm == Perm.from_string(''.join(map(str, perm)))

def test_one_based():
    assert Perm.one_based((4, 1, 3, 2)) == Perm((3, 0, 2, 1))
    assert Perm.one_based((1, )) == Perm((0))
    assert Perm.one_based(()) == Perm(())

    for _ in range(100):
        p = list(range(1, random.randint(2, 20)))
        random.shuffle(p)
        assert Perm.one_based(p) == Perm([i - 1 for i in p])

def test_identity():
    for length in range(11):
        assert Perm.identity(length) == Perm(range(length))

def test_random():
    Perm.toggle_check()
    try:
        for length in range(11):
            for _ in range(10):
                perm = Perm.random(length)
                assert len(perm) == length
                Perm(perm)
    finally:
        Perm.toggle_check()

def test_monotone_increasing():
    for length in range(11):
        assert Perm.monotone_increasing(length) ==  Perm(range(length))

def test_monotone_decreasing():
    for length in range(11):
        assert Perm.monotone_decreasing(length) ==  Perm(range(length-1, -1, -1))

def test_unrank():
    assert Perm.unrank(0) ==  Perm()
    assert Perm.unrank(1) ==  Perm((0, ))
    assert Perm.unrank(2) ==  Perm((0, 1))
    assert Perm.unrank(3) ==  Perm((1, 0))
    assert Perm.unrank(4) ==  Perm((0, 1, 2))
    assert Perm.unrank(5) ==  Perm((0, 2, 1))
    assert Perm.unrank(6) ==  Perm((1, 0, 2))
    assert Perm.unrank(10) ==  Perm((0, 1, 2, 3))
    amount = 1 + 1 + 2 + 6 + 24
    assert Perm.unrank(amount) == Perm((0, 1, 2, 3, 4))
    amount = (1 + 1 + 2 + 6 + 24 + 120) - 1
    assert Perm.unrank(amount) ==Perm((4, 3, 2, 1, 0))
    with pytest.raises(AssertionError): Perm.unrank(-1)
    with pytest.raises(AssertionError): Perm.unrank(6, 3)

def test_unrank_2():
    length = 7
    for number, perm in enumerate(PermSet(length)):
        assert Perm.unrank(number, length) == perm

def test_contained_in():
    def generate_contained(n, perm):
        for i in range(len(perm), n):
            r = random.randint(1, len(perm)+1)
            for i in range(len(perm)):
                if perm[i] >= r:
                    perm[i] += 1
            x = random.randint(0, len(perm))
            perm = perm[:x] + [r] + perm[x:]
        return Perm(perm)

    assert Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]).contained_in(Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]))
    assert Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]).contains(Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]))
    assert Perm([]).contained_in(Perm([]))
    assert Perm([]).contained_in(Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]))
    assert Perm([0]).contained_in(Perm([0]))
    assert not Perm([7, 3, 0, 8, 1, 6, 5, 2, 4]).contained_in(Perm([3, 7, 0, 8, 1, 6, 5, 2, 4]))

    for i in range(100):
        n = random.randint(0, 4)
        patt = PermSet(n).random()
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
    assert (sorted(Perm([0]).occurrences_in(Perm([4, 1, 2, 3, 0]))) 
            == [(0, ), (1, ), (2, ), (3, ), (4, )])
    assert (sorted(Perm([0, 1]).occurrences_in(Perm([4, 1, 2, 3, 0]))) 
            == [(1, 2), (1, 3), (2, 3)])
    assert (sorted(Perm([1, 0]).occurrences_in(Perm([4, 1, 2, 3, 0]))) 
            == [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)])
    assert list(Perm([4, 1, 2, 3, 0]).occurrences_in(Perm([]))) == []
    assert list(Perm([4, 1, 2, 3, 0]).occurrences_in(Perm([1, 0]))) == []

def test_apply():
    with pytest.raises(ValueError): Perm((1, 2, 4, 0, 3, 5)).apply(Perm((0, 2, 1, 3)))
    with pytest.raises(ValueError): Perm(()).apply(Perm((0)))

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
    p3 = Perm(201)
    p4 = Perm((0, ))
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
    with pytest.raises(TypeError): p1 + None
    with pytest.raises(TypeError): p1.direct_sum(p2, None)
    with pytest.raises(TypeError): p1.direct_sum(1237)
    with pytest.raises(TypeError): p5 + 'hahaha'

def test_skew_sum():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((0, 4, 2, 1, 3))
    p3 = Perm(201)
    p4 = Perm((0, ))
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

    with pytest.raises(TypeError): p1 - None
    with pytest.raises(TypeError): p2.skew_sum(p2, None)
    with pytest.raises(TypeError): p3.skew_sum(1237)
    with pytest.raises(TypeError): p5 - "hahaha"

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

    with pytest.raises(TypeError): p1.compose(None)
    with pytest.raises(TypeError): p1 * None
    with pytest.raises(TypeError): p2.compose(p2, None)
    with pytest.raises(TypeError): p3.compose(1237)
    with pytest.raises(TypeError): p5 * ("hahaha")
    with pytest.raises(TypeError): p5 * (p1,)

    with pytest.raises(ValueError): p1.compose(p0)
    with pytest.raises(ValueError): p0.compose(p5)
    with pytest.raises(ValueError): p2.compose(p3, p0)
    with pytest.raises(ValueError): p4.compose(p5, p6, p1)

def test_insert():
    assert Perm((0, 1)).insert() == Perm((0, 1, 2))
    assert Perm((0, 1)).insert(0) == Perm((2, 0, 1))
    assert Perm((0, 1)).insert(1) == Perm((0, 2, 1))
    assert Perm((0, 1)).insert(2) == Perm((0, 1, 2))

    assert Perm((2, 0, 1)).insert(2, 1) == Perm((3, 0, 1, 2))
    assert Perm((0, 3, 1, 2)).insert(3, 4) == Perm((0, 3, 1, 4, 2))
    assert Perm((0, 3, 1, 2)).insert(3, 3) == Perm((0, 4, 1, 3, 2))
    assert Perm((0, 3, 1, 2)).insert(1, 0) == Perm((1, 0, 4, 2, 3))

    with pytest.raises(TypeError): Perm((2, 1, 0, 3)).insert(new_element="hehe")
    with pytest.raises(TypeError): Perm((2, 1, 0, 3)).insert(3, "hehe")

    with pytest.raises(ValueError): Perm((2, 1, 0, 3)).insert(2, 100)
    with pytest.raises(ValueError): Perm((2, 1, 0, 3)).insert(0, 5)
    with pytest.raises(ValueError): Perm((2, 1, 0, 3)).insert(3, -3)

def test_remove():
    assert Perm(()).remove() == Perm(())
    assert Perm((2, 0, 1)).remove() == Perm((0, 1))
    assert Perm((3, 0, 1, 2)).remove(0) == Perm((0, 1, 2))
    assert Perm((2, 0, 1)).remove(2) == Perm((1, 0))
    assert Perm((0, )).remove(0) == Perm(())

    assert Perm((3, 0, 1, 2)).remove(3) == Perm((2, 0, 1))
    assert Perm((0, 3, 1, 4, 2)).remove(3) == Perm((0, 3, 1, 2))
    assert Perm((0, 4, 1, 3, 2)).remove(4) == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 4, 2, 3)).remove(0) == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 4, 2, 3)).remove() == Perm((1, 0, 2, 3))
    assert Perm((0, 4, 1, 3, 2)).remove() == Perm((0, 1, 3, 2))

def test_remove_element():
    assert Perm(()).remove() == Perm(())
    assert Perm((3, 0, 1, 2)).remove_element() == Perm((0, 1, 2))
    assert Perm((3, 0, 2, 1)).remove_element(0) == Perm((2, 1, 0))
    assert Perm((3, 0, 1, 2)).remove_element(1) == Perm((2, 0, 1))
    assert Perm((0, 3, 1, 4, 2)).remove_element(4) == Perm((0, 3, 1, 2))
    assert Perm((0, 4, 1, 3, 2)).remove_element(2) == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 4, 2, 3)).remove_element(1) == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 4, 2, 3)).remove_element() == Perm((1, 0, 2, 3))
    assert Perm((0, 4, 1, 3, 2)).remove_element() == Perm((0, 1, 3, 2))

    with pytest.raises(ValueError): Perm((1, 0, 4, 2, 3)).remove_element(5)
    with pytest.raises(ValueError): Perm((1, 0, 4, 2, 3)).remove_element(51)
    with pytest.raises(ValueError): Perm((1, 0, 4, 2, 3)).remove_element(-5)

    with pytest.raises(TypeError): Perm((2, 1, 0, 3)).remove_element("ble")
    with pytest.raises(TypeError): Perm((2, 1, 0, 3)).remove_element([0])
def test_inflate():
    # TODO: make proper tests when the Perm.inflate has been implemented.
    assert Perm((0, 1)).inflate([Perm((1, 0)), Perm((2, 1, 0))]) ==  Perm((1, 0, 4, 3, 2))
    assert Perm((1, 0, 2)).inflate([None, Perm((0, 1)), Perm((0, 1))]) == Perm((2, 0, 1, 3, 4))
    assert Perm((0, 1)).inflate([Perm(), Perm()]) ==  Perm(())

    with pytest.raises(TypeError): Perm((0, 1, 2, 3)).inflate(237)
    with pytest.raises(TypeError): Perm((0, 1, 2, 3)).inflate("hehe")

# TODO: The following three functions have yet to be implemented
@pytest.mark.xfail
def test_contract_inc_bonds():
    assert Perm(()).contract_inc_bonds() == Perm(())
    assert Perm((0)).contract_inc_bonds() == Perm((0))
    assert Perm((1, 2)).contract_inc_bonds() == Perm((0))
    assert Perm((1, 2, 3)).contract_inc_bonds() == Perm((0))
    assert Perm((3, 2, 1)).contract_inc_bonds() == Perm((3, 2, 1))

    assert Perm((0, 3, 1, 4, 2)).contract_inc_bonds() == Perm((0, 3, 1, 4, 2))
    assert Perm((1, 0, 4, 2, 3)).contract_inc_bonds() == Perm((1, 0, 3, 2))
    assert Perm((1, 0, 2, 3, 4)).contract_inc_bonds() == Perm((1, 0, 2))
    assert Perm((0, 4, 1, 2, 3)).contract_inc_bonds() == Perm((0, 2, 2))

@pytest.mark.xfail
def test_contract_dec_bonds():
    assert Perm(()).contract_dec_bonds() == Perm(())
    assert Perm((0)).contract_dec_bonds() == Perm((0))
    assert Perm((2, 1)).contract_dec_bonds() == Perm((0))
    assert Perm((3, 2, 1)).contract_dec_bonds() == Perm((0))
    assert Perm((1, 2, 3)).contract_inc_bonds() == Perm((1, 2, 3))

    assert Perm((0, 3, 1, 4, 2)).contract_dec_bonds() == Perm((0, 3, 1, 4, 2))
    assert Perm((0, 4, 3, 2, 1)).contract_dec_bonds() == Perm((0, 1))
    assert Perm((1, 0, 4, 2, 3)).contract_dec_bonds() == Perm((0, 3, 1, 2))
    assert Perm((0, 4, 1, 3, 2)).contract_dec_bonds() == Perm((0, 3, 1, 2))

@pytest.mark.xfail
def test_contract_bonds():
    assert Perm(()).contract_bonds() == Perm(())
    assert Perm((0)).contract_bonds() == Perm((0))
    assert Perm((2, 1)).contract_bonds() == Perm((0))
    assert Perm((1, 2)).contract_bonds() == Perm((0))
    assert Perm((3, 2, 1)).contract_bonds() == Perm((0))
    assert Perm((1, 2, 3)).contract_bonds() == Perm((0))

    assert Perm((0, 3, 1, 4, 2)).contract_bonds() == Perm((0, 3, 1, 4, 2))
    assert Perm((0, 4, 3, 2, 1)).contract_bonds() == Perm((0, 1))
    assert Perm((1, 0, 4, 2, 3)).contract_bonds() == Perm((0, 2, 1))
    assert Perm((0, 4, 1, 3, 2)).contract_bonds() == Perm((0, 3, 1, 2))
    assert Perm((1, 0, 2, 3, 4)).contract_bonds() == Perm((0, 1, 2))

def test_inverse():
    for i in range(10):
        assert Perm(range(i)) == Perm(range(i)).inverse()
    assert Perm([2, 1, 3, 0]) == Perm([3, 1, 0, 2]).inverse()
    assert Perm((1, 2, 5, 0, 3, 4)).inverse() == Perm((3, 0, 1, 4, 5, 2))
    assert Perm([4, 3, 1, 6, 5, 7, 8, 0, 2]) == Perm([7, 2, 8, 1, 0, 4, 3, 5, 6]).inverse()

def test_reverse():
    assert Perm([5, 2, 3, 0, 4, 6, 1]) == Perm([1, 6, 4, 0, 3, 2, 5]).reverse()
    assert Perm([7, 1, 0, 2, 4, 6, 3, 5]) == Perm([5, 3, 6, 4, 2, 0, 1, 7]).reverse()

def test_complement():
    assert Perm(()).complement() == Perm(())
    assert Perm((0)).complement() == Perm((0))
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
        assert Perm(range(i-1, -1, -1)) == Perm(range(i)).rotate_right()
    assert Perm([2, 1, 3, 4, 0, 5, 6]) == Perm([6, 5, 3, 2, 0, 1, 4]).rotate_right()
    assert Perm([4, 5, 3, 1, 7, 0, 2, 6]) == Perm([4, 7, 1, 0, 2, 6, 3, 5]).rotate_right()
    assert Perm([0, 1, 2]) == Perm([2, 1, 0]).rotate_right(5)
    assert Perm([4, 5, 3, 1, 0, 2]) == Perm([4, 5, 3, 1, 0, 2]).rotate_right(4)

def test_rotate_left():
    for i in range(10):
        assert Perm(list(range(i-1, -1, -1))) == Perm(range(i)).rotate_right()
    assert (Perm([6, 5, 3, 2, 0, 1, 4]).rotate_left() 
            == Perm([6, 5, 3, 2, 0, 1, 4]).rotate_right(3))
    assert (Perm([6, 5, 3, 2, 0, 1, 4]).rotate_left() 
            == Perm([6, 5, 3, 2, 0, 1, 4]).rotate_right(-1))
    assert (Perm([4, 7, 1, 0, 2, 6, 3, 5]).rotate_left() 
            == Perm([4, 7, 1, 0, 2, 6, 3, 5]).rotate_right(7))
    assert Perm([]).rotate_left() == Perm([]).rotate_left(123)

def test_shift_left():
    assert Perm([]) == Perm([]).shift_left()
    assert Perm([0]) == Perm([0]).shift_left()
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([0, 1, 2, 3, 4, 5, 6, 7]).shift_left(0)
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([5, 6, 7, 0, 1, 2, 3, 4]).shift_left(3)
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([0, 1, 2, 3, 4, 5, 6, 7]).shift_left(800)
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([5, 6, 7, 0, 1, 2, 3, 4]).shift_left(403)
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([0, 1, 2, 3, 4, 5, 6, 7]).shift_left(-8)
    assert Perm([0, 1, 2, 3, 4, 5, 6, 7]) == Perm([5, 6, 7, 0, 1, 2, 3, 4]).shift_left(-5)

def test_shift_down():
    assert Perm([]) == Perm([]).shift_down(1000)
    assert Perm([0]) == Perm([0]).shift_down(10)
    assert Perm([1, 0, 4, 2, 3, 5]) == Perm([2, 1, 5, 3, 4, 0]).shift_down()
    assert Perm([1, 0, 4, 2, 3, 5]) == Perm([2, 1, 5, 3, 4, 0]).shift_down(13)
    assert Perm([1, 0, 4, 2, 3, 5]) == Perm([5, 4, 2, 0, 1, 3]).shift_down(-2)
    assert Perm([1, 0, 4, 2, 3, 5]) == Perm([5, 4, 2, 0, 1, 3]).shift_down(-8)

def test_flip_horizontal():
    assert Perm(()).flip_horizontal() == Perm(())
    assert Perm((0)).flip_horizontal() == Perm((0))
    assert Perm((1, 2, 3, 0, 4)).flip_horizontal() == Perm((3, 2, 1, 4, 0))
    assert Perm((2, 0, 1)).flip_horizontal() == Perm((0, 2, 1))
    assert Perm([6, 4, 2, 3, 1, 0, 5]).flip_horizontal() == Perm([0, 2, 4, 3, 5, 6, 1])
    assert Perm([2, 5, 6, 3, 7, 4, 0, 1]).flip_horizontal() == Perm([5, 2, 1, 4, 0, 3, 7, 6])

def test_flip_vertical():
    assert Perm(()).flip_vertical() == Perm(())
    assert Perm((0)).flip_vertical() == Perm((0))
    assert Perm((0, 1)).flip_vertical() == Perm((1, 0))
    assert Perm((1, 2, 5, 0, 3, 4)).flip_vertical() == Perm((4, 3, 0, 5, 2, 1))
    assert Perm([5, 2, 3, 0, 4, 6, 1]).reverse() == Perm([1, 6, 4, 0, 3, 2, 5])
    assert Perm([7, 1, 0, 2, 4, 6, 3, 5]).reverse() == Perm([5, 3, 6, 4, 2, 0, 1, 7])

def test_flip_diagonal():
    for i in range(10):
        assert Perm(range(i)) == Perm(range(i)).flip_diagonal()
    assert Perm([2, 1, 3, 0]) == Perm([3, 1, 0, 2]).flip_diagonal()
    assert Perm((1, 2, 5, 0, 3, 4)).flip_diagonal() == Perm((3, 0, 1, 4, 5, 2))
    assert Perm([4, 3, 1, 6, 5, 7, 8, 0, 2]) == Perm([7, 2, 8, 1, 0, 4, 3, 5, 6]).flip_diagonal()

def test_flip_antidiagonal():
    for i in range(100):
        perm = Perm.random(random.randint(0, 20))
        assert perm.reverse().complement().inverse() == perm.flip_antidiagonal()

def test__rotate_180():
    for _ in range(100):
        perm = Perm.random(random.randint(0, 20))
        assert perm._rotate_180() == perm.rotate().rotate()

@pytest.mark.xfail
def test_all_syms():
    # TODO: write proper tests when the function is working
    assert Perm((0)).all_syms() == PermSet([Perm((0))])

@pytest.mark.xfail
def test_is_representative():
    # TODO: write porper tests when the function is working
    assert Perm(()).is_representative()
    assert Perm((0)).is_representative()

def test_fixed_points():
    assert Perm().fixed_points() == 0
    assert Perm((0, 2, 1)).fixed_points() == 1
    assert Perm(543210).fixed_points() == 0
    assert Perm(410325).fixed_points() == 3
    assert Perm((0, 1, 2, 3, 4, 5)).fixed_points() == 6

def test_is_skew_decomposable():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((0, 4, 2, 1, 3))
    p3 = Perm(201)
    p4 = Perm((0, ))
    p5 = Perm()

    assert p1.skew_sum(p2).is_skew_decomposable()
    assert p1.skew_sum(p2, p3).is_skew_decomposable()
    assert p1.skew_sum(p2, p3, p4).is_skew_decomposable()
    assert p2.skew_sum(p3, p4).is_skew_decomposable()

    assert not Perm((0, 1, 2, 3, 4)).is_skew_decomposable()
    assert not Perm((5, 0, 4, 1, 3, 2, 1)).is_skew_decomposable()

def test_is_sum_decomposable():
    p1 = Perm((0, 1, 3, 2))
    p2 = Perm((4, 2, 1, 3, 0))
    p3 = Perm(201)
    p4 = Perm((0, ))
    p5 = Perm()

    assert p1.is_sum_decomposable()
    assert p1.direct_sum(p2, p3).is_sum_decomposable()
    assert p1.direct_sum(p2, p3, p4).is_sum_decomposable()
    assert p1.direct_sum(p2, p3, p4, p5).is_sum_decomposable()

    assert not p2.is_sum_decomposable()
    assert not p3.is_sum_decomposable()
    assert not Perm((4, 3, 2, 1, 0)).is_sum_decomposable()

def test_descent_set():
    assert Perm().descent_set() == []
    assert Perm((0, 1, 2, 3)).descent_set() == []
    assert Perm(3210).descent_set() == [0, 1, 2]
    assert Perm(210435).descent_set() == [0, 1, 3]
    assert Perm(1230654).descent_set() == [2, 4, 5]
    assert Perm(31450762).descent_set() == [0, 3, 5, 6]

def test_count_descents():
    assert Perm().count_descents() == 0
    assert Perm((0, 1, 2, 3)).count_descents() == 0
    assert Perm(3210).count_descents() == 3
    assert Perm(210435).count_descents() == 3
    assert Perm(1230654).count_descents() == 3
    assert Perm(31450762).count_descents() == 4

def test_ascents():
    assert list(Perm().ascents()) == []
    assert list(Perm((0, 1, 2, 3)).ascents()) == [0, 1, 2]
    assert list(Perm(3210).ascents()) == []
    assert list(Perm(210435).ascents()) == [2, 4]
    assert list(Perm(1230654).ascents()) == [0, 1, 3]
    assert list(Perm(31450762).ascents()) == [1, 2, 4]

def test_ascent_set():
    assert Perm().ascent_set() == []
    assert Perm((0, 1, 2, 3)).ascent_set() == [0, 1, 2]
    assert Perm(3210).ascent_set() == []
    assert Perm(210435).ascent_set() == [2, 4]
    assert Perm(1230654).ascent_set() == [0, 1, 3]
    assert Perm(31450762).ascent_set() == [1, 2, 4]

def test_count_ascents():
    assert Perm().count_ascents() == 0
    assert Perm((0, 1, 2, 3)).count_ascents() == 3
    assert Perm(3210).count_ascents() == 0
    assert Perm(210435).count_ascents() == 2
    assert Perm(1230654).count_ascents() == 3
    assert Perm(31450762).count_ascents() == 3

def test_peaks():
    assert list(Perm().peaks()) == []
    assert list(Perm((0, 1, 2, 3)).peaks()) == []
    assert list(Perm((0, 1, 2, 4, 3)).peaks()) == [3]
    assert list(Perm(210435).peaks()) == [3]
    assert list(Perm(1230654).peaks()) == [2, 4]

def test_peak_list():
    assert Perm().peak_list() == []
    assert Perm((0, 1, 2, 3)).peak_list() == []
    assert Perm((0, 1, 2, 4, 3)).peak_list() == [3]
    assert Perm(210435).peak_list() == [3]
    assert Perm(1230654).peak_list() == [2, 4]

def test_count_peaks():
    assert Perm().count_peaks() == 0
    assert Perm((0, 1, 2, 3)).count_peaks() == 0
    assert Perm(210435).count_peaks() == 1
    assert Perm(1230654).count_peaks() == 2

def test_valleys():
    assert list(Perm().valleys()) == []
    assert list(Perm((0, 1, 2, 3)).valleys()) == []
    assert list(Perm(210435).valleys()) == [2, 4]
    assert list(Perm(1230654).valleys()) == [3]
    assert list(Perm(2130645).valleys()) == [1, 3, 5]

def test_valley_list():
    assert Perm().valley_list() == []
    assert Perm((0, 1, 2, 3)).valley_list() == []
    assert Perm(210435).valley_list() == [2, 4]
    assert Perm(1230654).valley_list() == [3]
    assert Perm(2130645).valley_list() == [1, 3, 5]

def test_count_valleys():
    assert Perm().count_valleys() == 0
    assert Perm((0, 1, 2, 3)).count_valleys() == 0
    assert Perm(210435).count_valleys() == 2
    assert Perm(1230654).count_valleys() == 1
    assert Perm(2130646).count_valleys() == 3

def test_bends():
    assert list(Perm(()).bends()) == []
    assert list(Perm((0, 1)).bends()) == []
    assert list(Perm((2, 0, 1)).bends()) == [1]
    assert list(Perm((5, 3, 4, 0, 2, 1)).bends()) == [1, 2, 3, 4,]
    assert list(Perm((4, 3, 5, 7, 6, 9, 1, 2, 8, 0)).bends()) == [1, 3, 4, 5, 6, 8]
    assert list(Perm((6, 4, 3, 0, 1, 7, 2, 5, 8, 9)).bends()) == [3, 5, 6]

def test_bend_list():
    assert Perm(()).bend_list() == []
    assert Perm((0, 1)).bend_list() == []
    assert Perm((2, 0, 1)).bend_list() == [1]
    assert Perm((5, 3, 4, 0, 2, 1)).bend_list() == [1, 2, 3, 4,]
    assert Perm((4, 3, 5, 7, 6, 9, 1, 2, 8, 0)).bend_list() == [1, 3, 4, 5, 6, 8]
    assert Perm((6, 4, 3, 0, 1, 7, 2, 5, 8, 9)).bend_list() == [3, 5, 6]

def test_order():
    assert Perm(()).order() == 1
    assert Perm((0)).order() == 1
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        args = tuple(perm for _ in range(perm.order() - 1))
        assert perm.compose(*args).is_identity()

def test_ltrmin():
    assert Perm(()).ltrmin() == []
    assert Perm((1)).ltrmin() == [0]
    assert Perm((2, 4, 3, 0, 1)).ltrmin() == [0, 3]
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        ltrmin_list = perm.ltrmin()
        assert ltrmin_list[0] == 0
        for i in range(len(ltrmin_list)):
            for j in range(ltrmin_list[i] + 1, len(perm)):
                if perm[j] < perm[ltrmin_list[i]]:
                    assert ltrmin_list[i + 1] == j
                    break
def test_rtlmin():
    assert Perm(()).rtlmin() == []
    assert Perm((1)).rtlmin() == [0]
    assert Perm((2, 4, 3, 0, 1)).rtlmin() == [3, 4]
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        rtlmin_list = perm.rtlmin()
        rtlmin_list.reverse()
        assert rtlmin_list[0] == len(perm) - 1
        for i in range(len(rtlmin_list)):
            for j in range(rtlmin_list[i] - 1, -1, -1):
                if perm[j] < perm[rtlmin_list[i]]:
                    assert rtlmin_list[i + 1] == j
                    break

def test_ltrmax():
    assert Perm(()).ltrmax() == []
    assert Perm((1)).ltrmax() == [0]
    assert Perm((2, 0, 4, 1, 5, 3)).ltrmax() == [0, 2, 4]
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        ltrmax_list = perm.ltrmax()
        assert ltrmax_list[0] == 0
        for i in range(len(ltrmax_list)):
            for j in range(ltrmax_list[i] + 1, len(perm)):
                if perm[j] > perm[ltrmax_list[i]]:
                    assert ltrmax_list[i + 1] == j
                    break

def test_rtlmax():
    assert Perm(()).rtlmax() == []
    assert Perm((1)).rtlmax() == [0]
    assert Perm((2, 4, 3, 0, 1)).rtlmax() == [1, 2, 4]
    for _ in range(100):
        perm = Perm.random(random.randint(2, 20))
        rtlmax_list = perm.rtlmax()
        rtlmax_list.reverse()
        assert rtlmax_list[0] == len(perm) - 1
        for i in range(len(rtlmax_list)):
            for j in range(rtlmax_list[i] - 1, -1, -1):
                if perm[j] > perm[rtlmax_list[i]]:
                    assert rtlmax_list[i + 1] == j
                    break

def test_count_ltrmin():
    assert Perm(()).count_ltrmin() == 0
    assert Perm((0)).count_ltrmin() == 1
    assert Perm((0, 1)).count_ltrmin() == 1
    assert Perm((4, 0, 6, 3, 2, 1, 5, 8, 7, 9)).count_ltrmin() == 2
    assert Perm((5, 7, 3, 4, 6, 8, 2, 9, 0, 1)).count_ltrmin() == 4
    assert Perm((3, 1, 5, 9, 6, 4, 7, 8, 2, 0)).count_ltrmin() == 3

def test_count_inversions():
    assert Perm(()).count_inversions() == 0
    assert Perm((0)).count_inversions() == 0
    assert Perm((0, 1)).count_inversions() == 0
    assert Perm((1, 0)).count_inversions() == 1
    for _ in range(50):
        perm = Perm.random(random.randint(0,20))
        invs = 0
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if perm[i] > perm[j]:
                    invs += 1
        assert perm.count_inversions() == invs

def test_count_noninversions():
    assert Perm(()).count_noninversions() == 0
    assert Perm((0)).count_noninversions() == 0
    assert Perm((0, 1)).count_noninversions() == 1
    assert Perm((1, 0)).count_noninversions() == 0
    for _ in range(50):
        perm = Perm.random(random.randint(0,20))
        invs = 0
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if perm[i] < perm[j]:
                    invs += 1
        assert perm.count_noninversions() == invs

def test_count_bonds():
    assert Perm(()).count_bonds() == 0
    assert Perm((1)).count_bonds() == 0
    for _ in range(50):
        perm = Perm.random(random.randint(0,20))
        bons = 0
        for i in range(len(perm) - 1):
            if perm[i] + 1 == perm[i + 1] or perm[i] == perm[i + 1] + 1:
                bons += 1
        assert bons == perm.count_bonds()

def test_majorindex():
    assert Perm(()).majorindex() == 0
    assert Perm((0)).majorindex() == 0
    assert Perm((0, 2, 1)).majorindex() == 2
    assert Perm((3, 1, 2, 4, 0)).majorindex() == 5
    assert Perm((3, 0, 7, 4, 1, 2, 5, 6)).majorindex() == 8
    assert Perm((7, 0, 4, 3, 1, 5, 2, 6)).majorindex() == 14

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
    assert Perm((0, 3, 1, 4, 7, 2, 8, 5, 6, 9)).longestruns_descending() == (2, [1, 4, 6])

def test_longestruns():
    assert Perm().longestruns() == (0, [])
    assert Perm((0, 1, 2, 3)).longestruns() == (4, [0])
    assert Perm((4, 3, 2, 1, 0)).longestruns() == (1, [0, 1, 2, 3, 4])
    assert Perm((8, 1, 7, 5, 6, 2, 9, 3, 0, 4)).longestruns() == (2, [1, 3, 5, 8])
    assert Perm((1, 2, 3, 4, 6, 0, 9, 7, 8, 5)).longestruns() == (5, [0])

def test_length_of_longestrun_ascending():
    assert Perm().length_of_longestrun_ascending() == 0
    assert Perm((2, 1, 0)).length_of_longestrun_ascending() == 1
    assert Perm((0, 1, 2)).length_of_longestrun_ascending() == 3
    assert Perm((0, 1, 2, 3, 4, 5, 6, 7, 8, 9)).length_of_longestrun_ascending() == 10
    assert Perm((6, 0, 9, 1, 4, 7, 3, 8, 5, 2)).length_of_longestrun_ascending() == 3

def test_length_of_longestrun_descending():
    assert Perm().length_of_longestrun_descending() == 0
    assert Perm((2, 1, 0)).length_of_longestrun_descending() == 3
    assert Perm((0, 1, 2)).length_of_longestrun_descending() == 1
    assert Perm((3, 5, 2, 7, 1, 8, 0, 6, 9, 4)).length_of_longestrun_descending() == 2
    assert Perm((5, 4, 8, 9, 7, 3, 2, 1, 0, 6)).length_of_longestrun_descending() == 6

def test_length_of_longestrun():
    assert Perm((6, 1, 3, 7, 4, 5, 9, 8, 0, 2)).length_of_longestrun() == 3
    assert Perm((4, 0, 9, 5, 3, 7, 1, 6, 8, 2)).length_of_longestrun() == 3
    assert Perm((1, 9, 4, 6, 0, 8, 2, 7, 5, 3)).length_of_longestrun() == 2
    assert Perm((2, 5, 8, 6, 0, 1, 3, 7, 9, 4)).length_of_longestrun() == 5

def test_count_cycles():
    for i in range(10):
        assert Perm.identity(i).count_cycles() == i
    assert Perm((2, 0, 1)).count_cycles() == 1
    assert Perm((4, 2, 7, 0, 3, 1, 6, 5)).count_cycles() == 3
    assert Perm((5, 3, 8, 1, 0, 4, 2, 7, 6)).count_cycles() == 4

def test_is_involution():
    assert Perm(()).is_involution()
    assert Perm((0)).is_involution()
    for _ in range(30):
        perm = Perm.random(random.randint(0, 20))
        cyclelist = perm.cycle_decomp()
        assert perm.is_involution() == all(map(lambda x: len(x) <= 2, cyclelist))


def test_rank():
    assert list(map(lambda x: x.rank(), PermSet(5))) == list(range(34, 154))


def test_threepats():
    assert all(v == 0 for v in Perm(()).threepats().values())
    assert all(v == 0 for v in Perm((0)).threepats().values())
    assert all(v == 0 for v in Perm((0, 1)).threepats().values())
    assert Perm((2, 1, 0, 3)).threepats() == {Perm((0, 1, 2)): 0, Perm((0, 2, 1)): 0, Perm((1, 0, 2)): 3, Perm((1, 2, 0)): 0, Perm((2, 0, 1)): 0, Perm((2, 1, 0)): 1}
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        threepatdict = perm.threepats()
        for key, val in threepatdict.items():
            assert key.count_occurrences_in(perm) == val

def test_fourpats():
    assert all(v == 0 for v in Perm(()).fourpats().values())
    assert all(v == 0 for v in Perm((0)).fourpats().values())
    assert all(v == 0 for v in Perm((0, 1)).fourpats().values())
    assert Perm((1, 0, 3, 5, 2, 4)).fourpats() == {Perm((0, 1, 2, 3)): 0,
            Perm((0, 1, 3, 2)): 2, Perm((0, 2, 1, 3)): 2, Perm((0, 2, 3, 1)): 2,
            Perm((0, 3, 1, 2)): 2, Perm((0, 3, 2, 1)): 0, Perm((1, 0, 2, 3)): 3,
            Perm((1, 0, 3, 2)): 3, Perm((1, 2, 0, 3)): 0, Perm((1, 2, 3, 0)): 0,
            Perm((1, 3, 0, 2)): 1, Perm((1, 3, 2, 0)): 0, Perm((2, 0, 1, 3)): 0,
            Perm((2, 0, 3, 1)): 0, Perm((2, 1, 0, 3)): 0, Perm((2, 1, 3, 0)): 0,
            Perm((2, 3, 0, 1)): 0, Perm((2, 3, 1, 0)): 0, Perm((3, 0, 1, 2)): 0,
            Perm((3, 0, 2, 1)): 0, Perm((3, 1, 0, 2)): 0, Perm((3, 1, 2, 0)): 0,
            Perm((3, 2, 0, 1)): 0, Perm((3, 2, 1, 0)): 0}
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        fourpatdict = perm.fourpats()
        for key, val in fourpatdict.items():
            assert key.count_occurrences_in(perm) == val

def test_rank_encoding():
    assert Perm(()).rank_encoding() == []
    assert Perm((0)).rank_encoding() == [0]
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        for index, val in enumerate(perm.rank_encoding()):
            invs = 0
            for i in range(index + 1, len(perm)):
                if perm[i] < perm[index]:
                    invs += 1
            assert invs == val

def test_block_decomposition():
    assert Perm(()).block_decomposition() == []
    assert Perm((0)).block_decomposition() == [[]]
    assert Perm((5, 3, 0, 1, 2, 4, 7, 6)).block_decomposition() == [[], [], [2, 3, 6], [2], [1], [1], [0], []]
    assert set(Perm((4, 1, 0, 5, 2, 3)).block_decomposition(True)) == set([Perm((0, 1)), Perm((1, 0))])
    for _ in range(20):
        perm = Perm.random(random.randint(0,20))
        blocks = perm.block_decomposition()
        patts = set(perm.block_decomposition(True))
        for length in range(len(blocks)):
            for start in blocks[length]:
                assert max(perm[start:start + length]) - min(perm[start:start + length]) == length - 1
                assert Perm.to_standard(perm[start:start + length]) in patts

def test_monotone_block_decomposition():
    assert Perm(()).monotone_block_decomposition(True) == []
    assert Perm((0)).monotone_block_decomposition() == []
    assert Perm((0)).monotone_block_decomposition(True) == [(0,0)]
    assert Perm((6, 7, 5, 3, 0, 1, 2, 4)).monotone_block_decomposition() == [(0, 1), (4, 6)]
    assert Perm((0, 2, 1, 5, 6, 7, 4, 3)).monotone_block_decomposition() == [(1, 2), (3, 5), (6, 7)]
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        monblocks = perm.monotone_block_decomposition(True)
        last = -1
        for block in monblocks:
            assert block[0] == last + 1
            last = block[1]
            assert all(perm[i] - perm[i - 1] == perm[block[0] + 1] - perm[block[0]] for i in range(block[0] + 2, block[1]))

def test_monotone_quotient():
    assert Perm(()).monotone_quotient() == Perm(())
    assert Perm((0)).monotone_quotient() == Perm((0))
    assert Perm((0, 2, 1, 5, 6, 7, 4, 3)).monotone_quotient() == Perm((0, 1, 3, 2))
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        monblocks = tuple(start for (start,end) in perm.monotone_block_decomposition(True))
        assert monblocks in list(perm.occurrences_of(perm.monotone_quotient()))

def test_simple_location():
    assert Perm(()).simple_location() == (0, 0)
    assert Perm((0)).simple_location() == (0, 0)
    assert Perm((0, 2, 1, 5, 6, 7, 4, 3)).simple_location() == (7, 1)
    assert Perm((3, 4, 0, 7, 2, 6, 1, 5)).simple_location() == (2, 0)
    for _ in range(20):
        perm = Perm.random(random.randint(0, 20))
        length, start = perm.simple_location()
        if length != 0:
            assert max(perm[start:start + length]) - min(perm[start:start + length]) == length - 1
        else:
            length = 2
        for bigger in range(length + 1, len(perm) - 1):
            for start in range(len(perm) - bigger - 1):
                assert max(perm[start:start + bigger]) - min(perm[start:start + bigger]) != bigger - 1

def test_is_simple():
    assert Perm(()).is_simple()
    assert Perm((0)).is_simple()
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
    assert Perm(()).is_strongly_simple()
    assert Perm((0)).is_strongly_simple()
    assert not Perm((0, 1, 2)).is_strongly_simple()
    assert not Perm((0, 2, 1)).is_strongly_simple()
    assert not Perm((1, 0, 2)).is_strongly_simple()
    assert Perm((4, 1, 6, 3, 0, 7, 2, 5)).is_strongly_simple()

def test_coveredby():
    assert Perm(()).coveredby() == [Perm((0))]
    assert sorted(Perm((0)).coveredby()) == sorted([Perm((0, 1)), Perm((1, 0))])
    assert sorted(Perm((0, 1)).coveredby()) == sorted([Perm((0, 2, 1)), Perm((1, 2, 0)), Perm((0, 1, 2)), Perm((2, 0, 1)), Perm((1, 0, 2))])
    for _ in range(10):
        perm = Perm.random(random.randint(0, 12))
        for p in perm.coveredby():
            assert perm in p.children()

def test_call_1():
    p = Perm((0, 1, 2, 3))
    for i in range(len(p)):
        assert p(i) == i
    with pytest.raises(ValueError): p(-1)
    with pytest.raises(ValueError): p(4)
    with pytest.raises(TypeError): p("abc")

def test_call_2():
    p = Perm((3, 4, 0, 2, 1))
    assert p(0) == 3
    assert p(1) == 4
    assert p(2) == 0
    assert p(3) == 2
    assert p(4) == 1
    with pytest.raises(ValueError): p(-1)
    with pytest.raises(ValueError): p(5)
    with pytest.raises(TypeError): p([1, 2, 3])

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
            l = i+1
            cnt = 0
            for p in PermSet(l):
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
        assert Perm(range(i-1, -1, -1)).is_decreasing()

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
        assert (Perm(l1) >= Perm(l1))
        assert (Perm(l2) >= Perm(l2))

def test_bool():
    assert Perm([0, 1, 2, 3])
    assert Perm([0])
    assert not (Perm([]))
    assert not (Perm())

def test_ascii_plot():
    assert Perm(())._ascii_plot() == ''
    assert Perm((0))._ascii_plot() == '*'
    assert Perm((1, 2, 4, 0, 3, 5))._ascii_plot() == '          *\n    *      \n        *  \n  *        \n*          \n      *    '
    for _ in range(10):
        perm = Perm.random(random.randint(0, 20))
        plot = perm._ascii_plot().split('\n')
        for i in range(len(perm)):
            assert plot[len(perm) - perm[i] - 1][2*i] == '*'

def test_cycle_notation():
    assert Perm(()).cycle_notation() == '( )'
    assert Perm((0)).cycle_notation() == '( 0 )'
    assert Perm((0, 1)).cycle_notation() == '( 0 ) ( 1 )'
    assert Perm((7, 0, 1, 2, 5, 4, 3, 6)).cycle_notation() == '( 5 4 ) ( 7 6 3 2 1 0 )'
