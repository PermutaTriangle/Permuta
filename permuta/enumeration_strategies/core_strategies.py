from abc import abstractproperty, abstractstaticmethod

from permuta import Av, MeshPatt, Perm
from permuta.enumeration_strategies.abstract_strategy import (
    EnumerationStrategyWithSymmetry,
)

R_U = Perm((1, 2, 0, 3))
C_U = Perm((2, 0, 1, 3))
R_D = Perm((1, 3, 0, 2))
C_D = Perm((2, 0, 3, 1))


# Abstract Core Strategy


class CoreStrategy(EnumerationStrategyWithSymmetry):
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

    def _applies_to_symmetry(self, b):
        """
        Check if the core strategy applies to the basis or any of its symmetry.

        INPUT:

        - `b`: a set of permutations.
        """
        assert isinstance(b, frozenset)
        perm_class = Av(b)
        patterns_are_contained = all(p not in perm_class for p in self.patterns_needed)
        extensions_are_valid = all(
            self.is_valid_extension(patt) for patt in b.difference(self.patterns_needed)
        )
        return patterns_are_contained and extensions_are_valid

    @classmethod
    def reference(cls):
        return (
            "Enumeration of Permutation Classes and Weighted Labelled "
            "Independent Sets: Corollary {}"
        ).format(cls.corr_number)

    @property
    @staticmethod
    def corr_number():
        """The number of the corollary in the that gives this strategy."""
        raise NotImplementedError


# Tool functions


def fstrip(perm):
    """
    Remove the leading 1 if the permutation is the sum of 1 + p.
    """
    if perm[0] == 0:
        return Perm.from_iterable(perm[1:])
    else:
        return perm


def bstrip(perm):
    """
    Remove the trailing n if the permutation is the sum of p + 1.
    """
    if perm[-1] == len(perm) - 1:
        return Perm.from_iterable(perm[:-1])
    else:
        return perm


def zero_plus_skewind(perm):
    """
    Return True if the permutation is of the form 1 + p where p is a
    skew-indecomposable permutations
    """
    return perm[0] == 0 and not fstrip(perm).skew_decomposable()


def zero_plus_sumind(perm):
    """
    Return True if the permutation is of the form 1 + p where p is a
    sum-indecomposable permutations
    """
    return perm[0] == 0 and not fstrip(perm).sum_decomposable()


def zero_plus_perm(perm):
    """
    Return True if the permutation starts with a zero.
    """
    return perm[0] == 0


def last_sum_component(p):
    """
    Return the last sum component of a permutation.
    """
    n = len(p)
    i = 1
    comp = set([p[n - i]])
    while comp != set(range(n - i, n)):
        i += 1
        comp.add(p[n - i])
    return Perm.to_standard(p[n - i : n])


def last_skew_component(p):
    """
    Return the last skew component of a permutation.
    """
    n = len(p)
    i = 1
    comp = set([p[n - i]])
    while comp != set(range(0, i)):
        i += 1
        comp.add(p[n - i])
    return Perm.to_standard(p[n - i : n])


# Core Strategies


class RuCuCoreStrategy(CoreStrategy):
    """
    This strategies uses independent set of the up-core graph to enumerate a
    class as inflation of an independent set.
    """

    patterns_needed = frozenset([R_U, C_U])
    is_valid_extension = staticmethod(zero_plus_skewind)
    corr_number = "4.3"


class RdCdCoreStrategy(CoreStrategy):
    """
    This strategies uses independent set of the down-core graph to enumerate a
    class as inflation of an independent set.
    """

    patterns_needed = frozenset([R_D, C_D])
    is_valid_extension = staticmethod(zero_plus_sumind)
    corr_number = "4.6"


class RuCuRdCdCoreStrategy(CoreStrategy):
    patterns_needed = frozenset([R_D, C_D, R_U, C_U])
    is_valid_extension = staticmethod(zero_plus_perm)
    corr_number = "5.4"


class RuCuCdCoreStrategy(CoreStrategy):
    patterns_needed = frozenset([R_U, C_U, C_D])
    is_valid_extension = staticmethod(zero_plus_skewind)
    corr_number = "6.3"


class RdCdCuCoreStrategy(CoreStrategy):
    patterns_needed = frozenset([R_D, C_D, C_U])
    corr_number = "7.4"

    @staticmethod
    def is_valid_extension(patt):
        return zero_plus_sumind(bstrip(patt))


class RdCuCoreStrategy(CoreStrategy):
    patterns_needed = frozenset([R_D, C_U])
    corr_number = "8.3"

    @staticmethod
    def is_valid_extension(patt):
        return zero_plus_skewind(patt) and zero_plus_sumind(bstrip(patt))


class Rd2134CoreStrategy(CoreStrategy):
    patterns_needed = frozenset([R_D, Perm((1, 0, 2, 3))])
    corr_number = "9.5"

    @staticmethod
    def is_valid_extension(patt):
        mp = MeshPatt(
            Perm((1, 0)), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]
        )
        last_comp = last_sum_component(fstrip(patt))
        return (
            patt[0] == 0
            and fstrip(patt).avoids(mp)
            and (last_comp not in Av([Perm((0, 1))]) or len(last_comp) == 1)
        )


class Ru2143CoreStrategy(CoreStrategy):
    patterns_needed = frozenset([R_U, Perm((1, 0, 3, 2))])
    corr_number = "10.5"

    @staticmethod
    def is_valid_extension(patt):
        mp = MeshPatt(
            Perm((0, 1)), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]
        )
        patt = fstrip(patt)
        return patt.avoids(mp) and last_skew_component(patt) not in Av([Perm((1, 0))])


core_strategies = [
    RuCuCoreStrategy,
    RdCdCoreStrategy,
    RuCuRdCdCoreStrategy,
    RuCuCdCoreStrategy,
    RdCdCuCoreStrategy,
    RdCuCoreStrategy,
    Rd2134CoreStrategy,
    Ru2143CoreStrategy,
]
