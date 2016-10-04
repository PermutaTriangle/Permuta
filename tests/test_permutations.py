import unittest
from permuta import MeshPattern, Permutation, Permutations
import random

class TestPermutations(unittest.TestCase):

    def test_random_element(self):
        for n in range(0,10):
            for it in range(10):
                self.assertEqual(list(range(1,n+1)), sorted(Permutations(n).random_element()))

