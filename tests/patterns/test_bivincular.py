from permuta import BivincularPatt, CovincularPatt, MeshPatt, Perm, VincularPatt


def test_init_bivpatt():
    p = BivincularPatt(Perm((0, 1, 2)), (1, 2), (0, 1))
    assert p.shading == {
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (0, 0),
        (3, 0),
        (0, 1),
        (3, 1),
    }


def test_init_covpatt():
    p = CovincularPatt(Perm((0, 1, 2)), (0, 1))
    assert p.shading == {
        (1, 0),
        (1, 1),
        (2, 0),
        (2, 1),
        (0, 0),
        (3, 0),
        (0, 1),
        (3, 1),
    }


def test_init_vinpatt():
    p = VincularPatt(Perm((0, 1, 2)), (1, 2))
    assert p.shading == {
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
    }


def test_perm_avoids_bv1():
    bp1 = BivincularPatt(Perm((0, 1, 2)), (2,), ())
    vp = VincularPatt(Perm((0, 1, 2)), (2,))
    bp2 = BivincularPatt(Perm((2, 0, 1)), (), (2,))
    cp = CovincularPatt(Perm((2, 0, 1)), (2,))

    assert Perm().avoids(bp1, bp2)
    assert Perm().avoids(vp, cp)
    for i in range(1, 7):
        assert 2 ** (i - 1) == sum(1 for p in Perm.of_length(i) if p.avoids(bp1, bp2))
        assert 2 ** (i - 1) == sum(1 for p in Perm.of_length(i) if p.avoids(vp, cp))


def test_perm_avoids_bv2():
    class_pat = Perm.identity(3)
    bp = BivincularPatt(Perm((2, 0, 1)), (), (1,))
    cp = CovincularPatt(Perm((2, 0, 1)), (1,))
    assert Perm().avoids(class_pat, bp)
    assert Perm().avoids(class_pat, cp)
    for i in range(1, 7):
        assert 2 ** (i - 1) == sum(
            1 for p in Perm.of_length(i) if p.avoids(class_pat, bp)
        )
        assert 2 ** (i - 1) == sum(
            1 for p in Perm.of_length(i) if p.avoids(class_pat, cp)
        )


def test_perm_avoids_bv3():
    motzkin = [1, 1, 2, 4, 9, 21, 51, 127, 323, 835, 2188, 5798, 15511, 41835]
    class_pat = Perm((0, 2, 1))
    bp = BivincularPatt(Perm.identity(3), (), (2,))
    cp = CovincularPatt(Perm.identity(3), (2,))
    for plen in range(8):
        assert (
            sum(1 for perm in Perm.of_length(plen) if perm.avoids(class_pat, bp))
            == motzkin[plen]
        )
        assert (
            sum(1 for perm in Perm.of_length(plen) if perm.avoids(class_pat, cp))
            == motzkin[plen]
        )


def test_avoids_bv():
    assert BivincularPatt(
        Perm((0, 1, 12, 14, 9, 10, 13, 5, 2, 7, 8, 4, 3, 6, 11)),
        [9, 13, 14],
        [1, 2, 3, 5, 7, 9, 14, 15],
    ).avoids(BivincularPatt(Perm((8, 9, 1, 3, 7, 6, 0, 2, 5, 4)), [4, 8], [9]))
    assert BivincularPatt(
        Perm((0, 1, 12, 14, 9, 10, 13, 5, 2, 7, 8, 4, 3, 6, 11)),
        [9, 13, 14],
        [1, 2, 3, 5, 7, 9, 14, 15],
    ).avoids(
        CovincularPatt(
            Perm((6, 10, 14, 0, 11, 7, 1, 4, 2, 3, 13, 8, 12, 5, 9)),
            [0, 1, 3, 6, 8, 9, 11, 12, 14, 15],
        )
    )
    assert BivincularPatt(
        Perm((0, 1, 12, 14, 9, 10, 13, 5, 2, 7, 8, 4, 3, 6, 11)),
        [9, 13, 14],
        [1, 2, 3, 5, 7, 9, 14, 15],
    ).avoids(VincularPatt(Perm((4, 1, 3, 2, 0, 6, 5, 7)), [0, 3, 6]))
    assert BivincularPatt(
        Perm((0, 1, 12, 14, 9, 10, 13, 5, 2, 7, 8, 4, 3, 6, 11)),
        [9, 13, 14],
        [1, 2, 3, 5, 7, 9, 14, 15],
    ).avoids(CovincularPatt(Perm((2, 3, 5, 9, 8, 7, 1, 6, 4, 0)), [2, 5, 7, 8]))
    assert BivincularPatt(
        Perm((0, 1, 12, 14, 9, 10, 13, 5, 2, 7, 8, 4, 3, 6, 11)),
        [9, 13, 14],
        [1, 2, 3, 5, 7, 9, 14, 15],
    ).avoids(
        VincularPatt(
            Perm((13, 0, 10, 2, 11, 7, 14, 3, 1, 6, 8, 12, 4, 5, 9)),
            [0, 5, 6, 8, 9, 10, 12, 15],
        )
    )
    assert CovincularPatt(
        Perm((6, 10, 14, 0, 11, 7, 1, 4, 2, 3, 13, 8, 12, 5, 9)),
        [0, 1, 3, 6, 8, 9, 11, 12, 14, 15],
    ).avoids(
        BivincularPatt(
            Perm((0, 1, 12, 14, 9, 10, 13, 5, 2, 7, 8, 4, 3, 6, 11)),
            [9, 13, 14],
            [1, 2, 3, 5, 7, 9, 14, 15],
        )
    )
    assert CovincularPatt(
        Perm((6, 2, 10, 1, 4, 7, 11, 9, 5, 8, 3, 0)), [0, 1, 3, 5, 6, 8, 10, 11, 12]
    ).avoids(
        BivincularPatt(
            Perm((9, 1, 0, 12, 4, 8, 2, 6, 11, 7, 5, 3, 10)),
            [0, 2, 6, 7, 8, 11, 13],
            [0, 2, 3, 4, 5, 6, 7, 9, 10, 13],
        )
    )


def test_get_perm():
    p = Perm((1, 0))
    assert BivincularPatt(p, (), ()).get_perm() == p


def test_complement():
    assert BivincularPatt(
        Perm((1, 2, 0, 3)), [0, 1, 3, 4], [4]
    ).complement() == MeshPatt(
        Perm((2, 1, 3, 0)),
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 0),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        ],
    )
    assert CovincularPatt(Perm((0, 1, 2)), [1, 2]).complement() == MeshPatt(
        Perm((2, 1, 0)),
        [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)],
    )
    assert VincularPatt(Perm((0, 2, 1)), [0]).complement() == MeshPatt(
        Perm((2, 0, 1)), [(0, 0), (0, 1), (0, 2), (0, 3)]
    )


def test_reverse():
    assert BivincularPatt(Perm((0, 1, 2)), [2], []).reverse() == MeshPatt(
        Perm((2, 1, 0)), [(1, 0), (1, 1), (1, 2), (1, 3)]
    )
    assert CovincularPatt(Perm((4, 2, 0, 1, 3)), [0, 1, 2, 4, 5]).reverse() == MeshPatt(
        Perm((3, 1, 0, 2, 4)),
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 4),
            (0, 5),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 4),
            (1, 5),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 4),
            (2, 5),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 4),
            (3, 5),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 4),
            (4, 5),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 4),
            (5, 5),
        ],
    )
    assert VincularPatt(Perm((0, 3, 4, 1, 2)), [0, 1]).reverse() == MeshPatt(
        Perm((2, 1, 4, 3, 0)),
        [
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
            (4, 5),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
        ],
    )


def test_inverse():
    assert BivincularPatt(Perm((1, 0, 2)), [3], [1, 3]).inverse() == MeshPatt(
        Perm((1, 0, 2)),
        [
            (0, 3),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
        ],
    )
    assert CovincularPatt(Perm((3, 1, 0, 2)), [1, 2, 3]).inverse() == MeshPatt(
        Perm((2, 1, 3, 0)),
        [
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
        ],
    )
    assert VincularPatt(Perm((0, 4, 3, 2, 1)), [0, 1, 4, 5]).inverse() == MeshPatt(
        Perm((0, 4, 3, 2, 1)),
        [
            (0, 0),
            (0, 1),
            (0, 4),
            (0, 5),
            (1, 0),
            (1, 1),
            (1, 4),
            (1, 5),
            (2, 0),
            (2, 1),
            (2, 4),
            (2, 5),
            (3, 0),
            (3, 1),
            (3, 4),
            (3, 5),
            (4, 0),
            (4, 1),
            (4, 4),
            (4, 5),
            (5, 0),
            (5, 1),
            (5, 4),
            (5, 5),
        ],
    )


def test_rotate():
    assert VincularPatt(Perm((0, 1, 2)), (0,)).rotate(2) == VincularPatt(
        Perm((0, 1, 2)).rotate(2), (3,)
    )
    assert VincularPatt(Perm((0, 1, 2)), (0,)).rotate(1) == CovincularPatt(
        Perm((0, 1, 2)).rotate(1), (3,)
    )
    assert VincularPatt(Perm((0, 1, 2)), (0,)).rotate(-1) == CovincularPatt(
        Perm((0, 1, 2)).rotate(1), (0,)
    )
    assert BivincularPatt(Perm((3, 2, 1, 0)), [0, 1, 3, 4], [0, 2, 3, 4]).rotate(
        0
    ) == BivincularPatt(Perm((3, 2, 1, 0)), [0, 1, 3, 4], [0, 2, 3, 4])
    assert BivincularPatt(Perm((3, 2, 1, 0)), [0, 1, 3, 4], [0, 2, 3, 4]).rotate(
        1
    ) == MeshPatt(
        Perm((0, 1, 2, 3)),
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        ],
    )
    assert BivincularPatt(Perm((3, 2, 1, 0)), [0, 1, 3, 4], [0, 2, 3, 4]).rotate(
        2
    ) == MeshPatt(
        Perm((3, 2, 1, 0)),
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 4),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        ],
    )
    assert BivincularPatt(Perm((3, 2, 1, 0)), [0, 1, 3, 4], [0, 2, 3, 4]).rotate(
        3
    ) == MeshPatt(
        Perm((0, 1, 2, 3)),
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 0),
            (3, 1),
            (3, 3),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        ],
    )
    assert CovincularPatt(Perm((2, 1, 3, 0)), [0, 1]).rotate(0) == CovincularPatt(
        Perm((2, 1, 3, 0)), [0, 1]
    )
    assert CovincularPatt(Perm((2, 1, 3, 0)), [0, 1]).rotate(1) == MeshPatt(
        Perm((0, 2, 3, 1)),
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
        ],
    )
    assert CovincularPatt(Perm((2, 1, 3, 0)), [0, 1]).rotate(2) == MeshPatt(
        Perm((3, 0, 2, 1)),
        [
            (0, 3),
            (0, 4),
            (1, 3),
            (1, 4),
            (2, 3),
            (2, 4),
            (3, 3),
            (3, 4),
            (4, 3),
            (4, 4),
        ],
    )
    assert CovincularPatt(Perm((2, 1, 3, 0)), [0, 1]).rotate(3) == MeshPatt(
        Perm((2, 0, 1, 3)),
        [
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        ],
    )
    assert VincularPatt(Perm((0, 1, 2)), [0, 1, 3]).rotate(0) == VincularPatt(
        Perm((0, 1, 2)), [0, 1, 3]
    )
    assert VincularPatt(Perm((0, 1, 2)), [0, 1, 3]).rotate(1) == MeshPatt(
        Perm((2, 1, 0)),
        [
            (0, 0),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 2),
            (1, 3),
            (2, 0),
            (2, 2),
            (2, 3),
            (3, 0),
            (3, 2),
            (3, 3),
        ],
    )
    assert VincularPatt(Perm((0, 1, 2)), [0, 1, 3]).rotate(2) == MeshPatt(
        Perm((0, 1, 2)),
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
        ],
    )
    assert VincularPatt(Perm((0, 1, 2)), [0, 1, 3]).rotate(3) == MeshPatt(
        Perm((2, 1, 0)),
        [
            (0, 0),
            (0, 1),
            (0, 3),
            (1, 0),
            (1, 1),
            (1, 3),
            (2, 0),
            (2, 1),
            (2, 3),
            (3, 0),
            (3, 1),
            (3, 3),
        ],
    )


def test_contains():
    assert VincularPatt(Perm((5, 2, 0, 6, 1, 3, 4)), [1, 3, 4, 5, 7]).contains(
        CovincularPatt(Perm((4, 0, 1, 2, 3)), []),
        VincularPatt(Perm((5, 2, 0, 6, 1, 3, 4)), [1, 3, 4, 5, 7]),
        VincularPatt(Perm((2, 1, 0, 3)), []),
    )
    assert BivincularPatt(
        Perm((4, 5, 1, 3, 2, 0)), [0, 2, 4, 5], [0, 1, 2, 4, 5, 6]
    ).contains(
        CovincularPatt(Perm((2, 1, 0)), [2]),
        VincularPatt(Perm((2, 3, 0, 1)), []),
        BivincularPatt(Perm((4, 5, 1, 3, 2, 0)), [0, 2, 4, 5], [0, 1, 2, 4, 5, 6]),
    )
    assert BivincularPatt(Perm((1, 3, 0, 4, 5, 6, 2)), [3, 4, 6], [1, 4, 5]).contains(
        BivincularPatt(Perm((0, 2, 1)), [2], []),
        BivincularPatt(Perm((1, 3, 0, 4, 5, 6, 2)), [3, 4, 6], [1, 4, 5]),
        CovincularPatt(Perm((1, 2, 0, 3)), [1]),
    )
    assert VincularPatt(Perm((3, 5, 1, 6, 2, 4, 0)), [0, 1, 2, 4, 5, 7]).contains(
        BivincularPatt(Perm((0, 2, 1)), [2], []),
        VincularPatt(Perm((3, 5, 1, 6, 2, 4, 0)), [0, 1, 2, 4, 5, 7]),
        VincularPatt(Perm((3, 1, 2, 0)), []),
    )
    assert BivincularPatt(Perm((3, 2, 0, 1)), [0], []).contains(
        BivincularPatt(Perm((3, 2, 0, 1)), [0], []),
        VincularPatt(Perm((3, 2, 0, 1)), []),
        VincularPatt(Perm((2, 1, 0)), []),
    )
    assert VincularPatt(Perm((4, 0, 2, 6, 3, 1, 5)), [0, 1, 2, 3, 5, 6, 7]).contains(
        BivincularPatt(Perm((1, 0, 2)), [0, 1, 3], []),
        VincularPatt(Perm((4, 0, 2, 6, 3, 1, 5)), [0, 1, 2, 3, 5, 6, 7]),
        VincularPatt(Perm((1, 0, 2)), [3]),
    )
    assert CovincularPatt(Perm((0,)), []).contains(
        BivincularPatt(Perm(()), [], []),
        VincularPatt(Perm(()), []),
        CovincularPatt(Perm((0,)), []),
    )
    assert BivincularPatt(
        Perm((6, 8, 1, 4, 2, 0, 5, 7, 3)),
        [2, 3, 4, 6, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    ).contains(
        BivincularPatt(Perm(()), [], []),
        BivincularPatt(
            Perm((6, 8, 1, 4, 2, 0, 5, 7, 3)),
            [2, 3, 4, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        CovincularPatt(Perm((0,)), []),
    )
    assert BivincularPatt(
        Perm((6, 8, 1, 4, 2, 0, 5, 7, 3)),
        [2, 3, 4, 6, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    ).contains(
        BivincularPatt(Perm(()), [], []),
        BivincularPatt(
            Perm((6, 8, 1, 4, 2, 0, 5, 7, 3)),
            [2, 3, 4, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        VincularPatt(Perm(()), []),
    )
    assert BivincularPatt(
        Perm((6, 8, 1, 4, 2, 0, 5, 7, 3)),
        [2, 3, 4, 6, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    ).contains(
        BivincularPatt(Perm(()), [], []),
        VincularPatt(Perm(()), []),
        CovincularPatt(Perm((0,)), []),
    )
    assert BivincularPatt(
        Perm((6, 8, 1, 4, 2, 0, 5, 7, 3)),
        [2, 3, 4, 6, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    ).contains(
        CovincularPatt(Perm((0,)), []),
        BivincularPatt(
            Perm((6, 8, 1, 4, 2, 0, 5, 7, 3)),
            [2, 3, 4, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        VincularPatt(Perm(()), []),
    )
    assert VincularPatt(
        Perm((9, 0, 2, 14, 5, 4, 10, 12, 3, 13, 8, 11, 7, 1, 6)),
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15],
    ).contains(VincularPatt(Perm((3, 0, 7, 4, 5, 6, 1, 2)), [8]))


def test_occuerrences_in_mesh():
    assert list(
        BivincularPatt(Perm((0, 1, 2)), (2,), ()).occurrences_in(Perm((0, 4, 3, 1, 2)))
    ) == [(0, 3, 4)]
    assert list(
        VincularPatt(Perm((0, 1, 2)), (2,)).occurrences_in(Perm((0, 4, 3, 1, 2)))
    ) == [(0, 3, 4)]
    assert list(
        BivincularPatt(Perm((2, 0, 1)), (), (2,)).occurrences_in(Perm((1, 2, 4, 0, 3)))
    ) == [(2, 3, 4)]
    assert list(
        CovincularPatt(Perm((2, 0, 1)), (2,)).occurrences_in(Perm((1, 2, 4, 0, 3)))
    ) == [(2, 3, 4)]
    assert (
        list(
            BivincularPatt(
                Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                [1, 7, 8, 12, 13],
                [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
            ).occurrences_in(
                BivincularPatt(
                    Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                    [0, 3, 5, 6, 7, 9, 10],
                    [2, 3, 6, 7],
                )
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                [1, 7, 8, 12, 13],
                [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
            ).occurrences_in(
                CovincularPatt(
                    Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
                )
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                [1, 7, 8, 12, 13],
                [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
            ).occurrences_in(
                VincularPatt(Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8])
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                [1, 7, 8, 12, 13],
                [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
            ).occurrences_in(
                VincularPatt(
                    Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                    [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
                )
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                [1, 7, 8, 12, 13],
                [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
            ).occurrences_in(
                CovincularPatt(
                    Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
            ).occurrences_in(
                BivincularPatt(
                    Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                    [0, 3, 5, 6, 7, 9, 10],
                    [2, 3, 6, 7],
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
            ).occurrences_in(
                CovincularPatt(
                    Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
            ).occurrences_in(
                VincularPatt(Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8])
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
            ).occurrences_in(
                BivincularPatt(
                    Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                    [1, 7, 8, 12, 13],
                    [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
            ).occurrences_in(
                CovincularPatt(
                    Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
                )
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                [0, 3, 5, 6, 7, 9, 10],
                [2, 3, 6, 7],
            ).occurrences_in(
                VincularPatt(
                    Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                    [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
                )
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                [0, 3, 5, 6, 7, 9, 10],
                [2, 3, 6, 7],
            ).occurrences_in(
                CovincularPatt(
                    Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
                )
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                [0, 3, 5, 6, 7, 9, 10],
                [2, 3, 6, 7],
            ).occurrences_in(
                VincularPatt(Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8])
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                [0, 3, 5, 6, 7, 9, 10],
                [2, 3, 6, 7],
            ).occurrences_in(
                BivincularPatt(
                    Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                    [1, 7, 8, 12, 13],
                    [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
                )
            )
        )
        == []
    )
    assert (
        list(
            BivincularPatt(
                Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                [0, 3, 5, 6, 7, 9, 10],
                [2, 3, 6, 7],
            ).occurrences_in(
                CovincularPatt(
                    Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
                )
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
            ).occurrences_in(
                VincularPatt(
                    Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                    [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
                )
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
            ).occurrences_in(
                CovincularPatt(
                    Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
                )
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
            ).occurrences_in(
                VincularPatt(Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8])
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
            ).occurrences_in(
                BivincularPatt(
                    Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                    [1, 7, 8, 12, 13],
                    [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
                )
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
            ).occurrences_in(
                BivincularPatt(
                    Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                    [0, 3, 5, 6, 7, 9, 10],
                    [2, 3, 6, 7],
                )
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
            ).occurrences_in(
                BivincularPatt(
                    Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                    [0, 3, 5, 6, 7, 9, 10],
                    [2, 3, 6, 7],
                )
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
            ).occurrences_in(
                BivincularPatt(
                    Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                    [1, 7, 8, 12, 13],
                    [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
                )
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
            ).occurrences_in(
                VincularPatt(Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8])
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
            ).occurrences_in(
                VincularPatt(
                    Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                    [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
                )
            )
        )
        == []
    )
    assert (
        list(
            CovincularPatt(
                Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
            ).occurrences_in(
                CovincularPatt(
                    Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8]
            ).occurrences_in(
                VincularPatt(
                    Perm((7, 11, 4, 2, 0, 9, 10, 3, 14, 6, 1, 5, 12, 13, 8)),
                    [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15],
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8]
            ).occurrences_in(
                CovincularPatt(
                    Perm((1, 6, 10, 3, 11, 0, 2, 7, 9, 8, 4, 5)), [7, 8, 11, 12]
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8]
            ).occurrences_in(
                CovincularPatt(
                    Perm((2, 0, 3, 5, 1, 6, 7, 8, 4)), [1, 2, 3, 4, 5, 7, 8, 9]
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8]
            ).occurrences_in(
                BivincularPatt(
                    Perm((6, 11, 5, 0, 12, 7, 2, 1, 4, 3, 9, 8, 10)),
                    [1, 7, 8, 12, 13],
                    [1, 3, 4, 5, 6, 7, 8, 11, 12, 13],
                )
            )
        )
        == []
    )
    assert (
        list(
            VincularPatt(
                Perm((8, 4, 2, 5, 0, 6, 3, 9, 1, 7)), [1, 2, 3, 8]
            ).occurrences_in(
                BivincularPatt(
                    Perm((1, 3, 7, 6, 5, 0, 8, 2, 4, 9)),
                    [0, 3, 5, 6, 7, 9, 10],
                    [2, 3, 6, 7],
                )
            )
        )
        == []
    )
    assert sorted(
        VincularPatt(Perm((1, 7, 0, 2, 4, 5, 3, 6)), [2, 8]).occurrences_in(
            BivincularPatt(
                Perm((10, 3, 0, 2, 14, 13, 1, 4, 12, 11, 7, 8, 6, 5, 9)),
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15],
                [4, 5, 6, 11],
            )
        )
    ) == [
        (1, 5, 6, 7, 10, 11, 12, 14),
        (1, 5, 6, 7, 10, 11, 13, 14),
        (3, 5, 6, 7, 10, 11, 12, 14),
        (3, 5, 6, 7, 10, 11, 13, 14),
    ]
    assert sorted(
        BivincularPatt(Perm((2, 4, 5, 7, 3, 6, 1, 0)), [5], [0]).occurrences_in(
            BivincularPatt(Perm((2, 4, 5, 7, 3, 6, 1, 0)), [5], [0])
        )
    ) == [(0, 1, 2, 3, 4, 5, 6, 7)]
    assert sorted(
        CovincularPatt(Perm((1, 3, 2, 6, 0, 4, 5, 7)), [3]).occurrences_in(
            CovincularPatt(
                Perm((1, 4, 3, 9, 0, 6, 2, 5, 8, 10, 7)), [0, 1, 2, 4, 6, 7, 8, 10, 11]
            )
        )
    ) == [(0, 1, 2, 3, 4, 5, 8, 9), (0, 1, 2, 3, 4, 7, 8, 9)]
    assert (
        sorted(
            CovincularPatt(Perm((1, 2, 3, 0, 6, 5, 4, 7)), []).occurrences_in(
                BivincularPatt(
                    Perm((2, 10, 8, 3, 12, 5, 1, 13, 9, 7, 0, 6, 4, 11)),
                    [0, 9, 12],
                    [2, 3, 9, 11, 12, 13],
                )
            )
        )
        == [(0, 3, 5, 6, 8, 9, 11, 13)]
    )
    assert sorted(
        VincularPatt(Perm((7, 1, 5, 2, 0, 4, 6, 3)), []).occurrences_in(
            CovincularPatt(
                Perm((13, 12, 5, 1, 8, 4, 2, 9, 6, 0, 7, 10, 3, 14, 11)), [6, 10]
            )
        )
    ) == [(0, 3, 4, 6, 9, 10, 11, 12), (1, 3, 4, 6, 9, 10, 11, 12)]
    assert (
        sorted(
            MeshPatt(
                Perm((2, 3, 0, 1, 4)),
                [
                    (0, 3),
                    (0, 4),
                    (0, 5),
                    (1, 4),
                    (3, 2),
                    (3, 4),
                    (3, 5),
                    (4, 0),
                    (4, 1),
                    (4, 2),
                    (4, 3),
                    (4, 5),
                    (5, 1),
                    (5, 2),
                    (5, 3),
                    (5, 4),
                ],
            ).occurrences_in(
                VincularPatt(
                    Perm((2, 7, 0, 6, 4, 3, 5, 1, 8)), [0, 1, 3, 4, 5, 6, 7, 8, 9]
                )
            )
        )
        == [(0, 1, 2, 7, 8)]
    )
    assert (
        sorted(
            BivincularPatt(Perm((0, 1)), [2], [1]).occurrences_in(
                MeshPatt(
                    Perm((2, 3, 4, 0, 1)),
                    [
                        (0, 0),
                        (0, 1),
                        (0, 2),
                        (0, 5),
                        (1, 0),
                        (1, 1),
                        (1, 2),
                        (1, 3),
                        (1, 5),
                        (2, 0),
                        (2, 1),
                        (3, 0),
                        (3, 1),
                        (3, 3),
                        (3, 5),
                        (4, 1),
                        (4, 2),
                        (4, 3),
                        (5, 0),
                        (5, 1),
                        (5, 2),
                        (5, 3),
                        (5, 4),
                        (5, 5),
                    ],
                )
            )
        )
        == [(3, 4)]
    )


def test_occuerrences_in_perm():
    assert (
        sorted(
            CovincularPatt(Perm((2, 0, 1)), [0, 1, 2]).occurrences_in(
                Perm((0, 2, 1, 3))
            )
        )
        == []
    )
    assert (
        sorted(
            CovincularPatt(Perm((2, 0, 1)), [0, 1, 2]).occurrences_in(Perm((1, 0, 2)))
        )
        == []
    )
    assert (
        sorted(
            BivincularPatt(Perm((2, 4, 3, 1, 0)), [0, 1], [3, 4]).occurrences_in(
                Perm((6, 2, 5, 9, 4, 3, 1, 8, 7, 0))
            )
        )
        == []
    )
    assert (
        sorted(
            BivincularPatt(Perm((2, 4, 3, 1, 0)), [0, 1], [3, 4]).occurrences_in(
                Perm((5, 1, 6, 7, 4, 2, 3, 0))
            )
        )
        == []
    )
    assert sorted(VincularPatt(Perm((0, 1)), [2]).occurrences_in(Perm((2, 1, 0)))) == []
    assert (
        sorted(
            BivincularPatt(Perm((1, 0)), [], [0, 2]).occurrences_in(
                Perm((0, 1, 2, 4, 3))
            )
        )
        == []
    )
    assert (
        sorted(
            BivincularPatt(Perm((1, 0)), [], [0, 2]).occurrences_in(
                Perm((2, 1, 3, 0, 4))
            )
        )
        == []
    )
    assert (
        sorted(CovincularPatt(Perm((2, 0, 1)), [1]).occurrences_in(Perm((0, 2, 1))))
        == []
    )
    assert (
        sorted(VincularPatt(Perm((0, 1, 2)), [0, 1, 3]).occurrences_in(Perm((1, 0))))
        == []
    )
    assert (
        sorted(BivincularPatt(Perm((1, 0)), [0, 2], []).occurrences_in(Perm(()))) == []
    )
    assert sorted(CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm(()))) == []
    assert (
        sorted(
            CovincularPatt(Perm((1, 3, 0, 2)), [1, 3]).occurrences_in(Perm((0, 2, 1)))
        )
        == []
    )
    assert (
        sorted(
            BivincularPatt(Perm((0, 2, 1, 3, 5, 4)), [], [1]).occurrences_in(
                Perm((1, 0))
            )
        )
        == []
    )
    assert (
        sorted(VincularPatt(Perm((3, 2, 4, 0, 1)), []).occurrences_in(Perm(()))) == []
    )
    assert sorted(
        VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((1, 0, 6, 4, 5, 2, 3)))
    ) == [(0, 1), (2, 3), (2, 4), (2, 5), (2, 6), (3, 5), (3, 6), (4, 5), (4, 6)]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((2, 1, 4, 0, 3)))
    ) == [(0, 2), (0, 4), (1, 2), (1, 4), (3, 4)]
    assert sorted(
        CovincularPatt(Perm((5, 0, 2, 1, 3, 4)), [6]).occurrences_in(
            Perm((6, 0, 3, 2, 1, 4, 5))
        )
    ) == [(0, 1, 2, 3, 5, 6), (0, 1, 2, 4, 5, 6), (0, 1, 3, 4, 5, 6)]
    assert sorted(VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((1, 2, 0)))) == [
        (0, 2),
        (1, 2),
    ]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((2, 5, 0, 3, 4, 1)))
    ) == [(0, 1), (0, 3), (0, 4), (2, 3), (2, 4), (2, 5), (3, 4)]
    assert sorted(
        BivincularPatt(Perm((0, 1, 3, 2)), [0, 1], [0, 4]).occurrences_in(
            Perm((0, 3, 6, 1, 4, 5, 2))
        )
    ) == [(0, 1, 2, 4), (0, 1, 2, 5)]
    assert sorted(VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((1, 0, 2)))) == [
        (0, 1)
    ]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((1, 5, 3, 2, 0, 4)))
    ) == [(0, 1), (0, 2), (0, 3), (0, 5), (2, 5), (3, 5), (4, 5)]
    assert sorted(
        VincularPatt(Perm((4, 1, 0, 3, 2)), [0, 1, 2, 3, 5]).occurrences_in(
            Perm((7, 3, 2, 6, 1, 0, 5, 4))
        )
    ) == [(0, 1, 2, 3, 7)]
    assert sorted(
        CovincularPatt(Perm((5, 0, 2, 1, 3, 4)), [6]).occurrences_in(
            Perm((7, 0, 6, 2, 1, 4, 5, 3))
        )
    ) == [(0, 1, 3, 4, 5, 6)]
    assert sorted(
        VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((4, 0, 3, 2, 1, 6, 5)))
    ) == [(0, 1), (0, 2), (0, 3), (0, 4), (2, 3), (2, 4), (3, 4), (5, 6)]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((1, 5, 4, 0, 2, 3, 6)))
    ) == [
        (0, 1),
        (0, 2),
        (0, 4),
        (0, 5),
        (0, 6),
        (1, 6),
        (2, 6),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 5),
        (4, 6),
        (5, 6),
    ]
    assert sorted(
        VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((3, 4, 0, 1, 2)))
    ) == [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((3, 0, 1, 2)))
    ) == [(1, 2), (1, 3), (2, 3)]
    assert sorted(
        CovincularPatt(Perm((5, 0, 2, 1, 3, 4)), [6]).occurrences_in(
            Perm((1, 4, 8, 2, 5, 3, 6, 7, 0))
        )
    ) == [(2, 3, 4, 5, 6, 7)]
    assert sorted(
        BivincularPatt(Perm((0, 1, 3, 2)), [0, 1], [0, 4]).occurrences_in(
            Perm((0, 2, 4, 1, 3))
        )
    ) == [(0, 1, 2, 4)]
    assert sorted(
        VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((0, 6, 3, 5, 1, 2, 4)))
    ) == [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
        (3, 6),
    ]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((3, 5, 4, 0, 2, 1)))
    ) == [(0, 1), (0, 2), (3, 4), (3, 5)]
    assert sorted(
        CovincularPatt(Perm((5, 0, 2, 1, 3, 4)), [6]).occurrences_in(
            Perm((9, 4, 1, 5, 2, 0, 6, 3, 8, 7))
        )
    ) == [(0, 2, 3, 4, 6, 8), (0, 2, 3, 4, 6, 9)]
    assert sorted(
        BivincularPatt(Perm((0, 1, 3, 2)), [0, 1], [0, 4]).occurrences_in(
            Perm((0, 3, 5, 6, 2, 7, 4, 1))
        )
    ) == [(0, 1, 5, 6)]
    assert sorted(
        VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((1, 5, 0, 4, 2, 6, 3)))
    ) == [(0, 2), (1, 2), (1, 3), (1, 4), (1, 6), (3, 4), (3, 6), (5, 6)]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((1, 0, 2, 3)))
    ) == [(0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    assert sorted(
        BivincularPatt(Perm((0, 1, 3, 2)), [0, 1], [0, 4]).occurrences_in(
            Perm((0, 4, 7, 8, 6, 2, 5, 1, 3))
        )
    ) == [(0, 1, 3, 4), (0, 1, 3, 6)]
    assert sorted(
        VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((4, 1, 2, 3, 0)))
    ) == [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((0, 2, 3, 1)))
    ) == [(0, 1), (0, 2), (0, 3), (1, 2)]
    assert sorted(
        CovincularPatt(Perm((5, 0, 2, 1, 3, 4)), [6]).occurrences_in(
            Perm((8, 0, 2, 5, 7, 1, 4, 3, 6))
        )
    ) == [(0, 1, 2, 5, 6, 8), (0, 1, 2, 5, 7, 8)]
    assert sorted(
        BivincularPatt(Perm((0, 1, 3, 2)), [0, 1], [0, 4]).occurrences_in(
            Perm((0, 1, 3, 2))
        )
    ) == [(0, 1, 2, 3)]
    assert sorted(
        VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((2, 0, 3, 4, 1)))
    ) == [(0, 1), (0, 4), (2, 4), (3, 4)]
    assert sorted(
        CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((5, 0, 4, 6, 1, 3, 2)))
    ) == [(0, 3), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (4, 5), (4, 6)]
    assert sorted(
        VincularPatt(Perm((4, 1, 0, 3, 2)), [0, 1, 2, 3, 5]).occurrences_in(
            Perm((4, 1, 0, 3, 2))
        )
    ) == [(0, 1, 2, 3, 4)]
    assert sorted(
        VincularPatt(Perm((1, 0)), []).occurrences_in(Perm((0, 1, 3, 2)))
    ) == [(2, 3)]
    assert sorted(CovincularPatt(Perm((0, 1)), []).occurrences_in(Perm((0, 1, 2)))) == [
        (0, 1),
        (0, 2),
        (1, 2),
    ]
    assert sorted(
        BivincularPatt(Perm((1, 3, 0, 2, 4)), [], [0, 1, 3]).occurrences_in(
            Perm((7, 1, 4, 0, 3, 6, 5, 8, 9, 2))
        )
    ) == [(1, 2, 3, 4, 5), (1, 2, 3, 4, 6), (1, 2, 3, 4, 7), (1, 2, 3, 4, 8)]
    assert sorted(
        VincularPatt(Perm((0, 2, 1, 3)), [0, 1]).occurrences_in(
            Perm((10, 16, 7, 1, 13, 15, 14, 0, 5, 12, 3, 4, 2, 11, 8, 17, 6, 9))
        )
    ) == [(0, 1, 4, 15), (0, 1, 5, 15), (0, 1, 6, 15), (0, 1, 9, 15), (0, 1, 13, 15)]
    assert sorted(
        CovincularPatt(Perm((1, 2, 0, 3)), []).occurrences_in(
            Perm((1, 6, 2, 0, 5, 4, 3))
        )
    ) == [(0, 2, 3, 4), (0, 2, 3, 5), (0, 2, 3, 6)]
    assert sorted(
        CovincularPatt(Perm((0, 1, 2)), [1, 2, 3]).occurrences_in(Perm((2, 0, 3, 1, 4)))
    ) == [(0, 2, 4)]
    assert sorted(
        VincularPatt(Perm((2, 3, 0, 1)), [1, 3, 4]).occurrences_in(
            Perm((5, 0, 6, 8, 9, 3, 1, 2, 4, 7))
        )
    ) == [(3, 4, 8, 9)]
    assert sorted(
        BivincularPatt(Perm((2, 4, 3, 1, 0, 5)), [], [2]).occurrences_in(
            Perm((15, 16, 8, 17, 7, 18, 11, 12, 9, 6, 4, 5, 2, 13, 0, 3, 1, 14, 19, 10))
        )
    ) == [
        (4, 5, 6, 9, 10, 18),
        (4, 5, 6, 9, 11, 18),
        (4, 5, 6, 9, 12, 18),
        (4, 5, 6, 9, 14, 18),
        (4, 5, 6, 9, 15, 18),
        (4, 5, 6, 9, 16, 18),
        (4, 5, 7, 9, 10, 18),
        (4, 5, 7, 9, 11, 18),
        (4, 5, 7, 9, 12, 18),
        (4, 5, 7, 9, 14, 18),
        (4, 5, 7, 9, 15, 18),
        (4, 5, 7, 9, 16, 18),
        (4, 5, 8, 9, 10, 18),
        (4, 5, 8, 9, 11, 18),
        (4, 5, 8, 9, 12, 18),
        (4, 5, 8, 9, 14, 18),
        (4, 5, 8, 9, 15, 18),
        (4, 5, 8, 9, 16, 18),
        (4, 6, 8, 9, 10, 13),
        (4, 6, 8, 9, 10, 17),
        (4, 6, 8, 9, 10, 18),
        (4, 6, 8, 9, 11, 13),
        (4, 6, 8, 9, 11, 17),
        (4, 6, 8, 9, 11, 18),
        (4, 6, 8, 9, 12, 13),
        (4, 6, 8, 9, 12, 17),
        (4, 6, 8, 9, 12, 18),
        (4, 6, 8, 9, 14, 17),
        (4, 6, 8, 9, 14, 18),
        (4, 6, 8, 9, 15, 17),
        (4, 6, 8, 9, 15, 18),
        (4, 6, 8, 9, 16, 17),
        (4, 6, 8, 9, 16, 18),
        (4, 7, 8, 9, 10, 13),
        (4, 7, 8, 9, 10, 17),
        (4, 7, 8, 9, 10, 18),
        (4, 7, 8, 9, 11, 13),
        (4, 7, 8, 9, 11, 17),
        (4, 7, 8, 9, 11, 18),
        (4, 7, 8, 9, 12, 13),
        (4, 7, 8, 9, 12, 17),
        (4, 7, 8, 9, 12, 18),
        (4, 7, 8, 9, 14, 17),
        (4, 7, 8, 9, 14, 18),
        (4, 7, 8, 9, 15, 17),
        (4, 7, 8, 9, 15, 18),
        (4, 7, 8, 9, 16, 17),
        (4, 7, 8, 9, 16, 18),
    ]
    assert sorted(
        CovincularPatt(Perm((1, 3, 0, 2)), [2, 4]).occurrences_in(
            Perm((3, 8, 6, 1, 4, 12, 15, 9, 0, 18, 10, 11, 7, 2, 14, 5, 13, 17, 16))
        )
    ) == [
        (4, 9, 13, 15),
        (5, 9, 10, 16),
        (5, 9, 11, 16),
        (5, 9, 12, 16),
        (5, 9, 13, 16),
        (5, 9, 15, 16),
        (6, 9, 10, 18),
        (6, 9, 11, 18),
        (6, 9, 12, 18),
        (6, 9, 13, 18),
        (6, 9, 14, 18),
        (6, 9, 15, 18),
        (6, 9, 16, 18),
    ]
    assert sorted(
        CovincularPatt(Perm((2, 5, 0, 3, 4, 1)), []).occurrences_in(
            Perm((1, 16, 0, 6, 2, 3, 13, 9, 14, 15, 5, 11, 10, 12, 7, 4, 8))
        )
    ) == [
        (7, 8, 10, 11, 13, 14),
        (7, 8, 10, 11, 13, 16),
        (7, 8, 10, 12, 13, 14),
        (7, 8, 10, 12, 13, 16),
        (7, 9, 10, 11, 13, 14),
        (7, 9, 10, 11, 13, 16),
        (7, 9, 10, 12, 13, 14),
        (7, 9, 10, 12, 13, 16),
    ]
    assert sorted(
        VincularPatt(Perm((1, 0, 2)), [2]).occurrences_in(
            Perm((6, 4, 8, 0, 2, 3, 1, 9, 7, 5))
        )
    ) == [(0, 1, 2), (0, 6, 7), (1, 6, 7), (2, 6, 7), (4, 6, 7), (5, 6, 7)]
    assert sorted(
        VincularPatt(Perm((2, 0, 1)), [0, 1, 2]).occurrences_in(
            Perm((13, 2, 12, 4, 10, 3, 1, 9, 6, 15, 5, 7, 0, 16, 8, 11, 14))
        )
    ) == [(0, 1, 2)]


def test_contain_dunder_method():
    assert BivincularPatt(Perm((0, 1, 2)), (2,), ()) in Perm((0, 4, 3, 1, 2))
    assert VincularPatt(Perm((0, 1, 2)), (2,)) in Perm((0, 4, 3, 1, 2))
    assert BivincularPatt(Perm((2, 0, 1)), (), (2,)) in Perm((1, 2, 4, 0, 3))
    assert CovincularPatt(Perm((2, 0, 1)), (2,)) in Perm((1, 2, 4, 0, 3))


def test_avoided_by():
    assert CovincularPatt(Perm((2, 3, 0, 1, 4)), [1, 2, 5]).avoided_by(
        Perm((7, 1, 2, 8, 6, 0, 3, 4, 5)),
        Perm((2, 5, 4, 3, 1, 0)),
        Perm((0, 2, 3, 4, 1, 5)),
    )
    assert BivincularPatt(Perm((0, 2, 1)), [0, 2], [0, 1, 2]).avoided_by(
        Perm((5, 1, 4, 0, 2, 6, 3)), Perm((3, 2, 0, 1, 5, 4)), Perm((0, 1))
    )
    assert BivincularPatt(Perm((1, 0)), [0, 2], [0, 1]).avoided_by(
        Perm((2, 3, 4, 5, 0, 1)), Perm((2, 0, 3, 1)), Perm((0, 1, 2, 3))
    )
    assert not VincularPatt(Perm((3, 1, 0, 2)), [1, 3]).avoided_by(
        Perm((1, 4, 8, 2, 3, 7, 6, 0, 5)),
        Perm((2, 1, 3, 4, 0)),
        Perm((6, 5, 1, 4, 0, 3, 7, 2)),
    )
    assert not CovincularPatt(Perm((2, 1, 3, 0)), [2]).avoided_by(
        Perm((8, 6, 4, 0, 7, 2, 3, 1, 5)),
        Perm((7, 3, 0, 1, 2, 6, 4, 5)),
        Perm((7, 2, 0, 4, 3, 8, 5, 6, 1)),
    )
    assert VincularPatt(Perm((0, 1, 3, 2)), [0]).avoided_by(
        Perm((4, 0, 3, 1, 2)), Perm((1, 0)), Perm((3, 1, 4, 0, 5, 2))
    )
    assert BivincularPatt(Perm((0, 2, 1)), [0, 1], [0, 1, 3]).avoided_by(
        Perm((3, 2, 1, 0)), Perm((5, 2, 4, 0, 3, 1)), Perm((3, 2, 1, 0, 4, 5))
    )
    assert not BivincularPatt(Perm((3, 2, 1, 0)), [], []).avoided_by(
        Perm((4, 3, 2, 0, 1)), Perm((1, 3, 4, 5, 6, 0, 2)), Perm((1, 3, 2, 0))
    )
    assert not CovincularPatt(Perm((0, 2, 1)), [0, 2]).avoided_by(
        Perm((6, 1, 2, 3, 0, 5, 4)), Perm((4, 2, 1, 0, 3)), Perm((0, 1, 2, 3))
    )
    assert not VincularPatt(Perm((1, 0)), []).avoided_by(
        Perm((2, 0, 6, 3, 5, 4, 1)), Perm((1, 3, 0, 2, 4)), Perm((0, 4, 1, 3, 2))
    )
    assert not CovincularPatt(Perm((1, 0, 2, 3)), [4]).avoided_by(
        Perm((3, 2, 0, 4, 1, 5)),
        Perm((3, 2, 4, 0, 1)),
        Perm((0, 3, 4, 8, 6, 1, 7, 5, 2)),
    )
    assert VincularPatt(Perm((5, 2, 1, 0, 3, 4)), [1, 4, 5, 6]).avoided_by(
        Perm((3, 4, 1, 0, 6, 5, 7, 2)),
        Perm((0, 5, 3, 1, 7, 4, 2, 6)),
        Perm((7, 0, 6, 3, 9, 1, 8, 2, 5, 4)),
    )
    assert CovincularPatt(Perm((0, 2, 1)), [0, 1, 3]).avoided_by(
        Perm((0, 6, 1, 8, 3, 2, 9, 7, 4, 5)),
        Perm((4, 2, 3, 6, 5, 8, 1, 0, 7)),
        Perm((0, 2, 9, 6, 5, 8, 1, 4, 7, 11, 10, 3)),
    )
    assert BivincularPatt(Perm((3, 1, 0, 2)), [0, 1, 2, 3], [2]).avoided_by(
        Perm((4, 3, 0, 7, 8, 2, 9, 6, 5, 1)),
        Perm((2, 9, 4, 0, 7, 1, 3, 8, 6, 5)),
        Perm((0, 1, 5, 4, 7, 6, 8, 3, 2)),
    )
    assert BivincularPatt(Perm((0, 2, 4, 5, 1, 3)), [], [1, 2, 3, 4, 5]).avoided_by(
        Perm((8, 4, 12, 11, 10, 6, 2, 1, 9, 7, 3, 5, 0)),
        Perm((11, 12, 4, 9, 8, 3, 10, 2, 6, 7, 5, 0, 1)),
        Perm((10, 14, 4, 3, 7, 15, 1, 11, 5, 6, 12, 8, 9, 2, 13, 0)),
    )


def test_count_occurrences_in():
    assert (
        BivincularPatt(
            Perm((4, 0, 1, 2, 3, 5)), [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5]
        ).count_occurrences_in(Perm((7, 2, 6, 4, 8, 5, 3, 0, 1)))
        == 0
    )
    assert (
        BivincularPatt(
            Perm((4, 0, 1, 2, 3, 5)), [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5]
        ).count_occurrences_in(
            Perm((10, 9, 3, 5, 12, 4, 6, 7, 1, 8, 14, 15, 0, 11, 13, 2))
        )
        == 0
    )
    assert (
        BivincularPatt(
            Perm((4, 0, 1, 2, 3, 5)), [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5]
        ).count_occurrences_in(Perm((1, 3, 7, 6, 5, 0, 8, 2, 4)))
        == 0
    )
    assert (
        VincularPatt(Perm((0, 1, 2)), [0, 1, 3]).count_occurrences_in(
            Perm((1, 4, 2, 6, 8, 5, 0, 3, 7))
        )
        == 1
    )
    assert (
        VincularPatt(Perm((0, 1, 2)), [0, 1, 3]).count_occurrences_in(
            Perm((8, 10, 3, 4, 6, 1, 11, 7, 0, 9, 2, 5))
        )
        == 0
    )
    assert (
        VincularPatt(Perm((0, 1, 2)), [0, 1, 3]).count_occurrences_in(
            Perm((0, 5, 2, 1, 4, 3))
        )
        == 0
    )
    assert (
        CovincularPatt(Perm((4, 2, 0, 1, 3)), [3]).count_occurrences_in(
            Perm((0, 7, 10, 2, 9, 12, 3, 1, 4, 5, 8, 11, 6, 13))
        )
        == 0
    )
    assert (
        CovincularPatt(Perm((4, 2, 0, 1, 3)), [3]).count_occurrences_in(
            Perm((3, 0, 7, 1, 4, 2, 5, 6))
        )
        == 0
    )
    assert (
        CovincularPatt(Perm((4, 2, 0, 1, 3)), [3]).count_occurrences_in(
            Perm((6, 11, 7, 5, 8, 1, 0, 10, 4, 3, 9, 2))
        )
        == 4
    )
    assert (
        CovincularPatt(Perm((0, 1)), [0, 1]).count_occurrences_in(
            Perm((6, 4, 2, 0, 5, 7, 1, 3))
        )
        == 1
    )
    assert (
        CovincularPatt(Perm((0, 1)), [0, 1]).count_occurrences_in(
            Perm((1, 4, 6, 3, 0, 9, 8, 2, 5, 7))
        )
        == 0
    )
    assert (
        CovincularPatt(Perm((0, 1)), [0, 1]).count_occurrences_in(
            Perm((0, 6, 2, 4, 3, 7, 5, 1))
        )
        == 1
    )
    assert (
        BivincularPatt(Perm((1, 0, 3, 2)), [1], [0, 1, 3, 4]).count_occurrences_in(
            Perm((6, 0, 5, 4, 7, 3, 2, 1))
        )
        == 0
    )
    assert (
        BivincularPatt(Perm((1, 0, 3, 2)), [1], [0, 1, 3, 4]).count_occurrences_in(
            Perm((1, 10, 6, 11, 13, 2, 3, 12, 9, 5, 0, 7, 8, 4))
        )
        == 0
    )
    assert (
        BivincularPatt(Perm((1, 0, 3, 2)), [1], [0, 1, 3, 4]).count_occurrences_in(
            Perm((11, 7, 2, 0, 4, 10, 1, 3, 6, 8, 12, 9, 5))
        )
        == 0
    )
    assert (
        VincularPatt(Perm((2, 4, 0, 3, 1)), [0, 3]).count_occurrences_in(
            Perm((10, 4, 9, 13, 6, 2, 0, 5, 1, 12, 11, 8, 7, 3))
        )
        == 3
    )
    assert (
        VincularPatt(Perm((2, 4, 0, 3, 1)), [0, 3]).count_occurrences_in(
            Perm((13, 12, 2, 0, 5, 11, 10, 3, 9, 4, 1, 6, 8, 7))
        )
        == 0
    )
    assert (
        VincularPatt(Perm((2, 4, 0, 3, 1)), [0, 3]).count_occurrences_in(
            Perm((4, 7, 11, 2, 0, 9, 5, 8, 14, 3, 1, 6, 13, 12, 10))
        )
        == 2
    )
    assert (
        VincularPatt(Perm((3, 0, 1, 2, 4)), [0, 2, 4, 5]).count_occurrences_in(
            BivincularPatt(Perm((1, 2, 0)), [0, 1], [1, 2, 3])
        )
        == 0
    )
    assert (
        CovincularPatt(Perm((1, 0, 2)), [2]).count_occurrences_in(
            BivincularPatt(Perm((2, 0, 1, 3, 4)), [], [0, 1, 2, 3])
        )
        == 2
    )
    assert (
        CovincularPatt(Perm((0, 2, 1)), [1, 3]).count_occurrences_in(
            BivincularPatt(Perm((0, 1, 3, 4, 2)), [0, 1, 2, 4], [2, 3, 4, 5])
        )
        == 1
    )


def test_contained_in():
    assert not BivincularPatt(Perm((2, 1, 0)), [0, 2, 3], [0, 1, 2]).contained_in(
        Perm((8, 4, 6, 3, 1, 7, 2, 0, 5))
    )
    assert not BivincularPatt(Perm((2, 1, 0)), [0, 2, 3], [0, 1, 2]).contained_in(
        Perm((5, 2, 3, 4, 1, 6, 0))
    )
    assert not BivincularPatt(Perm((2, 1, 0)), [0, 2, 3], [0, 1, 2]).contained_in(
        Perm((1, 0))
    )
    assert not CovincularPatt(Perm((3, 0, 2, 1)), []).contained_in(
        Perm((2, 0, 1, 5, 3, 6, 4))
    )
    assert not CovincularPatt(Perm((3, 0, 2, 1)), []).contained_in(Perm((0, 3, 1, 2)))
    assert CovincularPatt(Perm((3, 0, 2, 1)), []).contained_in(
        Perm((5, 3, 6, 7, 8, 0, 2, 1, 4, 9))
    )
    assert not BivincularPatt(Perm((1, 3, 0, 2)), [0], []).contained_in(Perm((1, 0)))
    assert not BivincularPatt(Perm((1, 3, 0, 2)), [0], []).contained_in(
        Perm((6, 0, 4, 1, 3, 5, 2, 7))
    )
    assert not BivincularPatt(Perm((1, 3, 0, 2)), [0], []).contained_in(
        Perm((9, 0, 1, 3, 4, 5, 7, 8, 2, 6))
    )
    assert not CovincularPatt(Perm((4, 3, 0, 2, 1)), []).contained_in(
        Perm((1, 2, 0, 6, 10, 3, 4, 7, 5, 9, 11, 8))
    )
    assert not CovincularPatt(Perm((4, 3, 0, 2, 1)), []).contained_in(
        Perm((3, 2, 4, 0, 1))
    )
    assert CovincularPatt(Perm((4, 3, 0, 2, 1)), []).contained_in(
        Perm((6, 0, 5, 1, 9, 2, 8, 11, 7, 4, 12, 3, 10))
    )
    assert VincularPatt(Perm((0, 1)), [0, 2]).contained_in(Perm((0, 3, 1, 2)))
    assert not VincularPatt(Perm((0, 1)), [0, 2]).contained_in(Perm(()))
    assert VincularPatt(Perm((0, 1)), [0, 2]).contained_in(Perm((3, 2, 0, 1, 4)))
    assert VincularPatt(Perm((1, 2, 0)), []).contained_in(
        Perm((2, 4, 10, 7, 5, 0, 6, 8, 3, 9, 11, 1))
    )
    assert VincularPatt(Perm((1, 2, 0)), []).contained_in(Perm((4, 1, 2, 5, 3, 0)))
    assert not VincularPatt(Perm((1, 2, 0)), []).contained_in(Perm((0,)))
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((11, 1, 4, 10, 12, 0, 9, 2, 6, 5, 7, 3, 8))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((0, 4, 2, 6, 3, 1, 5))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((2, 8, 6, 4, 3, 0, 9, 7, 5, 10, 1))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((0, 1, 2)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((0, 2, 1, 6, 3, 4, 5)))
    assert BivincularPatt(Perm((0, 2, 1)), [0, 3], [2]).contained_in(
        Perm((8, 3, 9, 1, 6, 10, 12, 0, 2, 7, 5, 4, 11))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(Perm((1, 3, 4, 2, 0)))
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((9, 0, 3, 6, 7, 2, 1, 8, 5, 4, 11, 10))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(
        Perm((6, 1, 0, 2, 10, 7, 5, 9, 3, 4, 8))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((3, 0, 4, 5, 2, 1, 6)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((1, 2, 0)))
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((7, 5, 8, 4, 1, 9, 3, 6, 2, 0))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((1, 3, 0, 4, 5, 6, 2))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((2, 7, 5, 0, 3, 6, 1, 4)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(
        Perm((6, 7, 0, 2, 8, 4, 1, 9, 3, 10, 5))
    )
    assert BivincularPatt(Perm((0, 2, 1)), [0, 3], [2]).contained_in(Perm((0, 2, 1)))
    assert BivincularPatt(Perm((0, 2, 1)), [0, 3], [2]).contained_in(Perm((1, 3, 0, 2)))
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((4, 5, 3, 0, 1, 8, 6, 2, 10, 11, 9, 7, 12))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((6, 2, 7, 5, 1, 4, 3, 0))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((1, 2, 0)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((1, 2, 3, 4, 0, 5)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((2, 3, 0, 1)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((0, 1, 2)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((0, 1)))
    assert BivincularPatt(Perm((0, 2, 1)), [0, 3], [2]).contained_in(
        Perm((5, 3, 4, 0, 6, 7, 1, 2, 9, 8))
    )
    assert BivincularPatt(Perm((0, 2, 1)), [0, 3], [2]).contained_in(Perm((1, 0, 3, 2)))
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((1, 3, 5, 10, 7, 4, 8, 0, 2, 9, 6))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(Perm((2, 3, 1, 0)))
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((7, 5, 3, 1, 8, 2, 0, 4, 11, 9, 10, 6))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((2, 3, 0, 1)))
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((5, 8, 9, 0, 3, 2, 7, 6, 1, 4))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(
        Perm((3, 6, 10, 7, 11, 1, 4, 2, 5, 8, 0, 9))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(
        Perm((9, 7, 4, 5, 0, 1, 10, 11, 6, 2, 3, 8))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(
        Perm((4, 9, 8, 6, 0, 5, 2, 3, 7, 1))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(Perm((1, 2, 0)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(
        Perm((4, 10, 1, 5, 11, 9, 2, 3, 8, 7, 6, 0))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(
        Perm((2, 5, 9, 3, 0, 1, 8, 4, 10, 6, 7))
    )
    assert BivincularPatt(Perm((0, 2, 1)), [0, 3], [2]).contained_in(
        Perm((5, 3, 2, 8, 4, 0, 1, 6, 7))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((2, 4, 5, 7, 0, 3, 6, 1))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((1, 0, 2)))
    assert BivincularPatt(Perm((0, 2, 1)), [0, 3], [2]).contained_in(
        Perm((0, 4, 2, 6, 1, 5, 3))
    )
    assert BivincularPatt(Perm((0, 2, 1)), [0, 3], [2]).contained_in(Perm((0, 2, 1)))
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((2, 12, 9, 1, 6, 10, 5, 8, 11, 3, 4, 0, 7))
    )
    assert CovincularPatt(Perm((1, 2, 0)), [1, 2]).contained_in(
        Perm((4, 5, 7, 9, 2, 1, 8, 0, 6, 3))
    )
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((5, 0, 2, 3, 4, 6, 1)))
    assert VincularPatt(Perm((0, 1)), [0]).contained_in(Perm((0, 1)))
