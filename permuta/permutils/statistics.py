from collections import defaultdict
from itertools import combinations, permutations, product
from typing import Callable, Counter, Dict, Iterator, List, Optional, Tuple

from permuta import Av, Perm

PermutationStatisticType = Callable[[Perm], int]
BijectionType = Dict[Perm, Perm]


def _count_descents(perm: Perm) -> int:
    return perm.count_descents()


def _count_ascents(perm: Perm) -> int:
    return perm.count_ascents()


class PermutationStatistic:
    """
    A class for checking preservation of statistics
    in bijections and their distribution.
    """

    # More statistics can be added here.
    _STATISTICS = (
        ("Number of inversions", Perm.count_inversions),
        ("Number of non-inversions", Perm.count_non_inversions),
        ("Major index", Perm.major_index),
        ("Number of descents", _count_descents),
        ("Number of ascents", _count_ascents),
        ("Number of peaks", Perm.count_peaks),
        ("Number of valleys", Perm.count_valleys),
        ("Number of cycles", Perm.count_cycles),
        ("Number of left-to-right minimas", Perm.count_ltrmin),
        ("Number of left-to-right maximas", Perm.count_ltrmax),
        ("Number of right-to-left minimas", Perm.count_rtlmin),
        ("Number of right-to-left maximas", Perm.count_rtlmax),
        ("Number of fixed points", Perm.count_fixed_points),
        ("Order", Perm.order),
        ("Longest increasing subsequence", Perm.length_of_longestrun_ascending),
        ("Longest decreasing subsequence", Perm.length_of_longestrun_descending),
        ("Depth", Perm.depth),
        ("Number of bounces", Perm.count_bounces),
        ("Maximum drop size", Perm.max_drop_size),
        ("Number of primes in the column sums", Perm.count_column_sum_primes),
        ("Holeyness of a permutation", Perm.holeyness),
        ("Number of stack-sorts needed", Perm.count_stack_sorts),
        ("Number of pop-stack-sorts needed", Perm.count_pop_stack_sorts),
        ("Number of pinnacles", Perm.count_pinnacles),
        ("Number of cyclic peaks", Perm.count_cyclic_peaks),
        ("Number of cyclic valleys", Perm.count_cyclic_valleys),
        ("Number of double excedance", Perm.count_double_excedance),
        ("Number of double drops", Perm.count_double_drops),
        ("Number of foremaxima", Perm.count_foremaxima),
        ("Number of afterminima", Perm.count_afterminima),
        ("Number of aftermaxima", Perm.count_aftermaxima),
        ("Number of foreminima", Perm.count_foreminima),
    )

    @staticmethod
    def show_predefined_statistics(idx: int = -1) -> None:
        """Show all or a specific predefined statistic."""
        if idx < 0:
            print(PermutationStatistic._predefined_statistics())
        else:
            print(PermutationStatistic._STATISTICS[idx][0])

    @staticmethod
    def _predefined_statistics() -> str:
        """Name and index of each statistics defined."""
        return "\n".join(
            f"[{i}] {name}"
            for i, (name, _) in enumerate(PermutationStatistic._STATISTICS)
        )

    @classmethod
    def get_by_index(cls, idx: int) -> "PermutationStatistic":
        """Get a statistic by index."""
        return cls(*PermutationStatistic._STATISTICS[idx])

    def __init__(self, name: str, func: PermutationStatisticType) -> None:
        self.name: str = name
        self.func: PermutationStatisticType = func

    def preserved_in(self, bijection: BijectionType) -> bool:
        """Check if statistic (self) is preserved in a bijection."""
        return all(self.func(k) == self.func(v) for k, v in bijection.items())

    def distribution_for_length(
        self, n: int, perm_class: Optional[Av] = None
    ) -> List[int]:
        """Return a distribution of statistic for a fixed length of permutations. If a
        class is not provided, we use the set of all permutations.
        """
        iterator = perm_class.of_length(n) if perm_class else Perm.of_length(n)
        cnt = Counter(self.func(p) for p in iterator)
        lis = [0] * (max(cnt.keys(), default=0) + 1)
        for key, val in cnt.items():
            lis[key] = val
        return lis

    def distribution_up_to(
        self, n: int, perm_class: Optional[Av] = None
    ) -> List[List[int]]:
        """Return a table (i,k) for the distribution of a statistic. Here i=0..n is the
        length of the permutation and k is the statistic. If a class is not provided,
        we use the set of all permutations.
        """
        return [self.distribution_for_length(i, perm_class) for i in range(n + 1)]

    @classmethod
    def equally_distributed(cls, class1: Av, class2: Av, n: int = 6) -> Iterator[str]:
        """Return all stats that are equally distributed for two classes up to a max
        length.
        """
        return (
            stat.name
            for stat in cls._get_all()
            if all(
                stat.distribution_for_length(i, class1)
                == stat.distribution_for_length(i, class2)
                for i in range(n + 1)
            )
        )

    @staticmethod
    def jointly_equally_distributed(
        class1: Av, class2: Av, n: int = 6, dim: int = 2
    ) -> Iterator[Tuple[str, ...]]:
        """Check if a combination of statistics is equally distributed between
        two classes up to a max length.
        """
        return (
            tuple(stat[0] for stat in stats)
            for stats in combinations(PermutationStatistic._STATISTICS, dim)
            if all(
                Counter(
                    tuple(stat[1](p) for stat in stats) for p in class1.of_length(i)
                )
                == Counter(
                    tuple(stat[1](p) for stat in stats) for p in class2.of_length(i)
                )
                for i in range(n + 1)
            )
        )

    @staticmethod
    def jointly_transformed_equally_distributed(
        class1: Av, class2: Av, n: int = 6, dim: int = 2
    ) -> Iterator[Tuple[Tuple[str, ...], Tuple[str, ...]]]:
        """Check if a combination of statistics in one class is equally distributed
        to any combination of statistics in the other class, up to a max length.
        """
        return (
            (tuple(stat[0] for stat in stats1), tuple(stat[0] for stat in stats2))
            for stats1, stats2 in combinations(
                permutations(PermutationStatistic._STATISTICS, dim), 2
            )
            if all(
                Counter(
                    tuple(stat[1](p) for stat in stats1) for p in class1.of_length(i)
                )
                == Counter(
                    tuple(stat[1](p) for stat in stats2) for p in class2.of_length(i)
                )
                for i in range(n + 1)
            )
        )

    def __str__(self) -> str:
        return self.name

    @classmethod
    def _get_all(cls) -> Iterator["PermutationStatistic"]:
        """Get all predefined statistics as an instance of PermutationStatistic."""
        yield from (cls(name, func) for name, func in PermutationStatistic._STATISTICS)

    @classmethod
    def check_all_preservations(cls, bijection: BijectionType) -> Iterator[str]:
        """Given a bijection, check which statistics are preserved."""
        return (stats.name for stats in cls._get_all() if stats.preserved_in(bijection))

    @classmethod
    def check_all_transformed(cls, bijection: BijectionType) -> Dict[str, List[str]]:
        """Given a bijection, check what statistics transform into others."""
        transf = defaultdict(list)
        all_stats = cls._get_all()
        for stat1, stat2 in product(all_stats, all_stats):
            if all(stat1.func(k) == stat2.func(v) for k, v in bijection.items()):
                transf[stat1.name].append(stat2.name)
        return dict(transf)

    @staticmethod
    def symmetry_duplication(
        bijection: BijectionType,
    ) -> Iterator[BijectionType]:
        """Yield all symmetric versions of a bijection."""
        return (
            bij
            for rotated in (
                {k.rotate(angle): v.rotate(angle) for k, v in bijection.items()}
                for angle in range(4)
            )
            for bij in (rotated, {k.inverse(): v.inverse() for k, v in rotated.items()})
        )

    # Some common ones for easy access

    @classmethod
    def inv(cls) -> "PermutationStatistic":
        """Number of inversions."""
        return cls("Number of inversions", Perm.count_inversions)

    @classmethod
    def maj(cls) -> "PermutationStatistic":
        """Major index."""
        return cls("Major index", Perm.major_index)

    @classmethod
    def des(cls) -> "PermutationStatistic":
        """Number of descents."""
        return cls("Number of descents", Perm.count_descents)

    @classmethod
    def asc(cls) -> "PermutationStatistic":
        """Number of ascents."""
        return cls("Number of ascents", Perm.count_ascents)
