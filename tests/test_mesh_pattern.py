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

    def test_add_point(self):
        pass

    def test_list_perm(self):
        self.assertTrue(Permutation([1,2,3,4,5]).contains(MeshPattern([1,2,3], set([(0,0)]))))
        self.assertEqual(set([(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]), MeshPattern([2,1], set([])).non_pointless_boxes())

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
