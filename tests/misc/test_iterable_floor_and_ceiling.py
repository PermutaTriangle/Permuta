import unittest
from permuta.misc import left_floor_and_ceiling, right_floor_and_ceiling

class TestIterableFloorAndCeiling(unittest.TestCase):

    def test_left_floor_and_ceiling(self):
        iterable = [4,5,1,2,3,6]
        expected = [
                     (None, None)  # 4
                   , (0   , None)  # 5
                   , (None, 0   )  # 1
                   , (2   , 0   )  # 2
                   , (3   , 0   )  # 3
                   , (1   , None)  # 6
                   ]
        index = 0
        for fac in left_floor_and_ceiling(iterable):
            self.assertEqual(fac, expected[index])
            index += 1

        iterable = [4,1,2,5,3]
        expected = [
                     (-1  , 5   )  # 4
                   , (-1  , 0   )  # 1
                   , (1   , 0   )  # 2
                   , (0   , 5   )  # 5
                   , (2   , 0   )  # 3
                   ]
        index = 0
        for fac in left_floor_and_ceiling(iterable, default_floor=-1, default_ceiling=5):
            self.assertEqual(fac, expected[index])
            index += 1

        iterable = [1,2,3]
        expected = [
                     (None, None)  # 1
                   , (0   , None)  # 2
                   , (1   , None)  # 3
                   ]
        index = 0
        for fac in left_floor_and_ceiling(iterable):
            self.assertEqual(fac, expected[index])
            index += 1

        iterable = [3,2,1]
        expected = [
                     (None, None)  # 3
                   , (None, 0   )  # 2
                   , (None, 1   )  # 1
                   ]
        index = 0
        for fac in left_floor_and_ceiling(iterable):
            self.assertEqual(fac, expected[index])
            index += 1

    def test_right_floor_and_ceiling(self):
        iterable = [4,5,1,2,3,6]
        expected = [
                     (None, "on")  # 4
                   , (0   , "on")  # 5
                   , (None, 0   )  # 1
                   , (2   , 0   )  # 2
                   , (3   , 0   )  # 3
                   , (1   , "on")  # 6
                   ]
        iterable = reversed(iterable)
        expected = list(reversed(expected))
        index = 0
        for fac in right_floor_and_ceiling(iterable, default_ceiling="on"):
            self.assertEqual(fac, expected[index])
            index += 1
