from .union_find import UnionFind

DIR_EAST = 0
DIR_NORTH = 1
DIR_WEST = 2
DIR_SOUTH = 3
DIR_NONE = -1
DIRS = [DIR_EAST, DIR_NORTH, DIR_WEST, DIR_SOUTH]

__all__ = [
    "UnionFind",
    "DIRS",
    "DIR_EAST",
    "DIR_NORTH",
    "DIR_WEST",
    "DIR_SOUTH",
    "DIR_NONE",
]


def signum(n):
    return 1 if n > 0 else -1 if n < 0 else 0
