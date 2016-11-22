import unittest
from permuta import MeshPattern, Permutation

class TestMeshPattern(unittest.TestCase):

    def setUp(self):
        pattern = [2,4,3,1]
        shading = set([(0,0),(4,0),(2,1),(4,1),(2,2),(4,2),(3,3),(0,4)])
        self.mesh_pattern = MeshPattern(pattern, shading)
        self.perm1 = Permutation([6,3,9,7,8,10,5,4,2,1])  # Occurrence: E.g., [1,3,6,9]
        self.perm2 = Permutation([2,3,9,7,6,10,5,4,8,1])  # Occurrence: E.g., [1,6,7,9]
        self.perm3 = Permutation([10,9,8,7,3,6,4,5,1,2])  # Occurrence: None (avoids)
        self.perm4 = Permutation([1,2,3,4,5])  # Avoids as well
        self.perm5 = Permutation([2,3,5,4,1])  # Two occurrences
        self.patt1 = self.perm4
        self.patt2 = self.perm5
        self.patt3 = Permutation((3,4,1,2))
        self.shad1 = frozenset([(5,0),(5,1),(5,2),(3,2),(2,1),(3,3),(0,0),(1,0),(2,0)])
        self.shad2 = frozenset([(3,3),(2,2),(1,1),(0,2)])
        self.shad3 = frozenset([(1,3),(4,4),(2,1),(2,2),(0,4),(4,0)])
        self.mesh1 = MeshPattern(self.patt1, self.shad1)
        self.mesh2 = MeshPattern(self.patt2, self.shad2)
        self.mesh3 = MeshPattern(self.patt3, self.shad3)

    def test_list_perm(self):
        # TODO: What is this?
        self.assertTrue(Permutation([1,2,3,4,5]).contains(MeshPattern([1,2,3], set([(0,0)]))))
        self.assertEqual(set([(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]), MeshPattern([2,1], set([])).non_pointless_boxes())

    def test_init_new(self):
        # TODO
        pass

    def test_complement(self):
        # TODO
        pass

    def test_reverse(self):
        # TODO
        pass

    def test_inverse(self):
        # TODO
        pass

    def test_sub_mesh_pattern(self):
        # Sub mesh pattern from indices 1, 2, and 3 of mesh1
        pattern = (1,2,3)
        shading = set([(1,0),(2,1),(2,2)])
        mesh_pattern = MeshPattern(pattern, shading)
        sub_mesh_pattern = self.mesh1.sub_mesh_pattern((1,2,3))
        self.assertEqual(sub_mesh_pattern, mesh_pattern)
        # Sub mesh pattern from indices 0, 1, and 4 of mesh1
        pattern = (1,2,3)
        shading = set([(0,0),(1,0),(3,0),(3,1)])
        mesh_pattern = MeshPattern(pattern, shading)
        sub_mesh_pattern = self.mesh1.sub_mesh_pattern((0,1,4))
        self.assertEqual(sub_mesh_pattern, mesh_pattern)
        # Sub mesh pattern from indices 3 and 4 of mesh1
        self.assertEqual(self.mesh1.sub_mesh_pattern((3,4)), MeshPattern((1,2)))
        # Sub mesh pattern from indices 2 and 3 of mesh1
        self.assertEqual(self.mesh1.sub_mesh_pattern((2,3)), MeshPattern((1,2), set([(1,1)])))
        # Sub mesh pattern from index 0 of mesh3
        self.assertEqual(self.mesh3.sub_mesh_pattern((0,)), MeshPattern((1,)))
        # Sub mesh pattern from indices 0, 1, and 3 of mesh3
        self.assertEqual(self.mesh3.sub_mesh_pattern((0,1,3)), MeshPattern((2,3,1), set([(0,3),(1,2),(3,3)])))
        # Some complete sub meshes
        self.assertEqual(self.mesh1.sub_mesh_pattern(range(len(self.mesh1))), self.mesh1)
        self.assertEqual(self.mesh2.sub_mesh_pattern(range(len(self.mesh2))), self.mesh2)
        self.assertEqual(self.mesh3.sub_mesh_pattern(range(len(self.mesh3))), self.mesh3)

    def test_rotate(self):
        # Rotate once
        pattern = self.patt2.rotate()
        shading = set([(2,3),(3,2),(2,5),(1,4)])
        mesh = MeshPattern(pattern, shading)
        self.assertEqual(mesh, self.mesh2.rotate())
        # Rotate twice
        pattern = self.patt2.rotate(2)
        shading = set([(2,2),(3,3),(4,4),(5,3)])
        mesh = MeshPattern(pattern, shading)
        self.assertEqual(mesh, self.mesh2.rotate(2))
        # Rotate thrice
        pattern = self.patt2.rotate(3)
        shading = set([(2,3),(3,2),(4,1),(3,0)])
        mesh = MeshPattern(pattern, shading)
        self.assertEqual(mesh, self.mesh2.rotate(3))

    def flip_horizontal(self):
        # TODO
        pass

    def flip_vertical(self):
        # TODO
        pass

    def flip_diagonal(self):
        # TODO
        pass

    def flip_antidiagonal(self):
        # TODO
        pass

    def test_shade(self):
        # TODO
        pass

    def test_add_point(self):
        # TODO
        pass

    def test_add_increase(self):
        # TODO
        pass

    def test_add_decrease(self):
        # TODO
        pass

    def test_occurrences_in(self):
        # TODO: Maybe the contained_in, etc. tests are enough?
        pass

    def test_contained_in(self):
        self.assertTrue(Permutation([1,2,3]).contains(MeshPattern([1,2], set([(1,0),(1,1),(1,2)]))))
        self.assertTrue(self.mesh_pattern.contained_in(self.perm1))
        self.assertTrue(self.mesh_pattern.contained_in(self.perm2))
        self.assertFalse(self.mesh_pattern.contained_in(self.perm3))
        self.assertTrue(self.mesh_pattern.contained_in(self.perm1, self.perm2))
        self.assertFalse(self.mesh_pattern.contained_in(self.perm1, self.perm3))

    def test_avoided_by(self):
        self.assertFalse(self.mesh_pattern.avoided_by(self.perm1))
        self.assertFalse(self.mesh_pattern.avoided_by(self.perm2))
        self.assertTrue(self.mesh_pattern.avoided_by(self.perm3))
        self.assertTrue(self.mesh_pattern.avoided_by(self.perm4))
        self.assertTrue(self.mesh_pattern.avoided_by(self.perm3, self.perm4))
        self.assertFalse(self.mesh_pattern.avoided_by(self.perm4, self.perm1, self.perm3))

    def test_count_occurrences_in(self):
        self.assertEqual(self.mesh_pattern.count_occurrences_in(self.perm1), 8)
        self.assertEqual(self.mesh_pattern.count_occurrences_in(self.perm2), 12)
        self.assertEqual(self.mesh_pattern.count_occurrences_in(self.perm3), 0)
        self.assertEqual(self.mesh_pattern.count_occurrences_in(self.perm4), 0)
        self.assertEqual(self.mesh_pattern.count_occurrences_in(self.perm5), 2)

    def test_is_shaded(self):
        # TODO
        pass

    def test_non_pointless_boxes(self):
        # TODO
        pass

    def test_rank(self):
        # TODO
        pass

    def test_unrank(self):
        pattern = Permutation([1,2])
        shading = set([(0,1),
                       (0,2),
                       (1,2),
                       (2,0),
                       (2,1)])
        number = 230
        mesh = MeshPattern(pattern, shading)
        self.assertEqual(MeshPattern.unrank(pattern, number), mesh)
        pattern = Permutation([3,1,2])
        shading = set([(0,0),
                       (0,1),
                       (0,2),
                       (1,0),
                       (1,2),
                       (2,0),
                       (2,1),
                       (2,2),
                       (2,3),
                       (3,0)])
        number = 8023
        mesh = MeshPattern(pattern, shading)
        self.assertEqual(MeshPattern.unrank(pattern, number), mesh)
        with self.assertRaises(AssertionError):
            self.assertEqual(MeshPattern.unrank([1,2,3], -1))
        with self.assertRaises(AssertionError):
            self.assertEqual(MeshPattern.unrank(Permutation([1]), "1"))
        with self.assertRaises(AssertionError):
            self.assertEqual(MeshPattern.unrank(Permutation([1]), 16))
        with self.assertRaises(AssertionError):
            self.assertEqual(MeshPattern.unrank(Permutation([1]), -1))
        pattern = self.patt1
        number = 0b111000000001100000011000001000001
        mesh = self.mesh1
        self.assertEqual(MeshPattern.unrank(pattern, number), mesh)

    def test_len(self):
        self.assertEqual(len(self.mesh1), 5)
        self.assertEqual(len(self.mesh2), 5)
        self.assertEqual(len(self.mesh3), 4)
        self.assertEqual(len(MeshPattern()), 0)
        self.assertEqual(len(MeshPattern((1,))), 1)

    def test_eq(self):
        self.assertNotEqual(self.mesh1, self.mesh2)
        self.assertNotEqual(self.mesh1, self.mesh3)
        self.assertNotEqual(self.mesh2, self.mesh1)
        self.assertNotEqual(self.mesh2, self.mesh3)
        self.assertNotEqual(self.mesh3, self.mesh1)
        self.assertNotEqual(self.mesh3, self.mesh2)
        mesh1copy = MeshPattern(self.patt1, self.shad1)
        mesh2copy = MeshPattern(self.patt2, self.shad2)
        mesh3copy = MeshPattern(self.patt3, self.shad3)
        self.assertEqual(self.mesh1, mesh1copy)
        self.assertEqual(self.mesh2, mesh2copy)
        self.assertEqual(self.mesh3, mesh3copy)
        self.assertEqual(mesh1copy, mesh1copy)
        self.assertEqual(mesh2copy, mesh2copy)
        self.assertEqual(mesh3copy, mesh3copy)

    def test_bool(self):
        self.assertTrue(self.mesh1)
        self.assertTrue(self.mesh2)
        self.assertTrue(self.mesh3)
        self.assertTrue(MeshPattern(Permutation((1,))))
        self.assertTrue(MeshPattern((), set([(0,0)])))
        self.assertFalse(MeshPattern())

    def test_contains(self):
        # TODO
        pass
