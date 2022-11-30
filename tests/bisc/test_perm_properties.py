from permuta import Perm
from permuta.bisc.perm_properties import (
    _perm_to_yt,
    av_231_and_mesh,
    baxter,
    dihedral,
    forest_like,
    hard_mesh,
    in_alternating_group,
    simsun,
    smooth,
    yt_perm_avoids_22,
    yt_perm_avoids_32,
)


def test_smooth():
    assert smooth(Perm(()))
    assert smooth(Perm((0,)))
    assert smooth(Perm((0, 1)))
    assert smooth(Perm((1, 0)))
    assert smooth(Perm((0, 1, 2)))
    assert smooth(Perm((0, 2, 1)))
    assert smooth(Perm((1, 0, 2)))
    assert smooth(Perm((1, 2, 0)))
    assert smooth(Perm((2, 0, 1)))
    assert smooth(Perm((2, 1, 0)))
    assert smooth(Perm((0, 1, 2, 3)))
    assert smooth(Perm((0, 1, 3, 2)))
    assert not smooth(Perm((0, 3, 5, 1, 2, 4)))
    assert not smooth(Perm((3, 4, 1, 0, 5, 2)))
    assert not smooth(Perm((0, 3, 2, 4, 5, 6, 1)))
    assert not smooth(Perm((5, 3, 1, 4, 2, 6, 0)))
    assert smooth(Perm((3, 7, 2, 0, 4, 5, 6, 1)))
    assert not smooth(Perm((4, 7, 1, 3, 8, 5, 0, 6, 2)))
    assert 1552 == sum(1 for p in Perm.of_length(7) if smooth(p))


def test_forest_like():
    assert forest_like(Perm(()))
    assert forest_like(Perm((0,)))
    assert forest_like(Perm((0, 1)))
    assert forest_like(Perm((1, 0)))
    assert forest_like(Perm((0, 1, 2)))
    assert forest_like(Perm((0, 2, 1)))
    assert forest_like(Perm((1, 0, 2)))
    assert forest_like(Perm((1, 2, 0)))
    assert forest_like(Perm((2, 0, 1)))
    assert forest_like(Perm((2, 1, 0)))
    assert forest_like(Perm((0, 1, 2, 3)))
    assert forest_like(Perm((0, 1, 3, 2)))
    assert not forest_like(Perm((3, 4, 1, 0, 5, 2)))
    assert forest_like(Perm((5, 4, 0, 1, 3, 2)))
    assert forest_like(Perm((6, 0, 1, 5, 2, 3, 4)))
    assert forest_like(Perm((6, 1, 2, 5, 3, 4, 0)))
    assert forest_like(Perm((7, 2, 3, 4, 6, 5, 1, 0)))
    assert not forest_like(Perm((0, 1, 6, 7, 4, 2, 3, 8, 5)))
    assert 1661 == sum(1 for p in Perm.of_length(7) if forest_like(p))


def test_baxter():
    assert baxter(Perm(()))
    assert baxter(Perm((0,)))
    assert baxter(Perm((0, 1)))
    assert baxter(Perm((1, 0)))
    assert baxter(Perm((0, 1, 2)))
    assert baxter(Perm((0, 2, 1)))
    assert baxter(Perm((1, 0, 2)))
    assert baxter(Perm((1, 2, 0)))
    assert baxter(Perm((2, 0, 1)))
    assert baxter(Perm((2, 1, 0)))
    assert baxter(Perm((0, 1, 2, 3)))
    assert baxter(Perm((0, 1, 3, 2)))
    assert not baxter(Perm((1, 3, 0, 5, 4, 2)))
    assert not baxter(Perm((5, 3, 1, 0, 4, 2)))
    assert baxter(Perm((5, 4, 3, 0, 1, 2, 6)))
    assert baxter(Perm((6, 0, 5, 3, 4, 1, 2)))
    assert baxter(Perm((5, 3, 4, 2, 0, 1, 6, 7)))
    assert baxter(Perm((1, 2, 4, 6, 5, 3, 0, 8, 7)))
    assert 2074 == sum(1 for p in Perm.of_length(7) if baxter(p))


def test_simsun():
    assert simsun(Perm(()))
    assert simsun(Perm((0,)))
    assert simsun(Perm((0, 1)))
    assert simsun(Perm((1, 0)))
    assert simsun(Perm((0, 1, 2)))
    assert simsun(Perm((0, 2, 1)))
    assert simsun(Perm((1, 0, 2)))
    assert simsun(Perm((1, 2, 0)))
    assert simsun(Perm((2, 0, 1)))
    assert not simsun(Perm((2, 1, 0)))
    assert simsun(Perm((0, 1, 2, 3)))
    assert simsun(Perm((0, 1, 3, 2)))
    assert simsun(Perm((0, 5, 1, 4, 2, 3)))
    assert not simsun(Perm((1, 3, 5, 4, 2, 0)))
    assert simsun(Perm((1, 5, 0, 2, 3, 6, 4)))
    assert not simsun(Perm((3, 1, 2, 6, 5, 0, 4)))
    assert not simsun(Perm((4, 7, 3, 0, 6, 5, 2, 1)))
    assert not simsun(Perm((4, 6, 7, 0, 3, 5, 2, 8, 1)))
    assert 1385 == sum(1 for p in Perm.of_length(7) if simsun(p))


def test_dihedral():
    assert not dihedral(Perm(()))
    assert not dihedral(Perm((0,)))
    assert not dihedral(Perm((0, 1)))
    assert not dihedral(Perm((1, 0)))
    assert dihedral(Perm((0, 1, 2)))
    assert dihedral(Perm((0, 2, 1)))
    assert dihedral(Perm((1, 0, 2)))
    assert dihedral(Perm((1, 2, 0)))
    assert dihedral(Perm((2, 0, 1)))
    assert dihedral(Perm((2, 1, 0)))
    assert dihedral(Perm((0, 1, 2, 3)))
    assert not dihedral(Perm((0, 1, 3, 2)))
    assert not dihedral(Perm((3, 4, 1, 0, 2, 5)))
    assert not dihedral(Perm((5, 4, 2, 1, 0, 3)))
    assert not dihedral(Perm((2, 3, 6, 1, 0, 5, 4)))
    assert not dihedral(Perm((6, 4, 2, 5, 1, 3, 0)))
    assert not dihedral(Perm((1, 6, 4, 2, 0, 5, 3, 7)))
    assert not dihedral(Perm((2, 0, 3, 8, 1, 5, 7, 4, 6)))
    assert not dihedral(Perm((1, 7, 4, 3, 8, 9, 6, 2, 5, 0)))
    assert not dihedral(Perm((5, 6, 2, 10, 1, 0, 9, 3, 7, 4, 8)))
    assert all(
        2 * n == sum(1 for perm in Perm.of_length(n) if dihedral(perm))
        for n in range(5, 8)
    )


def test_in_alternating_group():
    assert in_alternating_group(Perm(()))
    assert in_alternating_group(Perm((0,)))
    assert not in_alternating_group(Perm((0, 1)))
    assert not in_alternating_group(Perm((1, 0)))
    assert in_alternating_group(Perm((0, 1, 2)))
    assert not in_alternating_group(Perm((0, 2, 1)))
    assert not in_alternating_group(Perm((1, 0, 2)))
    assert in_alternating_group(Perm((1, 2, 0)))
    assert in_alternating_group(Perm((2, 0, 1)))
    assert not in_alternating_group(Perm((2, 1, 0)))
    assert in_alternating_group(Perm((0, 1, 2, 3)))
    assert not in_alternating_group(Perm((0, 1, 3, 2)))
    assert not in_alternating_group(Perm((0, 4, 1, 5, 2, 3)))
    assert in_alternating_group(Perm((5, 4, 0, 2, 1, 3)))
    assert not in_alternating_group(Perm((0, 4, 3, 5, 2, 6, 1)))
    assert not in_alternating_group(Perm((1, 3, 0, 2, 5, 6, 4)))
    assert in_alternating_group(Perm((5, 7, 2, 1, 4, 0, 3, 6)))
    assert not in_alternating_group(Perm((3, 0, 6, 1, 2, 8, 5, 4, 7)))
    assert in_alternating_group(Perm((5, 1, 6, 4, 9, 8, 2, 0, 7, 3)))
    assert not in_alternating_group(Perm((7, 0, 2, 4, 8, 5, 1, 9, 6, 3, 10)))
    assert 2520 == sum(1 for p in Perm.of_length(7) if in_alternating_group(p))


def test__perm_to_yt():
    z = {i: set() for i in range(8)}
    for i in range(8):
        for p in Perm.of_length(i):
            z[i].add(tuple(map(tuple, _perm_to_yt(p))))
    expected = [1, 1, 2, 4, 10, 26, 76, 232]
    for i in range(8):
        assert len(z[i]) == expected[i]
    assert _perm_to_yt(Perm((1, 0))) == [[0], [1]]
    assert _perm_to_yt(Perm((1, 0, 3, 5, 2, 4))) == [[0, 2, 4], [1, 3, 5]]
    assert _perm_to_yt(Perm((1, 0, 2, 3))) == [[0, 2, 3], [1]]
    assert _perm_to_yt(Perm((3, 1, 4, 0, 2))) == [[0, 2], [1, 4], [3]]
    assert _perm_to_yt(Perm((5, 4, 1, 0, 3, 2))) == [[0, 2], [1, 3], [4], [5]]
    assert _perm_to_yt(Perm((0, 1))) == [[0, 1]]
    assert _perm_to_yt(Perm((0,))) == [[0]]
    assert _perm_to_yt(Perm((2, 3, 0, 1))) == [[0, 1], [2, 3]]
    assert _perm_to_yt(Perm((1, 2, 3, 0))) == [[0, 2, 3], [1]]
    assert _perm_to_yt(Perm((4, 0, 1, 2, 5, 3))) == [[0, 1, 2, 3], [4, 5]]


def test_yt_perm_avoids_22():
    assert yt_perm_avoids_22(Perm())
    assert yt_perm_avoids_22(Perm((0,)))
    assert yt_perm_avoids_22(Perm((0, 1)))
    assert yt_perm_avoids_22(Perm((1, 0)))
    assert yt_perm_avoids_22(Perm((0, 1, 2)))
    assert yt_perm_avoids_22(Perm((0, 2, 1)))
    assert yt_perm_avoids_22(Perm((1, 0, 2)))
    assert yt_perm_avoids_22(Perm((1, 2, 0)))
    assert yt_perm_avoids_22(Perm((2, 0, 1)))
    assert yt_perm_avoids_22(Perm((2, 1, 0)))
    assert yt_perm_avoids_22(Perm((0, 1, 2, 3)))
    assert yt_perm_avoids_22(Perm((0, 1, 3, 2)))
    assert yt_perm_avoids_22(Perm((2, 5, 3, 1, 0, 4)))
    assert yt_perm_avoids_22(Perm((4, 3, 1, 2, 0, 5)))
    assert not yt_perm_avoids_22(Perm((3, 0, 4, 1, 5, 6, 2)))
    assert not yt_perm_avoids_22(Perm((5, 6, 0, 2, 4, 3, 1)))
    assert not yt_perm_avoids_22(Perm((7, 4, 3, 5, 0, 2, 6, 1)))
    assert yt_perm_avoids_22(Perm((3, 4, 5, 6, 2, 7, 1, 0, 8)))
    assert not yt_perm_avoids_22(Perm((7, 5, 2, 0, 4, 8, 6, 9, 1, 3)))
    assert not yt_perm_avoids_22(Perm((3, 5, 4, 6, 0, 7, 2, 10, 1, 8, 9)))
    assert not yt_perm_avoids_22(Perm((1, 2, 0, 4, 3, 5)))
    assert not yt_perm_avoids_22(Perm((5, 2, 0, 3, 1, 4)))
    assert not yt_perm_avoids_22(Perm((1, 0, 6, 4, 3, 5, 2)))
    assert not yt_perm_avoids_22(Perm((5, 0, 1, 3, 6, 2, 4)))
    assert not yt_perm_avoids_22(Perm((5, 1, 2, 7, 4, 3, 0, 6)))
    assert not yt_perm_avoids_22(Perm((5, 6, 0, 8, 3, 7, 4, 1, 2)))
    assert not yt_perm_avoids_22(Perm((2, 5, 7, 6, 1, 8, 9, 3, 0, 4)))
    assert not yt_perm_avoids_22(Perm((7, 8, 4, 0, 1, 5, 2, 10, 3, 9, 6)))
    assert 924 == sum(1 for p in Perm.of_length(7) if yt_perm_avoids_22(p))


def test_yt_perm_avoids_32():
    assert yt_perm_avoids_32(Perm())
    assert yt_perm_avoids_32(Perm((0,)))
    assert yt_perm_avoids_32(Perm((0, 1)))
    assert yt_perm_avoids_32(Perm((1, 0)))
    assert yt_perm_avoids_32(Perm((0, 1, 2)))
    assert yt_perm_avoids_32(Perm((0, 2, 1)))
    assert yt_perm_avoids_32(Perm((1, 0, 2)))
    assert yt_perm_avoids_32(Perm((1, 2, 0)))
    assert yt_perm_avoids_32(Perm((2, 0, 1)))
    assert yt_perm_avoids_32(Perm((2, 1, 0)))
    assert yt_perm_avoids_32(Perm((0, 1, 2, 3)))
    assert yt_perm_avoids_32(Perm((0, 1, 3, 2)))
    assert yt_perm_avoids_32(Perm((2, 3, 1, 4, 0, 5)))
    assert not yt_perm_avoids_32(Perm((2, 3, 1, 5, 4, 0)))
    assert not yt_perm_avoids_32(Perm((2, 0, 3, 1, 4, 5, 6)))
    assert not yt_perm_avoids_32(Perm((5, 1, 2, 0, 4, 3, 6)))
    assert not yt_perm_avoids_32(Perm((5, 0, 4, 2, 1, 6, 3, 7)))
    assert not yt_perm_avoids_32(Perm((0, 6, 3, 1, 8, 7, 4, 5, 2)))
    assert not yt_perm_avoids_32(Perm((6, 4, 9, 0, 3, 1, 8, 7, 5, 2)))
    assert not yt_perm_avoids_32(Perm((10, 8, 1, 4, 0, 5, 2, 7, 9, 3, 6)))
    assert yt_perm_avoids_32(Perm((7, 3, 2, 4, 5, 1, 0, 6)))
    assert yt_perm_avoids_32(Perm((5, 4, 6, 1, 3, 2, 0)))
    assert yt_perm_avoids_32(Perm((4, 6, 2, 0, 5, 3, 1)))
    assert 1316 == sum(1 for p in Perm.of_length(7) if yt_perm_avoids_32(p))
    assert yt_perm_avoids_32(Perm((0, 14, 1, 13, 11, 8, 3, 5, 7, 9, 6, 10, 12, 4, 2)))
    assert yt_perm_avoids_32(Perm((7, 5, 2, 4, 6, 8, 9, 10, 3, 11, 12, 1, 0, 13, 14)))
    assert yt_perm_avoids_32(Perm((13, 9, 8, 0, 5, 1, 3, 4, 2, 6, 7, 10, 11, 12, 14)))
    assert yt_perm_avoids_32(Perm((14, 10, 13, 12, 8, 7, 11, 5, 9, 6, 3, 4, 1, 0, 2)))
    assert yt_perm_avoids_32(Perm((13, 0, 1, 10, 8, 7, 9, 11, 6, 5, 4, 12, 3, 14, 2)))
    assert yt_perm_avoids_32(Perm((0, 14, 1, 3, 12, 4, 5, 6, 10, 11, 9, 8, 7, 13, 2)))
    assert yt_perm_avoids_32(Perm((12, 9, 14, 13, 11, 6, 10, 8, 5, 2, 1, 7, 4, 0, 3)))
    assert yt_perm_avoids_32(Perm((7, 14, 13, 6, 4, 12, 11, 3, 10, 9, 8, 1, 0, 5, 2)))


def test_av_231_and_mesh():
    assert av_231_and_mesh(Perm(()))
    assert av_231_and_mesh(Perm((0,)))
    assert av_231_and_mesh(Perm((0, 1)))
    assert av_231_and_mesh(Perm((1, 0)))
    assert av_231_and_mesh(Perm((0, 1, 2)))
    assert av_231_and_mesh(Perm((0, 2, 1)))
    assert av_231_and_mesh(Perm((1, 0, 2)))
    assert not av_231_and_mesh(Perm((1, 2, 0)))
    assert av_231_and_mesh(Perm((2, 0, 1)))
    assert av_231_and_mesh(Perm((2, 1, 0)))
    assert av_231_and_mesh(Perm((0, 1, 2, 3)))
    assert av_231_and_mesh(Perm((0, 1, 3, 2)))
    assert av_231_and_mesh(Perm((0, 5, 4, 3, 2, 1)))
    assert av_231_and_mesh(Perm((5, 2, 1, 0, 4, 3)))
    assert not av_231_and_mesh(Perm((3, 4, 6, 2, 5, 0, 1)))
    assert not av_231_and_mesh(Perm((5, 0, 1, 6, 3, 4, 2)))
    assert not av_231_and_mesh(Perm((2, 5, 0, 7, 3, 4, 6, 1)))
    assert not av_231_and_mesh(Perm((5, 7, 4, 8, 1, 6, 0, 2, 3)))
    assert not av_231_and_mesh(Perm((2, 5, 9, 1, 7, 3, 8, 0, 4, 6)))
    assert not av_231_and_mesh(Perm((5, 6, 0, 3, 2, 1, 10, 8, 7, 4, 9)))
    assert av_231_and_mesh(Perm((4, 1, 0, 3, 2, 5, 6)))
    assert not av_231_and_mesh(Perm((2, 6, 4, 0, 1, 7, 3, 5)))
    assert av_231_and_mesh(Perm((9, 8, 6, 5, 1, 0, 4, 3, 2, 7)))
    assert av_231_and_mesh(Perm((0, 3, 2, 1, 9, 8, 7, 6, 5, 4)))
    assert av_231_and_mesh(Perm((9, 1, 0, 2, 4, 3, 7, 5, 6, 8)))
    assert av_231_and_mesh(Perm((8, 5, 1, 0, 2, 4, 3, 7, 6, 9)))
    assert av_231_and_mesh(Perm((9, 1, 0, 8, 2, 5, 4, 3, 6, 7)))
    assert av_231_and_mesh(Perm((9, 8, 7, 4, 0, 3, 1, 2, 5, 6)))
    assert av_231_and_mesh(Perm((6, 1, 0, 2, 5, 3, 4, 9, 7, 8)))
    assert av_231_and_mesh(Perm((8, 6, 0, 5, 3, 2, 1, 4, 7, 9)))
    assert av_231_and_mesh(Perm((0, 1, 3, 2, 4, 6, 5, 9, 8, 7)))
    assert 417 == sum(1 for p in Perm.of_length(7) if av_231_and_mesh(p))


def test_hard_mesh():
    assert hard_mesh(Perm(()))
    assert hard_mesh(Perm((0,)))
    assert hard_mesh(Perm((0, 1)))
    assert hard_mesh(Perm((1, 0)))
    assert not hard_mesh(Perm((0, 1, 2)))
    assert hard_mesh(Perm((0, 2, 1)))
    assert hard_mesh(Perm((1, 0, 2)))
    assert hard_mesh(Perm((1, 2, 0)))
    assert hard_mesh(Perm((2, 0, 1)))
    assert hard_mesh(Perm((2, 1, 0)))
    assert not hard_mesh(Perm((0, 1, 2, 3)))
    assert not hard_mesh(Perm((0, 1, 3, 2)))
    assert not hard_mesh(Perm((1, 5, 0, 2, 3, 4)))
    assert not hard_mesh(Perm((2, 4, 1, 5, 0, 3)))
    assert hard_mesh(Perm((1, 3, 2, 5, 4, 6, 0)))
    assert not hard_mesh(Perm((4, 3, 1, 6, 2, 0, 5)))
    assert not hard_mesh(Perm((3, 4, 1, 5, 2, 6, 0, 7)))
    assert not hard_mesh(Perm((4, 3, 2, 0, 1, 5, 7, 6, 8)))
    assert not hard_mesh(Perm((7, 0, 5, 4, 6, 3, 2, 9, 1, 8)))
    assert not hard_mesh(Perm((2, 6, 9, 1, 8, 0, 10, 5, 7, 3, 4)))
    assert 692 == sum(1 for p in Perm.of_length(7) if hard_mesh(p))
