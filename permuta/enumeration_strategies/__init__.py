from typing import Iterable, List, Type

from permuta import Perm

from .abstract_strategy import EnumerationStrategy
from .core_strategies import core_strategies
from .insertion_encodable import InsertionEncodingStrategy

fast_enumeration_strategies: List[Type[EnumerationStrategy]] = [
    InsertionEncodingStrategy
]
fast_enumeration_strategies.extend(core_strategies)

long_enumeration_strategies: List[Type[EnumerationStrategy]] = []

all_enumeration_strategies: List[Type[EnumerationStrategy]] = (
    fast_enumeration_strategies + long_enumeration_strategies
)


def find_strategies(
    basis: Iterable[Perm], long_runnning: bool = True
) -> List[EnumerationStrategy]:
    """Test all enumeration strategies against the basis and return a list of
    potentially useful strategies. If `long_runnning` is False, test only the
    strategies that can be tested quickly.
    """
    if long_runnning:
        strategies: List[Type[EnumerationStrategy]] = all_enumeration_strategies
    else:
        strategies = fast_enumeration_strategies
    working_strategies: List[EnumerationStrategy] = []
    for strategy in strategies:
        strategy_object = strategy(basis)
        if strategy_object.applies():
            working_strategies.append(strategy_object)
    return working_strategies
