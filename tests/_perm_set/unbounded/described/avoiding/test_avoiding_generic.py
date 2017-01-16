from permuta import Perm
from permuta import PermSet
from permuta.descriptors import Basis


def test_iter_getitem_same():
    basis = Basis(Perm((3, 0, 1, 2)))
    avoiders = PermSet(basis)
    maximum = 1000
    for index, perm in enumerate(avoiders):
        assert perm == avoiders[index]
        if index > maximum:
            break
