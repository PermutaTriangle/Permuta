from permuta import Perm

from permuta.enumeration_strategies.core_strategies import (fstrip, bstrip,
                                                            zero_plus_perm,
                                                            zero_plus_sumind,
                                                            zero_plus_skewind)
from permuta.enumeration_strategies.core_strategies import RuCuCoreStrategy

ru = Perm((1,2,0,3))
cu = Perm((2,0,1,3))
rd = Perm((1,3,0,2))
cd = Perm((2,0,3,1))

class TestRuCu():
    def test_applies(self):
        assert RuCuCoreStrategy([ru, cu])
        assert RuCuCoreStrategy([ru, cu, Perm((0,1,2,3))])

    def test_applies_to_a_symmetry(self):
        assert RuCuCoreStrategy([Perm([0,2,3,1]), Perm([0,3,1,2])]).applies()
        assert RuCuCoreStrategy([Perm([0,2,3,1]), Perm([0,3,1,2]),
                                 Perm([0,1,2,3])]).applies()

    def test_specific_symmetry(self):
        b1 = set([ru, cu, Perm((3,0,1,2))])
        assert not RuCuCoreStrategy(b1)._applies_to_symmetry(b1)
        b2 = set([ru, cu, Perm((0,3,2,1))])
        assert not RuCuCoreStrategy(b2)._applies_to_symmetry(b2)
        b3 = set([ru, cu])
        assert RuCuCoreStrategy(b3)._applies_to_symmetry(b3)

# Test for tools functions

def test_fstrip():
    assert fstrip(Perm((0, 1, 3, 2))) == Perm((0, 2, 1))
    assert fstrip(Perm((4, 0, 1, 3, 2))) == Perm((4, 0, 1, 3, 2))


def test_bstrip():
    assert bstrip(Perm((0, 1, 3, 2))) == Perm((0, 1, 3, 2))
    assert bstrip(Perm((0, 1, 3, 2, 4))) == Perm((0, 1, 3, 2))


def test_zero_plus_perm():
    assert zero_plus_perm(Perm((0,1,2)))
    assert not zero_plus_perm(Perm((3,0,1,2)))


def test_zero_plus_skewind():
    assert zero_plus_skewind(Perm((0,1,3,2)))
    assert not zero_plus_skewind(Perm((0,3,1,2)))
    assert not zero_plus_skewind(Perm((1,3,0,2)))


def test_zero_plus_sumind():
    assert zero_plus_sumind(Perm((0,3,1,2)))
    assert not zero_plus_sumind(Perm((0,1,3,2)))
    assert not zero_plus_sumind(Perm((1,3,0,2)))
