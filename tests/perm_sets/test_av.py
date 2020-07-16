from math import factorial

import pytest
from permuta import MeshPatt, Perm
from permuta.perm_sets import Av
from permuta.perm_sets.basis import Basis, MeshBasis


# binom will be added to math in 3.8 so when pypy is compatible with 3.8, replace:
def binom(n, k):
    return factorial(n) // (factorial(n - k) * factorial(k))


def catalan(n):
    return binom(2 * n, n) // (n + 1)


test_classes = [
    ([[0, 1]], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
    ([[1, 0]], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
    ([[0, 1, 2]], [catalan(i) for i in range(8)]),
    ([[0, 2, 1]], [catalan(i) for i in range(8)]),
    ([[1, 0, 2]], [catalan(i) for i in range(8)]),
    ([[1, 2, 0]], [catalan(i) for i in range(8)]),
    ([[2, 0, 1]], [catalan(i) for i in range(8)]),
    ([[2, 1, 0]], [catalan(i) for i in range(8)]),
    ([[0, 2, 1, 3]], [1, 1, 2, 6, 23, 103, 513, 2762]),
    ([[0, 2, 3, 1]], [1, 1, 2, 6, 23, 103, 512, 2740, 15485]),
    ([[0, 3, 2, 1]], [1, 1, 2, 6, 23, 103, 513, 2761, 15767]),
    ([[1, 0, 2], [2, 1, 0]], [1, 1, 2, 4, 7, 11, 16, 22]),
    ([[0, 2, 1], [3, 2, 1, 0]], [1, 1, 2, 5, 13, 31, 66, 127]),
    ([[2, 1, 0], [1, 2, 3, 0]], [1, 1, 2, 5, 13, 34, 89, 233]),
    ([[3, 2, 1, 0], [3, 2, 0, 1]], [1, 1, 2, 6, 22, 90, 394, 1806]),
    ([[2, 3, 0, 1], [1, 3, 0, 2]], [1, 1, 2, 6, 22, 90, 395, 1823]),
    (
        [[3, 1, 2, 0], [2, 4, 0, 3, 1], [3, 1, 4, 0, 2], [2, 4, 0, 5, 1, 3]],
        [1, 1, 2, 6, 23, 101, 477, 2343, 11762],
    ),
    ([[0, 2, 1], [2, 1, 3, 4, 0]], [1, 1, 2, 5, 14, 41, 122, 365, 1094]),
]


@pytest.mark.parametrize("patts,enum", test_classes)
def test_avoiding_enumeration(patts, enum):
    patts = [Perm(patt) for patt in patts]
    basis = Basis(*patts)
    for (n, cnt) in enumerate(enum):
        # print(n, cnt)
        inst = Av(basis).of_length(n)
        gen = list(inst)
        # assert len(gen) == cnt
        assert len(gen) == len(set(gen))
        for perm in gen:
            assert perm.avoids(*patts)

    mx = len(enum) - 1
    cnt = [0 for _ in range(mx + 1)]
    for perm in Av(basis).up_to_length(mx):
        assert perm.avoids(*patts)
        cnt[len(perm)] += 1

    assert enum == cnt


def test_avoiding_generic_mesh_patterns():
    p = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mps = [MeshPatt(p, shading)]
    meshbasis = MeshBasis(*mps)
    avoiding_generic_basis = Av(meshbasis)
    enum = [1, 1, 2, 5, 15, 52, 203, 877]  # Bell numbers

    for (n, cnt) in enumerate(enum):
        inst = avoiding_generic_basis.of_length(n)
        gen = list(inst)
        assert len(gen) == cnt
        assert len(gen) == len(set(gen))
        for perm in gen:
            assert perm.avoids(*mps)
            assert perm in avoiding_generic_basis

    mx = len(enum) - 1
    cnt = [0 for _ in range(mx + 1)]
    for perm in Av(meshbasis).up_to_length(mx):
        assert perm.avoids(*mps)
        cnt[len(perm)] += 1

    assert enum == cnt


def test_avoiding_generic_finite_class():
    ts = [
        ([[0]], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ([[0, 1], [3, 2, 1, 0]], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]),
        ([[0, 1, 2], [3, 2, 1, 0]], [1, 1, 2, 5, 13, 25, 25, 0, 0, 0, 0, 0]),
    ]

    for (patts, enum) in ts:
        patts = [Perm(patt) for patt in patts]
        basis = Basis(*patts)
        for (n, cnt) in enumerate(enum):
            inst = Av(basis).of_length(n)
            gen = list(inst)
            assert len(gen) == cnt
            assert len(gen) == len(set(gen))
            for perm in gen:
                assert perm.avoids(*patts)

        mx = len(enum) - 1
        cnt = [0 for _ in range(mx + 1)]
        for perm in Av(basis).up_to_length(mx):
            assert perm.avoids(*patts)
            cnt[len(perm)] += 1

        assert enum == cnt


def test_is_subclass():
    av1 = Av((Perm((0,)),))
    av12_21 = Av((Perm((0, 1)), Perm((1, 0))))
    av123 = Av((Perm((0, 1, 2)),))
    av1234 = Av((Perm((0, 1, 2, 3)),))
    assert av1.is_subclass(av123)
    assert not av123.is_subclass(av1)
    assert av123.is_subclass(av1234)
    assert not av1234.is_subclass(av12_21)
    assert av12_21.is_subclass(av1234)
    assert av123.is_subclass(av123)
    av1324_1423_12345 = Av(
        (Perm((0, 2, 1, 3)), Perm((0, 3, 1, 2)), Perm((0, 1, 2, 3, 4, 5)))
    )
    av1324_1234 = Av((Perm((0, 2, 1, 3)), Perm((0, 1, 2, 3))))
    av1234_132 = Av((Perm((0, 1, 2, 3)), Perm((0, 2, 1))))
    assert av123.is_subclass(av1324_1423_12345)
    assert not av1324_1234.is_subclass(av1324_1423_12345)
    assert av1234_132.is_subclass(av1324_1423_12345)


def test_av_of_length():
    assert [
        sum(1 for _ in Av(Basis(Perm((0, 2, 1)))).of_length(i)) for i in range(8)
    ] == [1, 1, 2, 5, 14, 42, 132, 429]


def test_av_perm():
    p = Perm((0, 1))
    av = Av.from_iterable([p])
    for length in range(10):
        assert len(set(av.of_length(length))) == 1


def test_av_meshpatt():
    p = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp = MeshPatt(p, shading)
    av = Av.from_iterable([mp])
    enum = [1, 1, 2, 5, 15, 52, 203, 877]  # Bell numbers

    for (n, cnt) in enumerate(enum):
        inst = av.of_length(n)
        gen = list(inst)
        assert len(gen) == cnt


def test_enumeration():
    assert Av(Basis(Perm((0, 2, 1)))).enumeration(8) == [
        1,
        1,
        2,
        5,
        14,
        42,
        132,
        429,
        1430,
    ]
    assert Av(Basis(Perm((0, 1, 2)), Perm((1, 2, 0)))).enumeration(8) == [
        1,
        1,
        2,
        4,
        7,
        11,
        16,
        22,
        29,
    ]
