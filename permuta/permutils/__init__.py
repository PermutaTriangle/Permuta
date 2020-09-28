from .finite import is_finite
from .groups import dihedral_group
from .insertion_encodable import InsertionEncodablePerms
from .polynomial import PolyPerms
from .symmetry import (
    all_symmetry_sets,
    antidiagonal_set,
    complement_set,
    inverse_set,
    lex_min,
    reverse_set,
    rotate_90_clockwise_set,
    rotate_180_clockwise_set,
    rotate_270_clockwise_set,
)

is_insertion_encodable = InsertionEncodablePerms.is_insertion_encodable
is_insertion_encodable_maximum = InsertionEncodablePerms.is_insertion_encodable_maximum
is_insertion_encodable_rightmost = (
    InsertionEncodablePerms.is_insertion_encodable_rightmost
)
is_polynomial = PolyPerms.is_polynomial
is_non_polynomial = PolyPerms.is_non_polynomial

__all__ = [
    "is_insertion_encodable",
    "is_insertion_encodable_maximum",
    "is_insertion_encodable_rightmost",
    "is_polynomial",
    "is_non_polynomial",
    "InsertionEncodablePerms",
    "PolyPerms",
    "is_finite",
    "dihedral_group",
    "all_symmetry_sets",
    "antidiagonal_set",
    "complement_set",
    "inverse_set",
    "lex_min",
    "reverse_set",
    "rotate_90_clockwise_set",
    "rotate_180_clockwise_set",
    "rotate_270_clockwise_set",
]
