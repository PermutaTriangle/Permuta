from .insertion_encodable import InsertionEncodingStrategy

fast_enumeration_strategies = [InsertionEncodingStrategy]

long_enumeration_strategies = []

all_enumeration_strategies = (fast_enumeration_strategies +
                              long_enumeration_strategies)
