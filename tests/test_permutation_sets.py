import unittest
from permuta import MeshPattern, Permutation
from permuta.permutation_sets import *

class TestPermutationSets(unittest.TestCase):

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
            ginst = AvoidanceClass(5, avoiding=Permutation(patt))
            self.assertTrue(type(ginst) is cl)

            for (n,cnt) in enumerate(enum):
                inst = cl(n)
                gen = list(inst)
                self.assertEqual(len(gen), cnt)
                self.assertEqual(len(gen), len(set(gen)))
                for p in gen:
                    self.assertTrue(p.avoids(patt))

    def test_avoiders_generic(self):
        try:
            AvoidanceClass(5, avoiding="your mom")
            self.assertTrue(False)
        except RuntimeError:
            pass

        res = AvoidanceClass(5, avoiding=[Permutation([1,2,3,4]), Permutation([2,1])])
        self.assertTrue(type(res) is PermutationsAvoidingGeneric)

        res = AvoidanceClass(5, avoiding=(Permutation([1,2,3,4]), Permutation([2,1])))
        self.assertTrue(type(res) is PermutationsAvoidingGeneric)

