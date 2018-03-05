import itertools


def cyclic_range(start, end, restart):
    """Yields start,...,end-1,restart,...,start-1."""
    return itertools.chain(range(start, end), range(restart, start))


def modulo_range(start, modulo):
    """Yields start,...,modulo-1,0,...,start-1."""
    return cyclic_range(start, modulo, 0)
