"""
Enumeration strategies related to the insertion encoding.
"""

from permuta.enumeration_strategies.abstract_strategy import \
    EnumerationStrategyWithSymmetry
from permuta.permutils.insertion_encodable import \
    is_insertion_encodable_maximum


class InsertionEncodingStrategy(EnumerationStrategyWithSymmetry):

    def _applies_to_symmetry(self, b):
        return is_insertion_encodable_maximum(b)
