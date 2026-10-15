"""Enumeration strategy for classes closed under rotation: the cyclic shift that
moves the first entry of a permutation to the end, Perm.shift_left. This is not
Perm.rotate, which turns a permutation a quarter turn.
"""

from typing import Dict, FrozenSet, Iterable, List, Tuple

from permuta import Av, Perm
from permuta.enumeration_strategies.abstract_strategy import (
    EnumerationStrategyWithSymmetry,
)
from permuta.enumeration_strategies.core_strategies import bstrip, fstrip
from permuta.perm_sets.basis import Basis
from permuta.permutils.symmetry import all_symmetry_sets


def is_rotationally_stable(basis: Iterable[Perm]) -> bool:
    """Return True if the basis of the class is closed under rotation. The class
    is then closed under rotation too.

    Examples:
        >>> is_rotationally_stable(Basis.from_string("123_231_312"))
        True
        >>> is_rotationally_stable(Basis.from_string("123_3412"))
        False
    """
    patts = frozenset(Basis.from_iterable(basis))
    return all(patt.shift_left() in patts for patt in patts)


def min_cut(basis: Iterable[Perm]) -> Basis:
    """Return the basis of the permutations p for which 1 + p is in the class.

    If the class is closed under rotation, each of its permutations has exactly
    one rotation that starts with its minimum, so the class has n times as many
    permutations of length n as the min cut has of length n - 1.

    Examples:
        >>> min_cut(Basis.from_string("1234_2341_3412_4123"))
        Basis((Perm((0, 1, 2)), Perm((2, 3, 0, 1))))
    """
    return Basis.from_iterable(fstrip(patt) if patt else patt for patt in basis)


def max_cut(basis: Iterable[Perm]) -> Basis:
    """Return the basis of the permutations p for which p + 1 is in the class.

    If the class is closed under rotation, it has n times as many permutations of
    length n as the max cut has of length n - 1, as for the min cut.

    Examples:
        >>> max_cut(Basis.from_string("1324_3241_2413_4132"))
        Basis((Perm((0, 2, 1)), Perm((2, 1, 3, 0))))
    """
    return Basis.from_iterable(bstrip(patt) if patt else patt for patt in basis)


class RotationallyStableStrategy(EnumerationStrategyWithSymmetry):
    """Enumeration strategy for a class whose basis, or a symmetry of it, is
    closed under rotation. Each permutation in the class then has exactly one
    rotation that starts with its minimum, so the class is counted by its min
    cut, which may be rotationally stable again: see chain and count.
    """

    def _applies_to_symmetry(self, basis: FrozenSet[Perm]) -> bool:
        """Check if the basis is rotationally stable, leaving out the bases of the
        empty class and of the class of all permutations."""
        return bool(basis) and Perm() not in basis and is_rotationally_stable(basis)

    @classmethod
    def reference(cls) -> str:
        return (
            "The class is closed under rotation (cyclic shifts): one in n of its "
            "permutations of length n starts with the minimum, and the min cut "
            "counts these"
        )

    def chain(self) -> List[Basis]:
        """Return the bases B_0, B_1, ..., B_k of a longest chain of cuts. B_0 is
        the basis or a symmetry of it. Each basis but the last is rotationally
        stable, and the next one is its min cut or a symmetry of that, so
        |Av_n(B_i)| = n |Av_{n-1}(B_{i+1})| for n >= 1. The last basis is not
        rotationally stable under any symmetry. If the strategy does not apply,
        the chain is the basis alone.

        Examples:
            >>> strategy = RotationallyStableStrategy(Basis.from_string("123_231_312"))
            >>> [str(basis) for basis in strategy.chain()]
            ['{012, 120, 201}', '{01}']
        """
        return list(_chain(Basis.from_iterable(self.basis), {}))

    def count(self, length: int) -> int:
        """Return the number of permutations of the given length in the class. For
        a chain of k cuts, it generates only the permutations of the class of the
        last basis, of length k less.

        Examples:
            >>> basis = Basis.from_string("1234_2341_3412_4123")
            >>> [RotationallyStableStrategy(basis).count(n) for n in range(9)]
            [1, 1, 2, 6, 20, 65, 198, 560, 1480]
        """
        *stable, last = self.chain()
        result = 1
        for _ in stable:
            if length == 0:
                return result
            result *= length
            length -= 1
        if Perm() in last:
            return 0
        return result * Av(last).count(length)


def _chain(basis: Basis, known: Dict[Basis, Tuple[Basis, ...]]) -> Tuple[Basis, ...]:
    """Return a longest chain of cuts from the basis, as for chain, keeping in
    known the chain found from each basis on the way."""
    if basis not in known:
        best: Tuple[Basis, ...] = (basis,)
        if basis and Perm() not in basis:
            symmetries = {Basis(*sym) for sym in all_symmetry_sets(basis)} - {basis}
            for sym in [basis, *sorted(symmetries)]:
                if is_rotationally_stable(sym):
                    chain = (sym,) + _chain(min_cut(sym), known)
                    if len(chain) > len(best):
                        best = chain
        known[basis] = best
    return known[basis]
