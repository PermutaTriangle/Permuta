from permuta import Perm


def is_incr_next_incr(perm):
    for i in range(len(perm) - 1):
        if perm[i+1] < perm[i]:
            for j in range(i+1, len(perm) - 1):
                if perm[j+1] < perm[j]:
                    return False
            break
    return True


def is_incr_next_decr(perm):
    for i in range(len(perm) - 1):
        if perm[i+1] < perm[i]:
            for j in range(i+1, len(perm) - 1):
                if perm[j+1] > perm[j]:
                    return False
            break
    return True


def is_decr_next_incr(perm):
    for i in range(len(perm) - 1):
        if perm[i+1] > perm[i]:
            for j in range(i+1, len(perm) - 1):
                if perm[j+1] < perm[j]:
                    return False
            break
    return True


def is_decr_next_decr(perm):
    for i in range(len(perm) - 1):
        if perm[i+1] > perm[i]:
            for j in range(i+1, len(perm) - 1):
                if perm[j+1] > perm[j]:
                    return False
            break
    return True


mem = dict()


def insertion_encodable_properties(perm):
    if perm in mem:
        return mem[tuple(perm)]

    properties = []
    if is_incr_next_decr(perm):
        properties.append(0)
    if is_incr_next_incr(perm):
        properties.append(1)
    if is_decr_next_decr(perm):
        properties.append(2)
    if is_decr_next_incr(perm):
        properties.append(3)

    res = sum(1 << x for x in properties)
    mem[perm] = res

    return res


def is_insertion_encodable_rightmost(basis):
    goal = (1 << 4) - 1
    curr = 0
    # Check for insertion_encodable by rightmost
    for perm in basis:
        curr = curr | insertion_encodable_properties(perm)
        if curr == goal:
            return True
    return False


def is_insertion_encodable_maximum(basis):
    goal = (1 << 4) - 1
    curr = 0
    # Check for insertion_encodable by maximum
    for perm in basis:
        curr = curr | insertion_encodable_properties(perm.rotate())
        if curr == goal:
            return True
    return False


def is_insertion_encodable(basis):
    return (is_insertion_encodable_rightmost(basis) or
            is_insertion_encodable_maximum(basis))
