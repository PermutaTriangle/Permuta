"""Tests for :class:`permuta.CyclicPerm`.

Many checks are pulled directly from Domagalski-Liang-Minnich-Sagan-Schmidt-
Sietsema, "Cyclic Pattern Containment and Avoidance" (arXiv:2106.02534).
"""

from math import comb

import pytest

from permuta import CyclicPerm, Perm


# ---------------------------------------------------------------------------
# Canonical form
# ---------------------------------------------------------------------------


def test_canonicalization_collapses_rotations():
    rotations = [
        (3, 1, 2, 4, 0),  # 42351
        (1, 2, 4, 0, 3),  # 23514
        (2, 4, 0, 3, 1),  # 35142
        (4, 0, 3, 1, 2),  # 51423
        (0, 3, 1, 2, 4),  # 14235
    ]
    classes = {CyclicPerm(r) for r in rotations}
    assert len(classes) == 1
    (only,) = classes
    assert only.representative() == Perm((0, 3, 1, 2, 4))


def test_representative_always_starts_with_zero():
    for n in range(6):
        for cp in CyclicPerm.of_length(n):
            if n:
                assert cp.representative()[0] == 0


def test_of_length_count():
    # n! / n distinct cyclic classes for n >= 1
    for n in range(1, 7):
        from math import factorial

        assert sum(1 for _ in CyclicPerm.of_length(n)) == factorial(n) // n


# ---------------------------------------------------------------------------
# Containment — the paper's opening example
# ---------------------------------------------------------------------------


def test_paper_opening_example():
    # "even though 42351 avoids 1234 we have that [42351] contains [1234]"
    sigma_linear = Perm.to_standard("42351")
    p_linear = Perm.to_standard("1234")
    assert sigma_linear.avoids(p_linear)

    sigma_cyclic = CyclicPerm.to_standard("42351")
    p_cyclic = CyclicPerm.to_standard("1234")
    assert sigma_cyclic.contains(p_cyclic)
    assert not sigma_cyclic.avoids(p_cyclic)


# ---------------------------------------------------------------------------
# Degenerate patterns in small S_k
# ---------------------------------------------------------------------------


def test_only_cyclic_pattern_in_S2():
    # "[12] is the unique cyclic permutation of length 2 and every [σ] of
    # length ≥ 2 contains it."
    p12 = CyclicPerm((0, 1))
    for n in range(2, 7):
        for cp in CyclicPerm.of_length(n):
            assert cp.contains(p12)


def test_S3_cyclic_avoidance():
    # "In [S_3] there are only the patterns [123] and [321], and these are
    # only avoided by [δ_n] and [ι_n], respectively."
    p123 = CyclicPerm((0, 1, 2))
    p321 = CyclicPerm((2, 1, 0))

    for n in range(3, 8):
        iota_n = CyclicPerm(Perm(range(n)))
        delta_n = CyclicPerm(Perm(range(n - 1, -1, -1)))

        avoiders_of_123 = [cp for cp in CyclicPerm.of_length(n) if cp.avoids(p123)]
        avoiders_of_321 = [cp for cp in CyclicPerm.of_length(n) if cp.avoids(p321)]
        assert avoiders_of_123 == [delta_n]
        assert avoiders_of_321 == [iota_n]


# ---------------------------------------------------------------------------
# Callan's single-pattern enumeration (paper §3)
# ---------------------------------------------------------------------------


def _callan_1234(n):
    return 2**n + 1 - 2 * n - comb(n, 3)


def _callan_1243(n):
    return 2 ** (n - 1) - n + 1


def _fib(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a


def _callan_1324(n):
    # F_{2n-3} with F_1 = F_2 = 1
    return _fib(2 * n - 3)


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6])
def test_callan_1234_and_1432(n):
    p1234 = CyclicPerm((0, 1, 2, 3))
    p1432 = CyclicPerm.to_standard("1432")
    count_1234 = sum(1 for cp in CyclicPerm.of_length(n) if cp.avoids(p1234))
    count_1432 = sum(1 for cp in CyclicPerm.of_length(n) if cp.avoids(p1432))
    assert count_1234 == _callan_1234(n)
    assert count_1432 == _callan_1234(n)  # trivial Wilf equivalence


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6])
def test_callan_1243_and_1342(n):
    p1243 = CyclicPerm.to_standard("1243")
    p1342 = CyclicPerm.to_standard("1342")
    count_1243 = sum(1 for cp in CyclicPerm.of_length(n) if cp.avoids(p1243))
    count_1342 = sum(1 for cp in CyclicPerm.of_length(n) if cp.avoids(p1342))
    assert count_1243 == _callan_1243(n)
    assert count_1342 == _callan_1243(n)


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6])
def test_callan_1324_and_1423(n):
    p1324 = CyclicPerm.to_standard("1324")
    p1423 = CyclicPerm.to_standard("1423")
    count_1324 = sum(1 for cp in CyclicPerm.of_length(n) if cp.avoids(p1324))
    count_1423 = sum(1 for cp in CyclicPerm.of_length(n) if cp.avoids(p1423))
    assert count_1324 == _callan_1324(n)
    assert count_1423 == _callan_1324(n)


# ---------------------------------------------------------------------------
# Cyclic Erdős–Szekeres (Theorem §2)
# ---------------------------------------------------------------------------


def test_cyclic_erdos_szekeres_small():
    # With m = n = 2 the theorem forces any [σ] in [S_{m*n+2}] = [S_6] to
    # contain [ι_{m+2}] = [1234] or [δ_{n+2}] = [4321].  And [S_{mn+1}] =
    # [S_5] still admits an avoider.
    p_iota = CyclicPerm((0, 1, 2, 3))
    p_delta = CyclicPerm((3, 2, 1, 0))

    # [S_6]: no avoider
    for cp in CyclicPerm.of_length(6):
        assert cp.contains(p_iota) or cp.contains(p_delta)

    # [S_5]: at least one avoider exists
    assert any(
        cp.avoids(p_iota) and cp.avoids(p_delta) for cp in CyclicPerm.of_length(5)
    )


# ---------------------------------------------------------------------------
# Three-pattern results (paper §4)
# ---------------------------------------------------------------------------


def test_three_pattern_1234_1324_1342():
    # Theorem 4.x: #Av_n([1234],[1324],[1342]) = 3 for n >= 4.
    basis = [
        CyclicPerm((0, 1, 2, 3)),
        CyclicPerm.to_standard("1324"),
        CyclicPerm.to_standard("1342"),
    ]
    for n in range(4, 8):
        count = sum(
            1 for cp in CyclicPerm.of_length(n) if cp.avoids_set(basis)
        )
        assert count == 3, f"n={n}: got {count}"


def test_three_pattern_1234_1243_1342():
    # Theorem 4.x: #Av_n([1234],[1243],[1342]) = 2 for n >= 5.
    basis = [
        CyclicPerm((0, 1, 2, 3)),
        CyclicPerm.to_standard("1243"),
        CyclicPerm.to_standard("1342"),
    ]
    for n in range(5, 8):
        count = sum(
            1 for cp in CyclicPerm.of_length(n) if cp.avoids_set(basis)
        )
        assert count == 2, f"n={n}: got {count}"


def test_three_pattern_1234_1342_1423():
    # Theorem 4.x: #Av_n([1234],[1342],[1423]) = n - 1 for n >= 2.
    basis = [
        CyclicPerm((0, 1, 2, 3)),
        CyclicPerm.to_standard("1342"),
        CyclicPerm.to_standard("1423"),
    ]
    for n in range(2, 8):
        count = sum(
            1 for cp in CyclicPerm.of_length(n) if cp.avoids_set(basis)
        )
        assert count == n - 1, f"n={n}: got {count}"


# ---------------------------------------------------------------------------
# Symmetries — the trivial cyclic Wilf equivalences
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("n", [4, 5, 6])
def test_trivial_wilf_equivalences(n):
    # [π] ≡ [π^r] ≡ [π^c] ≡ [π^{rc}]
    for p in CyclicPerm.of_length(4):
        count = sum(1 for cp in CyclicPerm.of_length(n) if cp.avoids(p))
        for sym in (p.reverse(), p.complement(), p.reverse_complement()):
            sym_count = sum(
                1 for cp in CyclicPerm.of_length(n) if cp.avoids(sym)
            )
            assert sym_count == count


# ---------------------------------------------------------------------------
# Cyclic descent statistic
# ---------------------------------------------------------------------------


def test_cdes_paper_example():
    # "π = 23514 has cyclic descents at indices 3 and 5 so cdes[π] = 2"
    # In 0-indexed, 23514 → 12403; the paper indexes from 1 so positions
    # 3 and 5 become 2 and 4 here (wrap-around descent 3 → 1).
    assert CyclicPerm.to_standard("23514").cdes() == 2


def test_cdes_is_rotation_invariant():
    base = CyclicPerm.to_standard("52143")
    rep = base.representative()
    expected = base.cdes()
    for k in range(len(rep)):
        rotated = CyclicPerm(rep.shift_left(k))
        assert rotated.cdes() == expected


# ---------------------------------------------------------------------------
# Housekeeping
# ---------------------------------------------------------------------------


def test_avoidance_of_longer_pattern_is_vacuous():
    short = CyclicPerm((0, 1))
    long_patt = CyclicPerm.to_standard("1234")
    assert short.avoids(long_patt)
    assert not short.contains(long_patt)


def test_eq_hash_repr():
    a = CyclicPerm((3, 1, 2, 4, 0))
    b = CyclicPerm((0, 3, 1, 2, 4))
    assert a == b
    assert hash(a) == hash(b)
    assert repr(a) == "CyclicPerm((0, 3, 1, 2, 4))"
    assert str(a) == "[03124]"


def test_occurrences_of():
    sigma = CyclicPerm.to_standard("42351")
    patt = CyclicPerm((0, 1, 2, 3))  # [1234] in paper notation

    copies = list(sigma.occurrences_of(patt))
    assert copies  # paper guarantees at least one
    for _rot_index, positions in copies:
        assert len(positions) == 4
        values = [sigma.representative()[i] for i in positions]
        standardized = Perm.to_standard(values)
        rotations_of_patt = list(patt.rotations())
        assert standardized in rotations_of_patt


def test_empty_and_length_one():
    empty = CyclicPerm(())
    single = CyclicPerm((0,))
    assert len(empty) == 0
    assert len(single) == 1
    assert empty.avoids(CyclicPerm((0, 1)))
    assert single.avoids(CyclicPerm((0, 1)))
    assert single.cdes() == 0
