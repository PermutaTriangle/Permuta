import pytest

from permuta import MeshPatt
from permuta import Perm
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


def test_detect_mesh_basis_cls():
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp1 = MeshPatt(p1, shading)
    mp2 = MeshPatt(p2, shading)
    meshpatt_list = [mp1, mp2]

    assert detect_basis_cls(mp1) == MeshBasis
    assert detect_basis_cls(mp2) == MeshBasis
    assert detect_basis_cls(meshpatt_list) == MeshBasis
    assert detect_basis_cls(MeshBasis) == MeshBasis
    assert detect_basis_cls(MeshBasis(meshpatt_list)) == MeshBasis
