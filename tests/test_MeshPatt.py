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

def test_repr():
    for _ in range(20):
        length = random.randint(0, 20)
        m = MeshPatt(Perm.random(length), random.choices([ (i,j) for i in range(length + 1) for j in range(length + 1)], k=length))
        assert m.__repr__()[:11] == "MeshPattern"

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
