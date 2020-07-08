"""Return symmetries of sets."""


def rotate_90_clockwise_set(perms):
    try:
        return perms.__class__([p.rotate() for p in perms])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def rotate_180_clockwise_set(perms):
    try:
        return perms.__class__([p.rotate(2) for p in perms])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def rotate_270_clockwise_set(perms):
    try:
        return perms.__class__([p.rotate(3) for p in perms])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def rotate_set(perms):
    try:
        return perms.__class__([p.rotate() for p in perms])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def inverse_set(perms):
    try:
        return perms.__class__([p.inverse() for p in perms])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def reverse_set(perms):
    try:
        return perms.__class__([p.reverse() for p in perms])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def complement_set(perms):
    try:
        return perms.__class__([p.complement() for p in perms])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def antidiagonal_set(perms):
    try:
        return perms.__class__([p.flip_antidiagonal() for p in perms])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def all_symmetry_sets(input_perms):
    try:
        perms = sorted(tuple(input_perms))
        answer = set()
        for i in range(4):
            answer.add(tuple(sorted(perms)))
            answer.add(tuple(sorted(inverse_set(perms))))
            if i == 3:
                break
            perms = rotate_set(perms)
        return answer
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )


def lex_min(perms):
    try:
        return perms.__class__(sorted(all_symmetry_sets(perms))[0])
    except (AttributeError, TypeError):
        raise TypeError(
            ("perms parameter must be of type list, set, tuple of" " permuta.Perms")
        )
