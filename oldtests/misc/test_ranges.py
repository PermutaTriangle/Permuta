import unittest
from permuta.misc import cyclic_range, modulo_range

class TestRanges(unittest.TestCase):

    def test_cyclic_range(self):
        result = list(cyclic_range(5, 30, -20))
        expected = list(range(5, 30))
        expected.extend(range(-20, 5))
        self.assertEqual(result, expected)

    def test_modulo_range(self):
        result = list(modulo_range(7, 30))
        expected = list(range(7, 30))
        expected.extend(range(7))
        self.assertEqual(result, expected)

        result = list(modulo_range(0, 30))
        expected = list(range(0, 30))
        self.assertEqual(result, expected)
