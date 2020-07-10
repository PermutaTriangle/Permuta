from typing import Iterable

from permuta.patterns.perm import Iterator, Perm, Set, Tuple


def rotate_90_clockwise_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    """Rotate all perms by 90 degrees."""
    return (perm.rotate() for perm in perms)


def rotate_180_clockwise_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    """Rotate all perms by 180 degrees."""
    return (perm.rotate(2) for perm in perms)


def rotate_270_clockwise_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    """Rotate all perms by 270 degrees."""
    return (perm.rotate(3) for perm in perms)


def inverse_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    """Return the inverse of each permutation a collection of perms."""
    return (perm.inverse() for perm in perms)


def reverse_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    """Return the reverse of each permutation a collection of perms."""
    return (perm.reverse() for perm in perms)


def complement_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    """Return the complement of each permutation in a collection of perms."""
    return (perm.complement() for perm in perms)


def antidiagonal_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    """Return the antidiagonal of each permutation in a collection of perms."""
    return (perm.flip_antidiagonal() for perm in perms)


def all_symmetry_sets(perms: Iterable[Perm]) -> Set[Tuple[Perm, ...]]:
    """Given a collection of perms, return all possible collections formed by applying
    symmetric operations on all perms. Each group has their permutation sorted.
    """
    perms = perms if isinstance(perms, list) else list(perms)
    answer = {tuple(sorted(perms)), tuple(sorted(inverse_set(perms)))}
    for _ in range(3):
        perms = list(rotate_90_clockwise_set(perms))
        answer.add(tuple(sorted(perms)))
        answer.add(tuple(sorted(inverse_set(perms))))
    return answer


def lex_min(perms: Iterable[Perm]) -> Tuple[Perm, ...]:
    """Find the lexicographical minimum of the sets of all symmetries."""
    return min(all_symmetry_sets(perms))
