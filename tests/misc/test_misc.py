import pytest
import random
from permuta.misc import binary_search, flatten, choose, subsets


def test_binary_search():
    assert not binary_search([], 1337)
    for i in range(100):
        n = random.randint(1, 100)
        arr = [ random.randint(0, 10000) for i in range(n) ]
        arr = sorted(arr)
        for j in range(100):
            assert binary_search(arr, random.choice(arr))
            x = random.randint(0, 10000)
            assert (x in arr) == binary_search(arr, x)

def test_flatten():
    assert [] == flatten([])
    assert [1, 2, 3] == flatten([1, 2, 3])
    assert [1, 2, 3] == flatten([[1], 2, 3])
    assert [1, 2, 3] == flatten([[1], (2, 3)])
    assert [1, 2, 3] == flatten([[1], ([[(2,)]], 3)])
    assert [1, 2, 3] == flatten((1, 2, [[[[[3]]]]]))

def test_choose():
    it = choose(3, 2)
    assert [0, 1] == next(it)
    assert [0, 2] == next(it)
    assert [1, 2] == next(it)
    with pytest.raises(StopIteration): next(it)

    it = choose(5, 3)
    assert [0, 1, 2] == next(it)
    assert [0, 1, 3] == next(it)
    assert [0, 1, 4] == next(it)
    assert [0, 2, 3] == next(it)
    assert [0, 2, 4] == next(it)
    assert [0, 3, 4] == next(it)
    assert [1, 2, 3] == next(it)
    assert [1, 2, 4] == next(it)
    assert [1, 3, 4] == next(it)
    assert [2, 3, 4] == next(it)
    with pytest.raises(StopIteration): next(it)

    it = choose(100, 0)
    assert [] == next(it)
    with pytest.raises(StopIteration): next(it)

    it = choose(100, 1)
    for i in range(100):
        assert [i] == next(it)
    with pytest.raises(StopIteration): next(it)

def test_subsets():
    for lst in [[], [5, 6, 4], [1, 2, 3], [2, 8], [5, 9, 1, 1]]:
        it = subsets(lst)

        for i in range(1<<len(lst)):
            cur = next(it)
            assert [ v for k,v in enumerate(lst) if (i & (1<<(len(lst)-k-1))) != 0 ] == cur
        with pytest.raises(StopIteration): next(it)
