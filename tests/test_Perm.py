import random
import pytest
from permuta import Perm, PermSet

def test_init():
    Perm.toggle_check()
    try:
        with pytest.raises(ValueError): Perm([0,1,1])
        with pytest.raises(ValueError): Perm([1,0,1])
        with pytest.raises(ValueError): Perm([0,0])
        with pytest.raises(ValueError): Perm([1])
        with pytest.raises(ValueError): Perm(101)
        with pytest.raises(TypeError): Perm(None)
        Perm()
        Perm([])
        Perm([0])
        Perm([3,0,2,1])
        Perm(set([0,1,2]))
        p = Perm(502134)
        assert p == Perm((5,0,2,1,3,4))
    finally:
        Perm.toggle_check()

def test_to_standard():
    def gen(perm):
        res = list(perm)
        add = 0
        for i in perm.inverse():
            add += random.randint(0,10)
            res[i] += add
        return Perm(res)

    for _ in range(100):
        perm = Perm.random(random.randint(0,20))
        assert perm == Perm.to_standard(perm)
        assert perm == Perm.to_standard(gen(perm))

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
    assert Perm.unrank(1) ==  Perm((0,))
    assert Perm.unrank(2) ==  Perm((0,1))
    assert Perm.unrank(3) ==  Perm((1,0))
    assert Perm.unrank(4) ==  Perm((0,1,2))
    assert Perm.unrank(5) ==  Perm((0,2,1))
    assert Perm.unrank(6) ==  Perm((1,0,2))
    assert Perm.unrank(10) ==  Perm((0,1,2,3))
    amount = 1 + 1 + 2 + 6 + 24
    assert Perm.unrank(amount) == Perm((0,1,2,3,4))
    amount = (1 + 1 + 2 + 6 + 24 + 120) - 1
    assert Perm.unrank(amount) ==Perm((4,3,2,1,0))
    with pytest.raises(AssertionError): Perm.unrank(-1)
    with pytest.raises(AssertionError): Perm.unrank(6, 3)

# TODO: This test will work after PermSet have been changed to be 0 based
@pytest.mark.xfail
def test_unrank_2():
    ps = list(PermSet(7))
    urs = list(Perm.unrank(n, 7) for n in range(len(ps)))
    assert urs == ps

@pytest.mark.xfail
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
        return Perm(perm)

    assert Perm([3,7,0,8,1,6,5,2,4]).contained_in(Perm([3,7,0,8,1,6,5,2,4]))
    assert Perm([]).contained_in(Perm([]))
    assert Perm([]).contained_in(Perm([3,7,0,8,1,6,5,2,4]))
    assert Perm([0]).contained_in(Perm([0]))
    assert not Perm([7,3,0,8,1,6,5,2,4]).contained_in(Perm([3,7,0,8,1,6,5,2,4]))

    for i in range(100):
        # TODO: Ragnar: "That also means I haven't touched this."
        n = random.randint(0, 4)
        patt = PermSet(n).random_element()
        perm = generate_contained(random.randint(n, 8), list(patt))
        assert patt.contained_in(perm)

    assert not Perm([0]).contained_in(Perm([]))
    assert not Perm([0,1]).contained_in(Perm([]))
    assert not Perm([0,1]).contained_in(Perm([0]))
    assert not Perm([1, 0]).contained_in(Perm([0, 1]))
    assert not Perm([0,1,2]).contained_in(Perm([0,1]))
    assert not Perm([1, 0, 2]).contained_in(Perm([0, 1, 3, 4, 2]))
    assert not Perm([0, 1, 2]).contained_in(Perm([2, 1, 3, 0]))
    assert not Perm([2, 1, 3, 0]).contained_in(Perm([2, 0, 3, 1]))
    assert not Perm([0, 2, 1]).contained_in(Perm([2, 0, 1, 3]))
    assert not Perm([2, 0, 1, 3]).contained_in(Perm([5, 3, 2, 7, 1, 0, 6, 4]))
    assert not Perm([0, 1, 2, 3]).contained_in(Perm([4, 7, 5, 1, 6, 2, 3, 0]))

def test_count_occurrences_in():
    assert Perm([]).count_occurrences_in(Perm([4,1,2,3,0])) == 1
    assert Perm([0]).count_occurrences_in(Perm([4,1,2,3,0])) == 5
    assert Perm([0,1]).count_occurrences_in(Perm([4,1,2,3,0])) == 3
    assert Perm([1,0]).count_occurrences_in(Perm([4,1,2,3,0])) == 7
    assert Perm([4,1,2,3,0]).count_occurrences_in(Perm([])) == 0
    assert Perm([4,1,2,3,0]).count_occurrences_in(Perm([1,0])) == 0

def test_occurrences_in():
    assert list(Perm([]).occurrences_in(Perm([4,1,2,3,0]))) == [()]
    assert (sorted(Perm([0]).occurrences_in(Perm([4,1,2,3,0]))) 
            == [(0,),(1,),(2,),(3,),(4,)])
    assert (sorted(Perm([0,1]).occurrences_in(Perm([4,1,2,3,0]))) 
            == [(1,2),(1,3),(2,3)])
    assert (sorted(Perm([1,0]).occurrences_in(Perm([4,1,2,3,0]))) 
            == [(0,1),(0,2),(0,3),(0,4),(1,4),(2,4),(3,4)])
    assert list(Perm([4,1,2,3,0]).occurrences_in(Perm([]))) == []
    assert list(Perm([4,1,2,3,0]).occurrences_in(Perm([1,0]))) == []

def test_apply():
    for i in range(100):
        n = random.randint(0,20)
        lst = [random.randint(0,10000) for _ in range(n)]
        perm = Perm.random(n)
        res = list(perm.apply(lst))
        for j,k in enumerate(perm.inverse()):
            assert lst[j] == res[k]

def test_direct_sum():
    p1 = Perm((0,1,3,2))
    p2 = Perm((0,4,2,1,3))
    p3 = Perm(201)
    p4 = Perm((0,))
    p5 = Perm()
    # All together
    result = p1.direct_sum(p2, p3, p4, p5)
    expected = Perm((0,1,3,2,4,8,6,5,7,11,9,10,12))
    assert result == expected
    # Two
    result = p1.direct_sum(p3)
    expected = Perm((0,1,3,2,6,4,5))
    assert result == expected
    # None
    assert p1.direct_sum() == p1
    
def test_skew_sum():
    p1 = Perm((0,1,3,2))
    p2 = Perm((0,4,2,1,3))
    p3 = Perm(201)
    p4 = Perm((0,))
    p5 = Perm()
    # All together
    result = p1.skew_sum(p2, p3, p4, p5)
    expected = Perm((9,10,12,11,4,8,6,5,7,3,1,2,0))
    assert result == expected
    # Two
    result = p1.skew_sum(p3)
    expected = Perm((3,4,6,5,2,0,1))
    assert result == expected
    # None
    assert p1.skew_sum(), p1

def test_inverse():
    for i in range(10):
        assert Perm(range(i)) == Perm(range(i)).inverse()
    assert Perm([2,1,3,0]) == Perm([3,1,0,2]).inverse()
    assert Perm([4,3,1,6,5,7,8,0,2]) == Perm([7,2,8,1,0,4,3,5,6]).inverse()

def test_rotate_right():
    for i in range(10):
        assert Perm(range(i-1,-1,-1)) == Perm(range(i)).rotate_right()
    assert Perm([2,1,3,4,0,5,6]) == Perm([6,5,3,2,0,1,4]).rotate_right()
    assert Perm([4,5,3,1,7,0,2,6]) == Perm([4,7,1,0,2,6,3,5]).rotate_right()
    assert Perm([0,1,2]) == Perm([2,1,0]).rotate_right(5)
    assert Perm([4,5,3,1,0,2]) == Perm([4,5,3,1,0,2]).rotate_right(4)

def test_rotate_left():
    for i in range(10):
        assert Perm(list(range(i-1,-1,-1))) == Perm(range(i)).rotate_right()
    assert (Perm([6,5,3,2,0,1,4]).rotate_left() 
            == Perm([6,5,3,2,0,1,4]).rotate_right(3))
    assert (Perm([6,5,3,2,0,1,4]).rotate_left() 
            == Perm([6,5,3,2,0,1,4]).rotate_right(-1))
    assert (Perm([4,7,1,0,2,6,3,5]).rotate_left() 
            == Perm([4,7,1,0,2,6,3,5]).rotate_right(7))
    assert Perm([]).rotate_left() == Perm([]).rotate_left(123)

def test_shift_left():
    assert Perm([]) == Perm([]).shift_left()
    assert Perm([0]) == Perm([0]).shift_left()
    assert Perm([0,1,2,3,4,5,6,7]) == Perm([0,1,2,3,4,5,6,7]).shift_left(0)
    assert Perm([0,1,2,3,4,5,6,7]) == Perm([5,6,7,0,1,2,3,4]).shift_left(3)
    assert Perm([0,1,2,3,4,5,6,7]) == Perm([0,1,2,3,4,5,6,7]).shift_left(800)
    assert Perm([0,1,2,3,4,5,6,7]) == Perm([5,6,7,0,1,2,3,4]).shift_left(403)
    assert Perm([0,1,2,3,4,5,6,7]) == Perm([0,1,2,3,4,5,6,7]).shift_left(-8)
    assert Perm([0,1,2,3,4,5,6,7]) == Perm([5,6,7,0,1,2,3,4]).shift_left(-5)

def test_shift_down():
    assert Perm([]) == Perm([]).shift_down(1000)
    assert Perm([0]) == Perm([0]).shift_down(10)
    assert Perm([1,0,4,2,3,5]) == Perm([2,1,5,3,4,0]).shift_down()
    assert Perm([1,0,4,2,3,5]) == Perm([2,1,5,3,4,0]).shift_down(13)
    assert Perm([1,0,4,2,3,5]) == Perm([5,4,2,0,1,3]).shift_down(-2)
    assert Perm([1,0,4,2,3,5]) == Perm([5,4,2,0,1,3]).shift_down(-8)

def test_reverse():
    assert Perm([5,2,3,0,4,6,1]) == Perm([1,6,4,0,3,2,5]).reverse()
    assert Perm([7,1,0,2,4,6,3,5]) == Perm([5,3,6,4,2,0,1,7]).reverse()

def test_complement():
    assert Perm([6,4,2,3,1,0,5]) == Perm([0,2,4,3,5,6,1]).complement()
    assert Perm([2,5,6,3,7,4,0,1]) == Perm([5,2,1,4,0,3,7,6]).complement()

def test_reverse_complement():
    for _ in range(100):
        perm = Perm.random(random.randint(0,20))
        assert perm.reverse_complement() == perm.rotate().rotate()

def test_flip_antidiagonal():
    for i in range(100):
        perm = Perm.random(random.randint(0,20))
        assert perm.reverse().complement().inverse() == perm.flip_antidiagonal()

def test_fixed_points():
    assert Perm().fixed_points() == 0
    assert Perm((0,2,1)).fixed_points() == 1
    assert Perm(543210).fixed_points() == 0
    assert Perm(410325).fixed_points() == 3
    assert Perm((0,1,2,3,4,5)).fixed_points() == 6


def test_descents():
    assert list(Perm().descents()) == []
    assert list(Perm((0,1,2,3)).descents()) == []
    assert list(Perm(3210).descents()) == [1,2,3]
    assert list(Perm(210435).descents()) == [1, 2, 4]
    assert list(Perm(1230654).descents()) == [3, 5, 6]
    assert list(Perm(31450762).descents()) == [1, 4, 6, 7]

def test_count_descents():
    assert Perm().count_descents() == 0
    assert Perm((0,1,2,3)).count_descents() == 0
    assert Perm(3210).count_descents() == 3
    assert Perm(210435).count_descents() == 3
    assert Perm(1230654).count_descents() == 3
    assert Perm(31450762).count_descents() == 4

def test_ascents():
    assert list(Perm().ascents()) == []
    assert list(Perm((0,1,2,3)).ascents()) == [1,2,3]
    assert list(Perm(3210).ascents()) == []
    assert list(Perm(210435).ascents()) == [3, 5]
    assert list(Perm(1230654).ascents()) == [1, 2, 4]
    assert list(Perm(31450762).ascents()) == [2, 3, 5]

def test_count_ascents():
    assert Perm().count_ascents() == 0
    assert Perm((0,1,2,3)).count_ascents() == 3
    assert Perm(3210).count_ascents() == 0
    assert Perm(210435).count_ascents() == 2
    assert Perm(1230654).count_ascents() == 3
    assert Perm(31450762).count_ascents() == 3

def test_peaks():
    assert list(Perm().peaks()) == []
    assert list(Perm((0,1,2,3)).peaks()) == []
    assert list(Perm(210435).peaks()) == [3]
    assert list(Perm(1230654).peaks()) == [2, 4]

def test_count_peaks():
    assert Perm().count_peaks() == 0
    assert Perm((0,1,2,3)).count_peaks() == 0
    assert Perm(210435).count_peaks() == 1
    assert Perm(1230654).count_peaks() == 2

def test_valleys():
    assert list(Perm().valleys()) == []
    assert list(Perm((0,1,2,3)).valleys()) == []
    assert list(Perm(210435).valleys()) == [2, 4]
    assert list(Perm(1230654).valleys()) == [3]
    assert list(Perm(2130645).valleys()) == [1, 3, 5]

def test_count_valleys():
    assert Perm().count_valleys() == 0
    assert Perm((0,1,2,3)).count_valleys() == 0
    assert Perm(210435).count_valleys() == 2
    assert Perm(1230654).count_valleys() == 1
    assert Perm(2130646).count_valleys() == 3

def test_longestruns_ascending():
    assert Perm().longestruns_ascending() == (0, [])
    assert Perm((0, 1, 2, 3)).longestruns_ascending() == (4, [0])
    assert Perm((4, 3, 2, 1, 0)).longestruns_ascending() == (1, [0, 1, 2, 3, 4])
    assert Perm((8, 1, 7, 5, 6, 2, 9, 3, 0, 4)).longestruns_ascending() == (2, [1, 3, 5, 8])
    assert Perm((1, 2, 3, 4, 6, 0, 9, 7, 8, 5)).longestruns_ascending() == (5, [0])

def test_longestruns_descending():
    assert Perm().longestruns_descending() == (0, [])
    assert Perm((3,2,1,0)).longestruns_descending() == (4, [0])
    assert Perm((0, 1, 2, 3, 4)).longestruns_descending() == (1, [0, 1, 2, 3, 4])
    assert Perm((3, 9, 7, 0, 2, 5, 8, 6, 4, 1)).longestruns_descending() == (4, [6])
    assert Perm((0, 3, 1, 4, 7, 2, 8, 5, 6, 9)).longestruns_descending() == (2, [1, 4, 6])

def test_longestruns():
    assert Perm().longestruns_ascending() == (0, [])
    assert Perm((0, 1, 2, 3)).longestruns_ascending() == (4, [0])
    assert Perm((4, 3, 2, 1, 0)).longestruns_ascending() == (1, [0, 1, 2, 3, 4])
    assert Perm((8, 1, 7, 5, 6, 2, 9, 3, 0, 4)).longestruns_ascending() == (2, [1, 3, 5, 8])
    assert Perm((1, 2, 3, 4, 6, 0, 9, 7, 8, 5)).longestruns_ascending() == (5, [0])


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

def test_call_1():
    p = Perm((0,1,2,3))
    for i in range(len(p)):
        assert p(i) == i
    with pytest.raises(ValueError): p(-1)
    with pytest.raises(ValueError): p(4)
    with pytest.raises(TypeError): p("abc")

def test_call_2():
    p = Perm((3,4,0,2,1))
    assert p(0) == 3
    assert p(1) == 4
    assert p(2) == 0
    assert p(3) == 2
    assert p(4) == 1
    with pytest.raises(ValueError): p(-1)
    with pytest.raises(ValueError): p(5)
    with pytest.raises(TypeError): p([1,2,3])

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
        a = Perm.random(random.randint(0,10))
        b = Perm(a)
        c = Perm.random(random.randint(0,10))
        if a == c:
            continue
        assert a == b
        assert a != c
        assert b == a
        assert c != a

def test_avoids():
    assert Perm([4,0,1,2,3]).avoids()
    assert not (Perm([4,0,1,2,3]).avoids(Perm([0,1,2])))
    assert not (Perm([4,0,1,2,3]).avoids(Perm([1,0])))
    assert Perm([4,0,1,2,3]).avoids(Perm([2,1,0]))
    assert not (Perm([4,0,1,2,3]).avoids(Perm([2,1,0]), Perm([1,0])))
    assert Perm([4,0,1,2,3]).avoids(Perm([2,1,0]), Perm([1,2,0]))

# TODO: Have to examine this function
@pytest.mark.xfail
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
        assert Perm(range(i)).is_increasing()
        assert Perm(range(i-1,-1,-1)).is_decreasing()

    assert not (Perm([0,2,1]).is_increasing())
    assert not (Perm([0,2,1]).is_decreasing())
    assert not (Perm([1,0,2]).is_increasing())
    assert not (Perm([1,0,2]).is_decreasing())

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

def test_bool():
    assert Perm([0,1,2,3])
    assert Perm([0])
    assert not (Perm([]))
    assert not (Perm())
