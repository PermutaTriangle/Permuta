from random import randint

from permuta import Perm
from permuta.permutils.finite import is_finite


def test_is_finite():
    assert is_finite([Perm()])
    assert is_finite([Perm((0,))])
    for i in range(100):
        basis = [
            Perm.monotone_decreasing(randint(0, 100)),
            Perm.monotone_increasing(randint(0, 100)),
        ]
        basis.extend([Perm.random(randint(0, 100)) for _ in range(randint(0, 10))])
        assert is_finite(basis)
    assert not is_finite(
        (
            p
            for p in (Perm.random(randint(0, 100)) for _ in range(10))
            if not p.is_increasing()
        )
    )
    assert not is_finite(
        (
            p
            for p in (Perm.random(randint(0, 100)) for _ in range(10))
            if not p.is_decreasing()
        )
    )
    assert not is_finite([Perm((0, 1, 2))])
    assert not is_finite([Perm((2, 1, 0))])
    assert not is_finite((Perm.identity(i) for i in range(2, 10)))
    assert not is_finite((p for p in (Perm((1, 2, 0)), Perm((4, 1, 2, 0, 3)))))
    assert not is_finite((p for p in (Perm((1, 2)),)))
    # Old version failed for this
    assert is_finite((p for p in (Perm((0, 1)), Perm((1, 0)))))
