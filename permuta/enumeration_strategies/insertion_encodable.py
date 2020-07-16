from typing import Iterable

from permuta import Perm
from permuta.enumeration_strategies.abstract_strategy import (
    EnumerationStrategyWithSymmetry,
)
from permuta.permutils.insertion_encodable import InsertionEncodablePerms


class InsertionEncodingStrategy(EnumerationStrategyWithSymmetry):
    """Enumeration strategies related to the insertion encoding."""

    def _applies_to_symmetry(self, basis: Iterable[Perm]) -> bool:
        return InsertionEncodablePerms.is_insertion_encodable_maximum(basis)
