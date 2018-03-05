import bisect


def binary_search(a, x):
    i = bisect.bisect_left(a, x)
    return i != len(a) and a[i] == x


def flatten(lst):
    res = []

    def dfs(l):
        try:
            for i in l:
                dfs(i)
        except Exception:
            res.append(l)
    dfs(lst)
    return res


def choose(l, k):
    cur = []

    def gen(at, left):
        if left == 0:
            yield list(cur)
        elif at < l:
            cur.append(at)
            for res in gen(at + 1, left - 1):
                yield res

            cur.pop()

            for res in gen(at + 1, left):
                yield res

    return gen(0, k)


def subsets(elems):
    def bt(at, cur):
        if at == len(elems):
            yield cur
        else:
            for x in bt(at+1, cur):
                yield x
            for x in bt(at+1, cur + [elems[at]]):
                yield x
    for x in bt(0, []):
        yield x
