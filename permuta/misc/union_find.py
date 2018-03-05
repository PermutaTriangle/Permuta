
class UnionFind(object):
    """A collection of distjoint sets."""

    def __init__(self, n=0):
        """Creates a collection of n disjoint unit sets."""
        self.p = [-1]*n
        self.leaders = set(i for i in range(n))

    def find(self, x):
        """Return the identifier of a representative element for the set
        containing the element with identifier x."""
        if self.p[x] < 0:
            return x
        self.p[x] = self.find(self.p[x])
        return self.p[x]

    def size(self, x):
        """Return the number of elements in the set containing the element with
        identifier x."""
        return -self.p[self.find(x)]

    def unite(self, x, y):
        """Unite the two sets containing the elements with identifiers x and y,
        respectively."""
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.size(x) > self.size(y):
            x, y = y, x
        self.p[y] += self.p[x]
        self.p[x] = y
        self.leaders.remove(x)
        return True

    def add(self):
        """Add a unit set containing a new element to the collection, and
        return the identifier of the new element."""
        nid = len(self.p)
        self.p.append(nid)
        return nid
