from abc import abstractproperty, abstractstaticmethod

from permuta import Perm
from permuta.enumeration_strategies.abstract_strategy import \
        EnumerationStrategy

R_U = Perm((1, 2, 0, 3))
C_U = Perm((1, 0, 2, 3))
R_D = Perm((1, 3, 0, 2))
C_D = Perm((2, 0, 3, 1))

def fstrip(perm):
    """
    Remove the leading 1 if the permutation is the sum of 1 + p.

    >>> fstrip(Perm((0, 1, 3, 2)))
    Perm((0, 2, 1))
    >>> fstrip(Perm((4, 0, 1, 3, 2)))
    Perm((4, 0, 1, 3, 2))
    """
    if perm[0] == 0:
        return Perm.from_iterable(perm[1:])
    else:
        return perm

def bstrip(perm):
    """
    Remove the trailing n if the permutation is the sum of p + 1.

    >>> bstrip(Perm((0, 1, 3, 2)))
    Perm((0, 1, 3, 2))
    >>> bstrip(Perm((0, 1, 3, 2, 4)))
    Perm((0, 1, 3, 2))
    """
    if perm[-1] == len(perm)-1:
        return Perm.from_iterable(perm[:-1])
    else:
        return perm

class CoreStrategy(EnumerationStrategy):
    """
    Abstract class for a core related strategy.
    """

    @abstractproperty
    def PATTERNS_NEEDED():
        """
        Return the set of patterns that are needed for the strategy to be
        useful.
        """
        raise NotImplemented

    @abstractstaticmethod
    def is_valid_extension(patt):
        """
        Determine if the pattern satisfies the condition for strategy to apply.
        """
        pass

    def applies():
        b = set(self.basis)
        extensions_are_valid = all(self.is_valid_extension(patt) for patt in \
                                   b.difference(self.PATTERNS_NEEDED))
        return self.PATTERNS_NEEDED.issubset(b) and extensions_are_valid


class UpCoreStrategy(CoreStrategy):
    PATTERNS_NEEDED = set([R_U, C_U])

    def is_valid_extension(patt):
        return patt[0] == 0 and not fstrip(patt).skew_decomposable()


class DownCoreStrategy(CoreStrategy):
    PATTERNS_NEEDED = set([R_D, C_D])

    def is_valid_extension(patt):
        return patt[0] == 0 and not fstrip(patt).sum_decomposable()


class UpDownCoreStrategy(CoreStrategy):
    PATTERNS_NEEDED = set([R_D, C_D, R_U, C_U])

    def is_valid_extension(patt):
        return patt[0] == 0

__all__ = [UpCoreStrategy, DownCoreStrategy]
