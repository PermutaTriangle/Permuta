from permuta import Perm
from permuta import PermSet
from permuta.descriptors import Basis
from permuta.misc import catalan
from permuta._perm_set.unbounded.described.avoiding import AvoidingGeneric


def test_iter_getitem_same_principal_classes():
    maximum = 300
    for length in range(3, 6):
        for patt in PermSet(length):
            basis = Basis(patt)
            avoiders = AvoidingGeneric(basis)
            for index, perm in enumerate(avoiders):
                assert perm == avoiders[index]
                if index > maximum:
                    break


def test_avoiding_generic_principal_classes():
    ts = [
        ([[0, 1]], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        ([[1, 0]], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        ([[0, 1, 2]], [catalan(i) for i in range(8)]),
        ([[0, 2, 1]], [catalan(i) for i in range(8)]),
        ([[1, 0, 2]], [catalan(i) for i in range(8)]),
        ([[1, 2, 0]], [catalan(i) for i in range(8)]),
        ([[2, 0, 1]], [catalan(i) for i in range(8)]),
        ([[2, 1, 0]], [catalan(i) for i in range(8)]),
    ]

    for (patts, enum) in ts:
        patts = [Perm(patt) for patt in patts]
        basis = Basis(patts)
        for (n,cnt) in enumerate(enum):
            inst = AvoidingGeneric(basis).of_length(n)
            gen = list(inst)
            assert len(gen) == cnt
            assert len(gen) == len(set(gen))
            for perm in gen:
                assert perm.avoids(*patts)

        mx = len(enum)-1
        cnt = [0 for _ in range(mx+1)]
        for perm in AvoidingGeneric(basis):
            if len(perm) > mx:
                break
            assert perm.avoids(*patts)
            cnt[len(perm)] += 1

        assert enum == cnt


def test_avoiding_generic_principal_classes():
    ts = [
        ([[0, 1, 2], [0, 3, 2, 1]], [1, 1, 2, 5, 13, 34, 89, 233, 610]),
    ]

    for (patts, enum) in ts:
        patts = [Perm(patt) for patt in patts]
        basis = Basis(patts)
        for (n,cnt) in enumerate(enum):
            inst = AvoidingGeneric(basis).of_length(n)
            gen = list(inst)
            assert len(gen) == cnt
            assert len(gen) == len(set(gen))
            for perm in gen:
                assert perm.avoids(*patts)

        mx = len(enum)-1
        cnt = [0 for _ in range(mx+1)]
        for perm in AvoidingGeneric(basis):
            if len(perm) > mx:
                break
            assert perm.avoids(*patts)
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
        for (n,cnt) in enumerate(enum):
            inst = AvoidingGeneric(basis).of_length(n)
            gen = list(inst)
            assert len(gen) == cnt
            assert len(gen) == len(set(gen))
            for perm in gen:
                assert perm.avoids(*patts)

        mx = len(enum)-1
        cnt = [0 for _ in range(mx+1)]
        for perm in AvoidingGeneric(basis):
            if len(perm) > mx:
                break
            assert perm.avoids(*patts)
            cnt[len(perm)] += 1

        assert enum == cnt
