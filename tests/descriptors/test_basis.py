import pytest

from permuta import MeshPatt
from permuta import Perm
from permuta.descriptors.basis import Basis, MeshBasis, detectBasisCls


def test_detect_empty_basis_cls():
    assert detectBasisCls(()) == Basis
    assert detectBasisCls([]) == Basis


def test_detect_basis_cls_with_None_elmnt():
    # TypeError: 'NoneType' object is not iterable
    with pytest.raises(TypeError):
        detectBasisCls(None)

    # ValueError: A basis can only contain Perms and MeshPatts.
    with pytest.raises(ValueError):
        detectBasisCls([None])


def test_detect_basis_cls():
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    perm_list = [p1, p2]
    basis_cls = detectBasisCls(perm_list)
    assert basis_cls == Basis
    assert detectBasisCls(basis_cls) == Basis


def test_detect_mesh_basis_cls():
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp1 = MeshPatt(p1, shading)
    mp2 = MeshPatt(p2, shading)
    meshpatt_list = [mp1, mp2]
    meshbasis_cls = detectBasisCls(meshpatt_list)
    assert meshbasis_cls == MeshBasis
    assert detectBasisCls(meshbasis_cls) == MeshBasis
