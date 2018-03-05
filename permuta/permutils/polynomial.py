# Will return the set of polynomial types it intersects with
#   (W_++, W+-, W^-1 ++, L_2, L_2^R etc)
# 1: W++
# 2: W+-
# 3: W-+
# 4: W--
# 5: Winv++
# 6: Winv+-
# 7: Winv-+
# 8: Winv--
# 9: L2
# 10: L2inv
mem = {}


def types(perm):
    interset = mem.get(perm)
    if interset is None:
        interset = set([])
        for i in range(len(perm)+1):
            part1 = perm[0:i]
            part2 = perm[i:]

            if is_incr(part1):
                if is_incr(part2):
                    interset.add(1)
                if is_decr(part2):
                    interset.add(2)

            if is_decr(part1):
                if is_incr(part2):
                    interset.add(3)
                if is_decr(part2):
                    interset.add(4)

        flipperm = perm.inverse()
        for i in range(len(perm)+1):
            part1 = flipperm[0:i]
            part2 = flipperm[i:]

            if is_incr(part1):
                if is_incr(part2):
                    interset.add(5)
                if is_decr(part2):
                    interset.add(6)

            if is_decr(part1):
                if is_incr(part2):
                    interset.add(7)
                if is_decr(part2):
                    interset.add(8)
        if in_L2(perm):
            interset.add(9)
        if in_L2(perm.reverse()):
            interset.add(10)
    return interset


def is_decr(L):
    for i in range(len(L) - 1):
        if L[i] < L[i+1]:
            return False
    return True


def is_incr(L):
    for i in range(len(L) - 1):
        if L[i] > L[i+1]:
            return False
    return True


def in_L2(L):
    n = len(L)
    if n == 0 or n == 1:
        return True
    if L[-1] == n-1:
        return in_L2(L[0:n-1])
    elif L[-1] == n-1 and L[-2] == n-1:
        return in_L2(L[0:n-2])
    else:
        return False


def is_polynomial(basis):
    overallinterset = set([])
    for perm in basis:
        overallinterset = overallinterset.union(types(perm))
        if len(overallinterset) == 10:
            return True
    return False


def is_non_polynomial(basis): return not is_polynomial(basis)
