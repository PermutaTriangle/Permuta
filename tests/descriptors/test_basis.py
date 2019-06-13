from permuta import Perm
from permuta import MeshPatt
from permuta.descriptors.basis import Basis, MeshBasis, returnBasis


def test_correct_basis():
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    perm_list = [p1, p2]
    perm_basis = returnBasis(perm_list)
    assert isinstance(perm_basis, Basis)
    assert isinstance(returnBasis(perm_basis), Basis)

    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp1 = MeshPatt(p1, shading)
    mp2 = MeshPatt(p2, shading)
    meshpatt_list = [mp1, mp2]
    meshpatt_basis = returnBasis(meshpatt_list)
    assert isinstance(meshpatt_basis, MeshBasis)
    assert isinstance(returnBasis(meshpatt_basis), MeshBasis)
