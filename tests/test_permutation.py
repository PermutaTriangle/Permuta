import unittest
import random

from permuta import MeshPattern, Permutation, Permutations


class TestPermutation(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(AssertionError): Permutation([0,1,1], check=True)
        with self.assertRaises(AssertionError): Permutation([1,0,1], check=True)
        with self.assertRaises(AssertionError): Permutation([0,0], check=True)
        with self.assertRaises(AssertionError): Permutation([1], check=True)
        with self.assertRaises(AssertionError): Permutation(101, check=True)
        with self.assertRaises(TypeError): Permutation(None, check=True)
        Permutation(check=True)
        Permutation([], check=True)
        Permutation([0], check=True)
        Permutation([3,0,2,1], check=True)
        Permutation(set([0,1,2]), check=True)
        p = Permutation(502134, check=True)
        self.assertEqual(p, Permutation((5,0,2,1,3,4)))

    def test_to_standard(self):
        def gen(perm):
            res = list(perm)
            add = 0
            for i in perm.inverse():
                add += random.randint(0,10)
                res[i] += add
            return Permutation(res)

        for _ in range(100):
            perm = Permutation.random(random.randint(0,20))
            self.assertEqual(perm, Permutation.to_standard(perm))
            self.assertEqual(perm, Permutation.to_standard(gen(perm)))

    def test_identity(self):
        for length in range(11):
            self.assertEqual(Permutation.identity(length),
                             Permutation(range(length)))

    def test_random(self):
        for length in range(11):
            for _ in range(10):
                perm = Permutation.random(length)
                self.assertEqual(len(perm), length)
                Permutation(perm, check=True)

    def test_monotone_increasing(self):
        for length in range(11):
            self.assertEqual(Permutation.monotone_increasing(length),
                             Permutation(range(length)))

    def test_monotone_decreasing(self):
        for length in range(11):
            self.assertEqual(Permutation.monotone_decreasing(length),
                             Permutation(range(length-1, -1, -1)))

    def test_unrank(self):
        self.assertEqual(Permutation.unrank(0),
                         Permutation())
        self.assertEqual(Permutation.unrank(1),
                         Permutation((0,)))
        self.assertEqual(Permutation.unrank(2),
                         Permutation((0,1)))
        self.assertEqual(Permutation.unrank(3),
                         Permutation((1,0)))
        self.assertEqual(Permutation.unrank(4),
                         Permutation((0,1,2)))
        self.assertEqual(Permutation.unrank(5),
                         Permutation((0,2,1)))
        self.assertEqual(Permutation.unrank(6),
                         Permutation((1,0,2)))
        self.assertEqual(Permutation.unrank(10),
                         Permutation((0,1,2,3)))
        amount = 1 + 1 + 2 + 6 + 24
        self.assertEqual(Permutation.unrank(amount),
                         Permutation((0,1,2,3,4)))
        amount = (1 + 1 + 2 + 6 + 24 + 120) - 1
        self.assertEqual(Permutation.unrank(amount),
                         Permutation((4,3,2,1,0)))
        with self.assertRaises(AssertionError): Permutation.unrank(-1)
        with self.assertRaises(AssertionError): Permutation.unrank(6, 3)
        ps = list(Permutations(7))
        urs = list(Permutation.unrank(n, 7) for n in range(len(ps)))
        self.assertEqual(urs, ps)

    def test_contained_in(self):
        def generate_contained(n,perm):
            # TODO: Ragnar: "I don't know how to make this method 0-based, Murray?"
            for i in range(len(perm),n):
                r = random.randint(1,len(perm)+1)
                for i in range(len(perm)):
                    if perm[i] >= r:
                        perm[i] += 1
                x = random.randint(0,len(perm))
                perm = perm[:x] + [r] + perm[x:]
            return Permutation(perm)

        self.assertTrue(Permutation([3,7,0,8,1,6,5,2,4]).contained_in(Permutation([3,7,0,8,1,6,5,2,4])))
        self.assertTrue(Permutation([]).contained_in(Permutation([])))
        self.assertTrue(Permutation([]).contained_in(Permutation([3,7,0,8,1,6,5,2,4])))
        self.assertTrue(Permutation([0]).contained_in(Permutation([0])))
        self.assertFalse(Permutation([7,3,0,8,1,6,5,2,4]).contained_in(Permutation([3,7,0,8,1,6,5,2,4])))

        for i in range(100):
            # TODO: Ragnar: "That also means I haven't touched this."
            n = random.randint(0, 4)
            patt = Permutations(n).random_element()
            perm = generate_contained(random.randint(n, 8), list(patt))
            self.assertTrue(patt.contained_in(perm))

        self.assertFalse(Permutation([0]).contained_in(Permutation([])))
        self.assertFalse(Permutation([0,1]).contained_in(Permutation([])))
        self.assertFalse(Permutation([0,1]).contained_in(Permutation([0])))
        self.assertFalse(Permutation([1, 0]).contained_in(Permutation([0, 1])))
        self.assertFalse(Permutation([0,1,2]).contained_in(Permutation([0,1])))
        self.assertFalse(Permutation([1, 0, 2]).contained_in(Permutation([0, 1, 3, 4, 2])))
        self.assertFalse(Permutation([0, 1, 2]).contained_in(Permutation([2, 1, 3, 0])))
        self.assertFalse(Permutation([2, 1, 3, 0]).contained_in(Permutation([2, 0, 3, 1])))
        self.assertFalse(Permutation([0, 2, 1]).contained_in(Permutation([2, 0, 1, 3])))
        self.assertFalse(Permutation([2, 0, 1, 3]).contained_in(Permutation([5, 3, 2, 7, 1, 0, 6, 4])))
        self.assertFalse(Permutation([0, 1, 2, 3]).contained_in(Permutation([4, 7, 5, 1, 6, 2, 3, 0])))

    def test_count_occurrences_in(self):
        self.assertEqual(Permutation([]).count_occurrences_in(Permutation([4,1,2,3,0])), 1)
        self.assertEqual(Permutation([0]).count_occurrences_in(Permutation([4,1,2,3,0])), 5)
        self.assertEqual(Permutation([0,1]).count_occurrences_in(Permutation([4,1,2,3,0])), 3)
        self.assertEqual(Permutation([1,0]).count_occurrences_in(Permutation([4,1,2,3,0])), 7)
        self.assertEqual(Permutation([4,1,2,3,0]).count_occurrences_in(Permutation([])), 0)
        self.assertEqual(Permutation([4,1,2,3,0]).count_occurrences_in(Permutation([1,0])), 0)

    def test_occurrences_in(self):
        self.assertEqual(
                          list(Permutation([]).occurrences_in(Permutation([4,1,2,3,0])))
                        , [[]]
                        )
        self.assertEqual(
                          sorted(Permutation([0]).occurrences_in(Permutation([4,1,2,3,0])))
                        , [[0],[1],[2],[3],[4]]
                        )
        self.assertEqual(
                          sorted(Permutation([0,1]).occurrences_in(Permutation([4,1,2,3,0])))
                        , [[1,2],[1,3],[2,3]]
                        )
        self.assertEqual(
                          sorted(Permutation([1,0]).occurrences_in(Permutation([4,1,2,3,0])))
                        , [[0,1],[0,2],[0,3],[0,4],[1,4],[2,4],[3,4]]
                        )
        self.assertEqual(list(Permutation([4,1,2,3,0]).occurrences_in(Permutation([]))), [])
        self.assertEqual(list(Permutation([4,1,2,3,0]).occurrences_in(Permutation([1,0]))), [])

    def test_apply(self):
        for i in range(100):
            n = random.randint(0,20)
            lst = [random.randint(0,10000) for _ in range(n)]
            perm = Permutation.random(n)
            res = list(perm.apply(lst))
            for j,k in enumerate(perm.inverse()):
                self.assertEqual(lst[j], res[k])

    def test_direct_sum(self):
        p1 = Permutation((0,1,3,2))
        p2 = Permutation((0,4,2,1,3))
        p3 = Permutation(201)
        p4 = Permutation((0,))
        p5 = Permutation()
        # All together
        result = p1.direct_sum(p2, p3, p4, p5)
        expected = Permutation((0,1,3,2,4,8,6,5,7,11,9,10,12))
        self.assertEqual(result, expected)
        # Two
        result = p1.direct_sum(p3)
        expected = Permutation((0,1,3,2,6,4,5))
        self.assertEqual(result, expected)
        # None
        self.assertEqual(p1.direct_sum(), p1)
        
    def test_skew_sum(self):
        p1 = Permutation((0,1,3,2))
        p2 = Permutation((0,4,2,1,3))
        p3 = Permutation(201)
        p4 = Permutation((0,))
        p5 = Permutation()
        # All together
        result = p1.skew_sum(p2, p3, p4, p5)
        expected = Permutation((9,10,12,11,4,8,6,5,7,3,1,2,0))
        self.assertEqual(result, expected)
        # Two
        result = p1.skew_sum(p3)
        expected = Permutation((3,4,6,5,2,0,1))
        self.assertEqual(result, expected)
        # None
        self.assertEqual(p1.skew_sum(), p1)

    def test_inverse(self):
        for i in range(10):
            self.assertEqual(Permutation(range(i)), Permutation(range(i)).inverse())
        self.assertEqual(Permutation([2,1,3,0]), Permutation([3,1,0,2]).inverse())
        self.assertEqual(Permutation([4,3,1,6,5,7,8,0,2]), Permutation([7,2,8,1,0,4,3,5,6]).inverse())

    def test_rotate_right(self):
        for i in range(10):
            self.assertEqual(Permutation(range(i-1,-1,-1)), Permutation(range(i)).rotate_right())
        self.assertEqual(Permutation([2,1,3,4,0,5,6]), Permutation([6,5,3,2,0,1,4]).rotate_right())
        self.assertEqual(Permutation([4,5,3,1,7,0,2,6]), Permutation([4,7,1,0,2,6,3,5]).rotate_right())
        self.assertEqual(Permutation([0,1,2]), Permutation([2,1,0]).rotate_right(5))
        self.assertEqual(Permutation([4,5,3,1,0,2]), Permutation([4,5,3,1,0,2]).rotate_right(4))

    def test_rotate_left(self):
        for i in range(10):
            self.assertEqual(Permutation(list(range(i-1,-1,-1))), Permutation(range(i)).rotate_right())
        self.assertEqual(Permutation([6,5,3,2,0,1,4]).rotate_left(), Permutation([6,5,3,2,0,1,4]).rotate_right(3))
        self.assertEqual(Permutation([6,5,3,2,0,1,4]).rotate_left(), Permutation([6,5,3,2,0,1,4]).rotate_right(-1))
        self.assertEqual(Permutation([4,7,1,0,2,6,3,5]).rotate_left(), Permutation([4,7,1,0,2,6,3,5]).rotate_right(7))
        self.assertEqual(Permutation([]).rotate_left(), Permutation([]).rotate_left(123))

    def test_shift_left(self):
        self.assertEqual(Permutation([]), Permutation([]).shift_left())
        self.assertEqual(Permutation([0]), Permutation([0]).shift_left())
        self.assertEqual(Permutation([0,1,2,3,4,5,6,7]), Permutation([0,1,2,3,4,5,6,7]).shift_left(0))
        self.assertEqual(Permutation([0,1,2,3,4,5,6,7]), Permutation([5,6,7,0,1,2,3,4]).shift_left(3))
        self.assertEqual(Permutation([0,1,2,3,4,5,6,7]), Permutation([0,1,2,3,4,5,6,7]).shift_left(800))
        self.assertEqual(Permutation([0,1,2,3,4,5,6,7]), Permutation([5,6,7,0,1,2,3,4]).shift_left(403))
        self.assertEqual(Permutation([0,1,2,3,4,5,6,7]), Permutation([0,1,2,3,4,5,6,7]).shift_left(-8))
        self.assertEqual(Permutation([0,1,2,3,4,5,6,7]), Permutation([5,6,7,0,1,2,3,4]).shift_left(-5))

    def test_shift_down(self):
        self.assertEqual(Permutation([]), Permutation([]).shift_down(1000))
        self.assertEqual(Permutation([0]), Permutation([0]).shift_down(10))
        self.assertEqual(Permutation([1,0,4,2,3,5]), Permutation([2,1,5,3,4,0]).shift_down())
        self.assertEqual(Permutation([1,0,4,2,3,5]), Permutation([2,1,5,3,4,0]).shift_down(13))
        self.assertEqual(Permutation([1,0,4,2,3,5]), Permutation([5,4,2,0,1,3]).shift_down(-2))
        self.assertEqual(Permutation([1,0,4,2,3,5]), Permutation([5,4,2,0,1,3]).shift_down(-8))

    def test_reverse(self):
        self.assertEqual(Permutation([5,2,3,0,4,6,1]), Permutation([1,6,4,0,3,2,5]).reverse())
        self.assertEqual(Permutation([7,1,0,2,4,6,3,5]), Permutation([5,3,6,4,2,0,1,7]).reverse())

    def test_complement(self):
        self.assertEqual(Permutation([6,4,2,3,1,0,5]), Permutation([0,2,4,3,5,6,1]).complement())
        self.assertEqual(Permutation([2,5,6,3,7,4,0,1]), Permutation([5,2,1,4,0,3,7,6]).complement())

    def test_reverse_complement(self):
        for _ in range(100):
            perm = Permutation.random(random.randint(0,20))
            self.assertEqual(perm.reverse_complement(), perm.rotate().rotate())

    def test_flip_antidiagonal(self):
        for i in range(100):
            perm = Permutation.random(random.randint(0,20))
            self.assertEqual(perm.reverse().complement().inverse(), perm.flip_antidiagonal())

    def test_fixed_points(self):
        self.assertEqual(Permutation().fixed_points(), 0)
        self.assertEqual(Permutation((0,2,1)).fixed_points(), 1)
        self.assertEqual(Permutation(543210).fixed_points(), 0)
        self.assertEqual(Permutation(410325).fixed_points(), 3)
        self.assertEqual(Permutation((0,1,2,3,4,5)).fixed_points(), 6)

    def test_descents(self):
        self.assertEqual(list(Permutation().descents()), [])
        self.assertEqual(list(Permutation((0,1,2,3)).descents()), [])
        self.assertEqual(list(Permutation(3210).descents()), [1,2,3])
        self.assertEqual(list(Permutation(210435).descents()), [1, 2, 4])
        self.assertEqual(list(Permutation(1230654).descents()), [3, 5, 6])
        self.assertEqual(list(Permutation(31450762).descents()), [1, 4, 6, 7])

    def test_count_descents(self):
        self.assertEqual(Permutation().count_descents(), 0)
        self.assertEqual(Permutation((0,1,2,3)).count_descents(), 0)
        self.assertEqual(Permutation(3210).count_descents(), 3)
        self.assertEqual(Permutation(210435).count_descents(), 3)
        self.assertEqual(Permutation(1230654).count_descents(), 3)
        self.assertEqual(Permutation(31450762).count_descents(), 4)

    def test_ascents(self):
        self.assertEqual(list(Permutation().ascents()), [])
        self.assertEqual(list(Permutation((0,1,2,3)).ascents()), [1,2,3])
        self.assertEqual(list(Permutation(3210).ascents()), [])
        self.assertEqual(list(Permutation(210435).ascents()), [3, 5])
        self.assertEqual(list(Permutation(1230654).ascents()), [1, 2, 4])
        self.assertEqual(list(Permutation(31450762).ascents()), [2, 3, 5])

    def test_count_ascents(self):
        self.assertEqual(Permutation().count_ascents(), 0)
        self.assertEqual(Permutation((0,1,2,3)).count_ascents(), 3)
        self.assertEqual(Permutation(3210).count_ascents(), 0)
        self.assertEqual(Permutation(210435).count_ascents(), 2)
        self.assertEqual(Permutation(1230654).count_ascents(), 3)
        self.assertEqual(Permutation(31450762).count_ascents(), 3)

    def test_peaks(self):
        self.assertEqual(list(Permutation().peaks()), [])
        self.assertEqual(list(Permutation((0,1,2,3)).peaks()), [])
        self.assertEqual(list(Permutation(210435).peaks()), [3])
        self.assertEqual(list(Permutation(1230654).peaks()), [2, 4])

    def test_count_peaks(self):
        self.assertEqual(Permutation().count_peaks(), 0)
        self.assertEqual(Permutation((0,1,2,3)).count_peaks(), 0)
        self.assertEqual(Permutation(210435).count_peaks(), 1)
        self.assertEqual(Permutation(1230654).count_peaks(), 2)

    def test_valleys(self):
        self.assertEqual(list(Permutation().valleys()), [])
        self.assertEqual(list(Permutation((0,1,2,3)).valleys()), [])
        self.assertEqual(list(Permutation(210435).valleys()), [2, 4])
        self.assertEqual(list(Permutation(1230654).valleys()), [3])
        self.assertEqual(list(Permutation(2130645).valleys()), [1, 3, 5])

    def test_count_valleys(self):
        self.assertEqual(Permutation().count_valleys(), 0)
        self.assertEqual(Permutation((0,1,2,3)).count_valleys(), 0)
        self.assertEqual(Permutation(210435).count_valleys(), 2)
        self.assertEqual(Permutation(1230654).count_valleys(), 1)
        self.assertEqual(Permutation(2130646).count_valleys(), 3)

    def test_call_1(self):
        p = Permutation((0,1,2,3))
        for i in range(len(p)):
            self.assertEqual(p(i), i)
        with self.assertRaises(AssertionError): p(-1)
        with self.assertRaises(AssertionError): p(4)

    def test_call_2(self):
        p = Permutation((3,4,0,2,1))
        self.assertEqual(p(0), 3)
        self.assertEqual(p(1), 4)
        self.assertEqual(p(2), 0)
        self.assertEqual(p(3), 2)
        self.assertEqual(p(4), 1)
        with self.assertRaises(AssertionError): p(-1)
        with self.assertRaises(AssertionError): p(5)

    def test_eq(self):
        self.assertTrue(Permutation([]) == Permutation([]))
        self.assertTrue(Permutation([0]) == Permutation([0]))
        self.assertTrue(Permutation([]) != Permutation([0]))
        self.assertTrue(Permutation([0]) != Permutation([]))
        self.assertFalse(Permutation([]) != Permutation([]))
        self.assertFalse(Permutation([0]) != Permutation([0]))
        self.assertFalse(Permutation([]) == Permutation([0]))
        self.assertFalse(Permutation([0]) == Permutation([]))
        for _ in range(100):
            a = Permutation.random(random.randint(0,10))
            b = Permutation(a)
            c = Permutation.random(random.randint(0,10))
            if a == c:
                continue
            self.assertTrue(a == b)
            self.assertTrue(a != c)
            self.assertTrue(b == a)
            self.assertTrue(c != a)

    def test_avoids(self):
        self.assertTrue(Permutation([4,0,1,2,3]).avoids())
        self.assertFalse(Permutation([4,0,1,2,3]).avoids(Permutation([0,1,2])))
        self.assertFalse(Permutation([4,0,1,2,3]).avoids(Permutation([1,0])))
        self.assertTrue(Permutation([4,0,1,2,3]).avoids(Permutation([2,1,0])))
        self.assertFalse(Permutation([4,0,1,2,3]).avoids(Permutation([2,1,0]), Permutation([1,0])))
        self.assertTrue(Permutation([4,0,1,2,3]).avoids(Permutation([2,1,0]), Permutation([1,2,0])))

    def test_avoids_2(self):
        # TODO: Ragnar: "I leave the 0-indexing of this test as an exercise for Murray"
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
            self.assertTrue(Permutation(range(i)).is_increasing())
            self.assertTrue(Permutation(range(i-1,-1,-1)).is_decreasing())

        self.assertFalse(Permutation([0,2,1]).is_increasing())
        self.assertFalse(Permutation([0,2,1]).is_decreasing())
        self.assertFalse(Permutation([1,0,2]).is_increasing())
        self.assertFalse(Permutation([1,0,2]).is_decreasing())

    def test_lt(self):
        # TODO: No length testing is done here
        for _ in range(30):
            l1 = list(range(10))
            l2 = list(range(10))
            random.shuffle(l1)
            random.shuffle(l2)
            if l1 < l2:
                self.assertTrue(Permutation(l1) < permutation(l2))
            else:
                self.assertFalse(Permutation(l1) < Permutation(l2))
            self.assertFalse(Permutation(l1) < Permutation(l1))
            self.assertFalse(Permutation(l2) < Permutation(l2))

    def test_bool(self):
        self.assertTrue(Permutation([0,1,2,3]))
        self.assertTrue(Permutation([0]))
        self.assertFalse(Permutation([]))
        self.assertFalse(Permutation())
