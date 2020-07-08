from permuta.meshpatt import MeshPatt
from permuta.perm import Perm
from permuta.permutils.groups import dihedral_group


def is_sorted(w):
    """
    Return true if w is increasing, i.e., sorted

    EXAMPLES
    sage: is_sorted([1,3,2])
    False
    """

    n = len(w)

    if n <= 1:
        return True

    for i in range(n - 1):
        if w[i] > w[i + 1]:
            return False

    return True


#
# helper function for stack-sort and bubble-sort.
# finds the location of the maximal element
#


def loc_max(w):

    L = max(w)

    for i in range(L + 1):
        if w[i] == L:
            return i


#
# function takes a permutation w and does one pass of stack-sort on it
#


def stack_sort(w):

    i = len(w)

    if i == 0:
        return []

    if i == 1:
        return w
    else:
        [j, J] = [loc_max(w), max(w)]

        if j == 0:
            W2 = list(stack_sort(w[1:i]))
            W2.append(J)

            return W2

        if j == i - 1:
            W1 = list(stack_sort(w[0 : i - 1]))
            W1.append(J)

            return W1

        else:
            W1 = list(stack_sort(w[0:j]))
            W2 = list(stack_sort(w[j + 1 : i]))

            W1.extend(W2)
            W1.extend([J])

            return W1


#
# function takes a permutation w and does one pass of bubble-sort on it
#


def bubble_sort(w):

    i = len(w)

    if i == 0:
        return []

    if i == 1:
        return w
    else:
        [j, J] = [loc_max(w), max(w)]

        if j == 0:
            W2 = w[1:i]
            W2.append(J)

            return W2

        if j == i - 1:
            W1 = list(bubble_sort(w[0 : i - 1]))
            W1.append(J)

            return W1

        else:
            W1 = list(bubble_sort(w[0:j]))
            W2 = w[j + 1 : i]

            W1.extend(W2)
            W1.extend([J])

            return W1


def quick_sort_sub(perm):

    L = len(perm)

    if L == 0:
        return []

    sfps = list(Perm(perm).strong_fixed_points())
    if sfps:
        maxind = sfps[-1]
        return (
            quick_sort_sub([perm[i] for i in range(maxind)])
            + [perm[maxind]]
            + quick_sort_sub([perm[i] for i in range(maxind + 1, L)])
        )
    else:
        firstval = perm[0]
        smaller = filter(lambda x: x < firstval, perm)
        bigger = filter(lambda x: x > firstval, perm)
        return list(smaller) + [firstval] + list(bigger)


def quick_sort(perm):

    L = len(perm)

    if L == 0:
        return perm

    return Perm(quick_sort_sub(perm))


def BKV_sort(perm, B=[]):
    inp = list(perm)
    stackR = []  # the right stack read from top to bottom
    stackL = []  # the left stack read from top to bottom
    out = []
    while len(out) < len(perm):
        if inp and Perm.to_standard(stackR + [inp[0]]).reverse().avoids(*B):
            stackR.append(inp.pop(0))
        elif stackR and (
            Perm.to_standard(stackL + [stackR[-1]]).reverse().avoids(Perm((1, 0)))
        ):
            stackL.append(stackR.pop())
        elif stackL:
            out.append(stackL.pop())
        else:
            print("wtf")
            print(out, stackL, stackR, inp)
            assert False
    return Perm(out)


def stack_sortable(perm):
    return is_sorted(stack_sort(perm))


def quick_sortable(perm):
    return is_sorted(quick_sort(perm))


def BKV_sortable(perm, B=[]):
    return is_sorted(BKV_sort(perm, B))


def West_2_stack_sortable(perm):
    return is_sorted(stack_sort(stack_sort(perm)))


def West_3_stack_sortable(perm):
    return is_sorted(stack_sort(stack_sort(stack_sort(perm))))


def smooth(perm):
    return perm.avoids(Perm((0, 2, 1, 3)), Perm((1, 0, 3, 2)))


def forest_like(perm):
    return perm.avoids(Perm((0, 2, 1, 3)), MeshPatt(Perm((1, 0, 3, 2)), [(2, 2)]))


def Baxter(perm):
    return perm.avoids(
        MeshPatt(Perm((1, 3, 0, 2)), [(2, 2)]), MeshPatt(Perm((2, 0, 3, 1)), [(2, 2)])
    )


def SimSun(perm):
    return perm.avoids(MeshPatt(Perm((2, 1, 0)), [(1, 0), (1, 1), (2, 2)]))


def dihedral(perm):
    """
    We use the convention that D1 and D2 are not subgrroups of S1 and S2,
    respectively."""
    return any(perm == d_perm for d_perm in dihedral_group(len(perm)))


def in_alternating_group(perm):
    """
    We use the convention that D1 and D2 are not subgrroups of S1 and S2,
    respectively."""
    n = len(perm)
    if n == 0:
        return True
    if n < 3:
        return n % 2 == 1
    return perm.count_inversions() % 2 == 0


def perm_to_yt(perm):

    res = []

    def insert_in_row(i, k):
        if len(res) <= i:
            return res.append([k])

        cur_row = res[i]
        cur = cur_row[0]
        for ind, cur in enumerate(cur_row):
            if cur > k:
                cur_row[ind] = k
                return insert_in_row(i + 1, cur)
        else:
            cur_row.append(k)

    for k in perm:
        insert_in_row(0, k)

    return res


def tab_shape(tab):
    return list(map(len, tab))


def tableau_contains_shape(tab, sh):
    """
    Return True if the tableaux tab contains the shape sh
    """
    tab_sh = tab_shape(tab)

    lsh = len(sh)

    if len(tab_sh) < lsh:
        return False

    for i in range(lsh):
        if sh[i] > tab_sh[i]:
            return False

    return True


def yt_perm_avoids_22(perm):
    return not tableau_contains_shape(perm_to_yt(perm), [2, 2])


def yt_perm_avoids_32(perm):
    return not tableau_contains_shape(perm_to_yt(perm), [3, 2])


def av_231_and_mesh(perm):
    return perm.avoids(
        Perm((1, 2, 0)), MeshPatt(Perm((0, 1, 5, 2, 3, 4)), [(1, 6), (4, 5), (4, 6)])
    )


def hard_mesh(perm):
    return perm.avoids(
        MeshPatt(Perm((0, 1, 2)), [(0, 0), (1, 1), (2, 2), (3, 3)]),
        MeshPatt(Perm((0, 1, 2)), [(0, 3), (1, 2), (2, 1), (3, 0)]),
    )
