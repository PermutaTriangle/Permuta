

def is_finite(basis):
    return (any(perm.is_decreasing() for perm in basis) and
            any(perm.is_increasing() for perm in basis))
