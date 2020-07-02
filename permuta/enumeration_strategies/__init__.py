from typing import List

from .core_strategies import core_strategies
from .insertion_encodable import InsertionEncodingStrategy

fast_enumeration_strategies: List = [InsertionEncodingStrategy] + core_strategies

long_enumeration_strategies: List = []

all_enumeration_strategies: List = (
    fast_enumeration_strategies + long_enumeration_strategies
)


def find_strategies(basis, long_runnning=True):
    """
    Test all enumeration strategies against the basis and return a list of
    potentially useful strategies. If `long_runnning` is False, test only the
    strategies that can be tested quickly.
    """
    if long_runnning:
        strategies = all_enumeration_strategies
    else:
        strategies = fast_enumeration_strategies
    working_strategies = []
    for Strategy in strategies:
        strategy_object = Strategy(basis)
        if strategy_object.applies():
            working_strategies.append(strategy_object)
    return working_strategies
