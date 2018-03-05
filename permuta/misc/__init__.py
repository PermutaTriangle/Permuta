from . import checking
from .algorithm_x import AlgorithmX
from .counting import binomial, catalan, factorial
from .dancing_links import DancingLinks
from .exact_cover import exact_cover, exact_cover_smallest
from .iterable_floor_and_ceiling import (left_floor_and_ceiling,
                                         right_floor_and_ceiling)
from .misc import binary_search, choose, flatten, subsets
from .ordered_set_partitions import (ordered_set_partitions,
                                     ordered_set_partitions_no_cache)
from .progressbar import ProgressBar
from .ranges import cyclic_range, modulo_range
from .triemap import TrieMap
from .union_find import UnionFind

DIR_EAST = 0
DIR_NORTH = 1
DIR_WEST = 2
DIR_SOUTH = 3
DIR_NONE = -1
DIRS = [DIR_EAST, DIR_NORTH, DIR_WEST, DIR_SOUTH]


def signum(n):
    return 1 if n > 0 else -1 if n < 0 else 0
