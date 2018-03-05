import collections

FloorAndCeiling = collections.namedtuple("FloorAndCeiling",
                                         ["floor", "ceiling"])


def left_floor_and_ceiling(iterable, default_floor=None, default_ceiling=None):
    """Find the left floor and ceiling indices of iterable.

    Define left_floor of an element in a sequence to be the index of the
    greatest smaller element to the left of said element, or default_floor
    if there is none. Similarly define default_ceiling. This function yields
    a tuple (left_floor, left_ceiling) for each element of iterable.

    Args:
        iterable: <iterable>
            An iterable of totally ordered unique elements.
        default_floor: <object>
        default_ceiling: <object>

    Yields: (int, int)
        The i-th yielded tuple is the left floor and ceiling indices of
        the i-th element of the iterable. The tuples are named tuples
        with floor and ceiling attributes.
    """
    # TODO: Define behaviour for duplicate elements
    dq = collections.deque()
    smallest = None
    biggest = None
    index = 0
    for element in iterable:
        if index == 0:
            dq.append((element, index))
            smallest = element
            biggest = element
            yield FloorAndCeiling(default_floor, default_ceiling)
        else:
            if element <= smallest:
                # Rotate until smallest element is at front
                while dq[0][0] != smallest:
                    dq.rotate(-1)
                yield FloorAndCeiling(default_floor, dq[0][1])
                dq.appendleft((element, index))
                smallest = element
            elif element >= biggest:
                # Rotate until biggest element is at end
                while dq[-1][0] != biggest:
                    dq.rotate(-1)
                yield FloorAndCeiling(dq[-1][1], default_ceiling)
                dq.append((element, index))
                biggest = element
            else:
                while not dq[-1][0] <= element <= dq[0][0]:
                    dq.rotate()
                yield FloorAndCeiling(dq[-1][1], dq[0][1])
                dq.appendleft((element, index))
        index += 1


def right_floor_and_ceiling(iterable, default_floor=None,
                            default_ceiling=None):
    """The right counterpart of left_floor_and_ceiling."""
    # TODO: Implement nicely
    result = left_floor_and_ceiling(reversed(list(iterable)),
                                    default_floor, default_ceiling)
    for fac in reversed(list(result)):
        yield fac
