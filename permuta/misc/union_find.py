class UnionFind:
    """A collection of distjoint sets."""

    def __init__(self, size: int) -> None:
        """Creates a collection of size disjoint unit sets."""
        self._parent = [-1] * size

    def find(self, idx: int) -> int:
        """Return the identifier of a representative element for the set
        containing the element with identifier idx."""
        if self._parent[idx] < 0:
            return idx
        self._parent[idx] = self.find(self._parent[idx])
        return self._parent[idx]

    def size(self, idx: int) -> int:
        """Return the number of elements in the set containing the element with
        identifier idx."""
        return -self._parent[self.find(idx)]

    def unite(self, idx1: int, idx2: int) -> bool:
        """Unite the two sets containing the elements with identifiers idx1 and idx2,
        respectively."""
        idx1, idx2 = self.find(idx1), self.find(idx2)
        if idx1 == idx2:
            return False
        if self.size(idx1) > self.size(idx2):
            idx1, idx2 = idx2, idx1
        self._parent[idx2] += self._parent[idx1]
        self._parent[idx1] = idx2
        return True
