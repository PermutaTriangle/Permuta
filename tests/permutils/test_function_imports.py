from permuta import Perm
from permuta.permutils import (
    is_insertion_encodable,
    is_insertion_encodable_maximum,
    is_insertion_encodable_rightmost,
    is_non_polynomial,
    is_polynomial,
)


def test_functions_polynomial():
    assert is_polynomial(
        frozenset(
            {
                Perm((1, 0)),
                Perm((0, 2, 1, 3)),
                Perm((0, 1, 2)),
                Perm((2, 1, 0)),
                Perm((0, 2, 3, 1)),
            }
        )
    )
    assert is_non_polynomial(
        frozenset(
            {
                Perm((1, 0, 2, 3)),
                Perm((2, 0, 4, 1, 3)),
                Perm((2, 3, 4, 1, 0)),
                Perm((3, 4, 1, 0, 2)),
            }
        )
    )


def test_functions_insertion_encodable():
    assert is_insertion_encodable_rightmost(
        [
            Perm(()),
            Perm((1, 0)),
            Perm((0, 2, 1)),
            Perm((1, 2, 0)),
            Perm((0, 1, 4, 2, 3)),
            Perm((2, 3, 0, 1, 4)),
            Perm((4, 7, 3, 0, 1, 5, 6, 2)),
            Perm((4, 7, 3, 2, 5, 6, 0, 1)),
        ]
    )
    assert not is_insertion_encodable_rightmost(
        [
            Perm((3, 2, 1, 4, 0)),
            Perm((4, 2, 3, 0, 1)),
            Perm((2, 3, 4, 0, 1, 5)),
            Perm((3, 2, 5, 4, 0, 1)),
        ]
    )

    assert is_insertion_encodable_maximum(
        [
            Perm((0, 3, 2, 1)),
            Perm((1, 2, 3, 0)),
            Perm((0, 2, 1, 4, 3)),
            Perm((6, 1, 0, 5, 3, 4, 2)),
            Perm((6, 0, 2, 5, 1, 4, 7, 3)),
        ]
    )
    assert not is_insertion_encodable_maximum(
        [
            Perm((1, 0, 2)),
            Perm((1, 3, 2, 0)),
            Perm((1, 5, 4, 2, 0, 3)),
            Perm((4, 2, 0, 3, 5, 1)),
            Perm((4, 3, 2, 0, 5, 1)),
            Perm((5, 1, 2, 4, 3, 0, 6)),
        ]
    )

    assert is_insertion_encodable(
        [
            Perm((0, 3, 2, 1)),
            Perm((0, 2, 3, 4, 1)),
            Perm((3, 0, 1, 2, 4)),
            Perm((4, 2, 1, 0, 3, 5)),
            Perm((0, 2, 1, 4, 6, 3, 5)),
            Perm((6, 2, 1, 0, 5, 4, 3)),
        ]
    )
    assert not is_insertion_encodable(
        [
            Perm((0, 2, 1, 3)),
            Perm((1, 2, 3, 0, 4)),
            Perm((3, 1, 0, 2, 4)),
            Perm((3, 1, 4, 2, 0)),
        ]
    )
