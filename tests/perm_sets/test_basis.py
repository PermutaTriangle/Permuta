from permuta import MeshPatt, Perm
from permuta.perm_sets.basis import Basis, MeshBasis


def test_is_mesh_basis():
    assert not MeshBasis.is_mesh_basis(())
    assert not MeshBasis.is_mesh_basis([])
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    perm_list = [p1, p2]
    assert not MeshBasis.is_mesh_basis(p1)
    assert not MeshBasis.is_mesh_basis(p2)
    assert not MeshBasis.is_mesh_basis(perm_list)
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp1 = MeshPatt(p1, shading)
    mp2 = MeshPatt(p2, shading)
    meshpatt_list = [mp1, mp2]
    mixed_patt_list = [p1, mp2]
    assert MeshBasis.is_mesh_basis(mp1)
    assert MeshBasis.is_mesh_basis(mp2)
    assert MeshBasis.is_mesh_basis(meshpatt_list)
    assert MeshBasis.is_mesh_basis(mixed_patt_list)


def test_meshbasis_of_perms():
    p1 = Perm((0, 2, 1))
    p2 = Perm((2, 0, 1))
    assert MeshBasis(p1, p2) == MeshBasis(MeshPatt(p1, []), MeshPatt(p2, []))

    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp1 = MeshPatt(p1, shading)
    mp2 = MeshPatt(p2, shading)
    assert MeshBasis(p1, p2) == MeshBasis(p1, p2, mp1, mp2)

    for elmnt in MeshBasis(p1, p2):
        assert isinstance(elmnt, MeshPatt)


def test_meshbasis():
    assert MeshBasis(*[MeshPatt(), MeshPatt(Perm((0,)), ())]) == MeshBasis(MeshPatt())
    assert MeshBasis(*[MeshPatt(), Perm()]) == MeshBasis(MeshPatt())
    assert MeshBasis(*(Perm((1, 2, 0)), MeshPatt(Perm((1, 2, 0)), []))) == MeshBasis(
        *(MeshPatt(Perm((1, 2, 0)), []),)
    )
    assert MeshBasis(
        *(
            Perm((1, 2, 0)),
            MeshPatt(Perm((0, 2, 1)), [(0, 0), (0, 1), (1, 1), (2, 3), (3, 0), (3, 3)]),
        )
    ) == MeshBasis(
        *(
            MeshPatt(Perm((0, 2, 1)), [(0, 0), (0, 1), (1, 1), (2, 3), (3, 0), (3, 3)]),
            MeshPatt(Perm((1, 2, 0)), []),
        )
    )
    assert MeshBasis(
        *(
            Perm((1, 2, 0)),
            MeshPatt(Perm((0, 2, 1)), [(0, 0), (0, 1), (1, 1), (2, 3), (3, 0), (3, 3)]),
        )
    ) != MeshBasis(
        *(MeshPatt(Perm((0, 2, 1)), [(0, 0), (0, 1), (1, 1), (2, 3), (3, 0), (3, 3)]),)
    )
    assert MeshBasis(
        *(
            MeshPatt(Perm((1, 2, 0)), [(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 1)]),
            MeshPatt(
                Perm((3, 4, 2, 0, 1)),
                [
                    (0, 0),
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (0, 4),
                    (1, 2),
                    (1, 3),
                    (1, 4),
                    (1, 5),
                    (2, 0),
                    (2, 1),
                    (2, 2),
                    (2, 3),
                    (3, 0),
                    (3, 2),
                    (3, 4),
                    (3, 5),
                    (4, 0),
                    (4, 1),
                    (4, 3),
                    (4, 4),
                    (5, 0),
                    (5, 2),
                    (5, 4),
                    (5, 5),
                ],
            ),
        )
    ) == MeshBasis(
        *(MeshPatt(Perm((1, 2, 0)), [(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 1)]),)
    )
    assert MeshBasis(
        *(Perm((2, 0, 1)), MeshPatt(Perm((2, 0, 1)), [(2, 2)]))
    ) == MeshBasis(*(Perm((2, 0, 1)),))


def test_basis():
    assert Basis(*[Perm(), Perm((0,))]) == Basis(Perm())
    assert Basis(*[Perm((0, 2, 1)), Perm((0, 3, 2, 1))]) == Basis(Perm((0, 2, 1)))
    assert Basis(Perm((2, 0, 1))) == Basis(
        *(
            Perm((4, 0, 1, 7, 2, 6, 3, 5)),
            Perm((4, 2, 3, 0, 7, 9, 6, 8, 1, 5)),
            Perm((0, 10, 3, 8, 7, 12, 2, 4, 6, 13, 5, 16, 14, 17, 1, 11, 15, 9)),
            Perm((8, 11, 7, 1, 4, 5, 10, 6, 0, 3, 2, 9)),
            Perm((2, 0, 1)),
            Perm((4, 1, 0, 5, 2, 3)),
            Perm((5, 3, 4, 1, 2, 0)),
            Perm((1, 0, 3, 6, 4, 5, 2)),
            Perm((1, 7, 10, 2, 3, 6, 0, 4, 9, 5, 8)),
            Perm((1, 2, 8, 9, 4, 6, 14, 10, 3, 12, 13, 5, 7, 11, 0)),
            Perm((10, 13, 6, 9, 8, 12, 2, 4, 11, 0, 3, 16, 14, 15, 7, 5, 1)),
        )
    )
    assert Basis(*(Perm((0, 2, 1)), Perm((0, 1, 2)))) == Basis(
        *(
            Perm((2, 3, 16, 14, 0, 6, 7, 13, 8, 11, 9, 15, 5, 1, 10, 12, 4, 17)),
            Perm(
                (4, 3, 9, 6, 1, 7, 5, 0, 12, 17, 16, 11, 18, 14, 10, 19, 13, 15, 2, 8)
            ),
            Perm((12, 5, 14, 0, 2, 8, 7, 6, 9, 13, 10, 11, 3, 4, 1)),
            Perm((0, 4, 3, 6, 2, 1, 5)),
            Perm((0, 2, 4, 3, 7, 5, 1, 6, 8)),
            Perm((0, 1, 2)),
            Perm((4, 3, 8, 9, 7, 5, 1, 6, 2, 0)),
            Perm((8, 13, 6, 4, 10, 7, 2, 12, 3, 0, 11, 1, 15, 5, 14, 16, 9)),
            Perm((2, 4, 0, 1, 6, 7, 3, 5)),
            Perm((5, 1, 4, 7, 3, 2, 0, 6, 8, 9)),
            Perm((0, 2, 1)),
            Perm((6, 0, 2, 1, 5, 3, 4)),
        )
    )
    assert Basis(*(Perm((0, 1, 2)), Perm((5, 2, 4, 3, 0, 1)))) == Basis(
        *(
            Perm(
                (16, 14, 5, 8, 19, 4, 12, 15, 9, 10, 7, 18, 0, 2, 13, 3, 6, 17, 11, 1)
            ),
            Perm((12, 16, 9, 4, 5, 0, 10, 15, 13, 1, 14, 8, 17, 11, 6, 18, 7, 2, 3)),
            Perm(
                (8, 14, 19, 0, 12, 11, 2, 4, 16, 7, 18, 13, 15, 17, 6, 5, 3, 9, 10, 1)
            ),
            Perm((5, 2, 4, 3, 0, 1)),
            Perm(
                (8, 15, 7, 4, 9, 14, 17, 3, 10, 6, 19, 18, 2, 16, 0, 1, 5, 11, 13, 12)
            ),
            Perm((3, 7, 4, 6, 1, 5, 8, 9, 0, 10, 2)),
            Perm((9, 3, 8, 6, 12, 7, 11, 5, 10, 4, 13, 0, 1, 2)),
            Perm((0, 1, 2)),
            Perm((8, 11, 12, 15, 5, 9, 16, 13, 0, 4, 10, 6, 17, 7, 14, 1, 2, 3)),
            Perm((16, 11, 4, 5, 2, 10, 0, 12, 15, 14, 8, 6, 17, 9, 13, 3, 1, 7)),
            Perm((2, 1, 17, 16, 13, 9, 3, 15, 18, 10, 8, 6, 12, 14, 4, 0, 7, 11, 5)),
            Perm((14, 8, 2, 11, 10, 13, 7, 16, 0, 15, 3, 1, 12, 9, 6, 4, 5)),
        )
    )
    assert Basis(
        *(
            Perm((2, 0, 1)),
            Perm((1, 2, 3, 5, 4, 0)),
            Perm((2, 0, 1, 3)),
            Perm((1, 2, 3, 5, 4, 0, 6)),
        )
    ) == Basis(
        *(
            Perm(
                (7, 10, 18, 12, 13, 15, 11, 4, 17, 2, 9, 3, 1, 14, 8, 0, 5, 6, 16, 19)
            ),
            Perm((1, 2, 3, 5, 4, 0)),
            Perm((0, 14, 6, 13, 12, 2, 5, 3, 11, 16, 17, 4, 15, 8, 1, 10, 9, 7)),
            Perm((10, 3, 14, 18, 12, 8, 13, 6, 9, 16, 2, 17, 1, 7, 15, 11, 4, 5, 0)),
            Perm((2, 0, 1)),
            Perm((12, 14, 2, 18, 1, 11, 13, 17, 10, 7, 15, 4, 9, 8, 16, 5, 6, 0, 3)),
            Perm((5, 3, 7, 9, 10, 1, 4, 0, 2, 12, 11, 8, 6)),
            Perm(
                (17, 10, 8, 11, 6, 2, 12, 4, 1, 16, 0, 5, 3, 18, 14, 13, 15, 9, 7, 19)
            ),
            Perm((7, 11, 12, 5, 3, 14, 0, 6, 8, 4, 15, 1, 2, 9, 17, 16, 13, 10)),
            Perm((8, 1, 12, 14, 17, 2, 13, 10, 11, 5, 7, 15, 9, 0, 3, 6, 4, 16, 18)),
            Perm((7, 3, 1, 17, 0, 4, 18, 5, 16, 10, 15, 13, 11, 9, 12, 2, 14, 6, 8)),
            Perm(
                (3, 8, 19, 17, 18, 15, 7, 0, 6, 4, 1, 16, 13, 5, 14, 9, 2, 10, 11, 12)
            ),
        )
    )


def test_alternative_construction_methods():
    assert (
        Basis.from_string("123_321")
        == Basis.from_iterable([Perm((0, 1, 2)), Perm((2, 1, 0))])
        == Basis(Perm((0, 1, 2)), Perm((2, 1, 0)))
        == Basis.from_string("012:210")
    )
    assert MeshBasis.from_iterable(
        [MeshPatt(Perm((1, 2, 0)), [(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 1)])]
    ) == MeshBasis(
        MeshPatt(Perm((1, 2, 0)), [(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 1)])
    )
