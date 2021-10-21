from permuta import Perm
from permuta.enumeration_strategies import all_enumeration_strategies, find_strategies
from permuta.enumeration_strategies.core_strategies import (
    RdCdCoreStrategy,
    RuCuCoreStrategy,
)
from permuta.enumeration_strategies.finitely_many_simples import (
    FinitelyManySimplesStrategy,
)
from permuta.enumeration_strategies.insertion_encodable import InsertionEncodingStrategy
from permuta.perm_sets.basis import Basis

ru = Perm((1, 2, 0, 3))
cu = Perm((2, 0, 1, 3))
rd = Perm((1, 3, 0, 2))
cd = Perm((2, 0, 3, 1))


def test_init_strategy():
    b1 = [Perm((0, 1, 2))]
    b2 = Basis(*[Perm((0, 1, 2, 3)), Perm((2, 0, 1))])
    for Strat in all_enumeration_strategies:
        Strat(b1).applies()
        Strat(b2).applies()


def test_insertion_encoding():
    strat = InsertionEncodingStrategy([Perm((0, 1, 2)), Perm((2, 0, 1))])
    assert strat.applies()
    strat = InsertionEncodingStrategy([Perm((0, 2, 1, 3))])
    assert not strat.applies()


def test_finite_simples():
    strat = FinitelyManySimplesStrategy([Perm((0, 1, 2))])
    assert not strat.applies()
    strat = FinitelyManySimplesStrategy([Perm((1, 3, 0, 2))])
    assert not strat.applies()
    strat = FinitelyManySimplesStrategy([Perm((2, 0, 3, 1))])
    assert not strat.applies()
    strat = FinitelyManySimplesStrategy([Perm((0, 2, 1, 3))])
    assert not strat.applies()
    strat = FinitelyManySimplesStrategy([Perm((0, 2, 1))])
    assert strat.applies()
    strat = FinitelyManySimplesStrategy([Perm((1, 3, 0, 2)), Perm((2, 0, 3, 1))])
    assert strat.applies()


def test_RuCu():
    assert not RuCuCoreStrategy([ru, cu, Perm((1, 4, 0, 2, 3))]).applies()
    assert not RuCuCoreStrategy([ru, Perm((0, 1, 2, 3))]).applies()
    assert RuCuCoreStrategy([ru, cu]).applies()
    assert RuCuCoreStrategy([ru, cu, Perm((0, 1, 2, 3, 4))]).applies()


def test_RdCd():
    assert not RdCdCoreStrategy([rd, cd, Perm((0, 1, 2, 3, 4))]).applies()
    assert not RdCdCoreStrategy([rd, Perm((0, 3, 2, 1))]).applies()
    assert RdCdCoreStrategy([rd, cd]).applies()
    assert RdCdCoreStrategy([rd, cd, Perm((0, 4, 1, 2, 3))]).applies()


def test_find_strategies():
    b1 = [Perm((0, 1, 2, 3, 4))]
    b2 = Basis(*[Perm((0, 1, 2, 3)), Perm((2, 0, 1))])
    b3 = [Perm((1, 3, 0, 2)), Perm((2, 0, 3, 1))]
    assert len(find_strategies(b1, long_runnning=True)) == 0
    assert len(find_strategies(b1, long_runnning=False)) == 0
    assert len(find_strategies(b2)) > 0
    assert len(find_strategies(b3, long_runnning=False)) == 1
    assert len(find_strategies(b3, long_runnning=True)) == 2
    assert any(isinstance(s, InsertionEncodingStrategy) for s in find_strategies(b2))
    assert any(isinstance(s, RuCuCoreStrategy) for s in find_strategies([ru, cu]))
