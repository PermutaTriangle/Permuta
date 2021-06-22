from itertools import chain
from typing import Dict, Iterable, List, Optional, Tuple


def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization."""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


class Matrix:
    """
    Creates a square matrix of the dimensions (size x size).
    Arguments:
        `size:` The size of the `n x n` matrix.
        `binary:` If set to True then all calculations are done over GF(2).
        `elements:` The function from pos to value at pos. `f(pos) = value`.
    """

    def __init__(
        self,
        size: int,
        elements: Optional[Dict[Tuple[int, int], int]] = None,
        binary: bool = True,
    ) -> None:
        if elements:
            self.elements: Dict[Tuple[int, int], int] = {
                key: (1 if binary and val else val) for key, val in elements.items()
            }
        else:
            self.elements = dict()
        self.binary = binary
        self._size = size

    def __getitem__(self, pos) -> int:
        """Get value in row, col specified"""
        return self.elements[pos] if pos in self.elements else 0

    def __setitem__(self, pos, value) -> None:
        """Sets position in the matrix to val"""
        assert 0 <= pos[0] < len(self)
        assert 0 <= pos[1] < len(self)
        self.elements[pos] = value

    def __add__(self, other: "Matrix") -> "Matrix":
        """Adds two matrices together. Both classes have to be binary or not binary"""
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.binary != other.binary:
            return NotImplemented
        assert len(self) == len(other)
        new_mat = Matrix(size=len(self))
        funcs = [self.elements.items(), other.elements.items()]
        if self.binary:
            for idx, val in chain(*funcs):
                new_mat[idx] ^= val
        else:
            for idx, val in chain(*funcs):
                new_mat[idx] += val
        return new_mat

    def __mul__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.binary != other.binary:
            return NotImplemented
        assert len(self) == len(other)
        mat = Matrix(size=len(self), elements={})
        for row in range(len(self)):
            for col in range(len(self)):
                for k in range(len(self)):
                    mat[(row, col)] += self[(row, k)] * other[(k, col)]
        return mat

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        string = ""
        for row in range(len(self)):
            for col in range(len(self)):
                cell = self[row, col]
                string += f"|{cell}"
            string += "|\n"
        return string

    def __repr__(self) -> str:
        return f"Matrix({len(self)}, {self.elements})"

    def __eq__(self, other: object) -> bool:
        """Returns True if both matrices are equal."""
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.binary != other.binary:
            return NotImplemented
        if len(self) != len(other):
            return False
        for row in range(len(self)):
            for col in range(len(self)):
                if self[row, col] != other[row, col]:
                    return False
        return True

    def test_sum(self) -> int:
        """Sums up all the values in the matrix."""
        return sum(self.elements.values())

    def hamming_sums(self, row: bool = True) -> List[int]:
        """Gives the hamming sums for either the rows or columns"""
        key_idx = 0 if row else 1
        out = []
        for idx in range(len(self)):
            out.append(0)
            for key, val in self.elements.items():
                if key[key_idx] == idx:
                    out[idx] += val
        return out

    def row_labels(self) -> Tuple[int, ...]:
        """
        Looks at each row as a binary number and returns the binary value for each.
        """
        out_list: List[int] = list()
        for row_idx in range(len(self)):
            num = 0
            for key, val in self.elements.items():
                if key[0] == row_idx and val:
                    num += 2 ** (key[1])
            out_list.append(num)
        return tuple(sorted(out_list))

    def apply_perm(self, perm: Iterable[int], row: bool = True) -> "Matrix":
        """Returns a new matrix which has the given permutation
        applied on either the rows or columns of the matrix"""
        new_func: Dict[Tuple[int, int], int] = dict()
        for n_idx, p_idx in enumerate(perm):
            for idx in range(len(self)):
                if row:
                    pos = (p_idx, idx)
                else:
                    pos = (idx, p_idx)

                if pos in self.elements:
                    if row:
                        new_func[n_idx, idx] = self[pos]
                    else:
                        new_func[idx, n_idx] = self[pos]

        return Matrix(len(self), elements=new_func)

    def __hash__(self) -> int:
        return hash(str(self))


class LoTriMatrix(Matrix):
    """Returns a (n x n) lower triangular matrix"""

    def __init__(self, size: int):
        super().__init__(size)
        for row in range(size):
            for col in range(size):
                if col <= row:
                    self[row, col] = 1
