import itertools

from permuta import Perm


class Bijections:
    """A collection of known bijections."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def simion_and_schmidt(perm: Perm, inverse: bool = False) -> Perm:
        """The bijection from `Restricted permutations` by R. Simion and F. Schmidt
        between Av(123) and Av(132).
        """
        n = len(perm)
        if n == 0:
            return Perm()
        if inverse:
            if perm.contains(Perm((0, 2, 1))):
                raise ValueError("Map only works for 132 avoiding permutations")
            return Bijections._simion_and_schmidt_inv(perm, n)
        if perm.contains(Perm((0, 1, 2))):
            raise ValueError("Map only works for 123 avoiding permutations")
        return Bijections._simion_and_schmidt(perm, n)

    @staticmethod
    def _simion_and_schmidt(perm: Perm, n: int) -> Perm:
        used, img, min_val = {perm[0]}, [perm[0]] * n, perm[0]
        for idx, val in itertools.islice(enumerate(perm), 1, None):
            if min_val > val:  # val is L2R minima
                img[idx], min_val = val, val
            else:
                img[idx] = next(k for k in range(min_val + 1, n) if k not in used)
            used.add(img[idx])
        return Perm(img)

    @staticmethod
    def _simion_and_schmidt_inv(perm: Perm, n: int) -> Perm:
        used, img, min_val = {perm[0]}, [perm[0]] * n, perm[0]
        for idx, val in itertools.islice(enumerate(perm), 1, None):
            if min_val > val:  # val is L2R minima
                img[idx], min_val = val, val
            else:
                img[idx] = next(k for k in range(n - 1, -1, -1) if k not in used)
            used.add(img[idx])
        return Perm(img)
