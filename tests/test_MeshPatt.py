import random
import pytest
from permuta import Perm, MeshPatt

def test_init():
    Perm.toggle_check()
    try:
        with pytest.raises(ValueError): MeshPatt(Perm([0, 1, 1]), ())
        with pytest.raises(ValueError): MeshPatt(Perm([1, 0, 1]), ())
        with pytest.raises(ValueError): MeshPatt(Perm([0, 0]), ())
        with pytest.raises(ValueError): MeshPatt(Perm([1]), ())
        with pytest.raises(ValueError): MeshPatt(Perm((1)), ())
        with pytest.raises(ValueError): MeshPatt(Perm(101), ())
        with pytest.raises(ValueError): MeshPatt(Perm(-234), ())
        with pytest.raises(TypeError): MeshPatt(Perm(None), ())
        with pytest.raises(TypeError): MeshPatt(Perm([0.1, 0.2, 0.3]), ())
        with pytest.raises(TypeError): MeshPatt(Perm(()), (0, 1))
        with pytest.raises(TypeError): MeshPatt(Perm((0, 1, 2)), [(1, 'a')])
        with pytest.raises(TypeError): MeshPatt(Perm((0, 1, 2)), [('a', 1)])
        with pytest.raises(ValueError): MeshPatt(Perm.random(5), [(0,), (1, 1)])
        with pytest.raises(ValueError): MeshPatt(Perm.random(5), [(0, 0, 0), (1, 1, 1)])
        with pytest.raises(ValueError): MeshPatt(Perm(()), [(0, 1), (1, 0)])
        with pytest.raises(ValueError): MeshPatt(Perm.random(3), [(0, -1), (0, 0)])
        with pytest.raises(ValueError): MeshPatt(Perm.random(10), [(0, 0), (12, 7)])
        MeshPatt(Perm(), ())
        MeshPatt(Perm([]), ())
        MeshPatt(Perm(0), ())
        MeshPatt(Perm([0]), ())
        MeshPatt(Perm([3, 0, 2, 1]), ())
        MeshPatt(Perm([3, 0, 2, 1]), [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2),
            (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0),
            (4, 1), (4, 2), (4, 3), (4, 4)])
        MeshPatt(Perm([3, 0, 2, 1]), [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])
        MeshPatt([3, 0, 2, 1], [(0, 2), (0, 3), (0, 4)])
        MeshPatt(set([3, 0, 2, 1]), [(0, 2), (0, 3), (0, 4)])
    finally:
        Perm.toggle_check()

def test_complement():
    assert MeshPatt(Perm(), []).complement() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), []).complement() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [(0, 0)]).complement() == MeshPatt(Perm(0), [(0, 1)])
    assert MeshPatt(Perm(0), [(0, 1)]).complement() == MeshPatt(Perm(0), [(0, 0)])
    assert MeshPatt(Perm(0), [(1, 0)]).complement() == MeshPatt(Perm(0), [(1, 1)])
    assert MeshPatt(Perm(0), [(1, 1)]).complement() == MeshPatt(Perm(0), [(1, 0)])
    for _ in range(20):
        mpatt = MeshPatt.random(10)
        comp = mpatt.complement()
        assert len(mpatt.pattern) == len(comp.pattern)
        assert comp.complement() == mpatt

def test_flip_horizontal():
    assert MeshPatt(Perm(), []).flip_vertical() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), [(0, 1)]).flip_horizontal() == MeshPatt(Perm(0), [(0, 0)])

def test_reverse():
    assert MeshPatt(Perm(), []).reverse() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), []).reverse() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [(0, 0)]).reverse() == MeshPatt(Perm(0), [(1, 0)])
    assert MeshPatt(Perm(0), [(0, 1)]).reverse() == MeshPatt(Perm(0), [(1, 1)])
    assert MeshPatt(Perm(0), [(1, 0)]).reverse() == MeshPatt(Perm(0), [(0, 0)])
    assert MeshPatt(Perm(0), [(1, 1)]).reverse() == MeshPatt(Perm(0), [(0, 1)])
    for _ in range(20):
        mpatt = MeshPatt.random(10)
        comp = mpatt.reverse()
        assert len(mpatt.pattern) == len(comp.pattern)
        assert comp.reverse() == mpatt

def test_flip_vertical():
    assert MeshPatt(Perm(), []).flip_vertical() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), [(0, 0)]).flip_vertical() == MeshPatt(Perm(0), [(1, 0)])

def test_inverse():
    assert MeshPatt(Perm(), []).inverse() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), []).inverse() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [(0, 0)]).inverse() == MeshPatt(Perm(0), [(0, 0)])
    assert MeshPatt(Perm(0), [(0, 1)]).inverse() == MeshPatt(Perm(0), [(1, 0)])
    assert MeshPatt(Perm(0), [(1, 0)]).inverse() == MeshPatt(Perm(0), [(0, 1)])
    assert MeshPatt(Perm(0), [(1, 1)]).inverse() == MeshPatt(Perm(0), [(1, 1)])
    for _ in range(20):
        mpatt = MeshPatt.random(10)
        comp = mpatt.inverse()
        assert len(mpatt.pattern) == len(comp.pattern)
        assert comp.inverse() == mpatt

def test_flip_diagonal():
    assert MeshPatt(Perm(), []).flip_diagonal() ==  MeshPatt(Perm(), [])
    assert MeshPatt(Perm(0), [(0, 1)]).flip_diagonal() == MeshPatt(Perm(0), [(1, 0)])

def test_rotate():
    assert MeshPatt(Perm(), [])._rotate_right() == MeshPatt(Perm(), [])
    assert MeshPatt(Perm(), [])._rotate_left() == MeshPatt(Perm(), [])
    assert MeshPatt(Perm(), [])._rotate_180() == MeshPatt(Perm(), [])

    assert MeshPatt(Perm(0), [])._rotate_right() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [])._rotate_left() == MeshPatt(Perm(0), [])
    assert MeshPatt(Perm(0), [])._rotate_180() == MeshPatt(Perm(0), [])

    for _ in range(50):
        mpatt = MeshPatt.random(6)
        assert mpatt._rotate_right()._rotate_right() == mpatt._rotate_180()
        assert mpatt._rotate_left()._rotate_left() == mpatt._rotate_180()
        assert mpatt._rotate_right()._rotate_left() == mpatt
        assert mpatt._rotate_left()._rotate_right() == mpatt
        assert mpatt._rotate_180()._rotate_180() == mpatt

def test_unrank():
    assert MeshPatt.unrank(Perm((0, 1)), 498) == MeshPatt( Perm((0, 1)),
            frozenset({(0, 1), (1, 2), (2, 1), (2, 0), (2, 2), (1, 1)}))
    assert MeshPatt.unrank(Perm((1, 0, 2)), 59731) == MeshPatt( Perm((1, 0, 2)),
            frozenset({(3, 2), (0, 0), (2, 3), (1, 0), (0, 1), (1, 2), (3, 3), (3, 1), (2, 0)}))
    assert MeshPatt.unrank(Perm((0, 3, 2, 1)), 23077382) == MeshPatt(
            Perm((0, 3, 2, 1)),
            frozenset({(0, 1), (4, 4), (1, 4), (2, 3), (4, 2), (4, 1), (0, 2)}))
    for length in range(20):
        m = MeshPatt.unrank(Perm.random(length), 0)
        assert not m.shading
    for length in range(20):
        m = MeshPatt.unrank(Perm.random(length), 2**((length + 1)**2) - 1)
        assert len(m.shading) == (length + 1)**2

    with pytest.raises(TypeError): MeshPatt.unrank(Perm.random(length), 'haha')
    with pytest.raises(ValueError):
        MeshPatt.unrank(Perm.random(10), 2**((10 + 1)**2) + 1)

def test_random():
    assert MeshPatt.random(0) in set([MeshPatt(Perm(()), []), MeshPatt(Perm(()), [(0, 0)])])
    assert MeshPatt.random(1) in set(MeshPatt.unrank(Perm((0)), i) for i in range(0, 16))
    assert MeshPatt.random(2) in (
            set(MeshPatt.unrank(Perm((0, 1)), i) for i in range(0, 512))
            | set(MeshPatt.unrank(Perm((1, 0)), i) for i in range(0, 512)))
    for length in range(3, 20):
        assert len(MeshPatt.random(length)) == length

def test_repr():
    for _ in range(20):
        length = random.randint(0, 20)
        m = MeshPatt(Perm.random(length), random.choices([ (i,j) for i in range(length + 1) for j in range(length + 1)], k=length))
        assert m.__repr__()[:8] == "MeshPatt"

def test_len():
    for _ in range(20):
        length = random.randint(0, 20)
        m = MeshPatt(Perm.random(length), random.choices([ (i,j) for i in range(length + 1) for j in range(length + 1)], k=length))
        assert len(m) == length

def test_bool():
    assert MeshPatt(Perm([0, 1, 2, 3]), ())
    assert MeshPatt(Perm([0, 1, 2, 3]), ((0, 0),))
    assert MeshPatt(Perm([0]), ())
    assert not (MeshPatt(Perm([]), ()))
    assert not (MeshPatt(Perm(), ()))
