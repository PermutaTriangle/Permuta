from itertools import chain
from typing import Optional


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
    """Creates a matrix of the dimesions (size x size). If binary is set to True
    addition is modulo 2 addition."""

    def __init__(
        self, size: int, function: Optional[dict] = None, binary: bool = True
    ) -> None:
        self.labels = (list(range(size)), list(range(size)))
        if function:
            self.function = {
                key: (1 if binary and val else val) for key, val in function.items()
            }
        else:
            self.function = dict()
        self.binary = binary
        self.size = size

    def __getitem__(self, pos):
        """Get value in row, col specified"""
        return self.function[pos] if pos in self.function else 0

    def __setitem__(self, pos, value):
        """Sets position in the matrix to val"""
        assert pos[0] in self.labels[0]
        assert pos[1] in self.labels[1]
        self.function[pos] = value

    def __add__(self, other: "Matrix"):
        """Adds two matrices together. Both classes have to be binary or not binary"""
        assert self.binary == other.binary
        assert self.labels == other.labels
        new_mat = Matrix(size=self.size)
        funcs = [self.function.items(), other.function.items()]
        if self.binary:
            for idx, val in chain(*funcs):
                new_mat[idx] ^= val
        else:
            for idx, val in chain(*funcs):
                new_mat[idx] += val
        return new_mat

    def __mul__(self, other: "Matrix"):
        assert self.labels[1] == other.labels[0]
        mat = Matrix(size=len(self), function={})
        for row in self.labels[0]:
            for col in other.labels[1]:
                for k in self.labels[1]:
                    mat[(row, col)] += self[(row, k)] * other[(k, col)]
        return mat

    def __len__(self):
        return self.size

    def __str__(self) -> str:
        string = ""
        for row in self.labels[0]:
            for col in self.labels[1]:
                string += f"|{self[row, col]}"
            string += "|\n"
        return string

    def __repr__(self) -> str:
        return f"Matrix({self.labels}, {self.function})"

    def __eq__(self, other: object) -> bool:
        """Returns True if both matrices are equal."""
        if not isinstance(other, Matrix):
            raise Exception("Only able to compare a Matrix with another Matrix")
        if self.labels != other.labels:
            return False
        for row in self.labels[0]:
            for col in self.labels[1]:
                if self[row, col] != other[row, col]:
                    return False
        return True

    def test_sum(self):
        """Sums up all the values in the matrix."""
        return sum(self.function.values())


class LoTriMatrix(Matrix):
    """Returns a (n x n) lower triangular matrix"""

    def __init__(self, size: int):
        super().__init__(size)
        for row in range(size):
            for col in range(size):
                if col <= row:
                    self[row, col] = 1
