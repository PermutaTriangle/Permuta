import unittest
from permuta.misc import binary_search, flatten, choose, subsets
import random

class TestMiscMisc(unittest.TestCase):

    def test_binary_search(self):
        self.assertFalse(binary_search([],1337))
        for i in range(100):
            n = random.randint(1,100)
            arr = [ random.randint(0,10000) for i in range(n) ]
            arr = sorted(arr)
            for j in range(100):
                self.assertTrue(binary_search(arr, random.choice(arr)))
                x = random.randint(0,10000)
                self.assertEqual(x in arr, binary_search(arr, x))

    def test_flatten(self):
        self.assertEqual([], flatten([]))
        self.assertEqual([1,2,3], flatten([1,2,3]))
        self.assertEqual([1,2,3], flatten([[1],2,3]))
        self.assertEqual([1,2,3], flatten([[1],(2,3)]))
        self.assertEqual([1,2,3], flatten([[1],([[(2,)]],3)]))
        self.assertEqual([1,2,3], flatten((1,2,[[[[[3]]]]])))

    def test_choose(self):
        it = choose(3, 2)
        self.assertEqual([0,1], next(it))
        self.assertEqual([0,2], next(it))
        self.assertEqual([1,2], next(it))
        with self.assertRaises(StopIteration): next(it)

        it = choose(5, 3)
        self.assertEqual([0,1,2], next(it))
        self.assertEqual([0,1,3], next(it))
        self.assertEqual([0,1,4], next(it))
        self.assertEqual([0,2,3], next(it))
        self.assertEqual([0,2,4], next(it))
        self.assertEqual([0,3,4], next(it))
        self.assertEqual([1,2,3], next(it))
        self.assertEqual([1,2,4], next(it))
        self.assertEqual([1,3,4], next(it))
        self.assertEqual([2,3,4], next(it))
        with self.assertRaises(StopIteration): next(it)

        it = choose(100, 0)
        self.assertEqual([], next(it))
        with self.assertRaises(StopIteration): next(it)

        it = choose(100, 1)
        for i in range(100):
            self.assertEqual([i], next(it))
        with self.assertRaises(StopIteration): next(it)

    def test_subsets(self):
        for lst in [[], [5,6,4], [1,2,3], [2,8], [5,9,1,1]]:
            it = subsets(lst)

            for i in range(1<<len(lst)):
                cur = next(it)
                self.assertEqual([ v for k,v in enumerate(lst) if (i & (1<<(len(lst)-k-1))) != 0 ], cur)
            with self.assertRaises(StopIteration): next(it)

