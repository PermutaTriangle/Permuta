class Node:
    def __init__(self, row, col):
        self.left = None
        self.right = None
        self.u = None
        self.d = None
        self.p = None
        self.row = row
        self.col = col
        self.size = 0


def cover(c):
    c.right.left = c.left
    c.left.right = c.right
    i = c.d
    while i != c:
        j = i.right
        while j != i:
            j.d.u = j.u
            j.u.d = j.d
            j.p.size -= 1
            j = j.right
        i = i.d


def uncover(c):
    i = c.u
    while i != c:
        j = i.left
        while j != i:
            j.p.size += 1
            j.u.d = j
            j.d.u = j.u.d
            j = j.left
        i = i.u
    c.left.right = c
    c.right.left = c.left.right


class AlgorithmX:
    def __init__(self, rows, cols, solution_callback):
        assert rows > 0 and cols > 0
        self.rows = rows
        self.cols = cols
        self.head = None
        self.arr = [[False for c in range(self.cols)] for r in range(self.rows)]
        self.sol = [0 for i in range(self.rows)]
        self.solution_callback = solution_callback
        self.can_continue = False

    def set_value(self, row, col, val=True):
        self.arr[row][col] = val

    def setup(self):
        ptr = [
            [
                Node(i, j) if i == self.rows or self.arr[i][j] else None
                for j in range(self.cols)
            ]
            for i in range(self.rows + 1)
        ]
        for i in range(self.rows + 1):
            for j in range(self.cols):
                if ptr[i][j] is None:
                    continue

                ni = i + 1
                nj = j + 1

                while True:
                    if ni == self.rows + 1:
                        ni = 0
                    if ni == self.rows or self.arr[ni][j]:
                        break
                    ni += 1

                ptr[i][j].d = ptr[ni][j]
                ptr[ni][j].u = ptr[i][j]

                while True:
                    if nj == self.cols:
                        nj = 0
                    if i == self.rows or self.arr[i][nj]:
                        break
                    nj += 1

                ptr[i][j].right = ptr[i][nj]
                ptr[i][nj].left = ptr[i][j]

        self.head = Node(self.rows, -1)
        self.head.right = ptr[self.rows][0]
        ptr[self.rows][0].left = self.head
        self.head.left = ptr[self.rows][self.cols - 1]
        ptr[self.rows][self.cols - 1].right = self.head

        for j in range(self.cols):
            cnt = -1
            for i in range(self.rows + 1):
                if ptr[i][j] is not None:
                    cnt += 1
                    ptr[i][j].p = ptr[self.rows][j]
            ptr[self.rows][j].size = cnt

    def search(self, k=0, at_most=None):
        if self.head == self.head.right:
            res = [self.sol[i] for i in range(k)]
            res = sorted(res)
            return self.solution_callback(res)

        if at_most is not None and k >= at_most:
            self.can_continue = True
            return

        c = self.head.right
        tmp = self.head.right
        while tmp != self.head:
            if tmp.size < c.size:
                c = tmp
            tmp = tmp.right

        if c == c.d:
            return False

        cover(c)

        found = False
        r = c.d
        while not found and r != c:
            self.sol[k] = r.row

            j = r.right
            while j != r:
                cover(j.p)
                j = j.right

            found = self.search(k + 1, at_most)

            j = r.left
            while j != r:
                uncover(j.p)
                j = j.left

            r = r.d

        uncover(c)
        return found
