import unittest
from permuta import MeshPattern, Permutation

class TestMeshPattern(unittest.TestCase):

    def test_add_point(self):
        pass

    def test_list_perm(self):
        self.assertTrue(Permutation([1,2,3,4,5]).contains(MeshPattern([1,2,3], set([(0,0)]))))
        self.assertEqual(set([(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]), MeshPattern([2,1], set([])).non_pointless_boxes())

    def test_contained_in(self):
        self.assertTrue(Permutation([1,2,3]).contains(MeshPattern([1,2], set([(1,0),(1,1),(1,2)]))))
        shading = set([(0,0),(4,0),(2,1),(4,1),(2,2),(4,2),(3,3),(0,4)])
        pattern = [2,4,3,1]
        mesh_pattern = MeshPattern(pattern, shading)
        perm1 = Permutation([6,3,9,7,8,10,5,4,2,1])  # Occurrence: E.g., [1,3,6,9]
        perm2 = Permutation([2,3,9,7,6,10,5,4,8,1])  # Occurrence: E.g., [1,6,7,9]
        perm3 = Permutation([10,9,8,7,3,6,4,5,1,2])  # Occurrence: None
        self.assertTrue(mesh_pattern.contained_in(perm1))
        self.assertTrue(mesh_pattern.contained_in(perm2))
        self.assertFalse(mesh_pattern.contained_in(perm3))
        pass
