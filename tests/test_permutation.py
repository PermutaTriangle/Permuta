import unittest
from permuta import MeshPattern, Permutation, Permutations
import random

class TestPermutation(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(AssertionError): Permutation([1,2,2], check=True)
        with self.assertRaises(AssertionError): Permutation([2,1,2], check=True)
        with self.assertRaises(AssertionError): Permutation([1,1], check=True)
        with self.assertRaises(AssertionError): Permutation([2], check=True)
        with self.assertRaises(AssertionError): Permutation({1,2,3}, check=True)
        with self.assertRaises(AssertionError): Permutation(5, check=True)
        with self.assertRaises(AssertionError): Permutation(None, check=True)
        Permutation([], check=True)
        Permutation([1], check=True)
        Permutation([4,1,3,2], check=True)

    def test_contained_in(self):
        def generate_contained(n,perm):
            for i in range(len(perm),n):
                r = random.randint(1,len(perm)+1)
                for i in range(len(perm)):
                    if perm[i] >= r:
                        perm[i] += 1
                x = random.randint(0,len(perm))
                perm = perm[:x] + [r] + perm[x:]
            return Permutation(perm)

        self.assertTrue(Permutation([4,8,1,9,2,7,6,3,5]).contained_in(Permutation([4,8,1,9,2,7,6,3,5])))
        self.assertTrue(Permutation([]).contained_in(Permutation([])))
        self.assertTrue(Permutation([]).contained_in(Permutation([4,8,1,9,2,7,6,3,5])))
        self.assertTrue(Permutation([1]).contained_in(Permutation([1])))
        self.assertFalse(Permutation([8,4,1,9,2,7,6,3,5]).contained_in(Permutation([4,8,1,9,2,7,6,3,5])))

        for i in range(100):
            n = random.randint(0, 4)
            patt = Permutations(n).random_element()
            self.assertTrue(patt.contained_in(generate_contained(random.randint(n, 8), patt.perm)))

        # self.assertFalse(Permutation([]))

    def test_inverse(self):
        for i in range(10):
            self.assertEqual(Permutation(range(1,i)), Permutation(range(1,i)).inverse())
        self.assertEqual(Permutation([3,2,4,1]), Permutation([4,2,1,3]).inverse())
        self.assertEqual(Permutation([5,4,2,7,6,8,9,1,3]), Permutation([8,3,9,2,1,5,4,6,7]).inverse())

