"""
Enumeration strategies related to the insertion encoding.
"""

from permuta.enumeration_strategies.abstract_strategy import \
    EnumerationStrategy
from permuta.permutils.insertion_encodable import is_insertion_encodable


class InsertionEncodingStrategy(EnumerationStrategy):

    def applies(self):
        return is_insertion_encodable(self.basis)
