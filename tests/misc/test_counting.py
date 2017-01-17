from permuta.misc import factorial, binomial


def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(9) == 362880
    assert factorial(10) == 3628800

def test_binomial():
    assert binomial(0, 0) == 1
    assert binomial(0, 1) == 0
    assert binomial(120, 1231) == 0
    assert binomial(10, 3) == 120
    assert binomial(10, 1) == 10
    assert binomial(1243, 10) == 2339835883576802918726133
    assert binomial(1243, 20) == 27325212682042866855639367404897873973276230
