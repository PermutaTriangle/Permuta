from permuta import Perm


def rotate_90_clockwise_set(perms):
    if type(perms) == Perm:
        return perms.rotate_right()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p._rotate_right() for p in perms])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def rotate_180_clockwise_set(perms):
    if type(perms) == Perm:
        return perms.rotate_180()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p._rotate_180() for p in perms])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def rotate_270_clockwise_set(perms):
    if type(perms) == Perm:
        return perms.rotate_left()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p._rotate_left() for p in perms])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def rotate_set(perms):
    if type(perms) == Perm:
        return perms.rotate()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p.rotate() for p in perms])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def inverse_set(perms):
    if type(perms) == Perm:
        return perms.inverse()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p.inverse() for p in perms])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def reverse_set(perms):
    if type(perms) == Perm:
        return perms.reverse()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p.reverse() for p in perms])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def complement_set(perms):
    if type(perms) == Perm:
        return perms.complement()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p.complement() for p in perms])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def antidiagonal_set(perms):
    if type(perms) == Perm:
        return perms.flip_antidiagonal()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p.flip_antidiagonal() for p in perms])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def all_symmetry_sets(input_perms):
    if type(input_perms) == Perm:
        perms = (input_perms,)
    elif type(input_perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in input_perms]):
            perms = input_perms
        else:
            raise TypeError(("All elements of input_perms parameter must be "
                             "of type permuta.Perm"))
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))

    answer = set()
    for i in range(4):
        answer.add(tuple(sorted(perms)))
        answer.add(tuple(sorted(inverse_set(perms))))
        if i == 3:
            break
        perms = rotate_set(perms)
    return answer


def lex_min(perms):
    if type(perms) == Perm:
        return sorted(all_symmetry_sets(perms))[0][0]
    elif type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__(sorted(all_symmetry_sets(perms))[0])
        else:
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))


def reduced_set(input_perms):
    if type(input_perms) not in [list, set, tuple]:
        raise TypeError(("perms parameter must be of type list, set, tuple or"
                         " permuta.Perms"))
    else:
        if not all([type(p) == Perm for p in input_perms]):
            raise TypeError(
                "All elements of perms parameter must be of type permuta.Perm")
    perms = sorted(input_perms)
    output_set = set()
    for i, perm in enumerate(perms[::-1]):
        if not any([perm.contains(x) for x in perms[:-i - 1]]):
            output_set.add(perm)
    return input_perms.__class__(sorted(output_set))
