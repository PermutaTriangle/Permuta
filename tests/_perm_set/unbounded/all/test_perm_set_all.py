from permuta import PermSet


def test_random():
    for length in range(0, 10):
        for _ in range(100):
            assert list(range(length)) == sorted(PermSet(length).random())
