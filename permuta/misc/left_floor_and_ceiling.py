import collections

FloorAndCeiling = collections.namedtuple("FloorAndCeiling", ["floor", "ceiling"])

def left_floor_and_ceiling(iterable, default_floor=None, default_ceiling=None):
    # TODO: Make comment better
    """What is known when scanning self from left to right.

    TODO: Make comments nice and make betterer

    Yields: (int, int)
        The i-th yielded tuple is the left floor and ceiling (respectively) of
        the i-th element of the iterable.
    """
    for base_index in range(len(iterable)):
        left_floor_index = None
        left_ceiling_index = None
        left_floor = 1
        left_ceiling = len(iterable)
        base_element = iterable[base_index]
        for index in range(base_index):
            element = iterable[index]
            if element > base_element:
                if element <= left_ceiling:
                    left_ceiling_index = index

                    left_ceiling = element
            else:
                if element >= left_floor:
                    left_floor_index = index
                    left_floor = element
        # left_floor_difference:
        # How much greater than the left floor the element must be,
        # or how much greater than 1 it must be if left floor does not exist
        left_floor_difference = base_element - left_floor
        # left_ceiling_difference:
        # Subtract this number from the length of the permutation an
        # occurrence is being searched for in to get an upper bound for the
        # allowed value. Tighten the bound by subtracting from the left
        # ceiling value if its index is not None.
        left_ceiling_difference = left_ceiling - base_element
        yield FloorAndCeiling(left_floor_index, left_ceiling_index)
