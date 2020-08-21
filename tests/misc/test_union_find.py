import random
from itertools import combinations

from permuta.misc.union_find import UnionFind


def test_union_find_init():
    uf = UnionFind(10)
    assert sum(x == -1 for x in uf._parent) == 10


def test_union_find_1():
    uf = UnionFind(10)
    assert uf.find(1) != uf.find(3)
    assert uf.unite(1, 8)
    assert uf.unite(3, 8)
    assert uf.find(1) == uf.find(3)
    assert uf.size(1) == uf.size(3) == uf.size(8) == 3
    assert all(uf.size(i) == 1 for i in range(10) if i not in (1, 3, 8))


def test_union_find_2():
    uf = UnionFind(100)
    for i in range(1, 100):
        assert uf.unite(0, i)
    for (a, b) in combinations(range(100), 2):
        assert uf.find(a) == uf.find(b)
        assert uf.size(a) == 100
        assert uf.size(b) == 100


def test_union_find_3():
    uf = UnionFind(4)
    assert uf.find(0) == uf.find(0)
    assert not uf.unite(0, 0)
    assert uf.unite(1, 0)
    assert not uf.unite(0, 1)
    assert uf.unite(1, 2)
    assert not uf.unite(1, 2)
    assert not uf.unite(0, 2)
    assert uf.find(0) != uf.find(3)


def test_union_find_4():
    n = 5000
    d = {i: {i} for i in range(n)}
    uf = UnionFind(n)

    for i in range(2 * n):
        a, b = random.randint(0, n - 1), random.randint(0, n - 1)
        if random.randint(0, 1):
            combined = d[a].union(d[b])
            for x in combined:
                d[x] = combined
            uf.unite(a, b)
            assert uf.size(a) == len(combined) == uf.size(b)
        else:
            if a in d[b]:
                assert uf.find(a) == uf.find(b)
            else:
                assert uf.find(a) != uf.find(b)
