import json
import os
import types
from collections import defaultdict

from permuta.bisc.bisc_subfunctions import (
    forb,
    mine,
    patterns_suffice_for_bad,
    patterns_suffice_for_good,
    run_clean_up,
    show_me,
    show_me_basis,
    to_sg_format,
)
from permuta.patterns.perm import Perm


def bisc(A, m, n=None, report=False):

    if isinstance(A, list):
        D = defaultdict(list)
        for perm in A:
            D[len(perm)].append(perm)
    elif isinstance(A, types.FunctionType):
        if n is None:
            print("I will use permutations up to length 7")
            n = 7
        D = defaultdict(list)
        for i in range(n + 1):
            for perm in Perm.of_length(i):
                if A(perm):
                    D[i].append(perm)

    elif isinstance(A, dict):
        D = A

    else:
        print(
            """BiSC can accept inputs:
        1. A list of permutations
        2. A property of permutations
        3. A dictionary of lengths pointing to permutations"""
        )
        assert False

    if n is None:
        n = max(D.keys())

    ci, goodpatts = mine(D, m, n, report=report)
    SG = forb(ci, goodpatts, m, report=report)

    return SG


def auto_bisc(prop):

    L = 8  # Want to sanity check on at least S8, and one above n
    n = 4
    m = 2

    if isinstance(prop, list):
        # If a list is passed in then we put it in a dictionary at the start
        A = defaultdict(list)
        # We will put the complement up to S8 into another dictionary
        B = defaultdict(list)
        for perm in prop:
            A[len(perm)].append(perm)
        if L not in A.keys():
            print("You should have permutations up to length at least 8")
            return
        for i in range(L + 1):
            for perm in Perm.of_length(i):
                if perm not in A[i]:
                    B[i].append(perm)

    elif isinstance(prop, types.FunctionType):
        # If a property is passed in then we use it to populate both
        # both dictionaries up to S8
        A = defaultdict(list)
        B = defaultdict(list)
        for i in range(L + 1):
            A[i] = []
            B[i] = []
            for perm in Perm.of_length(i):
                if prop(perm):
                    A[i].append(perm)
                else:
                    B[i].append(perm)

    elif (
        isinstance(prop, tuple)
        and isinstance(prop[0], dict)
        and isinstance(prop[1], dict)
    ):
        # If you already have the dictionaries you can pass them in as a tuple
        A = prop[0]
        B = prop[1]
        if L not in A.keys():
            print("You should have permutations up to length at least 8")
            return

    elif isinstance(prop, str):
        # If you pass in a string we assume it is pointing to a file in permsets
        print("Attempting to read perms from permsets")
        good_entry = None
        bad_entry = None
        with os.scandir("../resources/bisc") as entries:
            for i, entry in enumerate(entries):
                en = entry.name[:-5]
                spl = en.split("_")
                if spl[0] == prop:
                    if (
                        good_entry is None
                        and spl[1] == "good"
                        and int(spl[2].split("len")[1]) >= L
                    ):
                        good_entry = en
                    if (
                        bad_entry is None
                        and spl[1] == "bad"
                        and int(spl[2].split("len")[1]) >= L
                    ):
                        bad_entry = en
                if good_entry is not None and bad_entry is not None:
                    break
        if good_entry is not None and bad_entry is not None:
            A = read_bisc_file("../resources/bisc/" + good_entry)
            B = read_bisc_file("../resources/bisc/" + bad_entry)
        else:
            print("The required files do not exist")
            return

    else:
        print(
            """BiSC can accept inputs:
        1. A list of permutations
        2. A property of permutations
        3. A dictionary of lengths pointing to permutations
        4. A string """
        )
        assert False

    while True:
        print("Learning patterns of length {} using perms of length {}".format(m, n))
        SG = bisc(A, m, n)
        show_me(SG, more=True)

        if SG != {}:
            print("Sanity checking the learned patterns up to length {}".format(L))
            val, avoiding_perms = patterns_suffice_for_bad(
                SG, L, B, stop_on_failure=True
            )
        else:
            val = False

        if val:
            print(
                "These patterns seem to suffice, I will now try to find a small basis"
            )

            ib = len(SG[min(SG.keys())].keys())
            while True:
                print("Trying to find a basis with at most {} patterns".format(ib))
                print("using perms of length {}".format(n))
                bases, dict_numbs_to_patts = run_clean_up(SG, B, n, limit_monitors=ib)

                if bases:
                    basis = bases[0]
                    show_me_basis(basis, dict_numbs_to_patts)

                    sg = to_sg_format(basis, dict_numbs_to_patts)

                    val, avoiding_perms = patterns_suffice_for_bad(
                        sg, L, B, stop_on_failure=True
                    )

                    if not val:
                        print("A bad basis was chosen.")
                        print("Increasing perm length to {}".format(n + 1))
                        n += 1
                        continue

                    val, containing_perms = patterns_suffice_for_good(
                        sg, L, A, stop_on_failure=True
                    )
                    if not val:
                        print("This is a bad basis. Need to learn from longer perms")
                        n += 1
                        break  # breaking out of the inner while-loop

                else:
                    print("No bases found. Increasing number of patterns in basis")
                    ib += 1
                    val = False

                if val:
                    print(
                        "!!! Found a basis with {} patts of length at most {}".format(
                            ib, m
                        )
                    )
                    print("!!! for the input using perms of length {}".format(n))
                    print("Basis: ", sg)
                    return sg

        else:
            print("Need to learn longer patterns")
            n += 1
            m += 1

        oldL = L
        if L < n + 1:
            L = n + 1
            if isinstance(prop, list) and L > max(A.keys):
                print("You need to input a longer list of permutations")
                return

            elif isinstance(prop, types.FunctionType):
                # Adding perms to the dictionaries
                for i in range(oldL + 1, L + 1):
                    print("Adding perms of length {}".format(i))
                    for perm in Perm.of_length(i):
                        if prop(perm):
                            A[i].append(perm)
                        else:
                            B[i].append(perm)

            elif isinstance(prop, tuple) and L > min(max(A.keys()), max(B.keys())):
                print("You need to add longer permutations to the dictionaries")
                return

            elif isinstance(prop, str) and L > min(max(A.keys()), max(B.keys())):
                # If you pass in a string we assume it is pointing to a file in permsets
                print("Attempting to read perms from permsets")
                good_entry = None
                bad_entry = None
                with os.scandir("../resources/bisc") as entries:
                    for i, entry in enumerate(entries):
                        en = entry.name[:-5]
                        spl = en.split("_")
                        if spl[0] == prop:
                            if (
                                good_entry is None
                                and spl[1] == "good"
                                and int(spl[2].split("len")[1]) >= L
                            ):
                                good_entry = en
                            if (
                                bad_entry is None
                                and spl[1] == "bad"
                                and int(spl[2].split("len")[1]) >= L
                            ):
                                bad_entry = en
                        if good_entry is not None and bad_entry is not None:
                            break
                if good_entry is not None and bad_entry is not None:
                    A = read_bisc_file("../resources/bisc/" + good_entry)
                    B = read_bisc_file("../resources/bisc/" + bad_entry)
                else:
                    print("The required files do not exist")
                    return


def create_bisc_input(N, prop):
    """
    Create a dictionary, D, containing keys 1, 2, 3, ..., N. Each key points to
    a list of permutations satisfying the property prop. The dictionary E has
    the same keys and they point to the complement.
    """

    A, B = {}, {}

    for n in range(N + 1):

        An, Bn = [], []

        for perm in Perm.of_length(n):
            if prop(perm):
                An.append(perm)
            else:
                Bn.append(perm)

        A[n], B[n] = An, Bn

    return A, B


def write_bisc_files(n: int, prop, info: str) -> None:
    """Create a dictionary, D, containing keys 1, 2, 3, ..., n. Each key points to
    a list of permutations satisfying the property prop. The dictionary E has
    the same keys and they point to the complement.
    """
    good, bad = create_bisc_input(n, prop)
    write_json_to_file(good, f"{info}_good_len{n}.json")
    write_json_to_file(bad, f"{info}_bad_len{n}.json")


def write_json_to_file(json_obj, file_name):
    try:
        with open(file_name, "a+") as f:
            f.write(json.dumps(json_obj))
    except OSError:
        print(f"Could not write to file: {file_name}")


def from_json(json_string):
    json_obj = json.loads(json_string)
    return {int(key): list(map(Perm, values)) for key, values in json_obj.items()}


def read_bisc_file(path):
    try:
        with open(f"{path}.json", "r") as f:
            return from_json(f.readline())
    except (ValueError, TypeError, OSError):
        print(f"File is invalid: {path}")
        return {}
