from permuta import *


def rotate_set(perms):
    if type(perms) == Perm:
        return perms.rotate()
    if type(perms) == dict:
        perms = list(perms)
    try:
        return perms.__class__(set([p.rotate() for p in perms]))
    except ValueError:
        return list([p.rotate() for p in perms])
    except TypeError as te:
        te.args += ("Argument must be of type permuta.Perm or an iterable",)
        raise
    except AttributeError as ae:
        ae.args += ("All elements of iterable arguments must be of type permuta.Perm",)
        raise



def inverse_set(perms):
    if type(perms) == Perm:
        return perms.inverse()
    if type(perms) == dict:
        perms = list(perms)
    try:
        return perms.__class__(set([p.inverse() for p in perms]))
    except ValueError:
        return list([p.inverse() for p in perms])
    except TypeError as te:
        te.args += ("Argument must be of type permuta.Perm or an iterable",)
        raise
    except AttributeError as ae:
        ae.args += ("All elements of iterable arguments must be of type permuta.Perm",)
        print("What?")
        raise


def reverse_set(perms):
    if type(perms) == Perm:
        return perms.reverse()
    if type(perms) == dict:
        perms = list(perms)
    try:
        return perms.__class__(set([p.reverse() for p in perms]))
    except ValueError:
        return list([p.reverse() for p in perms])
    except TypeError as te:
        te.args += ("Argument must be of type permuta.Perm or an iterable",)
        raise
    except AttributeError as ae:
        ae.args += ("All elements of iterable arguments must be of type permuta.Perm",)
        raise


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


if __name__ == "__main__":
    x = [Perm((1, 3, 2, 0)), Perm((5, 3, 2, 1, 4, 0)), Perm((2,1,0,3))]
    y = tuple(x)
    z = set(x)
    a = Perm((1, 3, 2, 0))
    d = {Perm((1, 3, 2, 0)): Perm((5, 3, 2, 1, 4, 0))}

    print(all_symmetry_sets(x))
    print(all_symmetry_sets(y))
    print(all_symmetry_sets(z))
    print(all_symmetry_sets(d))
    print(all_symmetry_sets(a))

    print(lex_min(x))
    print(lex_min(y))
    print(lex_min(z))
    print(lex_min(d))
    print(lex_min(a))

    #Now we break stuff:

    x.append(5)
    try:
        print(all_symmetry_sets(x))
    except RecursionError as re:
        print("Error")
        print(re)
        print("This should not happen.")
        print("It is a problem with sorting a list of permutations that do not only contain permutations")
        print("The problem occurs within the permuta class")