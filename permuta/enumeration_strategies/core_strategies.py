from abc import abstractmethod, abstractproperty, abstractstaticmethod

from permuta import Av, Perm
from permuta.descriptors import Basis
from permuta.enumeration_strategies.abstract_strategy import \
    EnumerationStrategy

R_U = Perm((1, 2, 0, 3))
C_U = Perm((2, 0, 1, 3))
R_D = Perm((1, 3, 0, 2))
C_D = Perm((2, 0, 3, 1))

# Abstract Core Strategy


class CoreStrategy(EnumerationStrategy):
    """
    Abstract class for a core related strategy.
    """

    @abstractproperty
    def patterns_needed():
        """
        Return the set of patterns that are needed for the strategy to be
        useful.
        """
        pass

    @abstractstaticmethod
    def is_valid_extension(patt):
        """
        Determine if the pattern satisfies the condition for strategy to apply.
        """
        pass

    def applies(self):
        b = set(self.basis)
        perm_class = Av(b)
        patterns_are_contained = all(p not in perm_class for p in
                                     self.patterns_needed)
        extensions_are_valid = all(self.is_valid_extension(patt) for patt in
                                   b.difference(self.patterns_needed))
        return patterns_are_contained and extensions_are_valid


# Tool functions

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


def one_plus_skewind(perm):
    """
    Return True if the permutation is of the form 1 + p where p is a
    skew-indecomposable permutations
    """
    return perm[0] == 0 and not fstrip(perm).skew_decomposable()


def one_plus_sumind(perm):
    """
    Return True if the permutation is of the form 1 + p where p is a
    sum-indecomposable permutations
    """
    return perm[0] == 0 and not fstrip(perm).sum_decomposable()


def one_plus_perm(perm):
    return perm[0] == 0


# Core Strategies

class RuCuCoreStrategy(CoreStrategy):
    """
    This strategies uses independent set of the up-core graph to enumerate a
    class as inflation of an independent set.
    """
    patterns_needed = set([R_U, C_U])
    is_valid_extension = staticmethod(one_plus_skewind)


class RdCdCoreStrategy(CoreStrategy):
    """
    This strategies uses independent set of the down-core graph to enumerate a
    class as inflation of an independent set.
    """
    patterns_needed = set([R_D, C_D])
    is_valid_extension = staticmethod(one_plus_sumind)


class RuCuRdCdCoreStrategy(CoreStrategy):
    patterns_needed = set([R_D, C_D, R_U, C_U])
    is_valid_extension = staticmethod(one_plus_perm)


class RuCuRdCoreStrategy(CoreStrategy):
    patterns_needed = set([R_U, C_U, R_D])
    is_valid_extension = staticmethod(one_plus_skewind)


class RuCuCdCoreStrategy(CoreStrategy):
    patterns_needed = set([R_U, C_U, C_D])
    is_valid_extension = staticmethod(one_plus_skewind)


class RdCdRuCoreStrategy(CoreStrategy):
    patterns_needed = set([R_D, C_D, R_U])
    is_valid_extension = staticmethod(one_plus_sumind)


class RdCdCuCoreStrategy(CoreStrategy):
    patterns_needed = set([R_D, C_D, C_U])
    is_valid_extension = staticmethod(one_plus_sumind)


class RdCuCoreStrategy(CoreStrategy):
    patterns_needed = set([R_D, C_U])

    @staticmethod
    def is_valid_extension(patt):
        return one_plus_skewind(patt) and \
                not bstrip(fstrip(patt)).sum_decomposable()


class RuCdCoreStrategy(CoreStrategy):
    patterns_needed = set([R_U, C_D])

    @staticmethod
    def is_valid_extension(patt):
        return one_plus_skewind(patt) and \
                not bstrip(fstrip(patt)).sum_decomposable()

core_strategies = [
    RuCuCoreStrategy,
    RdCdCoreStrategy,
    RuCuRdCdCoreStrategy,
    RuCuRdCoreStrategy,
    RuCuCdCoreStrategy,
    RdCdRuCoreStrategy,
    RdCdCuCoreStrategy,
    RdCuCoreStrategy,
    RuCdCoreStrategy,
]
