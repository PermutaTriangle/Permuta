import unittest
from permuta import MeshPattern, Permutation, Permutations
import random

class TestPermutation(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(AssertionError): Permutation([1,2,2], check=True)
        with self.assertRaises(AssertionError): Permutation([2,1,2], check=True)
        with self.assertRaises(AssertionError): Permutation([1,1], check=True)
        with self.assertRaises(AssertionError): Permutation([2], check=True)
        with self.assertRaises(AssertionError): Permutation(122, check=True)
        with self.assertRaises(TypeError): Permutation(None, check=True)
        Permutation(check=True)
        Permutation([], check=True)
        Permutation([1], check=True)
        Permutation([4,1,3,2], check=True)
        Permutation(set([1,2,3]), check=True)
        p = Permutation(613245, check=True)
        self.assertEqual(p, Permutation((6,1,3,2,4,5)))

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
            perm = generate_contained(random.randint(n, 8), list(patt))
            self.assertTrue(patt.contained_in(perm))

        self.assertFalse(Permutation([1]).contained_in(Permutation([])))
        self.assertFalse(Permutation([1,2]).contained_in(Permutation([])))
        self.assertFalse(Permutation([1,2]).contained_in(Permutation([1])))
        self.assertFalse(Permutation([2, 1]).contained_in(Permutation([1, 2])))
        self.assertFalse(Permutation([1,2,3]).contained_in(Permutation([1,2])))
        self.assertFalse(Permutation([2, 1, 3]).contained_in(Permutation([1, 2, 4, 5, 3])))
        self.assertFalse(Permutation([1, 2, 3]).contained_in(Permutation([3, 2, 4, 1])))
        self.assertFalse(Permutation([3, 2, 4, 1]).contained_in(Permutation([3, 1, 4, 2])))
        self.assertFalse(Permutation([1, 3, 2]).contained_in(Permutation([3, 1, 2, 4])))
        self.assertFalse(Permutation([3, 1, 2, 4]).contained_in(Permutation([6, 4, 3, 8, 2, 1, 7, 5])))
        self.assertFalse(Permutation([1, 2, 3, 4]).contained_in(Permutation([5, 8, 6, 2, 7, 3, 4, 1])))

    def test_count_occurrences_in(self):
        self.assertEqual(Permutation([]).count_occurrences_in(Permutation([5,2,3,4,1])), 1)
        self.assertEqual(Permutation([1]).count_occurrences_in(Permutation([5,2,3,4,1])), 5)
        self.assertEqual(Permutation([1,2]).count_occurrences_in(Permutation([5,2,3,4,1])), 3)
        self.assertEqual(Permutation([2,1]).count_occurrences_in(Permutation([5,2,3,4,1])), 7)
        self.assertEqual(Permutation([5,2,3,4,1]).count_occurrences_in(Permutation([])), 0)
        self.assertEqual(Permutation([5,2,3,4,1]).count_occurrences_in(Permutation([2,1])), 0)

    def test_occurrences_in(self):
        self.assertEqual(
                          list(Permutation([]).occurrences_in(Permutation([5,2,3,4,1])))
                        , [[]]
                        )
        self.assertEqual(
                          sorted(Permutation([1]).occurrences_in(Permutation([5,2,3,4,1])))
                        , [[0],[1],[2],[3],[4]]
                        )
        self.assertEqual(
                          sorted(Permutation([1,2]).occurrences_in(Permutation([5,2,3,4,1])))
                        , [[1,2],[1,3],[2,3]]
                        )
        self.assertEqual(
                          sorted(Permutation([2,1]).occurrences_in(Permutation([5,2,3,4,1])))
                        , [[0,1],[0,2],[0,3],[0,4],[1,4],[2,4],[3,4]]
                        )
        self.assertEqual(list(Permutation([5,2,3,4,1]).occurrences_in(Permutation([]))), [])
        self.assertEqual(list(Permutation([5,2,3,4,1]).occurrences_in(Permutation([2,1]))), [])

    def test_apply(self):
        for i in range(100):
            n = random.randint(0,20)
            lst = [ random.randint(0,10000) for i in range(n) ]
            perm = Permutations(n).random_element()
            res = list(perm.apply(lst))
            for j,k in enumerate(perm.inverse()):
                self.assertEqual(lst[j], res[k-1])

    def test_direct_sum(self):
        p1 = Permutation(1243)
        p2 = Permutation(15324)
        p3 = Permutation(312)
        p4 = Permutation(1)
        p5 = Permutation()
        # All together
        result = p1.direct_sum(p2, p3, p4, p5)
        expected = Permutation((1,2,4,3,5,9,7,6,8,12,10,11,13))
        self.assertEqual(result, expected)
        # Two
        result = p1.direct_sum(p3)
        expected = Permutation((1,2,4,3,7,5,6))
        self.assertEqual(result, expected)
        # None
        self.assertEqual(p1.direct_sum(), p1)
        
    def test_skew_sum(self):
        p1 = Permutation(1243)
        p2 = Permutation(15324)
        p3 = Permutation(312)
        p4 = Permutation(1)
        p5 = Permutation()
        # All together
        result = p1.skew_sum(p2, p3, p4, p5)
        expected = Permutation((10,11,13,12,5,9,7,6,8,4,2,3,1))
        self.assertEqual(result, expected)
        # Two
        result = p1.skew_sum(p3)
        expected = Permutation((4,5,7,6,3,1,2))
        self.assertEqual(result, expected)
        # None
        self.assertEqual(p1.skew_sum(), p1)

    def test_inverse(self):
        for i in range(10):
            self.assertEqual(Permutation(list(range(1,i))), Permutation(list(range(1,i))).inverse())
        self.assertEqual(Permutation([3,2,4,1]), Permutation([4,2,1,3]).inverse())
        self.assertEqual(Permutation([5,4,2,7,6,8,9,1,3]), Permutation([8,3,9,2,1,5,4,6,7]).inverse())

    def test_rotate_right(self):
        for i in range(10):
            self.assertEqual(Permutation(list(range(i-1,0,-1))), Permutation(list(range(1,i))).rotate_right())
        self.assertEqual(Permutation([3,2,4,5,1,6,7]), Permutation([7,6,4,3,1,2,5]).rotate_right())
        self.assertEqual(Permutation([5,6,4,2,8,1,3,7]), Permutation([5,8,2,1,3,7,4,6]).rotate_right())
        self.assertEqual(Permutation([1,2,3]), Permutation([3,2,1]).rotate_right(5))
        self.assertEqual(Permutation([5,6,4,2,1,3]), Permutation([5,6,4,2,1,3]).rotate_right(4))

    def test_rotate_left(self):
        for i in range(10):
            self.assertEqual(Permutation(list(range(i-1,0,-1))), Permutation(list(range(1,i))).rotate_right())
        self.assertEqual(Permutation([7,6,4,3,1,2,5]).rotate_left(), Permutation([7,6,4,3,1,2,5]).rotate_right(3))
        self.assertEqual(Permutation([7,6,4,3,1,2,5]).rotate_left(), Permutation([7,6,4,3,1,2,5]).rotate_right(-1))
        self.assertEqual(Permutation([5,8,2,1,3,7,4,6]).rotate_left(), Permutation([5,8,2,1,3,7,4,6]).rotate_right(7))
        self.assertEqual(Permutation([]).rotate_left(), Permutation([]).rotate_left(123))

    def test_shift_left(self):
        self.assertEqual(Permutation([]), Permutation([]).shift_left())
        self.assertEqual(Permutation([1]), Permutation([1]).shift_left())
        self.assertEqual(Permutation([1,2,3,4,5,6,7,8]), Permutation([1,2,3,4,5,6,7,8]).shift_left(0))
        self.assertEqual(Permutation([1,2,3,4,5,6,7,8]), Permutation([6,7,8,1,2,3,4,5]).shift_left(3))
        self.assertEqual(Permutation([1,2,3,4,5,6,7,8]), Permutation([1,2,3,4,5,6,7,8]).shift_left(800))
        self.assertEqual(Permutation([1,2,3,4,5,6,7,8]), Permutation([6,7,8,1,2,3,4,5]).shift_left(403))
        self.assertEqual(Permutation([1,2,3,4,5,6,7,8]), Permutation([1,2,3,4,5,6,7,8]).shift_left(-8))
        self.assertEqual(Permutation([1,2,3,4,5,6,7,8]), Permutation([6,7,8,1,2,3,4,5]).shift_left(-5))

    def test_shift_down(self):
        self.assertEqual(Permutation([]), Permutation([]).shift_down(1000))
        self.assertEqual(Permutation([1]), Permutation([1]).shift_down(10))
        self.assertEqual(Permutation([2,1,5,3,4,6]), Permutation([3,2,6,4,5,1]).shift_down())
        self.assertEqual(Permutation([2,1,5,3,4,6]), Permutation([3,2,6,4,5,1]).shift_down(13))
        self.assertEqual(Permutation([2,1,5,3,4,6]), Permutation([6,5,3,1,2,4]).shift_down(-2))
        self.assertEqual(Permutation([2,1,5,3,4,6]), Permutation([6,5,3,1,2,4]).shift_down(-8))

    def test_reverse(self):
        self.assertEqual(Permutation([6,3,4,1,5,7,2]), Permutation([2,7,5,1,4,3,6]).reverse())
        self.assertEqual(Permutation([8,2,1,3,5,7,4,6]), Permutation([6,4,7,5,3,1,2,8]).reverse())

    def test_complement(self):
        self.assertEqual(Permutation([7,5,3,4,2,1,6]), Permutation([1,3,5,4,6,7,2]).complement())
        self.assertEqual(Permutation([3,6,7,4,8,5,1,2]), Permutation([6,3,2,5,1,4,8,7]).complement())

    def test_reverse_complement(self):
        for i in range(100):
            perm = Permutations(random.randint(0,20)).random_element()
            self.assertEqual(perm.reverse_complement(), perm.rotate().rotate())

    def test_flip_antidiagonal(self):
        for i in range(100):
            perm = Permutations(random.randint(0,20)).random_element()
            self.assertEqual(perm.reverse().complement().inverse(), perm.flip_antidiagonal())

    def test_fixed_points(self):
        self.assertEqual(Permutation().fixed_points(), 0)
        self.assertEqual(Permutation(132).fixed_points(), 1)
        self.assertEqual(Permutation(654321).fixed_points(), 0)
        self.assertEqual(Permutation(521436).fixed_points(), 3)
        self.assertEqual(Permutation(123456).fixed_points(), 6)

    def test_to_standard(self):
        def gen(perm):
            res = list(perm)
            add = 0
            for i in perm.inverse():
                add += random.randint(0,10)
                res[i-1] += add
            return Permutation(res)

        for i in range(100):
            perm = Permutations(random.randint(0,20)).random_element()
            self.assertEqual(perm, Permutation.to_standard(perm))
            self.assertEqual(perm, Permutation.to_standard(gen(perm)))

        self.assertEqual(Permutation.to_standard(range(10)),
                         Permutation((1,2,3,4,5,6,7,8,9,10)))
        self.assertEqual(Permutation.to_standard(10 - x for x in range(5)),
                         Permutation((5,4,3,2,1)))

    def test_call_1(self):
        p = Permutation((1,2,3,4))
        for i in range(1, len(p)+1):
            self.assertEqual(p(i), i)
        with self.assertRaises(AssertionError): p(0)
        with self.assertRaises(AssertionError): p(5)

    def test_call_2(self):
        p = Permutation((4,5,1,3,2))
        self.assertEqual(p(1), 4)
        self.assertEqual(p(2), 5)
        self.assertEqual(p(3), 1)
        self.assertEqual(p(4), 3)
        self.assertEqual(p(5), 2)
        with self.assertRaises(AssertionError): p(0)
        with self.assertRaises(AssertionError): p(6)

    def test_eq(self):
        self.assertTrue(Permutation([]) == Permutation([]))
        self.assertTrue(Permutation([1]) == Permutation([1]))
        self.assertTrue(Permutation([]) != Permutation([1]))
        self.assertTrue(Permutation([1]) != Permutation([]))
        self.assertFalse(Permutation([]) != Permutation([]))
        self.assertFalse(Permutation([1]) != Permutation([1]))
        self.assertFalse(Permutation([]) == Permutation([1]))
        self.assertFalse(Permutation([1]) == Permutation([]))
        for i in range(100):
            a = Permutations(random.randint(0,10)).random_element()
            b = Permutation(a)
            c = Permutations(random.randint(0,10)).random_element()
            if a == c:
                continue
            self.assertTrue(a == b)
            self.assertTrue(a != c)
            self.assertTrue(b == a)
            self.assertTrue(c != a)

    def test_avoids(self):
        self.assertTrue(Permutation([5,1,2,3,4]).avoids())
        self.assertFalse(Permutation([5,1,2,3,4]).avoids(Permutation([1,2,3])))
        self.assertFalse(Permutation([5,1,2,3,4]).avoids(Permutation([2,1])))
        self.assertTrue(Permutation([5,1,2,3,4]).avoids(Permutation([3,2,1])))
        self.assertFalse(Permutation([5,1,2,3,4]).avoids(Permutation([3,2,1]), Permutation([2,1])))
        self.assertTrue(Permutation([5,1,2,3,4]).avoids(Permutation([3,2,1]), Permutation([2,3,1])))

    def test_avoids_2(self):
        bound = 6
        def do_test(patts, expected):
            for i in range(min(len(expected), bound)):
                l = i+1
                cnt = 0
                for p in Permutations(l):
                    ok = True
                    for patt in patts:
                        if not p.avoids(Permutation(patt)):
                            ok = False
                            break
                    if ok:
                        cnt += 1
                self.assertEqual(expected[i], cnt)

        do_test([[1,2,3]], [1, 2, 5, 14, 42, 132, 429, 1430])
        do_test([[2,3,1]], [1, 2, 5, 14, 42, 132, 429, 1430])
        do_test([[1,3,4,2]], [1, 2, 6, 23, 103, 512, 2740, 15485])
        do_test([[2,4,1,3]], [1, 2, 6, 23, 103, 512, 2740, 15485])
        do_test([[1,2,3,4]], [1, 2, 6, 23, 103, 513, 2761, 15767])
        do_test([[1,4,3,2]], [1, 2, 6, 23, 103, 513, 2761, 15767])
        do_test([[2,1,4,3]], [1, 2, 6, 23, 103, 513, 2761, 15767])
        do_test([[1,3,2,4]], [1, 2, 6, 23, 103, 513, 2762, 15793])

    def test_incr_decr(self):
        for i in range(100):
            self.assertTrue(Permutation(list(range(1,i+1))).is_increasing())
            self.assertTrue(Permutation(list(range(i,0,-1))).is_decreasing())

        self.assertFalse(Permutation([1,3,2]).is_increasing())
        self.assertFalse(Permutation([1,3,2]).is_decreasing())
        self.assertFalse(Permutation([2,1,3]).is_increasing())
        self.assertFalse(Permutation([2,1,3]).is_decreasing())

    def test_lt(self):
        for _ in range(30):
            l1 = list(range(1, 10))
            l2 = list(range(1, 10))
            if l1 < l2:
                self.assertTrue(Permutation(l1) < permutation(l2))
            else:
                self.assertFalse(Permutation(l1) < Permutation(l2))
            self.assertFalse(Permutation(l1) < Permutation(l1))
            self.assertFalse(Permutation(l2) < Permutation(l2))

    def test_bool(self):
        self.assertTrue(Permutation([1,2,3,4]))
        self.assertTrue(Permutation([1]))
        self.assertFalse(Permutation([]))
        self.assertFalse(Permutation())
