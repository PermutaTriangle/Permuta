from permuta import Av, MeshPatt, Perm
from permuta.permset import PermSetAll


def test_av_perm():
    p = Perm((0, 1))
    av = Av([p])
    for length in range(10):
        assert len(set(av.of_length(length))) == 1


def test_av_meshpatt():
    p = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp = MeshPatt(p, shading)
    av = Av([mp])
    enum = [1, 1, 2, 5, 15, 52, 203, 877]  # Bell numbers

    for (n, cnt) in enumerate(enum):
        inst = av.of_length(n)
        gen = list(inst)
        assert len(gen) == cnt


def test_av_empty():
    bases = [[], tuple(), set(), frozenset(), None]
    assert all(isinstance(Av(basis), PermSetAll) for basis in bases)
