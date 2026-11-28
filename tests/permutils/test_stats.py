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


def test_check_all_transformed_compares_every_pair_of_statistics():
    """Each statistic is compared with every statistic, itself among them."""
    identity = {perm: perm for perm in Perm.of_length(3)}
    transformed = PermutationStatistic.check_all_transformed(identity)
    for name, _ in PermutationStatistic._STATISTICS:
        assert name in transformed[name]
    reverse = {perm: perm.reverse() for perm in Perm.up_to_length(5)}
    transformed = PermutationStatistic.check_all_transformed(reverse)
    assert transformed["Number of inversions"] == ["Number of non-inversions"]
    assert transformed["Number of descents"] == ["Number of ascents"]
    assert transformed["Number of ascents"] == ["Number of descents"]
    assert transformed["Number of left-to-right maximas"] == [
        "Number of right-to-left maximas"
    ]


def test_jointly_transformed_pairs_take_either_order_and_a_statistic_itself():
    """A statistic is matched with any other, before or after it, or with itself."""
    av_231, av_312 = Av.from_string("231"), Av.from_string("312")
    pairs = set(
        PermutationStatistic.jointly_transformed_equally_distributed(
            av_231, av_312, n=5, dim=1
        )
    )
    assert (("Number of descents",), ("Number of ascents",)) in pairs
    assert (("Number of ascents",), ("Number of descents",)) in pairs
    assert (("Number of inversions",), ("Number of inversions",)) in pairs
    same_class = set(
        PermutationStatistic.jointly_transformed_equally_distributed(
            av_231, av_231, n=5, dim=1
        )
    )
    for name, _ in PermutationStatistic._STATISTICS:
        assert ((name,), (name,)) in same_class


def test_jointly_transformed_pairs_match_combinations_in_order(monkeypatch):
    """Each combination on the first class is in table order, matched in order."""
    monkeypatch.setattr(
        PermutationStatistic,
        "_STATISTICS",
        (
            ("Number of left-to-right maximas", Perm.count_ltrmax),
            ("Number of right-to-left minimas", Perm.count_rtlmin),
            ("Number of right-to-left maximas", Perm.count_rtlmax),
        ),
    )
    # The inverse takes Av(231) to Av(312), left-to-right maxima to right-to-left
    # minima and back, and right-to-left maxima to themselves
    av_231, av_312 = Av.from_string("231"), Av.from_string("312")
    pairs = set(
        PermutationStatistic.jointly_transformed_equally_distributed(
            av_231, av_312, n=5, dim=2
        )
    )
    assert (
        ("Number of right-to-left minimas", "Number of right-to-left maximas"),
        ("Number of left-to-right maximas", "Number of right-to-left maximas"),
    ) in pairs
    assert (
        ("Number of left-to-right maximas", "Number of right-to-left maximas"),
        ("Number of right-to-left minimas", "Number of right-to-left maximas"),
    ) in pairs
    assert (
        ("Number of left-to-right maximas", "Number of right-to-left minimas"),
        ("Number of right-to-left minimas", "Number of left-to-right maximas"),
    ) in pairs
    names = [name for name, _ in PermutationStatistic._STATISTICS]
    for first, _ in pairs:
        assert names.index(first[0]) < names.index(first[1])
    same_class = set(
        PermutationStatistic.jointly_transformed_equally_distributed(
            av_231, av_231, n=5, dim=2
        )
    )
    assert (
        ("Number of left-to-right maximas", "Number of right-to-left minimas"),
        ("Number of left-to-right maximas", "Number of right-to-left minimas"),
    ) in same_class


def test_jointly_transformed_checks_each_length_up_to_n():
    """Every length up to n is compared, and no more: 41 matches to 4, 40 to 5."""
    av_231, av_312 = Av.from_string("231"), Av.from_string("312")
    for n, count in ((4, 41), (5, 40)):
        matches = list(
            PermutationStatistic.jointly_transformed_equally_distributed(
                av_231, av_312, n=n, dim=1
            )
        )
        assert len(matches) == len(set(matches)) == count


def test_jointly_transformed_pairs_two_statistics_by_default():
    """dim is 2 by default; the first match of a class with itself comes at once."""
    av_231 = Av.from_string("231")
    stats1, stats2 = next(
        PermutationStatistic.jointly_transformed_equally_distributed(av_231, av_231)
    )
    assert len(stats1) == len(stats2) == 2
    assert stats1 == stats2


def test_check_all_transformed_reads_the_keys_with_the_first_statistic():
    """stat1 is taken on the keys and stat2 on the values; with no pairs at all,
    every statistic goes to every one, in the table's order."""
    bijection = {Perm((0, 1, 2)): Perm((0, 2, 1)), Perm((1, 0, 2)): Perm((0, 1, 2))}
    expected = {}
    for name1, func1 in PermutationStatistic._STATISTICS:
        for name2, func2 in PermutationStatistic._STATISTICS:
            if all(func1(key) == func2(value) for key, value in bijection.items()):
                expected.setdefault(name1, []).append(name2)
    assert expected
    assert PermutationStatistic.check_all_transformed(bijection) == expected
    names = [name for name, _ in PermutationStatistic._STATISTICS]
    assert PermutationStatistic.check_all_transformed({}) == {
        name: names for name in names
    }
