from permuta import Perm, Av
from permuta.enumeration_strategies.insertion_encodable import \
        InsertionEncodingStrategy

def test_insertion_encoding():
    strat = InsertionEncodingStrategy([Perm((0,1,2)), Perm((2,0,1))])
    assert strat.applies()
    strat = InsertionEncodingStrategy([Perm((0,2,1,3))])
    assert not strat.applies()
