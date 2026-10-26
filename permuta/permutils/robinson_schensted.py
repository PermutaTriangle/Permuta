"""
The Robinson-Schensted correspondence (RSK) on words of distinct letters,
Schützenberger's evacuation of standard Young tableaux, and tests of whether the
permutations avoiding some patterns are closed under Knuth equivalence, or are
determined by their RSK shape.
"""

from bisect import bisect_left
from functools import lru_cache
from typing import FrozenSet, Iterable, Iterator, List, Sequence, Tuple

from permuta.patterns.perm import Perm

Tableau = List[List[int]]


def rsk(word: Sequence[int]) -> Tuple[Tableau, Tableau]:
    """Return the insertion and recording tableaux of a word of distinct letters,
    by row insertion. The recording tableau records the steps 1, 2, ..., and both
    have the same shape.

    Examples:
        >>> rsk((1, 3, 0, 2))
        ([[0, 2], [1, 3]], [[1, 2], [3, 4]])
        >>> rsk((7, 2, 9, 4))
        ([[2, 4], [7, 9]], [[1, 3], [2, 4]])
    """
    insertion_tableau: Tableau = []
    recording_tableau: Tableau = []
    for step, letter in enumerate(word, 1):
        for insertion_row, recording_row in zip(insertion_tableau, recording_tableau):
            position = bisect_left(insertion_row, letter)
            if position == len(insertion_row):
                insertion_row.append(letter)
                recording_row.append(step)
                break
            letter, insertion_row[position] = insertion_row[position], letter
        else:
            insertion_tableau.append([letter])
            recording_tableau.append([step])
    return insertion_tableau, recording_tableau


def rsk_inverse(
    insertion_tableau: Sequence[Sequence[int]],
    recording_tableau: Sequence[Sequence[int]],
) -> List[int]:
    """Return the word whose insertion and recording tableaux are the given ones:
    tableaux of the same shape, the recording tableau standard, of the steps 1, 2,
    ....

    Examples:
        >>> rsk_inverse([[0, 2], [1, 3]], [[1, 2], [3, 4]])
        [1, 3, 0, 2]
    """
    insertion_rows = [list(row) for row in insertion_tableau]
    recording_rows = [list(row) for row in recording_tableau]
    row_of = {
        step: row_index for row_index, row in enumerate(recording_rows) for step in row
    }
    word = [0] * len(row_of)
    for step in range(len(word), 0, -1):
        row_index = row_of[step]
        recording_rows[row_index].pop()
        letter = insertion_rows[row_index].pop()
        for upper in range(row_index - 1, -1, -1):
            insertion_row = insertion_rows[upper]
            position = bisect_left(insertion_row, letter) - 1
            letter, insertion_row[position] = insertion_row[position], letter
        word[step - 1] = letter
    return word


def evacuation(tableau: Sequence[Sequence[int]]) -> Tableau:
    """Return Schützenberger's evacuation of a standard Young tableau of the entries
    1 to n: delete the smallest entry and slide the hole out by jeu de taquin, n
    times, writing n, n - 1, ... in the cells vacated. It is an involution that
    keeps the shape, and the recording tableau of a permutation's reverse-complement
    is the evacuation of the permutation's.

    Examples:
        >>> evacuation([[1, 2], [3]])
        [[1, 3], [2]]
    """
    current = [list(row) for row in tableau]
    result: Tableau = [[0] * len(row) for row in current]
    size = sum(len(row) for row in current)
    for label in range(size, 0, -1):
        row, column = 0, 0
        while True:
            right = current[row][column + 1] if column + 1 < len(current[row]) else None
            below = (
                current[row + 1][column]
                if row + 1 < len(current) and column < len(current[row + 1])
                else None
            )
            if right is None and below is None:
                break
            if below is None or (right is not None and right < below):
                assert right is not None
                current[row][column] = right
                column += 1
            else:
                current[row][column] = below
                row += 1
        current[row].pop()
        if not current[row]:
            current.pop()
        result[row][column] = label
    return result


def evacuate_recording_tableau(word: Sequence[int]) -> List[int]:
    """Return the word with the word's insertion tableau and the evacuation of its
    recording tableau, RSK^-1(P(w), evac(Q(w))) for the word w of m distinct
    letters. It is Knuth equivalent to w, as its insertion tableau is w's, and its
    factor at positions m + 1 - j to m + 1 - i has the RSK shape of w's factor at
    positions i to j. The map is an involution.

    Examples:
        >>> evacuate_recording_tableau((1, 3, 0, 2))
        [1, 3, 0, 2]
        >>> evacuate_recording_tableau((0, 2, 1))
        [2, 0, 1]
    """
    insertion_tableau, recording_tableau = rsk(word)
    return rsk_inverse(insertion_tableau, evacuation(recording_tableau))


def _knuth_neighbors(perm: Perm) -> Iterator[Perm]:
    """Yield the permutations one elementary Knuth move from the permutation:
    y z x <-> y x z and x z y <-> z x y, for x < y < z."""
    word = list(perm)
    for index in range(len(word) - 2):
        first, second, third = word[index], word[index + 1], word[index + 2]
        if min(second, third) < first < max(second, third):
            yield Perm(word[: index + 1] + [third, second] + word[index + 3 :])
        if min(first, second) < third < max(first, second):
            yield Perm(word[:index] + [second, first] + word[index + 2 :])


def is_knuth_closed(basis: Iterable[Perm]) -> bool:
    """Return True if the permutations avoiding all the patterns are closed under
    Knuth equivalence. It is decided locally: an occurrence that a Knuth move
    destroys uses both letters it exchanges, and with the letter that allows the
    move it lies in a permutation at most one entry longer than the pattern.

    Examples:
        >>> is_knuth_closed([Perm((0, 2, 1))])
        False
        >>> is_knuth_closed([Perm((0, 2, 1)), Perm((2, 0, 1))])
        True
    """
    return _is_knuth_closed(frozenset(basis))


@lru_cache(maxsize=1 << 16)
def _is_knuth_closed(patterns: FrozenSet[Perm]) -> bool:
    return not any(
        neighbor.avoids(*patterns)
        for pattern in patterns
        for container in (pattern, *pattern.coveredby())
        for neighbor in _knuth_neighbors(container)
    )


def is_shape_closed(basis: Iterable[Perm]) -> bool:
    """Return True if whether a permutation avoids the patterns depends only on its
    RSK shape: the patterns and their inverses are both Knuth closed. Monotone
    patterns are.

    Examples:
        >>> is_shape_closed([Perm((2, 1, 0))])
        True
        >>> is_shape_closed([Perm((0, 2, 1)), Perm((2, 0, 1))])
        False
    """
    patterns = frozenset(basis)
    return _is_knuth_closed(patterns) and _is_knuth_closed(
        frozenset(pattern.inverse() for pattern in patterns)
    )
