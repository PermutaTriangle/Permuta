from typing import Iterable

from permuta.patterns.perm import Iterator, Perm, Set, Tuple


def rotate_90_clockwise_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    return (perm.rotate() for perm in perms)


def rotate_180_clockwise_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    return (perm.rotate(2) for perm in perms)


def rotate_270_clockwise_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    return (perm.rotate(3) for perm in perms)


rotate_set = rotate_90_clockwise_set


def inverse_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    return (perm.inverse() for perm in perms)


def reverse_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    return (perm.reverse() for perm in perms)


def complement_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    return (perm.complement() for perm in perms)


def antidiagonal_set(perms: Iterable[Perm]) -> Iterator[Perm]:
    return (perm.flip_antidiagonal() for perm in perms)


def all_symmetry_sets(perms: Iterable[Perm]) -> Set[Tuple[Perm, ...]]:
    perms = perms if isinstance(perms, list) else list(perms)
    answer = {tuple(sorted(perms)), tuple(sorted(inverse_set(perms)))}
    for _ in range(3):
        perms = list(rotate_set(perms))
        answer.add(tuple(sorted(perms)))
        answer.add(tuple(sorted(inverse_set(perms))))
    return answer


def lex_min(perms: Iterable[Perm]) -> Tuple[Perm, ...]:
    return min(all_symmetry_sets(perms))
