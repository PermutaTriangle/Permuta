import json
import types
from collections import defaultdict

from permuta.bisc.bisc_subfunctions import forb, mine
from permuta.perm import Perm
from permuta.permset import PermSet


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
            for perm in PermSet(i):
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


def create_bisc_input(N, prop):
    """
    Create a dictionary, D, containing keys 1, 2, 3, ..., N. Each key points to
    a list of permutations satisfying the property prop. The dictionary E has
    the same keys and they point to the complement.
    """

    A, B = {}, {}

    for n in range(N + 1):

        An, Bn = [], []

        for perm in PermSet(n):
            if prop(perm):
                An.append(perm)
            else:
                Bn.append(perm)

        A[n], B[n] = An, Bn

    return A, B


def write_bisc_files(N, prop, info):
    """
    Create a dictionary, D, containing keys 1, 2, 3, ..., N. Each key points to
    a list of permutations satisfying the property prop. The dictionary E has
    the same keys and they point to the complement.
    """

    A, B = {}, {}

    for n in range(N + 1):

        An, Bn = [], []

        for perm in PermSet(n):
            if prop(perm):
                An.append(perm)
            else:
                Bn.append(perm)

        A[n], B[n] = An, Bn
    f = open("{}_good_len{}".format(info, N), "a+")
    f.write(json.dumps(A))
    f.close()

    f = open("{}_bad_len{}".format(info, N), "a+")
    f.write(json.dumps(B))
    f.close()


def from_json(s):
    d = json.loads(s)
    return {int(key): list(map(Perm, values)) for key, values in d.items()}


def read_bisc_file(p):

    A = dict()

    f = open(p, "r")
    for line in f:
        A = from_json(line)
    f.close()

    return A
