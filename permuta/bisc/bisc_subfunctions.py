from itertools import chain
from math import factorial

from permuta.patterns.meshpatt import MeshPatt
from permuta.patterns.perm import Perm


def mine(goodperms, M, N=None, report=False):
    """
    goodperms the set of permutations you are investigating
    M longest mesh patterns you want to consider
    N longest permutations from goodperms you want to consider
    report
    """

    goodpatts = dict()

    if N is None:
        N = max(goodperms.keys())

    interval = range(M + 1)

    if report:
        # minint = min(interval) # WTF This is always 1
        # maxint = max(interval) # WTF This is always M
        if 0 < M:
            print(
                "Starting search for allowed patterns of lengths {}, ..., {}".format(
                    0, M
                )
            )
        elif 0 == M:
            print("Starting search for allowed patterns of length {}".format(0))
        else:
            print("Wat")
            return [], dict()

    # INITIALIZING THE DICTIONARY goodpatts
    check_interval = []
    for j in interval:

        goodpatts[j] = dict()

        if len(goodperms[j]) == factorial(j):
            for perm in goodperms[j]:
                goodpatts[j][Perm(perm)] = [set([])]
        else:
            for perm in goodperms[j]:
                goodpatts[j][Perm(perm)] = [set([])]
            check_interval.append(j)

    if not check_interval:
        print("You need to search for longer patterns")
        return [], dict()

    minci = min(check_interval)
    maxci = max(check_interval)

    if report:
        if minci < maxci:
            print(
                "Only need to consider patterns of lengths {}, ..., {}".format(
                    minci, maxci
                )
            )
        else:
            print("Only need to consider patterns of length {}".format(minci))
        print("")

    def add_good_shadings_to_goodpatts(perm, shading, loc, min_len, max_patt_len):

        L = len(perm)

        # If there are too few elements in the perm left to complete a pattern of
        # length Jmin we stop.
        if L > min_len and loc <= max_patt_len:
            go_deeper = False
            if L > min_len + 1:
                go_deeper = True

            for i in range(loc, min(max_patt_len + 1, L)):

                newPerm = []
                for j in chain(range(i), range(i + 1, L)):
                    if perm[j] > perm[i]:
                        newPerm.append(perm[j] - 1)
                    else:
                        newPerm.append(perm[j])
                nL = len(newPerm)
                newPerm = Perm(newPerm)

                newShading = [
                    (sh[0] - (sh[0] > i), sh[1] - (sh[1] > perm[i])) for sh in shading
                ]
                newShading.append((i, perm[i]))
                newShading = set(newShading)

                if nL <= max_patt_len:

                    if newPerm in goodpatts[nL]:

                        if not any(
                            U.issubset(newShading) for U in goodpatts[nL][newPerm]
                        ):
                            goodpatts[nL][newPerm].append(newShading)

                    else:
                        goodpatts[nL][newPerm] = [newShading]

                if go_deeper:
                    add_good_shadings_to_goodpatts(
                        newPerm, newShading, i, min_len, max_patt_len
                    )

    """
    -----------------------------------------------------------------------------------
    """

    if report:
        print("Now looking at permutations of length")
        print("")

    for i in range(1, N + 1):

        if report:
            print("         {}".format(i))

        min_maxci_i = min(maxci, i)

        for perm in goodperms[i]:

            add_good_shadings_to_goodpatts(perm, set([]), 0, minci, min_maxci_i)

    if report:
        print("")
        print("Done")
        print("")

        for j in check_interval:
            print(
                "The number of allowed patterns of length {} is {}".format(
                    j, sum(len(goodpatts[j][perm]) for perm in goodpatts[j].keys())
                )
            )

        print("")
        print("Getting rid of the unnecessary allowed patterns")
        print("")

    for j in check_interval:
        for perm in goodpatts[j].keys():

            for R in goodpatts[j][perm]:
                listwoR = list(goodpatts[j][perm])
                listwoR.remove(R)

                if any(S.issubset(R) for S in listwoR):
                    goodpatts[j][perm] = listwoR

    if report:
        for j in check_interval:
            print(
                "The number of allowed patterns of length {} is now {}".format(
                    j, sum(len(goodpatts[j][perm]) for perm in goodpatts[j].keys())
                )
            )
        print("")

    """
    Now the first step is done: We have the maximum allowed shadings for
    any potentially bad classical pattern.
    """

    return check_interval, goodpatts


def forb(check_interval, goodpatts, M, report=False):

    badpatts = {}
    outpatts = {}

    def rec_w_reduce_pattern_pos(C, forb, lst, perm, pattern_positions, check_interval):

        # pruning lst
        newlst = []
        for L in lst:
            if L.issubset(
                forb
            ):  # If a member of lst is in forb then it is impossible to satisfy it
                return []
            if not C.intersection(
                L
            ):  # Here we find the members of lst that have not yet been satisfied
                newlst.append(L)

        if newlst:
            lst0 = newlst[0]  # Now we aim for satisfying the first member of lst, lst0
            # i = 0 # Here we find the first box in lst0 that we are allowed to fill
            # in (i.e., put in C)
            # while lst0[i] in forb:
            #     i = i+1
            # 2020
            for b in lst0:
                B = b
                if B not in forb:
                    break

            """
            This was added in September 2012.
            We now check if the addition of the box lst0[i] (B) makes this entire
            branch in the recursion redundant.
            """
            D = C.union(set([B]))
            for j in check_interval:
                if j == len(perm):
                    break
                for cl_patt in badpatts[j]:
                    if mesh_contains_cl_patt_many_shadings_with_positions(
                        perm, D, pattern_positions[cl_patt], badpatts[j][cl_patt]
                    ):
                        return rec_w_reduce_pattern_pos(
                            C,
                            forb.union(set([B])),
                            newlst,
                            perm,
                            pattern_positions,
                            check_interval,
                        )
            return rec_w_reduce_pattern_pos(
                D, forb, newlst, perm, pattern_positions, check_interval
            ) + rec_w_reduce_pattern_pos(
                C, forb.union(set([B])), newlst, perm, pattern_positions, check_interval
            )
        else:
            return [C]

    def find_badpatts(perm):

        n = len(perm)

        pattern_positions = {}
        for j in check_interval:
            if j == len(perm):
                break
            for cl_patt in badpatts[
                j
            ]:  # TODO 2020 This is a very stupid way of doing this.
                # Better to check the subsequences once in perm
                pattern_positions[cl_patt] = list(cl_patt.occurrences_in(perm))

        if perm in goodpatts[n]:

            R = sorted(
                rec_w_reduce_pattern_pos(
                    set([]),
                    set([]),
                    goodpatts[n][perm],
                    perm,
                    pattern_positions,
                    check_interval,
                ),
                key=lambda x: len(x),
                reverse=True,
            )
            newR = []

            for j, r in enumerate(R):
                if not any(map(lambda s: s.issubset(r), R[j + 1 :])):
                    newR.append(r)
            return newR

        else:

            for j in check_interval:
                if j == len(perm):
                    break
                for cl_patt in badpatts[j]:
                    if mesh_contains_cl_patt_many_shadings(
                        perm, [], cl_patt, badpatts[j][cl_patt]
                    ):
                        return []

            return [set([])]

    # finding the forbidden patterns
    for j in check_interval:

        if j > M:
            break

        if report:
            print("Starting search for forbidden patterns of length {}".format(j))

        badpatts[j] = {}
        for perm in Perm.of_length(j):
            badpatts[j][perm] = find_badpatts(perm)

        if report:
            print(
                "The number of bad patterns of length {} is {}".format(
                    j, sum(len(badpatts[j][perm]) for perm in badpatts[j].keys())
                )
            )

    # finding the minimal forbidden patterns
    if report:
        print("")
        print("Starting search for minimal forbidden patterns")
        print("")

    for j in check_interval:

        if j > M:
            break

        outpatts[j] = dict()
        for cl_patt in badpatts[j]:
            if badpatts[j][cl_patt]:
                outpatts[j][cl_patt] = badpatts[j][cl_patt]

    return outpatts


# This is the analouge of mesh_has_mesh_many_shadings
def mesh_contains_cl_patt_many_shadings(perm, S, patt, Rs):
    for candidate_indices in patt.occurrences_in(perm):
        candidate = [perm[index] for index in candidate_indices]
        hit_boxes = []
        x = 0
        for element in perm:
            if element in candidate:
                x += 1
                continue
            y = sum(1 for candidate_elt in candidate if candidate_elt < element)
            hit_boxes.append((x, y))
        shit_boxes = set(hit_boxes)

        for R in Rs:
            if shit_boxes.intersection(R) == set([]):
                candidate_sub_mesh_patt = MeshPatt(perm, S).sub_mesh_pattern(
                    candidate_indices
                )
                if set(R) <= set(candidate_sub_mesh_patt.shading):
                    return True
    return False


def mesh_contains_cl_patt_many_shadings_with_positions(perm, S, candidates_indices, Rs):
    for candidate_indices in candidates_indices:
        candidate = [perm[index] for index in candidate_indices]
        hit_boxes = []
        x = 0
        for element in perm:
            if element in candidate:
                x += 1
                continue
            y = sum(1 for candidate_elt in candidate if candidate_elt < element)
            hit_boxes.append((x, y))
        shit_boxes = set(hit_boxes)

        for R in Rs:
            if shit_boxes.intersection(R) == set([]):
                candidate_sub_mesh_patt = MeshPatt(perm, S).sub_mesh_pattern(
                    candidate_indices
                )
                if set(R) <= set(candidate_sub_mesh_patt.shading):
                    return True
    return False


def perm_contains_cl_patt_many_shadings(perm, patt, Rs):

    for candidate_indices in patt.occurrences_in(perm):
        candidate = [perm[index] for index in candidate_indices]
        hit_boxes = []
        x = 0
        for element in perm:
            if element in candidate:
                x += 1
                continue
            y = sum(1 for candidate_elt in candidate if candidate_elt < element)
            hit_boxes.append((x, y))
        shit_boxes = set(hit_boxes)
        if any(shit_boxes.intersection(R) == set([]) for R in Rs):
            return True
    return False


def perm_contains_cl_patts_many_shadings(perm, patts_w_shadings):
    """
    Returns True if any pattern from pats occurs in perm, otherwise returns False
    """
    for n in patts_w_shadings.keys():
        for pat in patts_w_shadings[n].keys():
            if perm_contains_cl_patt_many_shadings(perm, pat, patts_w_shadings[n][pat]):
                return True
    return False


def show_me(SG, more=True):
    """
    To get info on the output do

    show_me(SG)
    """
    describe_bisc_output(SG)

    if more:
        print("\nNow displaying the patterns\n")
        dfo = display_forb_output(SG)
        for mpat in dfo:
            print(MeshPatt(*mpat).ascii_plot())
            print("")


def describe_bisc_output(OP):

    mult = 1
    flip = True

    for k in OP.keys():
        clpatts_of_this_length = OP[k].keys()
        print(
            "There are "
            + str(len(clpatts_of_this_length))
            + " underlying classical patterns of length "
            + str(k)
        )
        for clpatt in clpatts_of_this_length:

            new_factor = len(OP[k][clpatt])
            mult = mult * new_factor

            print(
                "There are " + str(new_factor) + " different shadings on " + str(clpatt)
            )

        if flip:
            print(
                "The number of sets to monitor at the start of the clean-up phase is "
                + str(mult)
            )
        flip = False


def display_forb_output(patts_w_shadings_dict):
    """
    Input is the output of forb, i.e., a dictionary
    whose keys are lengths of pattern. Each length
    points to a dictionary of classical patterns of that
    length. The values of those dictionaries are the
    shadings of those patterns.

    The output is a list of mesh patterns that
    we can plot nicely
    """
    res = []
    for d in patts_w_shadings_dict.values():
        for patt, shadings in d.items():
            for s in shadings:
                res.append((patt, s))
    return res


def patterns_suffice_for_good(SG, L, A, stop_on_failure=False):
    print("Starting sanity check with good perms")
    for n in range(L + 1):

        if n not in A.keys():
            print("There are no good perms of length {} to check".format(n))
            return False, []

        print("Now checking permutations of length " + str(n))

        containing_perms_in_A = []
        for a in A[n]:

            if perm_contains_cl_patts_many_shadings(a, SG):
                if stop_on_failure:
                    print(
                        "!!!! The permutation " + str(a) + " contains the patterns !!!!"
                    )
                    return False, [a]
                else:
                    containing_perms_in_A.append(a)

        if A[n] and containing_perms_in_A:
            print(
                "!!!! There are permutations of length "
                + str(n)
                + " that contain the patterns !!!!"
            )
            return False, containing_perms_in_A
    print("Sanity check passes for the good perms")
    return True, []


def patterns_suffice_for_bad(SG, L, B, stop_on_failure=False):
    print("Starting sanity check with bad perms")
    for n in range(L + 1):

        if n not in B.keys():
            print("There are no bad perms of length {} to check".format(n))
            return False, []

        print("Now checking permutations of length " + str(n))

        avoiding_perms_in_B = []
        for b in B[n]:

            if not perm_contains_cl_patts_many_shadings(b, SG):
                if stop_on_failure:
                    print(
                        "!!!! The permutation " + str(b) + " avoids the patterns !!!!"
                    )
                    return False, [b]
                else:
                    avoiding_perms_in_B.append(b)

        if B[n] and avoiding_perms_in_B:
            print(
                "!!!! There are permutations of length "
                + str(n)
                + " that avoid the patterns !!!!"
            )
            return False, avoiding_perms_in_B

    print("Sanity check passes for the bad perms")
    return True, []


def run_clean_up(
    SG, B, bm=None, M=None, limit_monitors=0, report=False, detailed_report=False
):

    if M is None:
        M = max(k for k in SG.keys() if SG[k] != {})

    if bm is None:
        bm = max(B.keys())

    bases, dict_numbs_to_patts = clean_up(
        SG,
        B,
        min(SG.keys()) + 1,
        bm,
        min(SG.keys()),
        M,
        report,
        detailed_report,
        limit_monitors,
    )

    print("\nThe bases found have lengths")
    print(list(map(lambda x: len(x), bases)))

    return bases, dict_numbs_to_patts


def one_for_each(values):

    LV = len(values)

    if LV == 0:
        return []

    if LV == 1:
        return map(lambda x: [x], values[0])
    return sum(
        [list(map(lambda x: x + [v], one_for_each(values[1:]))) for v in values[0]], []
    )


def gaur(r, s):
    return all(map(lambda x: x in s, r))


def clean_up(
    SG,
    B,
    perm_len_min,
    perm_len_max,
    patt_len_min,
    patt_len_max,
    report=False,
    detailed_report=False,
    limit_monitors=0,
):

    """
    Note that if limit_monitors > 0 then
    we do not remove redundant monitors (last step)
    """
    # Dictionaries to go between mesh patterns
    # and numbers (length, pattern number, shading number)
    dict_clpatts_to_numbs = dict()
    dict_numbs_to_patts = dict()

    SG_keys = SG.keys()

    # A dictionary that "looks" like SG, but has only numbers
    sg = dict()

    # Putting values in the three dictionaries
    for k in SG_keys:

        sg[k] = dict()

        patt_i = 0

        for clpatt in sorted(SG[k]):

            sh_i = 0
            for sh in sorted(SG[k][clpatt]):
                dict_clpatts_to_numbs[clpatt] = patt_i
                dict_numbs_to_patts[(k, patt_i, sh_i)] = (clpatt, sh)
                sh_i = sh_i + 1

            sg[k][patt_i] = range(0, sh_i)

            patt_i = patt_i + 1

    # initialize len_calc_patts as the length of the smallest mesh patterns
    len_calc_patts = list(
        filter(lambda x: x in SG.keys(), range(patt_len_min, patt_len_max + 1))
    )  # [SG_keys[0]]

    if limit_monitors:
        if limit_monitors < len(SG[patt_len_min].keys()):
            print("You need to allow larger bases")
            return [], dict_numbs_to_patts

    # initialize monitor by taking one mesh pattern for
    # every bad permutation on the first level
    if report:
        print("Creating the sets to monitor")
        print()
    monitor = list(
        one_for_each(
            [
                [(len_calc_patts[0], x, y) for y in sg[len_calc_patts[0]][x]]
                for x in sg[len_calc_patts[0]]
            ]
        )
    )

    if report:
        print("There are " + str(len(monitor)) + " potential bases to monitor")
        print("Starting the tests")
    if detailed_report:
        print("The monitors are")
        for i, m in enumerate(monitor):
            print("Monitor {}".format(i))
            for patt_id in m:
                mpatt = dict_numbs_to_patts[patt_id]
                print(MeshPatt(mpatt[0], mpatt[1]).ascii_plot())
                print()
            print("-----------")
    # perm_len_min should be 1+len_calc_patts[0]
    for L in range(perm_len_min, perm_len_max + 1):

        # Restricting to the pattern lengths that are smaller than the length of
        # the permutations we are looking at
        appropriate_len_calc_patts = list(
            filter(lambda x: x < L, len_calc_patts)
        )  # TODO Should this be <= in 2020?

        # When we try to expand with larger patterns below we need to now if L is
        # available as a length of forbidden patterns
        L_is_a_key = False
        if L in SG.keys():
            L_is_a_key = True

        if report:
            print("----------------------------------------------------------------")
            print()
            print("Testing permutations of length " + str(L))
            print()

        for perm in B[L]:

            if not monitor:
                print("No sets to monitor, try allowing longer patterns")
                if limit_monitors:
                    print("or larger bases")
                return [], dict_numbs_to_patts

            if detailed_report:
                print("-----------------------------------")
                print("Testing the permutation " + str(perm))

            dict_numbs_to_perm_avoids_patt = dict()
            saviors = []

            for ell in appropriate_len_calc_patts:
                for patt_i in sg[ell].keys():
                    for sh_i in sg[ell][patt_i]:

                        mpat = dict_numbs_to_patts[(ell, patt_i, sh_i)]

                        # Checking whether perm avoids mpat
                        if perm.avoids(MeshPatt(mpat[0], mpat[1])):
                            dict_numbs_to_perm_avoids_patt[(ell, patt_i, sh_i)] = True
                        else:
                            dict_numbs_to_perm_avoids_patt[(ell, patt_i, sh_i)] = False
                            saviors.append((ell, patt_i, sh_i))

            if detailed_report:
                print(
                    "When monitors fail below they will extended with "
                    + str(len(saviors))
                    + " saviors"
                )
                print("They are " + str(saviors))

            # If L is available as a length of forbidden patterns (checked above) we
            # need to know if perm is one of the underlying classical patterns of that
            # length
            perm_is_a_key = False
            if L_is_a_key and perm in SG[L].keys():
                perm_is_a_key = True
                # Getting the number of this perm
                n_perm = dict_clpatts_to_numbs[perm]
                larger_patts = list(sg[L][n_perm])

                if detailed_report:
                    print(
                        "When monitors fail below they will extended with "
                        + str(len(larger_patts))
                        + " larger patterns"
                    )
                    print("They are " + str(larger_patts))

            h = -1
            capture_failure = False
            loop_monitor = list(monitor)

            for mon in loop_monitor:
                h = h + 1
                if all(
                    dict_numbs_to_perm_avoids_patt[m]
                    for m in filter(
                        lambda x: x[0] < L, mon
                    )  # TODO Should this be <= in 2020
                ):
                    capture_failure = True
                    if detailed_report:
                        print("Monitor nr. " + str(h) + " failed")
                        print("This monitor consists of:")
                        for m in mon:
                            print(m)
                    monitor.remove(mon)

                    if limit_monitors:
                        if len(mon) >= limit_monitors:
                            if detailed_report:
                                print(
                                    """Unable to extend this monitor because
                                    its size has reached the limit"""
                                )
                            continue

                    if saviors:

                        monitor.extend(map(lambda x: mon + [x], saviors))

                    if perm_is_a_key:

                        monitor.extend(
                            map(lambda x: mon + [(L, n_perm, x)], larger_patts)
                        )
            if detailed_report:
                print("Number of monitors " + str(len(list(monitor))))
            if capture_failure:
                lm = len(monitor)
                if report:
                    print()
                    print("There are " + str(lm) + " monitors left")
                if not monitor:
                    return [], dict_numbs_to_patts
                if report:
                    print("Sorting the monitors")

                R = sorted(monitor, key=len)

                if report:
                    print()
                    print("Removing redundant monitors")

                newR = []
                v = 0
                while v < lm:
                    r = R[0]
                    newR.append(r)
                    v = v + len(R)
                    R = list(filter(lambda s: not gaur(r, s), R[1:]))
                    v = v - len(R)

                if report:
                    print()
                    print("There are now " + str(len(newR)) + " monitors")
                monitor = newR

    return [sorted(m) for m in monitor], dict_numbs_to_patts


def show_me_basis(b, dict_numbs_to_patts):
    """
    To see the patterns in a basis b

    show_me_basis(b, dict_numbs_to_patts)
    """

    print("\nDisplaying the patterns in the basis\n")
    # dfo = display_forb_output(SG)
    for i in b:
        mpatt = dict_numbs_to_patts[i]
        print(MeshPatt(mpatt[0], mpatt[1]).ascii_plot())
        print()


def to_sg_format(basis, dict_numbs_to_patts):
    sg = {}
    for ind in basis:
        length = ind[0]
        if length not in sg:
            sg[length] = {}
        data = dict_numbs_to_patts[ind]
        cl_patt = data[0]
        sh = data[1]
        if cl_patt not in sg[length]:
            sg[length][cl_patt] = [sh]
        else:
            sg[length][cl_patt].append(sh)
    return sg


# TODO Compare this with the subfunction inside mine
def maximal_mesh_pattern_of_occurrence(perm, occ):
    """Return the maximal shading M of the classical pattern std(occ) so
    that the given occurrence is an occurrence of the mesh pattern
    (std(occ), M).
    """

    k = len(occ)

    con = set(perm[i] for i in occ)
    colcnt = 0
    col = [-1] * len(perm)
    for v in perm:
        if v in con:
            colcnt += 1
        else:
            col[v] = colcnt
    rowcnt = 0
    row = [-1] * len(perm)
    for v in range(len(perm)):
        if v in con:
            rowcnt += 1
        else:
            row[v] = rowcnt
    # bad is the set of boxes that contain points and can not be shaded
    bad = set((u, v) for u, v in zip(col, row) if u != -1)
    # cur is the set of boxes that can be shaded
    cur = set((u, v) for u in range(k + 1) for v in range(k + 1) if (u, v) not in bad)
    return cur
