from permuta import Perm
from permuta.permutils import Bijections


def test_simion_and_schmidt():
    assert Bijections.simion_and_schmidt(Perm(())) == Perm(())
    assert Bijections.simion_and_schmidt(Perm((0,))) == Perm((0,))
    assert Bijections.simion_and_schmidt(Perm((0, 1))) == Perm((0, 1))
    assert Bijections.simion_and_schmidt(Perm((1, 0))) == Perm((1, 0))
    assert Bijections.simion_and_schmidt(Perm((0, 2, 1))) == Perm((0, 1, 2))
    assert Bijections.simion_and_schmidt(Perm((1, 0, 2))) == Perm((1, 0, 2))
    assert Bijections.simion_and_schmidt(Perm((1, 2, 0))) == Perm((1, 2, 0))
    assert Bijections.simion_and_schmidt(Perm((2, 0, 1))) == Perm((2, 0, 1))
    assert Bijections.simion_and_schmidt(Perm((2, 1, 0))) == Perm((2, 1, 0))
    assert Bijections.simion_and_schmidt(Perm((0, 3, 2, 1))) == Perm((0, 1, 2, 3))
    assert Bijections.simion_and_schmidt(Perm((1, 0, 3, 2))) == Perm((1, 0, 2, 3))
    assert Bijections.simion_and_schmidt(Perm((1, 3, 0, 2))) == Perm((1, 2, 0, 3))
    assert Bijections.simion_and_schmidt(Perm((1, 3, 2, 0))) == Perm((1, 2, 3, 0))
    assert Bijections.simion_and_schmidt(Perm((2, 0, 3, 1))) == Perm((2, 0, 1, 3))
    assert Bijections.simion_and_schmidt(Perm((2, 1, 0, 3))) == Perm((2, 1, 0, 3))
    assert Bijections.simion_and_schmidt(Perm((2, 1, 3, 0))) == Perm((2, 1, 3, 0))
    assert Bijections.simion_and_schmidt(Perm((2, 3, 0, 1))) == Perm((2, 3, 0, 1))
    assert Bijections.simion_and_schmidt(Perm((2, 3, 1, 0))) == Perm((2, 3, 1, 0))
    assert Bijections.simion_and_schmidt(Perm((3, 0, 2, 1))) == Perm((3, 0, 1, 2))
    assert Bijections.simion_and_schmidt(Perm((3, 1, 0, 2))) == Perm((3, 1, 0, 2))
    assert Bijections.simion_and_schmidt(Perm((3, 1, 2, 0))) == Perm((3, 1, 2, 0))
    assert Bijections.simion_and_schmidt(Perm((3, 2, 0, 1))) == Perm((3, 2, 0, 1))
    assert Bijections.simion_and_schmidt(Perm((3, 2, 1, 0))) == Perm((3, 2, 1, 0))
    assert Bijections.simion_and_schmidt(Perm((0, 4, 3, 2, 1))) == Perm((0, 1, 2, 3, 4))
    assert Bijections.simion_and_schmidt(Perm((1, 0, 4, 3, 2))) == Perm((1, 0, 2, 3, 4))
    assert Bijections.simion_and_schmidt(Perm((1, 4, 0, 3, 2))) == Perm((1, 2, 0, 3, 4))
    assert Bijections.simion_and_schmidt(Perm((1, 4, 3, 0, 2))) == Perm((1, 2, 3, 0, 4))
    assert Bijections.simion_and_schmidt(Perm((1, 4, 3, 2, 0))) == Perm((1, 2, 3, 4, 0))
    assert Bijections.simion_and_schmidt(Perm((2, 0, 4, 3, 1))) == Perm((2, 0, 1, 3, 4))
    assert Bijections.simion_and_schmidt(Perm((2, 1, 0, 4, 3))) == Perm((2, 1, 0, 3, 4))
    assert Bijections.simion_and_schmidt(Perm((2, 1, 4, 0, 3))) == Perm((2, 1, 3, 0, 4))
    assert Bijections.simion_and_schmidt(Perm((2, 1, 4, 3, 0))) == Perm((2, 1, 3, 4, 0))
    assert Bijections.simion_and_schmidt(Perm((2, 4, 0, 3, 1))) == Perm((2, 3, 0, 1, 4))
    assert Bijections.simion_and_schmidt(Perm((2, 4, 1, 0, 3))) == Perm((2, 3, 1, 0, 4))
    assert Bijections.simion_and_schmidt(Perm((2, 4, 1, 3, 0))) == Perm((2, 3, 1, 4, 0))
    assert Bijections.simion_and_schmidt(Perm((2, 4, 3, 0, 1))) == Perm((2, 3, 4, 0, 1))
    assert Bijections.simion_and_schmidt(Perm((2, 4, 3, 1, 0))) == Perm((2, 3, 4, 1, 0))
    assert Bijections.simion_and_schmidt(Perm((3, 0, 4, 2, 1))) == Perm((3, 0, 1, 2, 4))
    assert Bijections.simion_and_schmidt(Perm((3, 1, 0, 4, 2))) == Perm((3, 1, 0, 2, 4))
    assert Bijections.simion_and_schmidt(Perm((3, 1, 4, 0, 2))) == Perm((3, 1, 2, 0, 4))
    assert Bijections.simion_and_schmidt(Perm((3, 1, 4, 2, 0))) == Perm((3, 1, 2, 4, 0))
    assert Bijections.simion_and_schmidt(Perm((3, 2, 0, 4, 1))) == Perm((3, 2, 0, 1, 4))

    # Examples from article
    assert Bijections.simion_and_schmidt(
        Perm.to_standard((6, 8, 3, 2, 7, 1, 5, 4))
    ) == Perm.to_standard((6, 7, 3, 2, 4, 1, 5, 8))
    assert Bijections.simion_and_schmidt(
        Perm.to_standard((6, 5, 10, 9, 3, 1, 8, 7, 4, 2))
    ) == Perm.to_standard((6, 5, 7, 8, 3, 1, 2, 4, 9, 10))
    assert Bijections.simion_and_schmidt(
        Perm.to_standard((6, 7, 3, 2, 4, 1, 5, 8)), inverse=True
    ) == Perm.to_standard((6, 8, 3, 2, 7, 1, 5, 4))
    assert Bijections.simion_and_schmidt(
        Perm.to_standard((6, 5, 7, 8, 3, 1, 2, 4, 9, 10)), inverse=True
    ) == Perm.to_standard((6, 5, 10, 9, 3, 1, 8, 7, 4, 2))

    for p in Perm.first(500):
        try:
            assert (
                Bijections.simion_and_schmidt(Bijections.simion_and_schmidt(p), True)
                == p
            )
        except ValueError:
            pass
