from collections import deque
from itertools import islice
from typing import Deque, List, Tuple

from permuta.patterns.meshpatt import MeshPatt
from permuta.patterns.patt import Patt
from permuta.patterns.perm import Perm
from permuta.permutils.groups import dihedral_group


def _is_sorted(lis: List[int]) -> bool:
    #  Return true if w is increasing, i.e., sorted.
    return all(elem == i for elem, i in zip(lis, range(len(lis))))


def _stack_sort(perm_slice: List[int]) -> List[int]:
    n = len(perm_slice)
    if n in (0, 1):
        return perm_slice
    max_i, max_v = max(enumerate(perm_slice), key=lambda pos_elem: pos_elem[1])
    # Recursively solve without largest
    if max_i == 0:
        n_lis = _stack_sort(perm_slice[1:n])
    elif max_i == n - 1:
        n_lis = _stack_sort(perm_slice[0 : n - 1])
    else:
        n_lis = _stack_sort(perm_slice[0:max_i])
        n_lis.extend(_stack_sort(perm_slice[max_i + 1 : n]))
    n_lis.append(max_v)
    return n_lis


def stack_sortable(perm: Perm) -> bool:
    """Returns true if perm is stack sortable."""
    return _is_sorted(_stack_sort(list(perm)))


def _bubble_sort(perm_slice: List[int]) -> List[int]:
    n = len(perm_slice)
    if n in (0, 1):
        return perm_slice
    max_i, max_v = max(enumerate(perm_slice), key=lambda pos_elem: pos_elem[1])
    # Recursively solve without largest
    if max_i == 0:
        n_lis = perm_slice[1:n]
    elif max_i == n - 1:
        n_lis = _bubble_sort(perm_slice[0 : n - 1])
    else:
        n_lis = _bubble_sort(perm_slice[0:max_i])
        n_lis.extend(perm_slice[max_i + 1 : n])
    n_lis.append(max_v)
    return n_lis


def bubble_sortable(perm: Perm) -> bool:
    """Returns true if perm is stack sortable."""
    return _is_sorted(_bubble_sort(list(perm)))


def _quick_sort(perm_slice: List[int]) -> List[int]:
    assert not perm_slice or set(perm_slice) == set(
        range(min(perm_slice), max(perm_slice) + 1)
    )
    n = len(perm_slice)
    if n == 0:
        return perm_slice
    maxind = -1
    # Note that perm does not need standardizing as sfp uses left to right maxima.
    for maxind in Perm(perm_slice).strong_fixed_points():
        pass
    if maxind != -1:
        lis: List[int] = (
            _quick_sort(perm_slice[:maxind])
            + [perm_slice[maxind]]
            + _quick_sort(perm_slice[maxind + 1 :])
        )
    else:
        firstval = perm_slice[0]
        lis = (
            list(filter(lambda x: x < firstval, perm_slice))
            + [perm_slice[0]]
            + list(filter(lambda x: x > firstval, perm_slice))
        )
    return lis


def quick_sortable(perm: Perm) -> bool:
    """Returns true if perm is quicksort sortable."""
    return _is_sorted(_quick_sort(list(perm)))


_BKV_PATT = Perm((1, 0))


def bkv_sortable(perm: Perm, patterns: Tuple[Patt, ...] = ()) -> bool:
    """Check if a permutation is BKV sortable.
    See:
        https://arxiv.org/pdf/1907.08142.pdf
        https://arxiv.org/pdf/2004.01812.pdf
    """
    # See
    n = len(perm)
    inp = deque(perm)
    # the right stack read from top to bottom
    # the left stack read from top to bottom
    right_stack: Deque[int] = deque([])
    left_stack: Deque[int] = deque([])
    expected = 0
    while expected < n:
        if inp:
            right_stack.appendleft(inp[0])
            if Perm.to_standard(right_stack).avoids(*patterns):
                inp.popleft()
                continue
            right_stack.popleft()

        if right_stack:
            left_stack.appendleft(right_stack[0])
            if Perm.to_standard(left_stack).avoids(_BKV_PATT):
                right_stack.popleft()
                continue
            left_stack.popleft()

        assert left_stack
        # Normally, we would gather elements from left stack but since we only care
        # about wether it sorts the permutation, we just compare it against expected.
        if expected != left_stack.popleft():
            return False
        expected += 1
    return True


def west_2_stack_sortable(perm: Perm) -> bool:
    """Returns true if perm can be sorted by two passes through a stack"""
    return _is_sorted(_stack_sort(_stack_sort(list(perm))))


def west_3_stack_sortable(perm: Perm) -> bool:
    """Returns true if perm can be sorted by three passes through a stack"""
    return _is_sorted(_stack_sort(_stack_sort(_stack_sort(list(perm)))))


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
