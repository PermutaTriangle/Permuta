import pytest
from permuta import Perm
from permuta import PermSet
from permuta.misc import catalan


def test_random_all():
    for length in range(0, 10):
        for _ in range(100):
            assert list(range(length)) == sorted(PermSet(length).random())

#    def test_avoiders(self):
#        ts = [
#            (PermutationsAvoiding12, [1,2], [1,1,1,1,1,1,1,1,1,1]),
#            (PermutationsAvoiding21, [2,1], [1,1,1,1,1,1,1,1,1,1]),
#            (PermutationsAvoiding123, [1,2,3], [ catalan(i) for i in range(8) ]),
#            (PermutationsAvoiding132, [1,3,2], [ catalan(i) for i in range(8) ]),
#            (PermutationsAvoiding213, [2,1,3], [ catalan(i) for i in range(8) ]),
#            (PermutationsAvoiding231, [2,3,1], [ catalan(i) for i in range(8) ]),
#            (PermutationsAvoiding312, [3,1,2], [ catalan(i) for i in range(8) ]),
#            (PermutationsAvoiding321, [3,2,1], [ catalan(i) for i in range(8) ]),
#        ]
#
#        for (cl, patt, enum) in ts:
#            ginst = Permutations(5, avoiding=Permutation(patt))
#            self.assertTrue(type(ginst) is cl)
#
#            for (n,cnt) in enumerate(enum):
#                inst = cl(n)
#                gen = list(inst)
#                self.assertEqual(len(gen), cnt)
#                self.assertEqual(len(gen), len(set(gen)))
#                for p in gen:
#                    self.assertTrue(p.avoids(Permutation(patt)))

def test_avoiders_generic():
    PermSet.avoiding(Perm.to_standard("your mom")).of_length(5)

    res = PermSet.avoiding([Perm((0, 1, 2, 3)), Perm((1, 0))])
    assert isinstance(res, PermSet)

    ts = [
#        ([[]], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ([[0, 1]], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        ([[1, 0]], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        ([[0, 1, 2]], [catalan(i) for i in range(8)]),
        ([[0, 2, 1]], [catalan(i) for i in range(8)]),
        ([[1, 0, 2]], [catalan(i) for i in range(8)]),
        ([[1, 2, 0]], [catalan(i) for i in range(8)]),
        ([[2, 0, 1]], [catalan(i) for i in range(8)]),
        ([[2, 1, 0]], [catalan(i) for i in range(8)]),
        ([[0, 1, 2], [0, 3, 2, 1]], [1, 1, 2, 5, 13, 34, 89, 233, 610]),
    ]

    for (patts, enum) in ts:
        patts = [ Perm(patt) for patt in patts ]
        for (n,cnt) in enumerate(enum):
            inst = PermSet.avoiding(patts).of_length(n)
            gen = list(inst)
            assert len(gen) == cnt
            assert len(gen) == len(set(gen))
            for perm in gen:
                assert perm.avoids(*patts)

        mx = len(enum)-1
        cnt = [0 for _ in range(mx+1)]
        for perm in PermSet.avoiding(patts):
            if len(perm) > mx:
                break
            assert perm.avoids(*patts)
            cnt[len(perm)] += 1

        assert enum == cnt

#    def test_is_polynomial(self):
#        self.assertEqual(PermSet(8, [Permutation([])]).is_polynomial(), True)
#        self.assertEqual(PermSet(8, [Permutation([1])]).is_polynomial(),True)
#        self.assertEqual(PermSet(8, [Permutation([1,2])]).is_polynomial(),True)
#        self.assertEqual(PermSet(8, [Permutation([1,3,2,4])]).is_polynomial(),False)
#        self.assertEqual(PermSet(8, [Permutation([3,2,1]), Permutation([1,2,3])]).is_polynomial(),True)
#        self.assertEqual(PermSet(8, [Permutation([1,2,3]), Permutation([2,3,1])]).is_polynomial(), True)
#        self.assertEqual(PermSet(8, [Permutation([1,2,3]), Permutation([1,3,2])]).is_polynomial(), False)
#        self.assertEqual(PermSet(8, [Permutation([1,3,2]), Permutation([3,1,2])]).is_polynomial(), False)
#        self.assertEqual(PermSet(8, [Permutation([2,3,1]), Permutation([3,1,2])]).is_polynomial(), False)
