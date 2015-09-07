
from .permutation import Permutation
from .permutations import Permutations
from .mesh_pattern import MeshPattern
from .mesh_patterns import MeshPatterns

def factorial(n):
    res = 1
    for i in range(2, n+1):
        res *= i
    return res

