import numbers

INDEX_TYPE_ERROR_MESSAGE = "'{}' object is not a valid index"
INDEX_VALUE_ERROR_MESSAGE = "{} is not a valid index"


def index(obj, maximum=None):
    """Check if an object is an index and raise exceptions if it isn't.

    Args:
        obj: <object>
            The object to be checked.
        maximum: <numbers.Integral>
            The number the object is not to exceed if it is a number.

    Raises:
        TypeError:
            Object is not an integral number.
        ValueError:
            Object is an integral number, but not a valid index.

    Examples:
        >>> index(4)
        >>> index(0)
        >>> index(-3)
        Traceback (most recent call last):
            ...
        ValueError: -3 is not a valid index
        >>> index(21, 30)
        >>> index(0.3)
        Traceback (most recent call last):
            ...
        TypeError: '0.3' object is not a valid index
        >>> index(333, 30)
        Traceback (most recent call last):
            ...
        ValueError: 333 is not a valid index

    """
    if isinstance(obj, numbers.Integral):
        if obj >= 0 and (maximum is None or obj <= maximum):
            return  # Index is good
        else:
            raise ValueError(INDEX_VALUE_ERROR_MESSAGE.format(obj))
    else:
        raise TypeError(INDEX_TYPE_ERROR_MESSAGE.format(repr(obj)))
