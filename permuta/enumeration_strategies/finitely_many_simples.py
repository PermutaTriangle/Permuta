from permuta.enumeration_strategies.abstract_strategy import EnumerationStrategy
from permuta.permutils.pin_words import (
    PinWords,
)


class FinitelyManySimplesStrategy(EnumerationStrategy):
    """Enumeration strategies related to the class having finitely many simple
    permutations."""

    def applies(self) -> bool:
        return PinWords.has_finite_simples(self.basis)

    @classmethod
    def reference(cls) -> str:
        return "The class contains only finitely many simple permutations"
