
class Node(object):
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

        if self.prev is not None:
            self.prev.next = self

        if self.next is not None:
            self.next.prev = self

    def __repr__(self):
        return 'Node(%s)' % repr(self.value)


class DancingLinks(object):

    def __init__(self, lst=None):
        self.front = None
        self.back = None
        self.count = 0

        if lst is not None:
            for value in lst:
                self.append(value)

    def append(self, value):
        self.count += 1
        self.back = Node(value, self.back)
        if self.front is None:
            self.front = self.back

    def erase(self, node):
        self.count -= 1

        if node.prev is not None:
            node.prev.next = node.next

        if node.next is not None:
            node.next.prev = node.prev

        if node == self.front:
            self.front = node.next

        if node == self.back:
            self.back = node.prev

    def restore(self, node):
        self.count += 1

        if node.prev is not None:
            node.prev.next = node

        if node.next is not None:
            node.next.prev = node

        if node.next == self.front:
            self.front = node

        if node.prev == self.back:
            self.back = node

    def __len__(self):
        return self.count

    def __repr__(self):
        cur = self.front
        lst = []
        while cur is not None:
            lst.append(cur)
            cur = cur.next
        return 'DancingLinks([%s])' % ', '.join(map(repr, lst))
