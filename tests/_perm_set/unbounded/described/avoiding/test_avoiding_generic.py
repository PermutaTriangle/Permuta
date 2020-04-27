import pytest
from permuta import MeshPatt, Perm, PermSet
from permuta._perm_set.unbounded.described.avoiding import AvoidingGeneric
from permuta.descriptors import Basis, MeshBasis
from permuta.misc import catalan


def test_iter_getitem_same_principal_classes():
    maximum = 100
    for length in range(3, 5):
        for patt in PermSet(length):
            basis = Basis(patt)
            avoiders = AvoidingGeneric(basis)
            for index, perm in enumerate(avoiders):
                assert perm == avoiders[index]
                if index > maximum:
                    break


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
    basis = Basis(patts)
    for (n, cnt) in enumerate(enum):
        print(n, cnt)
        inst = AvoidingGeneric(basis).of_length(n)
        gen = list(inst)
        assert len(gen) == cnt
        assert len(gen) == len(set(gen))
        for perm in gen:
            assert perm.avoids(*patts)

    mx = len(enum) - 1
    cnt = [0 for _ in range(mx + 1)]
    for perm in AvoidingGeneric(basis):
        if len(perm) > mx:
            break
        assert perm.avoids(*patts)
        cnt[len(perm)] += 1

    assert enum == cnt


def test_avoiding_generic_mesh_patterns():
    p = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mps = [MeshPatt(p, shading)]
    meshbasis = MeshBasis(mps)
    avoiding_generic_basis = AvoidingGeneric(meshbasis)
    enum = [1, 1, 2, 5, 15, 52, 203, 877]  # Bell numbers

    for (n, cnt) in enumerate(enum):
        inst = avoiding_generic_basis.of_length(n)
        gen = list(inst)
        assert len(gen) == cnt
        assert len(gen) == len(set(gen))
        for perm in gen:
            assert perm.avoids(*mps)
            assert perm in avoiding_generic_basis

    for mp in mps:
        with pytest.raises(TypeError):
            mp in avoiding_generic_basis

    mx = len(enum) - 1
    cnt = [0 for _ in range(mx + 1)]
    for perm in AvoidingGeneric(meshbasis):
        if len(perm) > mx:
            break
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
        basis = Basis(patts)
        for (n, cnt) in enumerate(enum):
            inst = AvoidingGeneric(basis).of_length(n)
            gen = list(inst)
            assert len(gen) == cnt
            assert len(gen) == len(set(gen))
            for perm in gen:
                assert perm.avoids(*patts)

        mx = len(enum) - 1
        cnt = [0 for _ in range(mx + 1)]
        for perm in AvoidingGeneric(basis):
            if len(perm) > mx:
                break
            assert perm.avoids(*patts)
            cnt[len(perm)] += 1

        assert enum == cnt


def test_is_subclass():
    av1 = AvoidingGeneric((Perm((0,)),))
    av12_21 = AvoidingGeneric((Perm((0, 1)), Perm((1, 0))))
    av123 = AvoidingGeneric((Perm((0, 1, 2)),))
    av1234 = AvoidingGeneric((Perm((0, 1, 2, 3)),))
    assert av1.is_subclass(av123)
    assert not av123.is_subclass(av1)
    assert av123.is_subclass(av1234)
    assert not av1234.is_subclass(av12_21)
    assert av12_21.is_subclass(av1234)
    assert av123.is_subclass(av123)
    av1324_1423_12345 = AvoidingGeneric(
        (Perm((0, 2, 1, 3)), Perm((0, 3, 1, 2)), Perm((0, 1, 2, 3, 4, 5)))
    )
    av1324_1234 = AvoidingGeneric((Perm((0, 2, 1, 3)), Perm((0, 1, 2, 3))))
    av1234_132 = AvoidingGeneric((Perm((0, 1, 2, 3)), Perm((0, 2, 1))))
    assert av123.is_subclass(av1324_1423_12345)
    assert not av1324_1234.is_subclass(av1324_1423_12345)
    assert av1234_132.is_subclass(av1324_1423_12345)
