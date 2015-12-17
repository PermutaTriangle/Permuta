import unittest
from permuta.misc import ordered_set_partitions

class TestMiscOrderedSetPartitions(unittest.TestCase):

    def test_ordered_set_partitions(self):
        it = ordered_set_partitions([1,2,3], [2,1])
        self.assertEqual([[1,2],[3]], next(it))
        self.assertEqual([[1,3],[2]], next(it))
        self.assertEqual([[2,3],[1]], next(it))
        with self.assertRaises(StopIteration): next(it)

        it = ordered_set_partitions([1,2,3], [2,1])
        self.assertEqual([[1,2],[3]], next(it))
        self.assertEqual([[1,3],[2]], next(it))
        self.assertEqual([[2,3],[1]], next(it))
        with self.assertRaises(StopIteration): next(it)

        lst = list(ordered_set_partitions([2,3,4,5,6], [2,1,2]))
        self.assertEqual([[[2, 3], [4], [5, 6]],
                          [[2, 3], [5], [4, 6]],
                          [[2, 3], [6], [4, 5]],
                          [[2, 4], [3], [5, 6]],
                          [[2, 4], [5], [3, 6]],
                          [[2, 4], [6], [3, 5]],
                          [[2, 5], [3], [4, 6]],
                          [[2, 5], [4], [3, 6]],
                          [[2, 5], [6], [3, 4]],
                          [[2, 6], [3], [4, 5]],
                          [[2, 6], [4], [3, 5]],
                          [[2, 6], [5], [3, 4]],
                          [[3, 4], [2], [5, 6]],
                          [[3, 4], [5], [2, 6]],
                          [[3, 4], [6], [2, 5]],
                          [[3, 5], [2], [4, 6]],
                          [[3, 5], [4], [2, 6]],
                          [[3, 5], [6], [2, 4]],
                          [[3, 6], [2], [4, 5]],
                          [[3, 6], [4], [2, 5]],
                          [[3, 6], [5], [2, 4]],
                          [[4, 5], [2], [3, 6]],
                          [[4, 5], [3], [2, 6]],
                          [[4, 5], [6], [2, 3]],
                          [[4, 6], [2], [3, 5]],
                          [[4, 6], [3], [2, 5]],
                          [[4, 6], [5], [2, 3]],
                          [[5, 6], [2], [3, 4]],
                          [[5, 6], [3], [2, 4]],
                          [[5, 6], [4], [2, 3]]], sorted(lst))

        lst = list(ordered_set_partitions([2,3,4,5,6], [3,1,1]))
        self.assertEqual([[[2, 3, 4], [5], [6]],
                          [[2, 3, 4], [6], [5]],
                          [[2, 3, 5], [4], [6]],
                          [[2, 3, 5], [6], [4]],
                          [[2, 3, 6], [4], [5]],
                          [[2, 3, 6], [5], [4]],
                          [[2, 4, 5], [3], [6]],
                          [[2, 4, 5], [6], [3]],
                          [[2, 4, 6], [3], [5]],
                          [[2, 4, 6], [5], [3]],
                          [[2, 5, 6], [3], [4]],
                          [[2, 5, 6], [4], [3]],
                          [[3, 4, 5], [2], [6]],
                          [[3, 4, 5], [6], [2]],
                          [[3, 4, 6], [2], [5]],
                          [[3, 4, 6], [5], [2]],
                          [[3, 5, 6], [2], [4]],
                          [[3, 5, 6], [4], [2]],
                          [[4, 5, 6], [2], [3]],
                          [[4, 5, 6], [3], [2]]], sorted(lst))

