
class TrieNode(object):
    def __init__(self):
        self.down = {}
        self.value = None
        self.end = False

    def child(self, k):
        if k not in self.down:
            self.down[k] = TrieNode()
        return self.down[k]

    def height(self):
        return 1 + max([n.height() for n in self.down.values()] + [0])


class TrieMap(object):

    def __init__(self):
        self.root = TrieNode()
        self.cnt = 0

    def __contains__(self, key):
        cur = self.root
        for k in key:
            cur = cur.down.get(k, None)
            if cur is None:
                return False
        return cur.end

    def __setitem__(self, key, value):
        cur = self.root
        for k in key:
            cur = cur.child(k)
        cur.value = value
        if not cur.end:
            cur.end = True
            self.cnt += 1

    def __getitem__(self, key):
        cur = self.root
        for k in key:
            cur = cur.down.get(k, None)
            if cur is None:
                raise KeyError()
        if not cur.end:
            raise KeyError()
        return cur.value

    def height(self):
        return self.root.height()

    def __len__(self):
        return self.cnt
