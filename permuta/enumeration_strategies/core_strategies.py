from abc import abstractmethod, abstractproperty
from typing import ClassVar, FrozenSet, List, Type

from permuta import Av, MeshPatt, Perm
from permuta.enumeration_strategies.abstract_strategy import (
    EnumerationStrategyWithSymmetry,
)


class CoreStrategy(EnumerationStrategyWithSymmetry):
    """Abstract class for a core related strategy."""

    # https://arxiv.org/pdf/1912.07503.pdf
    # See this paper for corr_number

    @abstractproperty
    def patterns_needed(self) -> FrozenSet[Perm]:
        """Return the set of patterns that are needed for the strategy to be useful."""

    @staticmethod
    @abstractmethod
    def is_valid_extension(patt: Perm) -> bool:
        """Determine if the pattern satisfies the condition for strategy to apply."""

    def _applies_to_symmetry(self, basis: FrozenSet[Perm]):
        """Check if the core strategy applies to the basis or any of its symmetry."""
        assert isinstance(basis, frozenset)
        perm_class: Av = Av.from_iterable(basis)
        patterns_are_contained = all(p not in perm_class for p in self.patterns_needed)
        extensions_are_valid = all(
            self.is_valid_extension(patt)
            for patt in basis.difference(self.patterns_needed)
        )
        return patterns_are_contained and extensions_are_valid

    @classmethod
    def reference(cls) -> str:
        return (
            "Enumeration of Permutation Classes and Weighted Labelled "
            f"Independent Sets: Corollary {cls.corr_number}"
        )

    @property
    @staticmethod
    def corr_number() -> str:
        """The number of the corollary in the that gives this strategy."""
        raise NotImplementedError


def fstrip(perm: Perm) -> Perm:
    """Remove the leading 1 if the permutation is the sum of 1 + p."""
    assert len(perm) > 0
    if perm[0] == 0:
        return Perm.one_based(perm[1:])
    return perm


def bstrip(perm: Perm) -> Perm:
    """Remove the trailing n if the permutation is the sum of p + 1."""
    assert len(perm) > 0
    if perm[-1] == len(perm) - 1:
        return Perm(perm[:-1])
    return perm


def zero_plus_skewind(perm: Perm) -> bool:
    """Return True if the permutation is of the form 1 + p where p is a
    skew-indecomposable permutations
    """
    assert len(perm) > 0
    return perm[0] == 0 and not fstrip(perm).skew_decomposable()


def zero_plus_sumind(perm: Perm) -> bool:
    """Return True if the permutation is of the form 1 + p where p is a
    sum-indecomposable permutations
    """
    assert len(perm) > 0
    return perm[0] == 0 and not fstrip(perm).sum_decomposable()


def zero_plus_perm(perm: Perm) -> bool:
    """Return True if the permutation starts with a zero."""
    assert len(perm) > 0
    return perm[0] == 0


def last_sum_component(perm: Perm) -> Perm:
    """Return the last sum component of a permutation."""
    assert len(perm) > 0
    n, i = len(perm), 1
    comp = {perm[-1]}
    while comp != set(range(n - i, n)):
        i += 1
        comp.add(perm[n - i])
    return Perm.to_standard(perm[n - i : n])


def last_skew_component(perm: Perm) -> Perm:
    """Return the last skew component of a permutation."""
    assert len(perm) > 0
    n, i = len(perm), 1
    i = 1
    comp = {perm[-1]}
    while comp != set(range(i)):
        i += 1
        comp.add(perm[n - i])
    return Perm.to_standard(perm[n - i : n])


R_U: Perm = Perm((1, 2, 0, 3))  # 2314, row up
C_U: Perm = Perm((2, 0, 1, 3))  # 3124, colmn up
R_D: Perm = Perm((1, 3, 0, 2))  # 2413, row down
C_D: Perm = Perm((2, 0, 3, 1))  # 3142, column down


class RuCuCoreStrategy(CoreStrategy):
    """This strategies uses independent set of the up-core graph to enumerate a
    class as inflation of an independent set.
    """

    patterns_needed: FrozenSet[Perm] = frozenset([R_U, C_U])
    corr_number: ClassVar[str] = "4.3"

    @staticmethod
    def is_valid_extension(patt: Perm) -> bool:
        return zero_plus_skewind(patt)


class RdCdCoreStrategy(CoreStrategy):
    """This strategies uses independent set of the down-core graph to enumerate a
    class as inflation of an independent set.
    """

    patterns_needed = frozenset([R_D, C_D])
    corr_number: ClassVar[str] = "4.6"

    @staticmethod
    def is_valid_extension(patt: Perm) -> bool:
        return zero_plus_sumind(patt)


class RuCuRdCdCoreStrategy(CoreStrategy):
    """TODO"""

    patterns_needed = frozenset([R_D, C_D, R_U, C_U])
    corr_number: ClassVar[str] = "5.4"

    @staticmethod
    def is_valid_extension(patt: Perm) -> bool:
        return zero_plus_perm(patt)


class RuCuCdCoreStrategy(CoreStrategy):
    """TODO"""

    patterns_needed = frozenset([R_U, C_U, C_D])
    corr_number: ClassVar[str] = "6.3"

    @staticmethod
    def is_valid_extension(patt: Perm) -> bool:
        return zero_plus_skewind(patt)


class RdCdCuCoreStrategy(CoreStrategy):
    """TODO"""

    patterns_needed = frozenset([R_D, C_D, C_U])
    corr_number: ClassVar[str] = "7.4"

    @staticmethod
    def is_valid_extension(patt):
        return zero_plus_sumind(bstrip(patt))


class RdCuCoreStrategy(CoreStrategy):
    """TODO"""

    patterns_needed = frozenset([R_D, C_U])
    corr_number: ClassVar[str] = "8.3"

    @staticmethod
    def is_valid_extension(patt):
        return zero_plus_skewind(patt) and zero_plus_sumind(bstrip(patt))


class Rd2134CoreStrategy(CoreStrategy):
    """TODO"""

    _NON_INC: ClassVar[Av] = Av.from_iterable([Perm((0, 1))])
    _M_PATT: ClassVar[MeshPatt] = MeshPatt(
        Perm((1, 0)), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]
    )

    patterns_needed = frozenset([R_D, Perm((1, 0, 2, 3))])
    corr_number: ClassVar[str] = "9.5"

    @staticmethod
    def is_valid_extension(patt: Perm) -> bool:
        last_comp = last_sum_component(fstrip(patt))
        return (
            patt[0] == 0
            and fstrip(patt).avoids(Rd2134CoreStrategy._M_PATT)
            and (last_comp not in Rd2134CoreStrategy._NON_INC or len(last_comp) == 1)
        )


class Ru2143CoreStrategy(CoreStrategy):
    """TODO"""

    _NON_DEC: ClassVar[Av] = Av.from_iterable([Perm((1, 0))])
    _M_PATT: ClassVar[MeshPatt] = MeshPatt(
        Perm((0, 1)), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]
    )

    patterns_needed = frozenset([R_U, Perm((1, 0, 3, 2))])
    corr_number: ClassVar[str] = "10.5"

    @staticmethod
    def is_valid_extension(patt: Perm) -> bool:
        patt = fstrip(patt)
        return (
            patt.avoids(Ru2143CoreStrategy._M_PATT)
            and last_skew_component(patt) not in Ru2143CoreStrategy._NON_DEC
        )


core_strategies: List[Type[CoreStrategy]] = [
    RuCuCoreStrategy,
    RdCdCoreStrategy,
    RuCuRdCdCoreStrategy,
    RuCuCdCoreStrategy,
    RdCdCuCoreStrategy,
    RdCuCoreStrategy,
    Rd2134CoreStrategy,
    Ru2143CoreStrategy,
]
