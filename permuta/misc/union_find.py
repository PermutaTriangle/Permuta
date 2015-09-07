
class UnionFind(object):
    def __init__(self, n):
        self.p = [-1]*n
        self.leaders = set( i for i in range(n) )

    def find(self, x):
        if self.p[x] < 0:
            return x
        self.p[x] = self.find(self.p[x])
        return self.p[x]

    def size(self, x):
        return -self.p[self.find(x)]

    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.size(x) > self.size(y):
            x,y = y,x
        self.p[y] += self.p[x]
        self.p[x] = y
        self.leaders.remove(x)

