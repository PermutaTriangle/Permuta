import random
import pytest
from permuta import MeshPattern, Permutation, Permutations
    

def test_init():
    Permutation.toggle_check()
    try:
        with pytest.raises(ValueError): Permutation([0,1,1])
        with pytest.raises(ValueError): Permutation([1,0,1])
        with pytest.raises(ValueError): Permutation([0,0])
        with pytest.raises(ValueError): Permutation([1])
        with pytest.raises(ValueError): Permutation(101)
        with pytest.raises(TypeError): Permutation(None)
        Permutation()
        Permutation([])
        Permutation([0])
        Permutation([3,0,2,1])
        Permutation(set([0,1,2]))
        p = Permutation(502134)
        assert p == Permutation((5,0,2,1,3,4))
    finally:
        Permutation.toggle_check()

def test_to_standard():
    def gen(perm):
        res = list(perm)
        add = 0
        for i in perm.inverse():
            add += random.randint(0,10)
            res[i] += add
        return Permutation(res)

    for _ in range(100):
        perm = Permutation.random(random.randint(0,20))
        assert perm == Permutation.to_standard(perm)
        assert perm == Permutation.to_standard(gen(perm))

def test_identity():
    for length in range(11):
        assert Permutation.identity(length) == Permutation(range(length))

def test_random():
    Permutation.toggle_check()
    try:
        for length in range(11):
            for _ in range(10):
                perm = Permutation.random(length)
                assert len(perm) == length
                Permutation(perm)
    finally:
        Permutation.toggle_check()

def test_monotone_increasing():
    for length in range(11):
        assert Permutation.monotone_increasing(length) ==  Permutation(range(length))

def test_monotone_decreasing():
    for length in range(11):
        assert Permutation.monotone_decreasing(length) ==  Permutation(range(length-1, -1, -1))

def test_unrank():
    assert Permutation.unrank(0) ==  Permutation()
    assert Permutation.unrank(1) ==  Permutation((0,))
    assert Permutation.unrank(2) ==  Permutation((0,1))
    assert Permutation.unrank(3) ==  Permutation((1,0))
    assert Permutation.unrank(4) ==  Permutation((0,1,2))
    assert Permutation.unrank(5) ==  Permutation((0,2,1))
    assert Permutation.unrank(6) ==  Permutation((1,0,2))
    assert Permutation.unrank(10) ==  Permutation((0,1,2,3))
    amount = 1 + 1 + 2 + 6 + 24
    assert Permutation.unrank(amount) == Permutation((0,1,2,3,4))
    amount = (1 + 1 + 2 + 6 + 24 + 120) - 1
    assert Permutation.unrank(amount) ==Permutation((4,3,2,1,0))
    with pytest.raises(AssertionError): Permutation.unrank(-1)
    with pytest.raises(AssertionError): Permutation.unrank(6, 3)

# TODO: This test will work after Permutations have been changed to be 0 based
@pytest.mark.xfail
def test_unrank_2():
    ps = list(Permutations(7))
    urs = list(Permutation.unrank(n, 7) for n in range(len(ps)))
    assert urs == ps

def test_contained_in():
    def generate_contained(n,perm):
        # TODO: Ragnar: "I don't know how to make this method 0-based, Murray?". Murray: "It works :\"
        for i in range(len(perm),n):
            r = random.randint(1,len(perm)+1)
            for i in range(len(perm)):
                if perm[i] >= r:
                    perm[i] += 1
            x = random.randint(0,len(perm))
            perm = perm[:x] + [r] + perm[x:]
        return Permutation(perm)

    assert Permutation([3,7,0,8,1,6,5,2,4]).contained_in(Permutation([3,7,0,8,1,6,5,2,4]))
    assert Permutation([]).contained_in(Permutation([]))
    assert Permutation([]).contained_in(Permutation([3,7,0,8,1,6,5,2,4]))
    assert Permutation([0]).contained_in(Permutation([0]))
    assert not Permutation([7,3,0,8,1,6,5,2,4]).contained_in(Permutation([3,7,0,8,1,6,5,2,4]))

    for i in range(100):
        # TODO: Ragnar: "That also means I haven't touched this."
        n = random.randint(0, 4)
        patt = Permutations(n).random_element()
        perm = generate_contained(random.randint(n, 8), list(patt))
        assert patt.contained_in(perm)

    assert not Permutation([0]).contained_in(Permutation([]))
    assert not Permutation([0,1]).contained_in(Permutation([]))
    assert not Permutation([0,1]).contained_in(Permutation([0]))
    assert not Permutation([1, 0]).contained_in(Permutation([0, 1]))
    assert not Permutation([0,1,2]).contained_in(Permutation([0,1]))
    assert not Permutation([1, 0, 2]).contained_in(Permutation([0, 1, 3, 4, 2]))
    assert not Permutation([0, 1, 2]).contained_in(Permutation([2, 1, 3, 0]))
    assert not Permutation([2, 1, 3, 0]).contained_in(Permutation([2, 0, 3, 1]))
    assert not Permutation([0, 2, 1]).contained_in(Permutation([2, 0, 1, 3]))
    assert not Permutation([2, 0, 1, 3]).contained_in(Permutation([5, 3, 2, 7, 1, 0, 6, 4]))
    assert not Permutation([0, 1, 2, 3]).contained_in(Permutation([4, 7, 5, 1, 6, 2, 3, 0]))

def test_count_occurrences_in():
    assert Permutation([]).count_occurrences_in(Permutation([4,1,2,3,0])) == 1
    assert Permutation([0]).count_occurrences_in(Permutation([4,1,2,3,0])) == 5
    assert Permutation([0,1]).count_occurrences_in(Permutation([4,1,2,3,0])) == 3
    assert Permutation([1,0]).count_occurrences_in(Permutation([4,1,2,3,0])) == 7
    assert Permutation([4,1,2,3,0]).count_occurrences_in(Permutation([])) == 0
    assert Permutation([4,1,2,3,0]).count_occurrences_in(Permutation([1,0])) == 0

def test_occurrences_in():
    assert list(Permutation([]).occurrences_in(Permutation([4,1,2,3,0]))) == [()]
    assert (sorted(Permutation([0]).occurrences_in(Permutation([4,1,2,3,0]))) 
            == [(0,),(1,),(2,),(3,),(4,)])
    assert (sorted(Permutation([0,1]).occurrences_in(Permutation([4,1,2,3,0]))) 
            == [(1,2),(1,3),(2,3)])
    assert (sorted(Permutation([1,0]).occurrences_in(Permutation([4,1,2,3,0]))) 
            == [(0,1),(0,2),(0,3),(0,4),(1,4),(2,4),(3,4)])
    assert list(Permutation([4,1,2,3,0]).occurrences_in(Permutation([]))) == []
    assert list(Permutation([4,1,2,3,0]).occurrences_in(Permutation([1,0]))) == []

def test_apply():
    for i in range(100):
        n = random.randint(0,20)
        lst = [random.randint(0,10000) for _ in range(n)]
        perm = Permutation.random(n)
        res = list(perm.apply(lst))
        for j,k in enumerate(perm.inverse()):
            assert lst[j] == res[k]

def test_direct_sum():
    p1 = Permutation((0,1,3,2))
    p2 = Permutation((0,4,2,1,3))
    p3 = Permutation(201)
    p4 = Permutation((0,))
    p5 = Permutation()
    # All together
    result = p1.direct_sum(p2, p3, p4, p5)
    expected = Permutation((0,1,3,2,4,8,6,5,7,11,9,10,12))
    assert result == expected
    # Two
    result = p1.direct_sum(p3)
    expected = Permutation((0,1,3,2,6,4,5))
    assert result == expected
    # None
    assert p1.direct_sum() == p1
    
def test_skew_sum():
    p1 = Permutation((0,1,3,2))
    p2 = Permutation((0,4,2,1,3))
    p3 = Permutation(201)
    p4 = Permutation((0,))
    p5 = Permutation()
    # All together
    result = p1.skew_sum(p2, p3, p4, p5)
    expected = Permutation((9,10,12,11,4,8,6,5,7,3,1,2,0))
    assert result == expected
    # Two
    result = p1.skew_sum(p3)
    expected = Permutation((3,4,6,5,2,0,1))
    assert result == expected
    # None
    assert p1.skew_sum(), p1

def test_inverse():
    for i in range(10):
        assert Permutation(range(i)) == Permutation(range(i)).inverse()
    assert Permutation([2,1,3,0]) == Permutation([3,1,0,2]).inverse()
    assert Permutation([4,3,1,6,5,7,8,0,2]) == Permutation([7,2,8,1,0,4,3,5,6]).inverse()

def test_rotate_right():
    for i in range(10):
        assert Permutation(range(i-1,-1,-1)) == Permutation(range(i)).rotate_right()
    assert Permutation([2,1,3,4,0,5,6]) == Permutation([6,5,3,2,0,1,4]).rotate_right()
    assert Permutation([4,5,3,1,7,0,2,6]) == Permutation([4,7,1,0,2,6,3,5]).rotate_right()
    assert Permutation([0,1,2]) == Permutation([2,1,0]).rotate_right(5)
    assert Permutation([4,5,3,1,0,2]) == Permutation([4,5,3,1,0,2]).rotate_right(4)

def test_rotate_left():
    for i in range(10):
        assert Permutation(list(range(i-1,-1,-1))) == Permutation(range(i)).rotate_right()
    assert (Permutation([6,5,3,2,0,1,4]).rotate_left() 
            == Permutation([6,5,3,2,0,1,4]).rotate_right(3))
    assert (Permutation([6,5,3,2,0,1,4]).rotate_left() 
            == Permutation([6,5,3,2,0,1,4]).rotate_right(-1))
    assert (Permutation([4,7,1,0,2,6,3,5]).rotate_left() 
            == Permutation([4,7,1,0,2,6,3,5]).rotate_right(7))
    assert Permutation([]).rotate_left() == Permutation([]).rotate_left(123)

def test_shift_left():
    assert Permutation([]) == Permutation([]).shift_left()
    assert Permutation([0]) == Permutation([0]).shift_left()
    assert Permutation([0,1,2,3,4,5,6,7]) == Permutation([0,1,2,3,4,5,6,7]).shift_left(0)
    assert Permutation([0,1,2,3,4,5,6,7]) == Permutation([5,6,7,0,1,2,3,4]).shift_left(3)
    assert Permutation([0,1,2,3,4,5,6,7]) == Permutation([0,1,2,3,4,5,6,7]).shift_left(800)
    assert Permutation([0,1,2,3,4,5,6,7]) == Permutation([5,6,7,0,1,2,3,4]).shift_left(403)
    assert Permutation([0,1,2,3,4,5,6,7]) == Permutation([0,1,2,3,4,5,6,7]).shift_left(-8)
    assert Permutation([0,1,2,3,4,5,6,7]) == Permutation([5,6,7,0,1,2,3,4]).shift_left(-5)

def test_shift_down():
    assert Permutation([]) == Permutation([]).shift_down(1000)
    assert Permutation([0]) == Permutation([0]).shift_down(10)
    assert Permutation([1,0,4,2,3,5]) == Permutation([2,1,5,3,4,0]).shift_down()
    assert Permutation([1,0,4,2,3,5]) == Permutation([2,1,5,3,4,0]).shift_down(13)
    assert Permutation([1,0,4,2,3,5]) == Permutation([5,4,2,0,1,3]).shift_down(-2)
    assert Permutation([1,0,4,2,3,5]) == Permutation([5,4,2,0,1,3]).shift_down(-8)

def test_reverse():
    assert Permutation([5,2,3,0,4,6,1]) == Permutation([1,6,4,0,3,2,5]).reverse()
    assert Permutation([7,1,0,2,4,6,3,5]) == Permutation([5,3,6,4,2,0,1,7]).reverse()

def test_complement():
    assert Permutation([6,4,2,3,1,0,5]) == Permutation([0,2,4,3,5,6,1]).complement()
    assert Permutation([2,5,6,3,7,4,0,1]) == Permutation([5,2,1,4,0,3,7,6]).complement()

def test_reverse_complement():
    for _ in range(100):
        perm = Permutation.random(random.randint(0,20))
        assert perm.reverse_complement() == perm.rotate().rotate()

def test_flip_antidiagonal():
    for i in range(100):
        perm = Permutation.random(random.randint(0,20))
        assert perm.reverse().complement().inverse() == perm.flip_antidiagonal()

def test_fixed_points():
    assert Permutation().fixed_points() == 0
    assert Permutation((0,2,1)).fixed_points() == 1
    assert Permutation(543210).fixed_points() == 0
    assert Permutation(410325).fixed_points() == 3
    assert Permutation((0,1,2,3,4,5)).fixed_points() == 6


def test_descents():
    assert list(Permutation().descents()) == []
    assert list(Permutation((0,1,2,3)).descents()) == []
    assert list(Permutation(3210).descents()) == [1,2,3]
    assert list(Permutation(210435).descents()) == [1, 2, 4]
    assert list(Permutation(1230654).descents()) == [3, 5, 6]
    assert list(Permutation(31450762).descents()) == [1, 4, 6, 7]

def test_count_descents():
    assert Permutation().count_descents() == 0
    assert Permutation((0,1,2,3)).count_descents() == 0
    assert Permutation(3210).count_descents() == 3
    assert Permutation(210435).count_descents() == 3
    assert Permutation(1230654).count_descents() == 3
    assert Permutation(31450762).count_descents() == 4

def test_ascents():
    assert list(Permutation().ascents()) == []
    assert list(Permutation((0,1,2,3)).ascents()) == [1,2,3]
    assert list(Permutation(3210).ascents()) == []
    assert list(Permutation(210435).ascents()) == [3, 5]
    assert list(Permutation(1230654).ascents()) == [1, 2, 4]
    assert list(Permutation(31450762).ascents()) == [2, 3, 5]

def test_count_ascents():
    assert Permutation().count_ascents() == 0
    assert Permutation((0,1,2,3)).count_ascents() == 3
    assert Permutation(3210).count_ascents() == 0
    assert Permutation(210435).count_ascents() == 2
    assert Permutation(1230654).count_ascents() == 3
    assert Permutation(31450762).count_ascents() == 3

def test_peaks():
    assert list(Permutation().peaks()) == []
    assert list(Permutation((0,1,2,3)).peaks()) == []
    assert list(Permutation(210435).peaks()) == [3]
    assert list(Permutation(1230654).peaks()) == [2, 4]

def test_count_peaks():
    assert Permutation().count_peaks() == 0
    assert Permutation((0,1,2,3)).count_peaks() == 0
    assert Permutation(210435).count_peaks() == 1
    assert Permutation(1230654).count_peaks() == 2

def test_valleys():
    assert list(Permutation().valleys()) == []
    assert list(Permutation((0,1,2,3)).valleys()) == []
    assert list(Permutation(210435).valleys()) == [2, 4]
    assert list(Permutation(1230654).valleys()) == [3]
    assert list(Permutation(2130645).valleys()) == [1, 3, 5]

def test_count_valleys():
    assert Permutation().count_valleys() == 0
    assert Permutation((0,1,2,3)).count_valleys() == 0
    assert Permutation(210435).count_valleys() == 2
    assert Permutation(1230654).count_valleys() == 1
    assert Permutation(2130646).count_valleys() == 3

def test_call_1():
    p = Permutation((0,1,2,3))
    for i in range(len(p)):
        assert p(i) == i
    with pytest.raises(ValueError): p(-1)
    with pytest.raises(ValueError): p(4)
    with pytest.raises(TypeError): p("abc")

def test_call_2():
    p = Permutation((3,4,0,2,1))
    assert p(0) == 3
    assert p(1) == 4
    assert p(2) == 0
    assert p(3) == 2
    assert p(4) == 1
    with pytest.raises(ValueError): p(-1)
    with pytest.raises(ValueError): p(5)
    with pytest.raises(TypeError): p([1,2,3])

def test_eq():
    assert Permutation([]) == Permutation([])
    assert Permutation([0]) == Permutation([0])
    assert Permutation([]) != Permutation([0])
    assert Permutation([0]) != Permutation([])
    assert not (Permutation([]) != Permutation([]))
    assert not (Permutation([0]) != Permutation([0]))
    assert not (Permutation([]) == Permutation([0]))
    assert not (Permutation([0]) == Permutation([]))
    for _ in range(100):
        a = Permutation.random(random.randint(0,10))
        b = Permutation(a)
        c = Permutation.random(random.randint(0,10))
        if a == c:
            continue
        assert a == b
        assert a != c
        assert b == a
        assert c != a

def test_avoids():
    assert Permutation([4,0,1,2,3]).avoids()
    assert not (Permutation([4,0,1,2,3]).avoids(Permutation([0,1,2])))
    assert not (Permutation([4,0,1,2,3]).avoids(Permutation([1,0])))
    assert Permutation([4,0,1,2,3]).avoids(Permutation([2,1,0]))
    assert not (Permutation([4,0,1,2,3]).avoids(Permutation([2,1,0]), Permutation([1,0])))
    assert Permutation([4,0,1,2,3]).avoids(Permutation([2,1,0]), Permutation([1,2,0]))

# TODO: Have to examine this function
@pytest.mark.xfail
def test_avoids_2():
    bound = 6
    def do_test(patts, expected):
        for i in range(min(len(expected), bound)):
            l = i+1
            cnt = 0
            for p in Permutations(l):
                ok = True
                for patt in patts:
                    if not p.avoids(Permutation(patt)):
                        ok = False
                        break
                if ok:
                    cnt += 1
            assert expected[i] == cnt

    do_test([[0,1,2]], [1, 2, 5, 14, 42, 132, 429, 1430])
    do_test([[1,2,0]], [1, 2, 5, 14, 42, 132, 429, 1430])
    do_test([[0,2,3,1]], [1, 2, 6, 23, 103, 512, 2740, 15485])
    do_test([[1,3,0,2]], [1, 2, 6, 23, 103, 512, 2740, 15485])
    do_test([[0,1,2,3]], [1, 2, 6, 23, 103, 513, 2761, 15767])
    do_test([[0,3,2,1]], [1, 2, 6, 23, 103, 513, 2761, 15767])
    do_test([[1,0,3,2]], [1, 2, 6, 23, 103, 513, 2761, 15767])
    do_test([[0,2,1,3]], [1, 2, 6, 23, 103, 513, 2762, 15793])

def test_incr_decr():
    for i in range(100):
        assert Permutation(range(i)).is_increasing()
        assert Permutation(range(i-1,-1,-1)).is_decreasing()

    assert not (Permutation([0,2,1]).is_increasing())
    assert not (Permutation([0,2,1]).is_decreasing())
    assert not (Permutation([1,0,2]).is_increasing())
    assert not (Permutation([1,0,2]).is_decreasing())

def test_lt():
    # TODO: No length testing is done here
    for _ in range(30):
        l1 = list(range(10))
        l2 = list(range(10))
        random.shuffle(l1)
        random.shuffle(l2)
        if l1 < l2:
            assert Permutation(l1) < Permutation(l2)
        else:
            assert not (Permutation(l1) < Permutation(l2))
        assert not (Permutation(l1) < Permutation(l1))
        assert not (Permutation(l2) < Permutation(l2))

def test_bool():
    assert Permutation([0,1,2,3])
    assert Permutation([0])
    assert not (Permutation([]))
    assert not (Permutation())
