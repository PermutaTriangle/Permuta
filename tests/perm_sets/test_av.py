from math import factorial

import pytest

from permuta import MeshPatt, Perm
from permuta.perm_sets import Av
from permuta.perm_sets.basis import Basis, MeshBasis


# binom will be added to math in 3.8 so when pypy is compatible with 3.8, replace:
def binom(n, k):
    return factorial(n) // (factorial(n - k) * factorial(k))


def catalan(n):
    return binom(2 * n, n) // (n + 1)


test_classes = [
    ([[0, 1]], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
    ([[1, 0]], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
    ([[0, 1, 2]], [catalan(i) for i in range(8)]),
    ([[0, 2, 1]], [catalan(i) for i in range(8)]),
    ([[1, 0, 2]], [catalan(i) for i in range(8)]),
    ([[1, 2, 0]], [catalan(i) for i in range(8)]),
    ([[2, 0, 1]], [catalan(i) for i in range(8)]),
    ([[2, 1, 0]], [catalan(i) for i in range(8)]),
    ([[0, 2, 1, 3]], [1, 1, 2, 6, 23, 103, 513, 2762]),
    ([[0, 2, 3, 1]], [1, 1, 2, 6, 23, 103, 512, 2740, 15485]),
    ([[0, 3, 2, 1]], [1, 1, 2, 6, 23, 103, 513, 2761, 15767]),
    ([[1, 0, 2], [2, 1, 0]], [1, 1, 2, 4, 7, 11, 16, 22]),
    ([[0, 2, 1], [3, 2, 1, 0]], [1, 1, 2, 5, 13, 31, 66, 127]),
    ([[2, 1, 0], [1, 2, 3, 0]], [1, 1, 2, 5, 13, 34, 89, 233]),
    ([[3, 2, 1, 0], [3, 2, 0, 1]], [1, 1, 2, 6, 22, 90, 394, 1806]),
    ([[2, 3, 0, 1], [1, 3, 0, 2]], [1, 1, 2, 6, 22, 90, 395, 1823]),
    (
        [[3, 1, 2, 0], [2, 4, 0, 3, 1], [3, 1, 4, 0, 2], [2, 4, 0, 5, 1, 3]],
        [1, 1, 2, 6, 23, 101, 477, 2343, 11762],
    ),
    ([[0, 2, 1], [2, 1, 3, 4, 0]], [1, 1, 2, 5, 14, 41, 122, 365, 1094]),
]


@pytest.mark.parametrize("patts,enum", test_classes)
def test_avoiding_enumeration(patts, enum):
    patts = [Perm(patt) for patt in patts]
    basis = Basis(*patts)
    for n, cnt in enumerate(enum):
        # print(n, cnt)
        inst = Av(basis).of_length(n)
        gen = list(inst)
        # assert len(gen) == cnt
        assert len(gen) == len(set(gen))
        for perm in gen:
            assert perm.avoids(*patts)

    mx = len(enum) - 1
    cnt = [0 for _ in range(mx + 1)]
    for perm in Av(basis).up_to_length(mx):
        assert perm.avoids(*patts)
        cnt[len(perm)] += 1

    assert enum == cnt


def test_avoiding_generic_mesh_patterns():
    p = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mps = [MeshPatt(p, shading)]
    meshbasis = MeshBasis(*mps)
    avoiding_generic_basis = Av(meshbasis)
    enum = [1, 1, 2, 5, 15, 52, 203, 877]  # Bell numbers

    for n, cnt in enumerate(enum):
        inst = avoiding_generic_basis.of_length(n)
        gen = list(inst)
        assert len(gen) == cnt
        assert len(gen) == len(set(gen))
        for perm in gen:
            assert perm.avoids(*mps)
            assert perm in avoiding_generic_basis

    mx = len(enum) - 1
    cnt = [0 for _ in range(mx + 1)]
    for perm in Av(meshbasis).up_to_length(mx):
        assert perm.avoids(*mps)
        cnt[len(perm)] += 1

    assert enum == cnt


def test_avoiding_generic_finite_class():
    ts = [
        ([[0]], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ([[0, 1], [3, 2, 1, 0]], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]),
        ([[0, 1, 2], [3, 2, 1, 0]], [1, 1, 2, 5, 13, 25, 25, 0, 0, 0, 0, 0]),
    ]

    for patts, enum in ts:
        patts = [Perm(patt) for patt in patts]
        basis = Basis(*patts)
        for n, cnt in enumerate(enum):
            inst = Av(basis).of_length(n)
            gen = list(inst)
            assert len(gen) == cnt
            assert len(gen) == len(set(gen))
            for perm in gen:
                assert perm.avoids(*patts)

        mx = len(enum) - 1
        cnt = [0 for _ in range(mx + 1)]
        for perm in Av(basis).up_to_length(mx):
            assert perm.avoids(*patts)
            cnt[len(perm)] += 1

        assert enum == cnt


def test_is_subclass():
    av1 = Av.from_iterable((Perm((0,)),))
    av12_21 = Av.from_iterable((Perm((0, 1)), Perm((1, 0))))
    av123 = Av.from_iterable((Perm((0, 1, 2)),))
    av1234 = Av.from_iterable((Perm((0, 1, 2, 3)),))
    assert av1.is_subclass(av123)
    assert not av123.is_subclass(av1)
    assert av123.is_subclass(av1234)
    assert not av1234.is_subclass(av12_21)
    assert av12_21.is_subclass(av1234)
    assert av123.is_subclass(av123)
    av1324_1423_12345 = Av.from_iterable(
        (Perm((0, 2, 1, 3)), Perm((0, 3, 1, 2)), Perm((0, 1, 2, 3, 4, 5)))
    )
    av1324_1234 = Av.from_iterable((Perm((0, 2, 1, 3)), Perm((0, 1, 2, 3))))
    av1234_132 = Av.from_iterable((Perm((0, 1, 2, 3)), Perm((0, 2, 1))))
    assert av123.is_subclass(av1324_1423_12345)
    assert not av1324_1234.is_subclass(av1324_1423_12345)
    assert av1234_132.is_subclass(av1324_1423_12345)


def test_av_of_length():
    assert [
        sum(1 for _ in Av(Basis(Perm((0, 2, 1)))).of_length(i)) for i in range(8)
    ] == [1, 1, 2, 5, 14, 42, 132, 429]


def test_av_perm():
    p = Perm((0, 1))
    av = Av([p])
    for length in range(10):
        assert len(set(av.of_length(length))) == 1


def test_av_meshpatt():
    p = Perm((2, 0, 1))
    shading = ((2, 0), (2, 1), (2, 2), (2, 3))
    mp = MeshPatt(p, shading)
    av = Av([mp])
    enum = [1, 1, 2, 5, 15, 52, 203, 877]  # Bell numbers

    for n, cnt in enumerate(enum):
        inst = av.of_length(n)
        gen = list(inst)
        assert len(gen) == cnt


def test_enumeration():
    assert (
        Av.from_string("132").enumeration(8)
        == Av(Basis(Perm((0, 2, 1)))).enumeration(8)
        == [1, 1, 2, 5, 14, 42, 132, 429, 1430]
    )
    assert (
        Av.from_string("Av(123,231)").enumeration(8)
        == Av(Basis(Perm((0, 1, 2)), Perm((1, 2, 0)))).enumeration(8)
        == [1, 1, 2, 4, 7, 11, 16, 22, 29]
    )
    assert Av(
        (Perm((0, 1, 2)), MeshPatt(Perm((2, 0, 1)), [(0, 1), (1, 1), (2, 1), (3, 1)]))
    ).enumeration(7) == [1, 1, 2, 4, 8, 16, 32, 64]
    assert (
        Av.from_string("0123_2013_1023").enumeration(8)
        == Av(
            Basis(Perm((0, 1, 2, 3)), Perm((2, 0, 1, 3)), Perm((1, 0, 2, 3)))
        ).enumeration(8)
        == [1, 1, 2, 6, 21, 79, 309, 1237, 5026]
    )
    assert (
        Av.from_string("1243 1342 3241 3241").enumeration(8)
        == Av(
            Basis(
                Perm((0, 1, 3, 2)),
                Perm((0, 2, 3, 1)),
                Perm((2, 1, 3, 0)),
                Perm((2, 1, 3, 0)),
            )
        ).enumeration(8)
        == [1, 1, 2, 6, 21, 75, 262, 891, 2964]
    )
    assert (
        Av.from_string("Av(1342, 3124, 1432, 4312)").enumeration(8)
        == Av(
            Basis(
                Perm((0, 2, 3, 1)),
                Perm((2, 0, 1, 3)),
                Perm((0, 3, 2, 1)),
                Perm((3, 2, 0, 1)),
            )
        ).enumeration(8)
        == [1, 1, 2, 6, 20, 61, 169, 442, 1120]
    )


def test_generators():
    assert list(Av(Basis(Perm((0, 1)), Perm((1, 0)))).first(500)) == [
        Perm(),
        Perm((0,)),
    ]
    assert sorted(Av(Basis(Perm((0, 2, 1)), Perm((1, 2, 0)))).of_length(3)) == sorted(
        set(Perm.of_length(3)) - {Perm((0, 2, 1)), Perm((1, 2, 0))}
    )
    assert sorted(
        Av(Basis(Perm((0, 2, 1)), Perm((1, 2, 0)))).up_to_length(3)
    ) == sorted(set(Perm.up_to_length(3)) - {Perm((0, 2, 1)), Perm((1, 2, 0))})


def test_instance_variable_cache():
    Av.clear_cache()
    basis = Basis(Perm((0, 1)))
    av = Av(basis)
    assert basis in Av._CLASS_CACHE
    list(av.of_length(5))
    assert len(av.cache) == 6
    assert len(Av(Basis(Perm((0, 1)))).cache) == 6
    av2 = Av(Basis(Perm((0, 1))))
    assert len(av2.cache) == 6
    list(av2.of_length(10))
    assert len(av.cache) == 11
    assert len(av2.cache) == 11
    assert len(Av.from_string("12").cache) == 11
    assert len(Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0)))).cache) == 1
    list(Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0)))).of_length(5))
    assert len(Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0)))).cache) == 6
    assert (
        len(Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0)), Perm((1, 2, 0, 3)))).cache) == 6
    )
    assert len(Av(Basis(Perm((1, 2, 0)), Perm((2, 0, 1)))).cache) == 6
    for p in Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0)), Perm((1, 2, 0, 3)))).of_length(
        10
    ):
        pass
    assert len(Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0)))).cache) == 11
    Av.clear_cache()


def test_class_variable_cache():
    Av.clear_cache()
    assert len(Av._CLASS_CACHE) == 0
    assert Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0)))) is Av(
        Basis(Perm((2, 0, 1)), Perm((1, 2, 0)))
    )
    av = Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0))))
    assert av is Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0))))
    assert av is Av(Basis(Perm((2, 0, 1)), Perm((1, 2, 0)), Perm((1, 2, 0, 3))))
    assert len(Av._CLASS_CACHE) == 1
    av2 = Av(Basis(Perm((0, 1, 3, 2)), Perm((0, 2, 1))))
    assert len(Av._CLASS_CACHE) == 2
    assert av is not av2
    assert av2 is Av(Basis(Perm((0, 2, 1))))
    assert Av.from_string("132") is av2
    assert Basis(Perm((0, 2, 1))) in Av._CLASS_CACHE
    assert (
        Av._CLASS_CACHE[Basis(Perm((0, 2, 1)))]
        is Av._CLASS_CACHE[Basis(Perm((0, 1, 3, 2)), Perm((0, 2, 1)))]
    )
    assert Av((Perm((2, 0, 1)),)) is Av(Basis(Perm((2, 0, 1))))
    Av.clear_cache()
    assert len(Av._CLASS_CACHE) == 0


def test_valid_error_in_construction():
    with pytest.raises(ValueError):
        Av(Basis())
    with pytest.raises(ValueError):
        Av(Basis(Perm()))


def test_invalid_ops_with_mesh_patt():
    with pytest.raises(NotImplementedError):
        Av(MeshBasis(Perm((0, 1)))).is_finite()
    with pytest.raises(NotImplementedError):
        Av(MeshBasis(Perm((0, 1)))).is_insertion_encodable()
    with pytest.raises(NotImplementedError):
        Av(MeshBasis(Perm((0, 1)))).is_polynomial()


# Tests for right_juxtaposition


def test_right_juxtaposition_basic():
    """Test Av(21) | Av(12) = Av(213, 312)."""
    av_21 = Av(Basis(Perm((1, 0))))
    av_12 = Av(Basis(Perm((0, 1))))
    result = av_21.right_juxtaposition(av_12)
    expected_basis = {Perm((1, 0, 2)), Perm((2, 0, 1))}
    assert set(result.basis) == expected_basis


def test_right_juxtaposition_same_class():
    """Test Av(21) | Av(21) gives expected basis."""
    av_21 = Av(Basis(Perm((1, 0))))
    result = av_21.right_juxtaposition(av_21)
    # Basis should be {321, 2143, 2431} = {(2,1,0), (1,0,3,2), (1,3,2,0)}
    expected_basis = {Perm((2, 1, 0)), Perm((1, 0, 3, 2)), Perm((2, 0, 3, 1))}
    assert set(result.basis) == expected_basis


def test_right_juxtaposition_enumeration():
    """Test that juxtaposition class has correct enumeration."""
    av_21 = Av(Basis(Perm((1, 0))))
    av_12 = Av(Basis(Perm((0, 1))))
    result = av_21.right_juxtaposition(av_12)
    # [Av(21)|Av(12)] = permutations that can be split into decreasing|increasing
    # Enumeration: 1, 1, 2, 4, 8, 16, 32 (powers of 2 starting at n=2)
    assert result.enumeration(6) == [1, 1, 2, 4, 8, 16, 32]


def test_right_juxtaposition_multiple_basis_elements():
    """Test juxtaposition with multiple basis elements."""
    # Only contains empty and singleton permutations
    av_21_12 = Av(Basis(Perm((1, 0)), Perm((0, 1))))
    av_132 = Av(Basis(Perm((0, 2, 1))))
    result = av_21_12.right_juxtaposition(av_132)
    # The result should be a valid Av object with a minimized basis
    assert isinstance(result.basis, Basis)
    assert len(result.basis) > 0


def test_right_juxtaposition_longer_patterns():
    """Test juxtaposition with longer patterns."""
    av_132 = Av(Basis(Perm((0, 2, 1))))
    av_231 = Av(Basis(Perm((1, 2, 0))))
    result = av_132.right_juxtaposition(av_231)
    # Verify result is valid and has expected structure
    assert isinstance(result.basis, Basis)
    # All basis elements should have length between 3 and 6 (|b1|+|b2|-1 to |b1|+|b2|)
    for perm in result.basis:
        assert 5 <= len(perm) <= 6


def test_right_juxtaposition_mesh_basis_raises():
    """Test that juxtaposition with MeshBasis raises NotImplementedError."""
    av_classical = Av(Basis(Perm((1, 0))))
    av_mesh = Av(MeshBasis(Perm((0, 1))))
    with pytest.raises(NotImplementedError):
        av_classical.right_juxtaposition(av_mesh)
    with pytest.raises(NotImplementedError):
        av_mesh.right_juxtaposition(av_classical)


def test_right_juxtaposition_containment():
    """Test that permutations in the juxtaposition class can be split correctly."""
    av_21 = Av(Basis(Perm((1, 0))))
    av_12 = Av(Basis(Perm((0, 1))))
    result = av_21.right_juxtaposition(av_12)

    # Check some permutations that should be in the class
    # 21 can be split as (2)|(1) where (2) is decreasing and (1) is increasing
    assert Perm((1, 0)) in result
    # 12 can be split as ()|(12) where () is trivially decreasing and (12) is increasing
    assert Perm((0, 1)) in result
    # 1 is trivially in the class
    assert Perm((0,)) in result

    # Check some permutations that should NOT be in the class
    # 213 = (1,0,2) is a basis element, so not in the class
    assert Perm((1, 0, 2)) not in result
    # 312 = (2,0,1) is a basis element, so not in the class
    assert Perm((2, 0, 1)) not in result


# Tests for above_juxtaposition


def test_above_juxtaposition_basic():
    """Test basic above juxtaposition with Av(21) below and Av(12) above."""
    av_21 = Av(Basis(Perm((1, 0))))
    av_12 = Av(Basis(Perm((0, 1))))
    result = av_21.above_juxtaposition(av_12)
    # Result should be valid Av with Basis
    assert isinstance(result.basis, Basis)
    assert len(result.basis) > 0


def test_above_juxtaposition_inverse_relationship():
    """Test that above_juxtaposition relates to right_juxtaposition via inverses."""
    av_21 = Av(Basis(Perm((1, 0))))
    av_132 = Av(Basis(Perm((0, 2, 1))))

    # Compute above juxtaposition directly
    above_result = av_21.above_juxtaposition(av_132)

    # Compute via inverses manually
    av_21_inv = Av(Basis(*[p.inverse() for p in av_21.basis]))
    av_132_inv = Av(Basis(*[p.inverse() for p in av_132.basis]))
    right_result = av_21_inv.right_juxtaposition(av_132_inv)
    manual_result = Av(Basis(*[p.inverse() for p in right_result.basis]))

    # The bases should be equivalent
    assert set(above_result.basis) == set(manual_result.basis)


def test_above_juxtaposition_enumeration():
    """Test that above juxtaposition class has expected enumeration."""
    av_21 = Av(Basis(Perm((1, 0))))
    av_12 = Av(Basis(Perm((0, 1))))
    result = av_21.above_juxtaposition(av_12)
    # Permutations that can be split by value: lower values decreasing, upper increasing
    # This should give 2^(n-1) for n >= 1
    assert result.enumeration(6) == [1, 1, 2, 4, 8, 16, 32]


def test_above_juxtaposition_same_class():
    """Test above juxtaposition with the same class."""
    av_21 = Av(Basis(Perm((1, 0))))
    result = av_21.above_juxtaposition(av_21)
    # Should be valid and have a non-empty basis
    assert isinstance(result.basis, Basis)
    assert len(result.basis) > 0


def test_above_juxtaposition_longer_patterns():
    """Test above juxtaposition with longer patterns."""
    av_132 = Av(Basis(Perm((0, 2, 1))))
    av_231 = Av(Basis(Perm((1, 2, 0))))
    result = av_132.above_juxtaposition(av_231)
    # Verify result is valid
    assert isinstance(result.basis, Basis)
    # All basis elements should have length between 5 and 6
    for perm in result.basis:
        assert 5 <= len(perm) <= 6


def test_above_juxtaposition_mesh_basis_raises():
    """Test that above_juxtaposition with MeshBasis raises NotImplementedError."""
    av_classical = Av(Basis(Perm((1, 0))))
    av_mesh = Av(MeshBasis(Perm((0, 1))))
    with pytest.raises(NotImplementedError):
        av_classical.above_juxtaposition(av_mesh)
    with pytest.raises(NotImplementedError):
        av_mesh.above_juxtaposition(av_classical)
