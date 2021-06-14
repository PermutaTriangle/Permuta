from itertools import islice
from typing import List

from permuta.patterns.meshpatt import MeshPatt
from permuta.patterns.perm import Perm
from permuta.permutils.groups import dihedral_group

_SMOOTH_PATT = (Perm((0, 2, 1, 3)), Perm((1, 0, 3, 2)))


def smooth(perm: Perm) -> bool:
    """Returns true if the perm is smooth, i.e. 0213- and 1032-avoiding."""
    return perm.avoids(*_SMOOTH_PATT)


_FOREST_LIKE_PATT = (Perm((0, 2, 1, 3)), MeshPatt(Perm((1, 0, 3, 2)), [(2, 2)]))


def forest_like(perm: Perm) -> bool:
    """Returns true if the perm is forest like."""
    return perm.avoids(*_FOREST_LIKE_PATT)


_BAXTER_PATT = (
    MeshPatt(Perm((1, 3, 0, 2)), [(2, 2)]),
    MeshPatt(Perm((2, 0, 3, 1)), [(2, 2)]),
)


def baxter(perm: Perm) -> bool:
    """Returns true if the perm is a baxter permutation."""
    return perm.avoids(*_BAXTER_PATT)


_SIMSUN_PATT = MeshPatt(Perm((2, 1, 0)), [(1, 0), (1, 1), (2, 2)])


def simsun(perm: Perm) -> bool:
    """Returns true if the perm is a simsun permutation."""
    return perm.avoids(*_SIMSUN_PATT)


def dihedral(perm: Perm) -> bool:
    """Does perm belong to a dihedral group? We use the convention that D1 and D2 are
    not subgrroups of S1 and S2, respectively."""
    return any(perm == d_perm for d_perm in dihedral_group(len(perm)))


def in_alternating_group(perm: Perm) -> bool:
    """Does perm belong to alternating group? We use the convention that D1 and D2 are
    not subgrroups of S1 and S2, respectively."""
    n = len(perm)
    if n == 0:
        return True
    if n < 3:
        return n % 2 == 1
    return perm.count_inversions() % 2 == 0


def _perm_to_yt(perm: Perm) -> List[List[int]]:
    # transform perm to standard young table

    def insert_in_row(i, k):
        cur_row = res[i]
        found = next(((ind, cur) for ind, cur in enumerate(cur_row) if cur > k), None)
        if not found:
            cur_row.append(k)
        else:
            ind, cur = found
            cur_row[ind] = k
            if len(res) <= i + 1:
                res.append([cur])
            else:
                insert_in_row(i + 1, cur)

    res: List[List[int]] = [[perm[0]]] if perm else []
    for val in islice(perm, 1, None):
        insert_in_row(0, val)
    return res


def _tableau_contains_shape(tab: List[List[int]], shape: List[int]) -> bool:
    #  Return True if the tableaux tab contains the shape
    return len(tab) >= len(shape) and all(s <= t for s, t in zip(shape, map(len, tab)))


def yt_perm_avoids_22(perm: Perm) -> bool:
    """Returns true if perm's standard young table avoids shape [2,2]."""
    return not _tableau_contains_shape(_perm_to_yt(perm), [2, 2])


def yt_perm_avoids_32(perm: Perm) -> bool:
    """Returns true if perm's standard young table avoids shape [3,2]."""
    return not _tableau_contains_shape(_perm_to_yt(perm), [3, 2])


_AV_231_AND_MESH_PATT = (
    Perm((1, 2, 0)),
    MeshPatt(Perm((0, 1, 5, 2, 3, 4)), [(1, 6), (4, 5), (4, 6)]),
)


def av_231_and_mesh(perm: Perm) -> bool:
    """Check if perm avoids MeshPatt(Perm((0, 1, 5, 2, 3, 4)), [(1, 6), (4, 5), (4, 6)])
    and the classial pattern 231.
    """
    return perm.avoids(*_AV_231_AND_MESH_PATT)


_HARD_MESH_PATT = (
    MeshPatt(Perm((0, 1, 2)), [(0, 0), (1, 1), (2, 2), (3, 3)]),
    MeshPatt(Perm((0, 1, 2)), [(0, 3), (1, 2), (2, 1), (3, 0)]),
)


def hard_mesh(perm: Perm) -> bool:
    """Check if perm avoids MeshPatt(Perm((0, 1, 2)), [(0, 0), (1, 1), (2, 2), (3, 3)])
    and MeshPatt(Perm((0, 1, 2)), [(0, 3), (1, 2), (2, 1), (3, 0)])."""
    return perm.avoids(*_HARD_MESH_PATT)
