from fractions import Fraction
from itertools import chain
from typing import Callable, Dict, Iterable, List, Optional, Tuple


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


class PinWordUtil:
    """Utility class for pinwords"""

    def __init__(self) -> None:
        self.caller: Dict[str, Callable[[List[int]], Tuple[int, int]]] = {
            "1": self.char_1,
            "2": self.char_2,
            "3": self.char_3,
            "4": self.char_4,
            "U": self.char_u,
            "L": self.char_l,
            "D": self.char_d,
            "R": self.char_r,
        }
        self.zero = Fraction(0, 1)
        self.one = Fraction(1, 1)
        self.half = Fraction(1, 2)

    @staticmethod
    def rzero():
        """Returns the fraction zero"""
        return Fraction(0, 1)

    def call(self, char, pre_perm):
        """Main help function"""
        return self.caller[char](pre_perm)

    def char_1(self, pre_perm: List[int]):
        """."""
        next_x = PinWordUtil.max_x(pre_perm) + self.one
        next_y = PinWordUtil.max_y(pre_perm) + self.one
        return next_x, next_y

    def char_2(self, pre_perm: List[int]):
        """."""
        next_x = PinWordUtil.min_x(pre_perm) - self.one
        next_y = PinWordUtil.max_y(pre_perm) + self.one
        return next_x, next_y

    def char_3(self, pre_perm: List[int]):
        """."""
        next_x = PinWordUtil.min_x(pre_perm) - self.one
        next_y = PinWordUtil.min_y(pre_perm) - self.one
        return next_x, next_y

    def char_4(self, pre_perm: List[int]):
        """."""
        next_x = PinWordUtil.max_x(pre_perm) + self.one
        next_y = PinWordUtil.min_y(pre_perm) - self.one
        return next_x, next_y

    def char_u(self, pre_perm: List[int]):
        """."""
        (last_x,) = pre_perm[-1]
        if last_x > PinWordUtil.max_x(pre_perm[:-1]):
            next_x = self.half * (last_x + PinWordUtil.max_x(pre_perm[:-1]))
            next_y = PinWordUtil.max_y(pre_perm) + self.one
        elif last_x < PinWordUtil.min_x(pre_perm[:-1]):
            next_x = self.half * (last_x + PinWordUtil.min_x(pre_perm[:-1]))
            next_y = PinWordUtil.max_y(pre_perm) + self.one
        else:
            assert False
        return next_x, next_y

    def char_l(self, pre_perm: List[int]):
        """."""
        _, last_y = pre_perm[-1]
        if last_y > PinWordUtil.max_y(pre_perm[:-1]):
            next_x = PinWordUtil.min_x(pre_perm) - self.one
            next_y = self.half * (last_y + PinWordUtil.max_y(pre_perm[:-1]))
        elif last_y < PinWordUtil.min_y(pre_perm[:-1]):
            next_x = PinWordUtil.min_x(pre_perm) - self.one
            next_y = self.half * (last_y + PinWordUtil.min_y(pre_perm[:-1]))
        else:
            assert False
        return next_x, next_y

    def char_d(self, pre_perm: List[int]):
        """."""
        (last_x,) = pre_perm[-1]
        if last_x > PinWordUtil.max_x(pre_perm[:-1]):
            next_x = self.half * (last_x + PinWordUtil.max_x(pre_perm[:-1]))
            next_y = PinWordUtil.min_y(pre_perm) - self.one
        elif last_x < PinWordUtil.min_x(pre_perm[:-1]):
            next_x = self.half * (last_x + PinWordUtil.min_x(pre_perm[:-1]))
            next_y = PinWordUtil.min_y(pre_perm) - self.one
        else:
            assert False
        return next_x, next_y

    def char_r(self, pre_perm: List[int]):
        """."""
        _, last_y = pre_perm[-1]
        if last_y > PinWordUtil.max_y(pre_perm[:-1]):
            next_x = PinWordUtil.max_x(pre_perm) + self.one
            next_y = self.half * (last_y + PinWordUtil.max_y(pre_perm[:-1]))
        elif last_y < PinWordUtil.min_y(pre_perm[:-1]):
            next_x = PinWordUtil.max_x(pre_perm) + self.one
            next_y = self.half * (last_y + PinWordUtil.min_y(pre_perm[:-1]))
        else:
            assert False
        return next_x, next_y

    @staticmethod
    def min_x(pre_perm):
        """Utility function"""
        return min(pre_perm, key=lambda x: x[0])[0]

    @staticmethod
    def max_x(pre_perm):
        """Utility function"""
        return max(pre_perm, key=lambda x: x[0])[0]

    @staticmethod
    def min_y(pre_perm):
        """Utility function"""
        return min(pre_perm, key=lambda x: x[1])[1]

    @staticmethod
    def max_y(pre_perm):
        """Utility function"""
        return max(pre_perm, key=lambda x: x[1])[1]


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
