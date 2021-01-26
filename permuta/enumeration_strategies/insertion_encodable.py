from permuta.enumeration_strategies.abstract_strategy import EnumerationStrategy
from permuta.permutils.insertion_encodable import InsertionEncodablePerms
from permuta.permutils.symmetry import rotate_90_clockwise_set


class InsertionEncodingStrategy(EnumerationStrategy):
    """Enumeration strategies related to the insertion encoding."""

    def applies(self) -> bool:
        return InsertionEncodablePerms.is_insertion_encodable(
            self.basis
        ) or InsertionEncodablePerms.is_insertion_encodable(
            rotate_90_clockwise_set(self.basis)
        )

    @classmethod
    def reference(cls) -> str:
        return "The insertion encoding of permutations: Corollary 10"
