import unittest
from permuta import MeshPattern, Permutation

class TestMeshPattern(unittest.TestCase):

    def test_add_point(self):
        pass

    def test_list_perm(self):
        #self.assertTrue(Permutation([1,2,3,4,5]).contains(MeshPattern([1,2,3], set([(0,0)]))))
        self.assertEqual(set([(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]), MeshPattern([2,1], set([])).non_pointless_boxes())

