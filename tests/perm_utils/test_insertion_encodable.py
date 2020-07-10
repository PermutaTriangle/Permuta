from permuta import Perm
from permuta.perm_utils import InsertionEncodablePerms


def test_is_insertion_encodable_rightmost():
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0, 1)),
            Perm((0, 1, 2)),
            Perm((4, 0, 2, 3, 5, 1)),
            Perm((0, 6, 3, 4, 2, 5, 1)),
            Perm((6, 0, 3, 7, 5, 1, 2, 4)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm(()),
            Perm((0, 1)),
            Perm((1, 0)),
            Perm((3, 0, 1, 2)),
            Perm((2, 1, 3, 0, 4)),
            Perm((4, 1, 3, 2, 5, 0)),
            Perm((5, 1, 2, 3, 4, 0)),
            Perm((2, 0, 4, 1, 5, 6, 3)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0,)),
            Perm((1, 0, 2, 3)),
            Perm((0, 4, 1, 2, 3)),
            Perm((6, 0, 1, 7, 4, 5, 2, 3)),
            Perm((7, 3, 6, 4, 2, 5, 1, 0)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm(()),
            Perm((1, 0)),
            Perm((2, 1, 0)),
            Perm((0, 3, 1, 2)),
            Perm((3, 2, 0, 5, 7, 4, 6, 1)),
            Perm((4, 1, 5, 7, 0, 3, 2, 6)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
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
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((3, 2, 1, 4, 0)),
            Perm((4, 2, 3, 0, 1)),
            Perm((2, 3, 4, 0, 1, 5)),
            Perm((3, 2, 5, 4, 0, 1)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((4, 2, 5, 0, 3, 1)), Perm((6, 5, 3, 4, 1, 0, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((2, 1, 0)), Perm((3, 1, 2, 0))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((6, 1, 3, 0, 2, 4, 5)), Perm((4, 3, 5, 6, 0, 2, 1, 7))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((1, 0, 2)), Perm((0, 2, 3, 1, 4))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0, 1, 2)),
            Perm((0, 2, 1)),
            Perm((1, 0, 2, 3)),
            Perm((3, 1, 0, 2)),
            Perm((3, 4, 1, 2, 0)),
            Perm((1, 5, 2, 3, 0, 4)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((2, 0, 1)),
            Perm((0, 2, 3, 1)),
            Perm((3, 1, 0, 2)),
            Perm((3, 2, 1, 4, 0)),
            Perm((4, 0, 2, 3, 1)),
            Perm((4, 2, 0, 5, 1, 3)),
            Perm((6, 5, 0, 2, 7, 4, 3, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((1, 0, 2)),
            Perm((1, 2, 0)),
            Perm((2, 1, 0)),
            Perm((3, 6, 1, 5, 0, 2, 4)),
            Perm((6, 1, 2, 5, 4, 3, 0)),
            Perm((5, 4, 6, 0, 3, 2, 7, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((1, 0, 2)), Perm((1, 3, 2, 0))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((1, 2, 0)),
            Perm((2, 3, 0, 1)),
            Perm((3, 2, 1, 0)),
            Perm((1, 3, 2, 0, 4)),
            Perm((2, 1, 6, 0, 5, 4, 3)),
            Perm((4, 5, 0, 2, 3, 6, 7, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((2, 1, 0)),
            Perm((1, 2, 0, 3)),
            Perm((2, 0, 1, 3, 4)),
            Perm((4, 0, 1, 2, 3)),
            Perm((1, 3, 0, 5, 2, 4)),
            Perm((1, 5, 3, 0, 2, 4)),
            Perm((4, 3, 5, 0, 2, 1, 6)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((1, 0, 2)),
            Perm((2, 3, 1, 0)),
            Perm((0, 4, 1, 3, 2)),
            Perm((6, 3, 5, 1, 2, 4, 0)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((0, 1, 2)), Perm((4, 2, 5, 3, 1, 0)), Perm((1, 2, 3, 0, 5, 6, 4))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((1, 2, 0)), Perm((2, 4, 0, 1, 3)), Perm((7, 5, 4, 3, 1, 0, 2, 6))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0, 1, 2)),
            Perm((1, 2, 0)),
            Perm((1, 0, 3, 2)),
            Perm((2, 0, 3, 1)),
            Perm((5, 3, 2, 4, 0, 1)),
            Perm((2, 0, 3, 4, 6, 5, 1)),
            Perm((5, 1, 6, 2, 7, 0, 4, 3)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0, 2, 1)),
            Perm((2, 0, 1)),
            Perm((2, 0, 3, 1, 4)),
            Perm((4, 0, 3, 1, 2)),
            Perm((4, 3, 1, 2, 0)),
            Perm((4, 2, 5, 1, 0, 3)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0, 2, 1)),
            Perm((1, 2, 0)),
            Perm((0, 3, 1, 2)),
            Perm((1, 0, 3, 2)),
            Perm((2, 4, 1, 0, 3)),
            Perm((4, 3, 0, 1, 2)),
            Perm((2, 5, 0, 3, 6, 4, 1)),
            Perm((5, 7, 1, 6, 3, 4, 0, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0, 2, 1)),
            Perm((2, 0, 1, 3)),
            Perm((1, 3, 0, 2, 4)),
            Perm((5, 0, 4, 3, 2, 7, 6, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0, 2, 1)),
            Perm((2, 1, 0)),
            Perm((3, 0, 2, 1)),
            Perm((0, 1, 2, 3, 4)),
            Perm((0, 1, 3, 2, 4)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((0, 1, 2)),
            Perm((2, 0, 1, 3)),
            Perm((2, 1, 3, 0)),
            Perm((1, 0, 4, 2, 3)),
            Perm((1, 6, 2, 3, 4, 0, 5)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((2, 0, 1)),
            Perm((3, 1, 0, 4, 2)),
            Perm((1, 6, 4, 2, 0, 3, 7, 5)),
            Perm((2, 6, 1, 5, 4, 7, 0, 3)),
            Perm((3, 0, 7, 2, 1, 4, 5, 6)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((1, 0, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((2, 0, 1)),
            Perm((3, 1, 0, 2)),
            Perm((1, 0, 5, 2, 4, 3)),
            Perm((4, 3, 0, 5, 6, 1, 2)),
            Perm((1, 2, 5, 6, 7, 3, 0, 4)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((3, 4, 2, 1, 0)),
            Perm((3, 6, 2, 0, 5, 4, 1)),
            Perm((6, 3, 0, 2, 4, 5, 1)),
            Perm((5, 7, 0, 4, 2, 1, 3, 6)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((3, 1, 0, 2)),
            Perm((4, 0, 2, 3, 1)),
            Perm((2, 5, 4, 1, 0, 3)),
            Perm((0, 6, 1, 2, 4, 5, 3)),
            Perm((6, 2, 4, 1, 5, 7, 3, 0)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((1, 2, 0)),
            Perm((1, 2, 0, 3)),
            Perm((1, 5, 7, 2, 3, 4, 6, 0)),
            Perm((3, 6, 7, 4, 5, 2, 0, 1)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((2, 5, 1, 3, 0, 4))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((4, 0, 3, 1, 2)), Perm((1, 3, 5, 2, 0, 4)), Perm((1, 5, 4, 0, 3, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((1, 2, 0)), Perm((4, 1, 2, 5, 0, 3)), Perm((1, 4, 0, 6, 2, 3, 7, 5))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((1, 2, 0)),
            Perm((3, 4, 1, 5, 2, 0)),
            Perm((1, 4, 3, 5, 6, 2, 0)),
            Perm((3, 2, 4, 1, 6, 5, 0)),
            Perm((3, 0, 4, 2, 6, 7, 5, 1)),
            Perm((4, 1, 3, 6, 5, 2, 7, 0)),
            Perm((4, 2, 5, 0, 6, 1, 3, 7)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((2, 1, 3, 0)),
            Perm((2, 1, 3, 0, 4)),
            Perm((4, 0, 3, 1, 2)),
            Perm((1, 3, 4, 2, 5, 0)),
            Perm((2, 0, 6, 4, 1, 3, 5)),
            Perm((3, 4, 1, 6, 2, 5, 7, 0)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((1, 3, 2, 0)), Perm((0, 4, 2, 1, 3)), Perm((4, 0, 3, 2, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [
            Perm((2, 1, 3, 0)),
            Perm((3, 1, 2, 0)),
            Perm((1, 2, 0, 4, 3)),
            Perm((4, 2, 1, 0, 3)),
            Perm((0, 1, 2, 5, 3, 4)),
            Perm((3, 2, 5, 4, 0, 1)),
            Perm((2, 5, 7, 3, 4, 0, 6, 1)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((3, 5, 0, 1, 4, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_rightmost(
        [Perm((0, 1, 2)), Perm((6, 1, 3, 0, 4, 2, 5, 7))]
    )


def test_is_insertion_encodable_maximum():
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((0,)), Perm((0, 1)), Perm((2, 0, 1, 3)), Perm((2, 1, 3, 0))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 1, 2)),
            Perm((1, 2, 0)),
            Perm((0, 1, 2, 4, 3)),
            Perm((2, 0, 4, 1, 3)),
            Perm((3, 0, 6, 1, 4, 2, 5)),
            Perm((3, 5, 1, 4, 6, 0, 2)),
            Perm((6, 1, 2, 3, 0, 5, 7, 4)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((0, 2, 1)), Perm((2, 1, 0)), Perm((3, 1, 2, 0, 4, 5))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((1, 2, 0)),
            Perm((2, 0, 1)),
            Perm((2, 3, 1, 0)),
            Perm((3, 1, 4, 0, 2)),
            Perm((0, 5, 4, 1, 3, 2)),
            Perm((3, 2, 5, 4, 0, 1)),
            Perm((0, 5, 3, 6, 4, 1, 7, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((1, 2, 0)),
            Perm((2, 1, 0)),
            Perm((1, 2, 0, 3)),
            Perm((2, 3, 1, 0, 4)),
            Perm((1, 2, 5, 6, 3, 4, 0)),
            Perm((5, 4, 6, 1, 0, 3, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((2, 1, 0, 3)), Perm((3, 1, 0, 2)), Perm((0, 1, 4, 2, 3))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 1, 2)),
            Perm((0, 2, 1)),
            Perm((2, 0, 1)),
            Perm((2, 1, 0)),
            Perm((1, 3, 2, 0)),
            Perm((1, 4, 3, 2, 0)),
            Perm((1, 2, 4, 0, 3, 6, 5)),
            Perm((1, 7, 0, 3, 4, 5, 6, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((2, 0, 1)),
            Perm((1, 2, 3, 0)),
            Perm((3, 0, 2, 1, 4)),
            Perm((4, 1, 6, 3, 0, 5, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((1, 0)), Perm((0, 2, 1)), Perm((1, 2, 0)), Perm((2, 1, 0))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm(()), Perm((0, 1, 3, 2))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 2, 1)),
            Perm((0, 1, 2, 3)),
            Perm((0, 3, 5, 1, 4, 2)),
            Perm((3, 5, 2, 6, 0, 1, 4, 7)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((2, 0, 1, 3)),
            Perm((3, 1, 2, 0)),
            Perm((3, 2, 1, 0)),
            Perm((2, 3, 4, 1, 0)),
            Perm((4, 2, 0, 3, 5, 1)),
            Perm((6, 5, 4, 3, 7, 1, 2, 0)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((0, 1, 2, 3)), Perm((3, 2, 5, 1, 4, 0))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((0, 1)), Perm((0, 1, 2)), Perm((2, 1, 4, 0, 3)), Perm((3, 2, 0, 1, 4))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 1, 2)),
            Perm((0, 2, 1)),
            Perm((0, 2, 1, 4, 3)),
            Perm((2, 1, 4, 3, 0)),
            Perm((2, 4, 3, 5, 1, 0)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 1, 2)),
            Perm((2, 0, 1)),
            Perm((0, 4, 2, 1, 3)),
            Perm((1, 0, 3, 4, 2)),
            Perm((3, 2, 4, 0, 1)),
            Perm((1, 4, 5, 3, 0, 2)),
            Perm((0, 4, 2, 5, 1, 3, 6)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 2, 1)),
            Perm((0, 3, 2, 1)),
            Perm((1, 2, 3, 0)),
            Perm((1, 2, 3, 4, 0)),
            Perm((1, 4, 0, 3, 2)),
            Perm((4, 0, 1, 5, 2, 3)),
            Perm((3, 6, 1, 2, 0, 5, 4)),
            Perm((4, 0, 5, 1, 6, 2, 3)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 2, 1)),
            Perm((1, 2, 0, 3)),
            Perm((1, 3, 4, 0, 2)),
            Perm((1, 2, 5, 4, 3, 0)),
            Perm((5, 0, 2, 1, 4, 3)),
            Perm((4, 5, 2, 6, 3, 1, 0)),
            Perm((5, 0, 1, 4, 6, 3, 2)),
            Perm((5, 0, 3, 1, 6, 2, 4)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 2, 1)),
            Perm((1, 2, 0)),
            Perm((3, 1, 2, 0)),
            Perm((3, 2, 4, 0, 1)),
            Perm((2, 0, 5, 1, 3, 4)),
            Perm((3, 5, 0, 1, 4, 2, 7, 6)),
            Perm((4, 5, 2, 0, 3, 6, 1, 7)),
            Perm((6, 3, 2, 0, 1, 7, 4, 5)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 3, 2, 1)),
            Perm((1, 2, 3, 0)),
            Perm((0, 2, 1, 4, 3)),
            Perm((6, 1, 0, 5, 3, 4, 2)),
            Perm((6, 0, 2, 5, 1, 4, 7, 3)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((3, 0, 5, 2, 4, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((1, 0, 2)),
            Perm((1, 3, 2, 0)),
            Perm((1, 5, 4, 2, 0, 3)),
            Perm((4, 2, 0, 3, 5, 1)),
            Perm((4, 3, 2, 0, 5, 1)),
            Perm((5, 1, 2, 4, 3, 0, 6)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((2, 0, 1)),
            Perm((1, 2, 0, 4, 3)),
            Perm((3, 0, 2, 1, 4, 5)),
            Perm((5, 3, 2, 0, 1, 6, 4)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((0, 4, 3, 1, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((0, 2, 1)), Perm((0, 4, 2, 3, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((2, 3, 1, 5, 0, 4)), Perm((6, 2, 4, 1, 3, 7, 5, 0))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 4, 2, 1, 3)),
            Perm((1, 4, 0, 2, 3)),
            Perm((3, 1, 2, 5, 6, 0, 4)),
            Perm((0, 4, 6, 5, 7, 1, 2, 3)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((1, 0, 3, 4, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((2, 0, 1, 3))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((1, 3, 2, 4, 0))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 2, 1, 3)),
            Perm((0, 2, 3, 1)),
            Perm((0, 5, 3, 1, 2, 6, 4)),
            Perm((2, 4, 3, 0, 1, 6, 7, 5)),
            Perm((2, 7, 1, 4, 5, 6, 0, 3)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((3, 0, 2, 1)),
            Perm((3, 1, 2, 0)),
            Perm((3, 1, 0, 4, 2)),
            Perm((4, 0, 2, 3, 1)),
            Perm((4, 0, 3, 1, 2)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((1, 5, 6, 4, 2, 0, 3))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((3, 2, 1, 0, 4)),
            Perm((4, 3, 2, 0, 5, 1)),
            Perm((5, 4, 2, 3, 0, 1)),
            Perm((0, 3, 2, 1, 4, 6, 5)),
            Perm((2, 3, 0, 5, 1, 6, 4)),
            Perm((3, 6, 2, 4, 1, 0, 5)),
            Perm((0, 5, 3, 4, 2, 6, 7, 1)),
            Perm((0, 6, 4, 3, 7, 1, 5, 2)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((1, 2, 0)), Perm((4, 2, 5, 0, 1, 3)), Perm((6, 3, 5, 1, 7, 4, 0, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((3, 0, 2, 1)), Perm((4, 2, 1, 3, 0))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((3, 2, 0, 1)), Perm((6, 1, 3, 2, 4, 0, 5))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 2, 3, 1)),
            Perm((0, 3, 2, 1)),
            Perm((3, 0, 1, 2)),
            Perm((4, 3, 2, 0, 5, 1)),
            Perm((1, 0, 6, 4, 3, 5, 2)),
            Perm((3, 1, 6, 2, 5, 0, 4)),
            Perm((5, 2, 6, 7, 0, 3, 1, 4)),
            Perm((7, 1, 6, 2, 5, 0, 4, 3)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [Perm((0, 2, 1)), Perm((3, 1, 2, 0))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable_maximum(
        [
            Perm((0, 2, 1)),
            Perm((4, 0, 2, 1, 3)),
            Perm((2, 5, 4, 1, 3, 0)),
            Perm((3, 5, 4, 0, 2, 1)),
            Perm((1, 0, 4, 2, 3, 6, 5)),
            Perm((6, 3, 2, 0, 5, 1, 4)),
            Perm((4, 0, 1, 2, 3, 5, 6, 7)),
        ]
    )


def test_is_insertion_encodable():
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm(()), Perm((0, 1)), Perm((0, 1, 2))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 3, 2, 1)),
            Perm((0, 2, 3, 4, 1)),
            Perm((3, 0, 1, 2, 4)),
            Perm((4, 2, 1, 0, 3, 5)),
            Perm((0, 2, 1, 4, 6, 3, 5)),
            Perm((6, 2, 1, 0, 5, 4, 3)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 1)), Perm((1, 0)), Perm((1, 0, 3, 2))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable([Perm(()), Perm((1, 0))])
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 1, 2)),
            Perm((2, 0, 1)),
            Perm((0, 2, 4, 3, 1)),
            Perm((1, 2, 4, 0, 3)),
            Perm((3, 2, 4, 1, 5, 0)),
            Perm((2, 0, 3, 6, 4, 1, 5)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm((1, 0)), Perm((0, 1, 2)), Perm((0, 3, 1, 2)), Perm((1, 3, 2, 0))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((2, 1, 0)),
            Perm((0, 3, 1, 2)),
            Perm((0, 3, 2, 1)),
            Perm((3, 2, 1, 0)),
            Perm((2, 1, 3, 5, 0, 4)),
            Perm((3, 1, 5, 2, 4, 0)),
            Perm((5, 1, 4, 3, 0, 2, 6)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm(()), Perm((1, 0)), Perm((2, 0, 1)), Perm((0, 1, 2, 4, 3))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm(()), Perm((0,)), Perm((0, 1)), Perm((1, 0)), Perm((0, 3, 1, 2, 4))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 2, 1)),
            Perm((3, 2, 0, 1)),
            Perm((2, 1, 0, 3, 4)),
            Perm((3, 4, 2, 0, 5, 1)),
            Perm((4, 2, 7, 5, 0, 6, 3, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable([Perm(()), Perm((2, 1, 0))])
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((2, 0, 1)),
            Perm((3, 0, 1, 2)),
            Perm((1, 0, 2, 3, 4)),
            Perm((2, 3, 0, 1, 4)),
            Perm((3, 4, 1, 0, 2)),
            Perm((4, 3, 1, 6, 0, 7, 2, 5)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 1, 2)),
            Perm((1, 2, 0)),
            Perm((0, 2, 1, 3)),
            Perm((0, 3, 2, 1)),
            Perm((3, 0, 1, 2)),
            Perm((1, 0, 2, 4, 5, 6, 3)),
            Perm((1, 3, 6, 7, 2, 5, 4, 0)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm(()), Perm((0,)), Perm((1, 0)), Perm((4, 0, 1, 2, 3))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 1, 2)),
            Perm((2, 1, 0)),
            Perm((1, 2, 0, 3, 4)),
            Perm((3, 1, 0, 4, 2)),
            Perm((0, 5, 1, 4, 3, 2, 6)),
            Perm((2, 5, 4, 3, 6, 0, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 0, 2)),
            Perm((2, 3, 1, 0)),
            Perm((0, 1, 4, 3, 2)),
            Perm((0, 4, 3, 1, 2)),
            Perm((4, 0, 1, 3, 2)),
            Perm((0, 3, 2, 1, 5, 4)),
            Perm((2, 4, 0, 3, 5, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((2, 0, 1)),
            Perm((3, 0, 1, 2)),
            Perm((0, 1, 4, 3, 2)),
            Perm((0, 5, 4, 7, 6, 3, 1, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm(()), Perm((1, 0, 2)), Perm((2, 0, 1, 3)), Perm((0, 3, 1, 2, 4))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 2, 0)),
            Perm((2, 0, 1)),
            Perm((2, 1, 0)),
            Perm((3, 0, 2, 1)),
            Perm((1, 4, 2, 3, 5, 0)),
            Perm((1, 5, 0, 2, 3, 7, 6, 4)),
            Perm((4, 6, 5, 0, 2, 1, 3, 7)),
            Perm((7, 0, 1, 6, 3, 5, 4, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 2, 1)),
            Perm((2, 0, 1, 3)),
            Perm((0, 3, 2, 4, 1)),
            Perm((3, 4, 2, 0, 1)),
            Perm((1, 4, 5, 2, 0, 3)),
            Perm((4, 5, 3, 2, 0, 1)),
            Perm((6, 3, 0, 1, 2, 5, 4)),
            Perm((4, 3, 7, 5, 2, 1, 6, 0)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable([Perm((0,))])
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 1, 2)),
            Perm((0, 2, 1)),
            Perm((2, 0, 1)),
            Perm((2, 3, 1, 0, 4)),
            Perm((4, 1, 3, 0, 2)),
            Perm((1, 3, 2, 0, 6, 4, 5)),
            Perm((1, 4, 5, 3, 2, 6, 0)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((3, 2, 1, 0)),
            Perm((1, 0, 2, 3, 4)),
            Perm((3, 1, 4, 0, 2, 7, 5, 6)),
            Perm((4, 5, 1, 7, 0, 6, 3, 2)),
            Perm((6, 5, 2, 4, 3, 0, 1, 7)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0,)), Perm((0, 1)), Perm((1, 2, 0)), Perm((2, 1, 0))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm((2, 0, 1)), Perm((2, 1, 3, 0, 4))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 0, 2)),
            Perm((0, 2, 3, 1)),
            Perm((2, 1, 3, 0)),
            Perm((3, 0, 4, 1, 2)),
            Perm((6, 5, 4, 2, 0, 3, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 2, 1)),
            Perm((2, 0, 1)),
            Perm((2, 5, 4, 1, 0, 3)),
            Perm((3, 2, 1, 5, 0, 4)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 0, 2, 3)),
            Perm((1, 3, 2, 0)),
            Perm((2, 1, 3, 0, 4)),
            Perm((5, 2, 1, 4, 3, 0)),
            Perm((0, 5, 1, 3, 6, 4, 2)),
            Perm((1, 4, 0, 2, 3, 5, 6)),
            Perm((6, 1, 2, 0, 3, 5, 4)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm(()), Perm((1, 0)), Perm((1, 2, 0, 3)), Perm((3, 1, 0, 2))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 2, 1)),
            Perm((1, 0, 2)),
            Perm((1, 2, 0)),
            Perm((3, 1, 2, 5, 4, 0)),
            Perm((0, 2, 3, 5, 6, 4, 1)),
            Perm((4, 5, 6, 3, 1, 0, 2)),
            Perm((0, 4, 6, 7, 2, 3, 5, 1)),
            Perm((7, 5, 3, 6, 2, 4, 0, 1)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 1)), Perm((0, 1, 2)), Perm((1, 3, 0, 2)), Perm((0, 3, 4, 2, 1))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 0, 2)),
            Perm((2, 0, 1)),
            Perm((1, 3, 4, 0, 2)),
            Perm((2, 6, 4, 5, 0, 1, 3)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 2, 0)),
            Perm((2, 1, 0)),
            Perm((0, 2, 3, 1)),
            Perm((0, 2, 3, 1, 4)),
            Perm((0, 5, 3, 2, 4, 1)),
            Perm((0, 4, 6, 1, 5, 3, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 2, 0)),
            Perm((0, 2, 1, 3)),
            Perm((0, 3, 2, 1)),
            Perm((1, 0, 2, 3)),
            Perm((3, 0, 1, 2, 4)),
            Perm((4, 0, 1, 3, 2)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm(()), Perm((3, 1, 2, 0)), Perm((1, 0, 3, 2, 4)), Perm((4, 2, 1, 0, 3))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm((1, 2, 3, 0)), Perm((2, 1, 0, 3)), Perm((2, 1, 3, 0))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 2, 0, 3)),
            Perm((1, 2, 3, 0)),
            Perm((4, 3, 0, 2, 1)),
            Perm((2, 1, 4, 7, 6, 3, 0, 5)),
            Perm((7, 4, 1, 3, 6, 5, 2, 0)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 2, 1)),
            Perm((2, 3, 1, 0)),
            Perm((3, 1, 0, 2)),
            Perm((3, 1, 2, 0, 4)),
            Perm((2, 3, 1, 0, 4, 5)),
            Perm((1, 4, 7, 2, 6, 0, 5, 3)),
            Perm((5, 0, 3, 1, 7, 2, 4, 6)),
        ]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [Perm(()), Perm((0, 1, 3, 2)), Perm((2, 1, 4, 3, 0))]
    )
    assert InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 1, 2)),
            Perm((1, 0, 3, 2)),
            Perm((0, 1, 4, 3, 2)),
            Perm((1, 4, 3, 0, 2)),
            Perm((4, 2, 1, 3, 0, 5)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((3, 1, 6, 2, 7, 0, 4, 5))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 3, 1, 2)),
            Perm((1, 0, 3, 2)),
            Perm((1, 3, 2, 0, 4)),
            Perm((3, 2, 4, 0, 1)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 2, 0)),
            Perm((0, 2, 3, 1)),
            Perm((2, 3, 1, 4, 0)),
            Perm((2, 3, 4, 0, 1)),
            Perm((4, 3, 1, 5, 0, 2)),
            Perm((0, 3, 2, 6, 4, 1, 5)),
            Perm((1, 5, 3, 2, 7, 6, 0, 4)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((2, 0, 1, 3)),
            Perm((2, 1, 0, 3)),
            Perm((3, 1, 0, 2)),
            Perm((3, 1, 2, 0)),
            Perm((6, 5, 1, 4, 0, 3, 2)),
            Perm((4, 2, 1, 0, 6, 3, 7, 5)),
            Perm((6, 2, 5, 3, 4, 1, 0, 7)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((0, 3, 1, 2))])
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 2, 1, 3)),
            Perm((1, 2, 3, 0, 4)),
            Perm((3, 1, 0, 2, 4)),
            Perm((3, 1, 4, 2, 0)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((1, 0, 2)), Perm((3, 1, 2, 6, 4, 0, 5)), Perm((3, 4, 2, 1, 0, 5, 6))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 2, 1, 3)),
            Perm((2, 0, 3, 4, 1)),
            Perm((3, 4, 0, 1, 2)),
            Perm((4, 0, 3, 1, 2)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 4, 3, 2, 1)),
            Perm((1, 0, 2, 4, 3)),
            Perm((2, 3, 0, 1, 4)),
            Perm((3, 1, 4, 2, 0)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((4, 5, 0, 1, 2, 6, 3))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((0, 3, 4, 2, 1))])
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((3, 5, 6, 0, 7, 4, 2, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((3, 1, 2, 4, 0))])
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((1, 0, 3, 2)), Perm((2, 3, 0, 1, 4, 6, 5)), Perm((5, 4, 2, 1, 3, 0, 6))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 2, 1)), Perm((2, 7, 6, 5, 0, 4, 3, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((2, 0, 1, 3)),
            Perm((3, 0, 2, 1)),
            Perm((1, 2, 4, 0, 3)),
            Perm((2, 3, 4, 0, 1)),
            Perm((3, 0, 2, 4, 1)),
            Perm((4, 2, 1, 0, 3)),
            Perm((4, 3, 7, 2, 0, 6, 1, 5)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((2, 1, 0)), Perm((1, 3, 4, 2, 0)), Perm((0, 2, 6, 5, 1, 4, 3))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 4, 5, 1, 3, 2)),
            Perm((5, 0, 2, 4, 1, 3)),
            Perm((0, 2, 4, 3, 6, 5, 1)),
            Perm((3, 0, 4, 1, 2, 5, 7, 6)),
            Perm((7, 5, 1, 6, 3, 2, 4, 0)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((0, 2, 1, 3))])
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 1, 2)), Perm((0, 4, 5, 1, 3, 2)), Perm((0, 6, 3, 5, 4, 1, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 2, 1)), Perm((0, 2, 1, 3)), Perm((0, 2, 3, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((1, 2, 0)), Perm((2, 0, 3, 1)), Perm((2, 1, 3, 0))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((3, 2, 1, 0))])
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 1, 2)), Perm((2, 3, 0, 4, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((0, 1, 2, 3))])
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 3, 1, 2)), Perm((3, 1, 0, 2, 4))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((2, 1, 0)), Perm((0, 4, 3, 2, 1)), Perm((4, 3, 0, 2, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((2, 1, 3, 0))])
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((1, 0, 2))])
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((1, 3, 4, 0, 2, 6, 5)), Perm((4, 0, 3, 1, 6, 5, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((1, 2, 0)), Perm((3, 1, 2, 0))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((1, 2, 0, 3)),
            Perm((4, 2, 0, 5, 1, 3)),
            Perm((5, 4, 3, 1, 0, 2)),
            Perm((6, 1, 5, 4, 0, 2, 3)),
            Perm((7, 5, 4, 2, 0, 1, 6, 3)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((1, 3, 0, 2)), Perm((4, 0, 3, 2, 1))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((2, 3, 4, 5, 1, 0)),
            Perm((1, 0, 5, 3, 4, 2, 6)),
            Perm((0, 3, 6, 4, 1, 7, 2, 5)),
            Perm((0, 6, 5, 3, 2, 1, 4, 7)),
            Perm((4, 5, 1, 6, 0, 7, 3, 2)),
            Perm((6, 3, 2, 5, 1, 4, 0, 7)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable([Perm((0, 1, 2))])
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 1, 2)), Perm((0, 1, 2, 3, 4)), Perm((2, 5, 1, 0, 4, 6, 3))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [Perm((0, 3, 2, 1, 4)), Perm((4, 3, 1, 0, 2))]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((2, 0, 1)),
            Perm((4, 2, 0, 1, 5, 6, 3)),
            Perm((6, 7, 2, 4, 5, 1, 3, 0)),
            Perm((7, 4, 2, 1, 3, 0, 5, 6)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((0, 1, 2)),
            Perm((1, 3, 0, 2, 4)),
            Perm((0, 1, 5, 3, 4, 6, 2)),
            Perm((0, 2, 6, 1, 3, 4, 5)),
        ]
    )
    assert not InsertionEncodablePerms.is_insertion_encodable(
        [
            Perm((4, 2, 3, 1, 0)),
            Perm((0, 4, 6, 3, 5, 2, 1)),
            Perm((2, 3, 0, 6, 1, 5, 4)),
        ]
    )
