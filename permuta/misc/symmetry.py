from permuta import Perm


def rotate_set(perms):
    if type(perms) == Perm:
        return perms.rotate()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p.rotate() for p in perms])
        else:
            raise TypeError("All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError("perms parameter must be of type list, set, tuple or permuta.Perms")



def inverse_set(perms):
    if type(perms) == Perm:
        return perms.inverse()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p.inverse() for p in perms])
        else:
            raise TypeError("All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError("perms parameter must be of type list, set, tuple or permuta.Perms")


def reverse_set(perms):
    if type(perms) == Perm:
        return perms.reverse()
    if type(perms) in [list, set, tuple]:
        if all([type(p) == Perm for p in perms]):
            return perms.__class__([p.reverse() for p in perms])
        else:
            raise TypeError("All elements of perms parameter must be of type permuta.Perm")
    else:
        raise TypeError("perms parameter must be of type list, set, tuple or permuta.Perms")


def all_symmetry_sets(input_perms):
    if type(input_perms) == Perm:
        perms = (input_perms,)
    else:
        perms = input_perms

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
    if type(perms) == dict:
        perms = list(perms)
    try:
        return perms.__class__(sorted(all_symmetry_sets(perms))[0])
    except ValueError:
        return list(sorted(all_symmetry_sets(perms))[0])
    except TypeError as te:
        te.args += ("Argument must be of type permuta.Perm or an iterable",)
        raise

