from permuta import Av, Perm
from permuta.permutils.statistics import PermutationStatistic


def test_distribution_all_perms():
    assert sum(PermutationStatistic.inv().distribution_up_to(7), []) == [
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        1,
        1,
        3,
        5,
        6,
        5,
        3,
        1,
        1,
        4,
        9,
        15,
        20,
        22,
        20,
        15,
        9,
        4,
        1,
        1,
        5,
        14,
        29,
        49,
        71,
        90,
        101,
        101,
        90,
        71,
        49,
        29,
        14,
        5,
        1,
        1,
        6,
        20,
        49,
        98,
        169,
        259,
        359,
        455,
        531,
        573,
        573,
        531,
        455,
        359,
        259,
        169,
        98,
        49,
        20,
        6,
        1,
    ]
    assert PermutationStatistic.maj().distribution_for_length(8) == [
        1,
        7,
        27,
        76,
        174,
        343,
        602,
        961,
        1415,
        1940,
        2493,
        3017,
        3450,
        3736,
        3836,
        3736,
        3450,
        3017,
        2493,
        1940,
        1415,
        961,
        602,
        343,
        174,
        76,
        27,
        7,
        1,
    ]


def test_longest_increasing_and_decreasing_subsequences():
    """The two statistics are the longest monotone subsequences, not runs."""
    statistics = dict(PermutationStatistic._STATISTICS)
    increasing = statistics["Longest increasing subsequence"]
    decreasing = statistics["Longest decreasing subsequence"]
    assert increasing(Perm((0, 2, 1, 3))) == 3
    assert decreasing(Perm((3, 1, 2, 0))) == 3
    assert increasing(Perm(())) == decreasing(Perm(())) == 0
    for length in range(7):
        for perm in Perm.of_length(length):
            # The longest increasing subsequence ending at each point, found the
            # slow way, from those ending at the smaller points before it
            ending_at = []
            for index, value in enumerate(perm):
                ending_before = [ending_at[i] for i in range(index) if perm[i] < value]
                ending_at.append(1 + max(ending_before, default=0))
            longest = max(ending_at, default=0)
            assert increasing(perm) == longest
            assert decreasing(perm.reverse()) == longest
    # The permutations of length 6 by their longest increasing subsequence's
    # length, from 0: OEIS A047874
    by_length = [0, 1, 131, 381, 181, 25, 1]
    for name in ("Longest increasing subsequence", "Longest decreasing subsequence"):
        statistic = PermutationStatistic(name, statistics[name])
        assert statistic.distribution_for_length(6) == by_length


def test_distribution_av():
    assert sum(
        PermutationStatistic.des().distribution_up_to(11, Av.from_string("123")), []
    ) == [
        1,
        1,
        1,
        1,
        0,
        4,
        1,
        0,
        2,
        11,
        1,
        0,
        0,
        15,
        26,
        1,
        0,
        0,
        5,
        69,
        57,
        1,
        0,
        0,
        0,
        56,
        252,
        120,
        1,
        0,
        0,
        0,
        14,
        364,
        804,
        247,
        1,
        0,
        0,
        0,
        0,
        210,
        1800,
        2349,
        502,
        1,
        0,
        0,
        0,
        0,
        42,
        1770,
        7515,
        6455,
        1013,
        1,
        0,
        0,
        0,
        0,
        0,
        792,
        11055,
        27940,
        16962,
        2036,
        1,
    ]
