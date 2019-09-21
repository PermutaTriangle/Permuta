import pytest

from permuta import MeshPatt, Perm
from permuta.descriptors.basis import Basis, MeshBasis, detect_basis_cls


def test_detect_empty_basis_cls():
    assert detect_basis_cls(()) == Basis
    assert detect_basis_cls([]) == Basis


def test_detect_basis_cls_with_None_elmnt():
    # TypeError: 'NoneType' object is not iterable
    with pytest.raises(TypeError):
        detect_basis_cls(None)

    # ValueError: A basis can only contain Perms and MeshPatts.
    with pytest.raises(ValueError):
        detect_basis_cls([None])


def test_detect_basis_cls():
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    perm_list = [p1, p2]

    assert detect_basis_cls(p1) == Basis
    assert detect_basis_cls(p2) == Basis
    assert detect_basis_cls(perm_list) == Basis
    assert detect_basis_cls(Basis) == Basis
    assert detect_basis_cls(Basis(perm_list)) == Basis


def test_detect_meshbasis_cls():
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp1 = MeshPatt(p1, shading)
    mp2 = MeshPatt(p2, shading)
    meshpatt_list = [mp1, mp2]
    mixed_patt_list = [p1, mp2]

    assert detect_basis_cls(mp1) == MeshBasis
    assert detect_basis_cls(mp2) == MeshBasis
    assert detect_basis_cls(meshpatt_list) == MeshBasis
    assert detect_basis_cls(mixed_patt_list) == MeshBasis
    assert detect_basis_cls(MeshBasis) == MeshBasis
    assert detect_basis_cls(MeshBasis(meshpatt_list)) == MeshBasis


def test_meshbasis_of_perms():
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    assert MeshBasis([p1, p2]) == MeshBasis([MeshPatt(p1, []), MeshPatt(p2, [])])

    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp1 = MeshPatt(p1, shading)
    mp2 = MeshPatt(p2, shading)
    assert MeshBasis([p1, p2]) == MeshBasis([p1, p2, mp1, mp2])

    # TypeError: Elements of a basis should all be of type(s) Perm
    with pytest.raises(TypeError):
        Basis([mp1, mp2])

    for elmnt in MeshBasis([p1, p2]):
        assert isinstance(elmnt, MeshPatt)


def test_basis_with_empty_perm():
    basis = Basis([Perm(), Perm((0,))])
    assert basis == Basis(Perm())


def test_meshbasis_with_empty_meshpatt():
    meshbasis = MeshBasis([MeshPatt(), MeshPatt(Perm((0,)), ())])
    assert meshbasis == MeshBasis(MeshPatt())


def test_meshbasis_with_empty_perm():
    meshbasis = MeshBasis([MeshPatt(), Perm()])
    assert meshbasis == MeshBasis(MeshPatt())
