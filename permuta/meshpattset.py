from .meshpatt import MeshPatt
from .perm import Perm
from .permset import PermSet


def gen_meshpatts(length, patt=None):
    """Generates all mesh patterns of length n. If the classical pattern is
    specified then only the mesh patterns with the classical pattern as the
    underlying pattern are generated.

    Args:
        length: <numbers.Integral>
            The length(size) of the mesh pattern.
        patt: <permutation.Permutation>, <numbers.Integral> or
              <collections.Iterable>

    Yields: <permuta.MeshPatt>
        Every permutation of the specified length with the specified classical
        pattern or each of them if the pattern is not specified.

    Examples:
        >>> mps = list(gen_meshpatts(0))
        >>> len(mps)
        2
        >>> mps[0]
        MeshPatt(Perm(()), [])
        >>> mps[1]
        MeshPatt(Perm(()), [(0, 0)])
        >>> len(list(gen_meshpatts(2, (1, 2))))
        512
    """
    if patt is None:
        for p in PermSet(length):
            for i in range(2**((length + 1)**2)):
                yield MeshPatt.unrank(p, i)
    else:
        if not isinstance(patt, Perm):
            patt = Perm(patt)
        for i in range(2**((length + 1)**2)):
            yield MeshPatt.unrank(patt, i)
