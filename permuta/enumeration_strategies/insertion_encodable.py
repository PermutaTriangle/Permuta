"""
Enumeration strategies related to the insertion encoding.
"""

from permuta.enumeration_strategies.abstract_strategy import (
    EnumerationStrategyWithSymmetry,
)
from permuta.permutils.insertion_encodable import InsertionEncodablePerms


class InsertionEncodingStrategy(EnumerationStrategyWithSymmetry):
    def _applies_to_symmetry(self, b):
        return InsertionEncodablePerms.is_insertion_encodable_maximum(b)
