from itertools import combinations


def ordered_set_partitions(lst, parts, CACHE={}):
    key = tuple(parts)
    if key not in CACHE:
        CACHE[key] = list(helper(lst, parts))
    for partition in CACHE[key]:
        yield partition


def ordered_set_partitions_no_cache(lst, parts):
    for partition in list(helper(lst, parts)):
        yield partition


def helper(lst, parts):
    if not parts:
        yield []
    else:
        for comb in combinations(lst, parts[0]):
            new_lst = list(i for i in lst if i not in comb)
            for f in helper(new_lst, parts[1:]):
                yield [list(comb)] + f


def ordered_set_partitions_list(lst):
    for parts in partitions(len(lst)):
        if len(parts) == len(lst) or len(parts) == 1:
            continue
        for partition in ordered_set_partitions_no_cache(lst, parts):
            yield partition


def partitions(n, CACHE={}):
    if n not in CACHE:
        if n == 0:
            CACHE[n] = [[]]
        elif n == 1:
            CACHE[n] = [[1]]
        else:

            CACHE[n] = [[n]]
            for i in range(1, n):
                for part in partitions(n - i):
                    if part:
                        CACHE[n].append([i] + part)
    return CACHE[n]


def partitions_of_n_of_size_k(n, k):
    """possibly empty parts"""
    if n == 0 and k == 0:
        return [[]]
    elif k < 0:
        return []
    else:
        parts = []
        for i in range(n + 1):
            for part in partitions_of_n_of_size_k(n - i, k - 1):
                parts.append([i] + part)
    return parts

# internet versions

# def ordered_set_partitions(lst, parts):
#     return partitions(*parts)
#
# def partitions(*args):
#     def p(s, *args):
#         if not args: return [[]]
#         res = []
#         for c in combinations(s, args[0]):
#             s0 = [x for x in s if x not in c]
#             for r in p(s0, *args[1:]):
#                 res.append([c] + r)
#         return res
#     s = range(sum(args))
#     return p(s, *args)
#
# def partitions(*args):
#     def minus(s1, s2): return [x for x in s1 if x not in s2]
#     def p(s, *args):
#         if not args: return [[]]
#         return [[c] + r for c in combinations(s, args[0])
#                 for r in p(minus(s, c), *args[1:])]
#     return p(range(1, sum(args) + 1), *args)


# Raggis index

# def ordered_set_partitions(lst, parts):
#     if
#     result = [() for _ in range(len(parts))]
#     for partition in _helper(lst, parts, index):
#         yield partition
#
#
# def _helper(lst, parts, index):
#     if index >= len(parts):
#         yield
#
#
# def splits(lst, k):
#     for comb in combinations(lst, k):
#         yield comb, tuple(i for i in lst if i not in comb)
