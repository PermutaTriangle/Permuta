import unittest
from permuta import MeshPattern, Permutation
from permuta.permutations import *

class TestPermutationSets(unittest.TestCase):

    def test_random_element_of_all_permutations(self):
        for n in range(0,10):
            for it in range(10):
                self.assertEqual(list(range(1,n+1)), sorted(Permutations(n).random_element()))

    def test_avoiders(self):
        ts = [
            (PermutationsAvoiding12, [1,2], [1,1,1,1,1,1,1,1,1,1]),
            (PermutationsAvoiding21, [2,1], [1,1,1,1,1,1,1,1,1,1]),
            (PermutationsAvoiding123, [1,2,3], [ catalan(i) for i in range(8) ]),
            (PermutationsAvoiding132, [1,3,2], [ catalan(i) for i in range(8) ]),
            (PermutationsAvoiding213, [2,1,3], [ catalan(i) for i in range(8) ]),
            (PermutationsAvoiding231, [2,3,1], [ catalan(i) for i in range(8) ]),
            (PermutationsAvoiding312, [3,1,2], [ catalan(i) for i in range(8) ]),
            (PermutationsAvoiding321, [3,2,1], [ catalan(i) for i in range(8) ]),
        ]

        for (cl, patt, enum) in ts:
            ginst = Permutations(5, avoiding=Permutation(patt))
            self.assertTrue(type(ginst) is cl)

            for (n,cnt) in enumerate(enum):
                inst = cl(n)
                gen = list(inst)
                self.assertEqual(len(gen), cnt)
                self.assertEqual(len(gen), len(set(gen)))
                for p in gen:
                    self.assertTrue(p.avoids(Permutation(patt)))

    def test_avoiders_generic(self):
        try:
            Permutations(5, avoiding="your mom")
            self.assertTrue(False)
        except RuntimeError:
            pass

        res = Permutations(5, avoiding=[Permutation([1,2,3,4]), Permutation([2,1])])
        self.assertTrue(type(res) is PermutationsAvoidingGeneric)

        res = Permutations(5, avoiding=(Permutation([1,2,3,4]), Permutation([2,1])))
        self.assertTrue(type(res) is PermutationsAvoidingGeneric)

        ts = [
            ([[]], [0,0,0,0,0,0,0,0,0,0]),
            ([[1,2]], [1,1,1,1,1,1,1,1,1,1]),
            ([[2,1]], [1,1,1,1,1,1,1,1,1,1]),
            ([[1,2,3]], [ catalan(i) for i in range(8) ]),
            ([[1,3,2]], [ catalan(i) for i in range(8) ]),
            ([[2,1,3]], [ catalan(i) for i in range(8) ]),
            ([[2,3,1]], [ catalan(i) for i in range(8) ]),
            ([[3,1,2]], [ catalan(i) for i in range(8) ]),
            ([[3,2,1]], [ catalan(i) for i in range(8) ]),
            ([[1,2,3], [1,4,3,2]], [1, 1, 2, 5, 13, 34, 89, 233, 610]),
        ]

        for (patts, enum) in ts:
            patts = [ Permutation(patt) for patt in patts ]
            for (n,cnt) in enumerate(enum):
                inst = Permutations(n, avoiding=patts)
                gen = list(inst)
                self.assertEqual(len(gen), cnt)
                self.assertEqual(len(gen), len(set(gen)))
                for p in gen:
                    self.assertTrue(p.avoids(*patts))

            mx = len(enum)-1
            cnt = [ 0 for _ in range(mx+1) ]
            inst = Permutations(mx, avoiding=patts, upto=True)
            gen = list(inst)
            for p in gen:
                self.assertTrue(p.avoids(*patts))
                cnt[len(p)] += 1

            self.assertEqual(enum, cnt)

    def test_is_polynomial(self):
        self.assertEqual(Permutations(8, [Permutation([])]).is_polynomial(), True)
        self.assertEqual(Permutations(8, [Permutation([1])]).is_polynomial(),True)
        self.assertEqual(Permutations(8, [Permutation([1,2])]).is_polynomial(),True)
        self.assertEqual(Permutations(8, [Permutation([1,3,2,4])]).is_polynomial(),False)
        self.assertEqual(Permutations(8, [Permutation([3,2,1]), Permutation([1,2,3])]).is_polynomial(),True)
        self.assertEqual(Permutations(8, [Permutation([1,2,3]), Permutation([2,3,1])]).is_polynomial(), True)
        self.assertEqual(Permutations(8, [Permutation([1,2,3]), Permutation([1,3,2])]).is_polynomial(), False)
        self.assertEqual(Permutations(8, [Permutation([1,3,2]), Permutation([3,1,2])]).is_polynomial(), False)
        self.assertEqual(Permutations(8, [Permutation([2,3,1]), Permutation([3,1,2])]).is_polynomial(), False)
