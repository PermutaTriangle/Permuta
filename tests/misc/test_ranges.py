from permuta.misc import cyclic_range, modulo_range


def test_cyclic_range():
    result = list(cyclic_range(5, 30, -20))
    expected = list(range(5, 30))
    expected.extend(range(-20, 5))
    assert result == expected

def test_modulo_range():
    result = list(modulo_range(7, 30))
    expected = list(range(7, 30))
    expected.extend(range(7))
    assert result == expected

    result = list(modulo_range(0, 30))
    expected = list(range(0, 30))
    assert result == expected
