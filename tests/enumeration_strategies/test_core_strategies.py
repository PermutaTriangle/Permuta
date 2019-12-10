from permuta import Perm

from permuta.enumeration_strategies.core_strategies import (fstrip, bstrip,
                                                            zero_plus_perm,
                                                            zero_plus_sumind,
                                                            zero_plus_skewind,
                                                            last_sum_component,
                                                            last_skew_component)
from permuta.enumeration_strategies.core_strategies import (RuCuCoreStrategy,
                                                            RdCdCoreStrategy,
                                                            RuCuRdCdCoreStrategy,
                                                            RuCuCdCoreStrategy,
                                                            RdCdCuCoreStrategy,
                                                            RdCuCoreStrategy,
                                                            Rd2134CoreStrategy,
                                                            Ru2143CoreStrategy)

ru = Perm((1,2,0,3))
cu = Perm((2,0,1,3))
rd = Perm((1,3,0,2))
cd = Perm((2,0,3,1))
p2134 = Perm((1,0,2,3))
p2143 = Perm((1,0,3,2))

class TestRuCu():
    def test_applies(self):
        assert RuCuCoreStrategy([ru, cu])
        assert RuCuCoreStrategy([ru, cu, Perm((0,1,2,3))])
        assert not RuCuCoreStrategy([ru, Perm((0,1,2,3))]).applies()
        assert not RuCuCoreStrategy([ru, cu, Perm((1,4,0,2,3))]).applies()
        assert RuCuCoreStrategy([ru, cu, Perm((0,1,2,3,4))]).applies()
        assert RuCuCoreStrategy([ru, cu, Perm((0,2,4,1,3)),
                                 Perm((0,1,3,2,4))]).applies()

    def test_applies_to_a_symmetry(self):
        assert RuCuCoreStrategy([Perm([0,2,3,1]), Perm([0,3,1,2])]).applies()
        assert RuCuCoreStrategy([Perm([0,2,3,1]), Perm([0,3,1,2]),
                                 Perm([0,1,2,3])]).applies()

    def test_specific_symmetry(self):
        b1 = frozenset([ru, cu, Perm((3,0,1,2))])
        assert not RuCuCoreStrategy(b1)._applies_to_symmetry(b1)
        b2 = frozenset([ru, cu, Perm((0,3,2,1))])
        assert not RuCuCoreStrategy(b2)._applies_to_symmetry(b2)
        b3 = frozenset([ru, cu])
        assert RuCuCoreStrategy(b3)._applies_to_symmetry(b3)


class TestRdCd():

    def test_applies(self):
        assert not RdCdCoreStrategy([rd, cd, Perm((0,1,2,3,4))]).applies()
        assert not RdCdCoreStrategy([rd, Perm((0,3,2,1))]).applies()
        assert RdCdCoreStrategy([rd, cd]).applies()
        assert RdCdCoreStrategy([rd, cd, Perm((0,4,1,2,3))]).applies()

    def test_applies_to_a_symmetry(self):
        assert RdCdCoreStrategy([Perm((1,3,0,2)), Perm((2,0,3,1))]).applies()

    def test_specific_symmetry(self):
        b1 = frozenset([Perm((1,3,0,2)), Perm((2,0,3,1))])
        assert RdCdCoreStrategy(b1)._applies_to_symmetry(b1)
        b2 = frozenset([rd, cd])
        assert RdCdCoreStrategy(b2)._applies_to_symmetry(b2)


class TestRuCuRdCd():

    def test_applies(self):
        assert not RuCuRdCdCoreStrategy([rd, cd]).applies()
        assert not RuCuRdCdCoreStrategy([rd, cd, ru, Perm((0,3,2,1))]).applies()
        assert RuCuRdCdCoreStrategy([rd, cd, ru, cu]).applies()
        assert RuCuRdCdCoreStrategy([rd, cd, ru, cu, Perm((0,1,2,3))]).applies()

    def test_applies_to_a_symmetry(self):
        assert RuCuRdCdCoreStrategy([Perm((0,2,3,1)), Perm((0,3,1,2)),
                                     Perm((1,3,0,2)), Perm((2,0,3,1))]).applies()

    def test_specific_symmetry(self):
        b1 = frozenset([Perm((0,2,3,1)), Perm((0,3,1,2)),
                        Perm((1,3,0,2)), Perm((2,0,3,1))])
        assert not RuCuRdCdCoreStrategy(b1)._applies_to_symmetry(b1)
        b2 = frozenset([rd, cd, cu, ru])
        assert RuCuRdCdCoreStrategy(b2)._applies_to_symmetry(b2)


class TestRuCuCd():

    def test_applies(self):
        assert RuCuCdCoreStrategy([cd, ru, cu]).applies()
        assert not RuCuCdCoreStrategy([rd, cd]).applies()
        assert not RuCuCdCoreStrategy([rd, cd, ru, Perm((0,3,2,1))]).applies()
        assert RuCuCdCoreStrategy([ru, cu, cd, Perm((0,1,2,3))]).applies()

    def test_applies_to_a_symmetry(self):
        assert RuCuCdCoreStrategy([ru, cu, rd]).applies()
        assert RuCuCdCoreStrategy([ru, cu, rd, Perm((0,2,1,3))]).applies()
        assert RuCuCdCoreStrategy([Perm((0,2,3,1)), Perm((0,3,1,2)),
                                     Perm((1,3,0,2))]).applies()
        assert RuCuCdCoreStrategy([Perm((0,2,3,1)), Perm((0,3,1,2)),
                                     Perm((1,3,0,2)), Perm((0,1,2,3))]).applies()
        # 123 implies the avoidance of ru and cu
        assert RuCuCdCoreStrategy([rd, Perm((0,1,2))]).applies()


class TestRdCdCu():
    def test_applies(self):
        assert RdCdCuCoreStrategy([rd, cd, cu]).applies()
        assert not RdCdCuCoreStrategy([rd, cd]).applies()
        assert not RdCdCuCoreStrategy([rd, cd, cu, Perm((0,1,2,3))]).applies()
        assert RdCdCuCoreStrategy([rd, cd, cu, Perm((0,2,1,3))]).applies()
        assert RdCdCuCoreStrategy([rd, cd, cu, Perm((0,3,2,1))]).applies()

    def test_applies_to_a_symmetry(self):
        assert RdCdCuCoreStrategy([rd, cd, ru]).applies()
        # Symmetry and adding pattern
        assert RdCdCuCoreStrategy([Perm((1,0,2)), Perm((0,3,1,2))]).applies()

    def test_is_valid_extension(self):
        assert RdCdCuCoreStrategy.is_valid_extension(Perm((0,2,1,3)))
        assert not RdCdCuCoreStrategy.is_valid_extension(Perm((1,2,0,3)))


class TestRdCu():
    def test_applies(self):
        assert RdCuCoreStrategy([rd, cu]).applies()
        assert not RdCuCoreStrategy([rd, cd]).applies()
        assert not RdCuCoreStrategy([rd, cu, Perm((0,1,2,3))]).applies()
        assert not RdCuCoreStrategy([rd, cu, Perm((0,3,2,1))]).applies()
        assert RdCuCoreStrategy([rd, cu, Perm((0,2,1,3))]).applies()
        assert RdCuCoreStrategy([rd, cu, Perm((0,3,1,2,4))]).applies()

    def test_applies_to_a_symmetry(self):
        assert RdCuCoreStrategy([ru, cd]).applies()

    def test_is_valid_extension(self):
        assert RdCuCoreStrategy.is_valid_extension(Perm((0,2,1,3)))
        assert not RdCuCoreStrategy.is_valid_extension(Perm((1,2,0,3)))


class TestRd2134():
    def test_applies(self):
        assert Rd2134CoreStrategy([rd, p2134]).applies()
        assert not Rd2134CoreStrategy([rd, cu]).applies()
        assert not Rd2134CoreStrategy([rd, p2134, Perm((0,4,3,1,2))]).applies()
        assert not Rd2134CoreStrategy([rd, cu, Perm((0,1,2,3))]).applies()
        assert Rd2134CoreStrategy([rd, p2134, Perm((0,3,4,2,1))]).applies()
        assert Rd2134CoreStrategy([rd, p2134, Perm((0,3,2,4,1))]).applies()
        assert Rd2134CoreStrategy([rd, p2134, Perm((0,1,2,3))]).applies()
        assert Rd2134CoreStrategy([rd, p2134, Perm((0,2,1,3)),
                                   Perm((0,1,4,2,3))]).applies()

    def test_applies_to_a_symmetry(self):
        assert Rd2134CoreStrategy([cd, p2134]).applies()
        assert Rd2134CoreStrategy([Perm.from_string('0132'),
                                   Perm.from_string('1302'),
                                   Perm.from_string('32014')]).applies()

    def test_is_valid_extension(self):
        assert Rd2134CoreStrategy.is_valid_extension(Perm((0,3,4,2,1)))
        assert not Rd2134CoreStrategy.is_valid_extension(Perm((0,4,3,1,2)))
        assert Rd2134CoreStrategy.is_valid_extension(Perm((0,1,2,3)))
        assert not Rd2134CoreStrategy.is_valid_extension(Perm((0,1,2,4,3)))


class TestRu2143():
    def test_applies(self):
        assert Ru2143CoreStrategy([ru, p2143]).applies()
        assert not Ru2143CoreStrategy([ru]).applies()
        assert not Ru2143CoreStrategy([ru, p2143, Perm((0,2,1,3,4))]).applies()
        assert not Ru2143CoreStrategy([ru, p2143, Perm((0,4,3,1,2))]).applies()
        assert Ru2143CoreStrategy([ru, p2143, Perm((0,2,4,1,3))]).applies()
        assert Ru2143CoreStrategy([ru, p2143, Perm((0,1,2,4,3))]).applies()

    def test_applies_to_a_symmetry(self):
        assert Ru2143CoreStrategy([cu, p2143]).applies()
        assert Ru2143CoreStrategy([Perm.from_string('0231'),
                                   Perm.from_string('1032'),
                                   Perm.from_string('03124')]).applies()

    def test_is_valid_extension(self):
        assert Ru2143CoreStrategy.is_valid_extension(Perm((0,2,4,1,3)))
        assert not Ru2143CoreStrategy.is_valid_extension(Perm((0,2,1,3,4)))
        assert not Ru2143CoreStrategy.is_valid_extension(Perm((0,4,3,1,2)))

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


def test_last_sum_component():
    assert last_sum_component(Perm((0,1,2,4,3))) == Perm((1, 0))
    assert last_sum_component(Perm((0,1,2,3))) == Perm((0,))
    assert last_sum_component(Perm((3,2,1,0))) == Perm((3, 2, 1, 0))


def test_last_skew_component():
    last_skew_component(Perm((2,4,3,0,1))) == Perm((0, 1))
    last_skew_component(Perm((0,1,2,3))) == Perm((0, 1, 2, 3))
    last_skew_component(Perm((3,2,1,0))) == Perm((0,))
