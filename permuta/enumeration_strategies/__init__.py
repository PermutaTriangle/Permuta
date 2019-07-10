from .core_strategies import core_strategies
from .insertion_encodable import InsertionEncodingStrategy

fast_enumeration_strategies = [InsertionEncodingStrategy] + core_strategies

long_enumeration_strategies = []

all_enumeration_strategies = (fast_enumeration_strategies +
                              long_enumeration_strategies)
