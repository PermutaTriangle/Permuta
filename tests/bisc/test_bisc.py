from permuta.bisc.bisc import bisc, read_bisc_file
from permuta.bisc.bisc_subfunctions import patterns_suffice_for_bad, run_clean_up
from permuta.patterns.perm import Perm

# Path to permutation files
ppf = "permuta/resources/bisc/"


def test_stack_sortable():
    """
    Testing stack-sortable permutations
    Expected answer is
        120
    Suffices to look at permutations up to length 3
    """

    A = read_bisc_file(ppf + "stack_sortable_good_len8")
    B = read_bisc_file(ppf + "stack_sortable_bad_len8")

    # Too short
    assert bisc(A, 2, 3) == {}
    assert bisc(A, 2, 4) == {}

    # Should get expected answer
    assert bisc(A, 3, 3) == {3: {Perm((1, 2, 0)): [set()]}}
    assert bisc(A, 3, 4) == {3: {Perm((1, 2, 0)): [set()]}}

    SG = bisc(A, 3, 7)
    assert SG == {3: {Perm((1, 2, 0)): [set()]}}
    assert patterns_suffice_for_bad(SG, 6, B) == (True, [])
    assert run_clean_up(SG, B, limit_monitors=5) == (
        [[(3, 0, 0)]],
        {(3, 0, 0): (Perm((1, 2, 0)), set())},
    )

    # Looking for longer patterns
    assert bisc(A, 4, 7) == {3: {Perm((1, 2, 0)): [set()]}, 4: {}}


def test_West2():
    """
    Testing West-2-stack-sortable permutations
    Expected answer is
        1230
        2130 (1,4)
    Suffices to look at permutations up to length 5
    """

    A = read_bisc_file(ppf + "West_2_stack_sortable_good_len8")
    B = read_bisc_file(ppf + "West_2_stack_sortable_bad_len8")

    # Too short
    assert bisc(A, 3, 4) == {}
    assert bisc(A, 4, 4) == {
        4: {Perm((1, 2, 3, 0)): [set()], Perm((2, 1, 3, 0)): [set()]}
    }

    # Should get expected answer
    assert bisc(A, 4, 5) == {
        4: {Perm((1, 2, 3, 0)): [set()], Perm((2, 1, 3, 0)): [{(1, 4)}]}
    }
    assert bisc(A, 4, 6) == {
        4: {Perm((1, 2, 3, 0)): [set()], Perm((2, 1, 3, 0)): [{(1, 4)}]}
    }
    assert bisc(A, 4, 7) == {
        4: {Perm((1, 2, 3, 0)): [set()], Perm((2, 1, 3, 0)): [{(1, 4)}]}
    }

    # Looking for longer patterns
    assert bisc(A, 5, 7) == {
        4: {Perm((1, 2, 3, 0)): [set()], Perm((2, 1, 3, 0)): [{(1, 4)}]},
        5: {Perm((4, 2, 1, 3, 0)): [{(2, 4), (1, 5)}]},
    }

    SG = bisc(A, 5, 7)
    assert SG == {
        4: {Perm((1, 2, 3, 0)): [set()], Perm((2, 1, 3, 0)): [{(1, 4)}]},
        5: {Perm((4, 2, 1, 3, 0)): [{(2, 4), (1, 5)}]},
    }
    assert patterns_suffice_for_bad(SG, 6, B) == (True, [])
    assert run_clean_up(SG, B, limit_monitors=5) == (
        [[(4, 0, 0), (4, 1, 0)]],
        {
            (4, 0, 0): (Perm((1, 2, 3, 0)), set()),
            (4, 1, 0): (Perm((2, 1, 3, 0)), {(1, 4)}),
            (5, 0, 0): (Perm((4, 2, 1, 3, 0)), {(2, 4), (1, 5)}),
        },
    )


def test_smooth():
    """
    Testing smooth permutations
    Expected answer is
        0213
        1032
    Suffices to look at permutations up to length 4
    """

    A = read_bisc_file(ppf + "smooth_good_len8")
    B = read_bisc_file(ppf + "smooth_bad_len8")

    # Too short
    assert bisc(A, 3, 4) == {}

    # # Should get expected answer
    assert bisc(A, 4, 4) == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [set()]}
    }
    assert bisc(A, 4, 5) == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [set()]}
    }
    assert bisc(A, 4, 6) == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [set()]}
    }
    assert bisc(A, 4, 7) == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [set()]}
    }

    # # Looking for longer patterns
    SG = bisc(A, 5, 7)
    assert SG == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [set()]},
        5: {},
    }
    assert patterns_suffice_for_bad(SG, 6, B) == (True, [])
    assert run_clean_up(SG, B, limit_monitors=5) == (
        [[(4, 0, 0), (4, 1, 0)]],
        {
            (4, 0, 0): (Perm((0, 2, 1, 3)), set()),
            (4, 1, 0): (Perm((1, 0, 3, 2)), set()),
        },
    )


def test_forestlike():
    """
    Testing forest-like permutations
    Expected answer is
        0213
        1032 (2,2)
    Suffices to look at permutations up to length 5
    """

    A = read_bisc_file(ppf + "forest_like_good_len8")
    B = read_bisc_file(ppf + "forest_like_bad_len8")

    # Too short
    assert bisc(A, 3, 4) == {}
    assert bisc(A, 4, 4) == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [set()]}
    }

    # # Should get expected answer
    assert bisc(A, 4, 5) == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [{(2, 2)}]}
    }
    assert bisc(A, 4, 6) == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [{(2, 2)}]}
    }
    assert bisc(A, 4, 7) == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [{(2, 2)}]}
    }

    # # Looking for longer patterns
    SG = bisc(A, 5, 7)
    assert SG == {
        4: {Perm((0, 2, 1, 3)): [set()], Perm((1, 0, 3, 2)): [{(2, 2)}]},
        5: {Perm((1, 3, 0, 4, 2)): [set()], Perm((2, 0, 4, 1, 3)): [set()]},
    }
    assert patterns_suffice_for_bad(SG, 6, B) == (True, [])
    assert run_clean_up(SG, B, limit_monitors=5) == (
        [[(4, 0, 0), (4, 1, 0)]],
        {
            (4, 0, 0): (Perm((0, 2, 1, 3)), set()),
            (4, 1, 0): (Perm((1, 0, 3, 2)), {(2, 2)}),
            (5, 0, 0): (Perm((1, 3, 0, 4, 2)), set()),
            (5, 1, 0): (Perm((2, 0, 4, 1, 3)), set()),
        },
    )


def test_Baxter():
    """
    Testing Baxter permutations
    Expected answer is
        1302 (2,2)
        2031 (2,2)
    Suffices to look at permutations up to length 5
    """

    A = read_bisc_file(ppf + "Baxter_good_len8")
    B = read_bisc_file(ppf + "Baxter_bad_len8")

    # Too short
    assert bisc(A, 3, 4) == {}
    assert bisc(A, 4, 4) == {
        4: {Perm((1, 3, 0, 2)): [set()], Perm((2, 0, 3, 1)): [set()]}
    }

    # Should get expected answer
    assert bisc(A, 4, 5) == {
        4: {Perm((1, 3, 0, 2)): [{(2, 2)}], Perm((2, 0, 3, 1)): [{(2, 2)}]}
    }
    assert bisc(A, 4, 6) == {
        4: {Perm((1, 3, 0, 2)): [{(2, 2)}], Perm((2, 0, 3, 1)): [{(2, 2)}]}
    }
    assert bisc(A, 4, 7) == {
        4: {Perm((1, 3, 0, 2)): [{(2, 2)}], Perm((2, 0, 3, 1)): [{(2, 2)}]}
    }

    # Looking for longer patterns
    SG = bisc(A, 5, 6)
    assert SG == {
        4: {Perm((1, 3, 0, 2)): [{(2, 2)}], Perm((2, 0, 3, 1)): [{(2, 2)}]},
        5: {
            Perm((1, 3, 0, 4, 2)): [set()],
            Perm((2, 0, 4, 1, 3)): [set()],
            Perm((2, 4, 0, 3, 1)): [set()],
            Perm((3, 1, 4, 0, 2)): [set()],
        },
    }
    assert patterns_suffice_for_bad(SG, 6, B) == (True, [])
    assert run_clean_up(SG, B, limit_monitors=5) == (
        [[(4, 0, 0), (4, 1, 0)]],
        {
            (4, 0, 0): (Perm((1, 3, 0, 2)), {(2, 2)}),
            (4, 1, 0): (Perm((2, 0, 3, 1)), {(2, 2)}),
            (5, 0, 0): (Perm((1, 3, 0, 4, 2)), set()),
            (5, 1, 0): (Perm((2, 0, 4, 1, 3)), set()),
            (5, 2, 0): (Perm((2, 4, 0, 3, 1)), set()),
            (5, 3, 0): (Perm((3, 1, 4, 0, 2)), set()),
        },
    )

    assert bisc(A, 5, 7) == {
        4: {Perm((1, 3, 0, 2)): [{(2, 2)}], Perm((2, 0, 3, 1)): [{(2, 2)}]},
        5: {},
    }


def test_SimSun():
    """
    Testing SimSun permutations
    Expected answer is
        210 (1,0), (1,1), (2,2)
    Suffices to look at permutations up to length 4
    """

    A = read_bisc_file(ppf + "SimSun_good_len8")

    # Too short
    assert bisc(A, 2, 4) == {}
    assert bisc(A, 3, 3) == {3: {Perm((2, 1, 0)): [set()]}}

    # Should get expected answer
    assert bisc(A, 3, 4) == {3: {Perm((2, 1, 0)): [{(1, 0), (1, 1), (2, 2)}]}}
    assert bisc(A, 3, 5) == {3: {Perm((2, 1, 0)): [{(1, 0), (1, 1), (2, 2)}]}}
    assert bisc(A, 3, 6) == {3: {Perm((2, 1, 0)): [{(1, 0), (1, 1), (2, 2)}]}}
    assert bisc(A, 4, 6) == {3: {Perm((2, 1, 0)): [{(1, 0), (1, 1), (2, 2)}]}, 4: {}}


def test_dihedral():
    """
    Testing permutations from the dihedral groups
    Expected answer is
        fully shaded 1, 12, and 21
        16 classical patterns of length 4
    Suffices to look at permutations up to length 4
    """

    A = read_bisc_file(ppf + "dihedral_good_len8")

    # Too short
    assert bisc(A, 2, 4) == {
        0: {Perm(()): [{(0, 0)}]},
        1: {Perm((0,)): [{(0, 0), (1, 1), (0, 1), (1, 0)}]},
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (1, 2), (2, 1), (0, 1), (1, 0), (2, 0), (0, 2)}
            ],
            Perm((1, 0)): [
                {(0, 0), (2, 2), (0, 1), (1, 2), (1, 0), (2, 1), (0, 2), (1, 1), (2, 0)}
            ],
        },
    }
    assert bisc(A, 3, 3) == {
        0: {Perm(()): [{(0, 0)}]},
        1: {Perm((0,)): [{(0, 0), (1, 1), (0, 1), (1, 0)}]},
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (1, 2), (2, 1), (0, 1), (1, 0), (2, 0), (0, 2)}
            ],
            Perm((1, 0)): [
                {(0, 0), (2, 2), (0, 1), (1, 2), (1, 0), (2, 1), (0, 2), (1, 1), (2, 0)}
            ],
        },
    }

    # Should get expected answer
    assert bisc(A, 4, 4) == {
        0: {Perm(()): [{(0, 0)}]},
        1: {Perm((0,)): [{(0, 0), (1, 1), (0, 1), (1, 0)}]},
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (1, 2), (2, 1), (0, 1), (1, 0), (2, 0), (0, 2)}
            ],
            Perm((1, 0)): [
                {(0, 0), (2, 2), (0, 1), (1, 2), (1, 0), (2, 1), (0, 2), (1, 1), (2, 0)}
            ],
        },
        4: {
            Perm((0, 1, 3, 2)): [set()],
            Perm((0, 2, 1, 3)): [set()],
            Perm((0, 2, 3, 1)): [set()],
            Perm((0, 3, 1, 2)): [set()],
            Perm((1, 0, 2, 3)): [set()],
            Perm((1, 2, 0, 3)): [set()],
            Perm((1, 3, 0, 2)): [set()],
            Perm((1, 3, 2, 0)): [set()],
            Perm((2, 0, 1, 3)): [set()],
            Perm((2, 0, 3, 1)): [set()],
            Perm((2, 1, 3, 0)): [set()],
            Perm((2, 3, 1, 0)): [set()],
            Perm((3, 0, 2, 1)): [set()],
            Perm((3, 1, 0, 2)): [set()],
            Perm((3, 1, 2, 0)): [set()],
            Perm((3, 2, 0, 1)): [set()],
        },
    }
    assert bisc(A, 4, 5) == {
        0: {Perm(()): [{(0, 0)}]},
        1: {Perm((0,)): [{(0, 0), (1, 1), (0, 1), (1, 0)}]},
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (1, 2), (2, 1), (0, 1), (1, 0), (2, 0), (0, 2)}
            ],
            Perm((1, 0)): [
                {(0, 0), (2, 2), (0, 1), (1, 2), (1, 0), (2, 1), (0, 2), (1, 1), (2, 0)}
            ],
        },
        4: {
            Perm((0, 1, 3, 2)): [set()],
            Perm((0, 2, 1, 3)): [set()],
            Perm((0, 2, 3, 1)): [set()],
            Perm((0, 3, 1, 2)): [set()],
            Perm((1, 0, 2, 3)): [set()],
            Perm((1, 2, 0, 3)): [set()],
            Perm((1, 3, 0, 2)): [set()],
            Perm((1, 3, 2, 0)): [set()],
            Perm((2, 0, 1, 3)): [set()],
            Perm((2, 0, 3, 1)): [set()],
            Perm((2, 1, 3, 0)): [set()],
            Perm((2, 3, 1, 0)): [set()],
            Perm((3, 0, 2, 1)): [set()],
            Perm((3, 1, 0, 2)): [set()],
            Perm((3, 1, 2, 0)): [set()],
            Perm((3, 2, 0, 1)): [set()],
        },
    }
    assert bisc(A, 4, 6) == {
        0: {Perm(()): [{(0, 0)}]},
        1: {Perm((0,)): [{(0, 0), (1, 1), (0, 1), (1, 0)}]},
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (1, 2), (2, 1), (0, 1), (1, 0), (2, 0), (0, 2)}
            ],
            Perm((1, 0)): [
                {(0, 0), (2, 2), (0, 1), (1, 2), (1, 0), (2, 1), (0, 2), (1, 1), (2, 0)}
            ],
        },
        4: {
            Perm((0, 1, 3, 2)): [set()],
            Perm((0, 2, 1, 3)): [set()],
            Perm((0, 2, 3, 1)): [set()],
            Perm((0, 3, 1, 2)): [set()],
            Perm((1, 0, 2, 3)): [set()],
            Perm((1, 2, 0, 3)): [set()],
            Perm((1, 3, 0, 2)): [set()],
            Perm((1, 3, 2, 0)): [set()],
            Perm((2, 0, 1, 3)): [set()],
            Perm((2, 0, 3, 1)): [set()],
            Perm((2, 1, 3, 0)): [set()],
            Perm((2, 3, 1, 0)): [set()],
            Perm((3, 0, 2, 1)): [set()],
            Perm((3, 1, 0, 2)): [set()],
            Perm((3, 1, 2, 0)): [set()],
            Perm((3, 2, 0, 1)): [set()],
        },
    }

    # Looking for longer patterns
    assert bisc(A, 5, 6) == {
        0: {Perm(()): [{(0, 0)}]},
        1: {Perm((0,)): [{(0, 0), (1, 1), (0, 1), (1, 0)}]},
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (1, 2), (2, 1), (0, 1), (1, 0), (2, 0), (0, 2)}
            ],
            Perm((1, 0)): [
                {(0, 0), (2, 2), (0, 1), (1, 2), (1, 0), (2, 1), (0, 2), (1, 1), (2, 0)}
            ],
        },
        4: {
            Perm((0, 1, 3, 2)): [set()],
            Perm((0, 2, 1, 3)): [set()],
            Perm((0, 2, 3, 1)): [set()],
            Perm((0, 3, 1, 2)): [set()],
            Perm((1, 0, 2, 3)): [set()],
            Perm((1, 2, 0, 3)): [set()],
            Perm((1, 3, 0, 2)): [set()],
            Perm((1, 3, 2, 0)): [set()],
            Perm((2, 0, 1, 3)): [set()],
            Perm((2, 0, 3, 1)): [set()],
            Perm((2, 1, 3, 0)): [set()],
            Perm((2, 3, 1, 0)): [set()],
            Perm((3, 0, 2, 1)): [set()],
            Perm((3, 1, 0, 2)): [set()],
            Perm((3, 1, 2, 0)): [set()],
            Perm((3, 2, 0, 1)): [set()],
        },
        5: {},
    }


def test_alternating():
    """
    Testing permutations from the alternating groups
    Expected answer is
        infinite list of fully shaded patterns
    Suffices to look at permutations up to length infinity!
    """

    A = read_bisc_file(ppf + "in_alternating_group_good_len8")

    # Too short
    assert bisc(A, 1, 4) == {}
    assert bisc(A, 2, 4) == {
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (2, 0), (0, 2), (1, 2), (2, 1), (0, 1), (1, 0)}
            ],
            Perm((1, 0)): [
                {(0, 1), (1, 2), (1, 0), (2, 1), (0, 0), (2, 2), (0, 2), (1, 1), (2, 0)}
            ],
        }
    }
    assert bisc(A, 3, 4) == {
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (2, 0), (0, 2), (1, 2), (2, 1), (0, 1), (1, 0)}
            ],
            Perm((1, 0)): [
                {(0, 1), (1, 2), (1, 0), (2, 1), (0, 0), (2, 2), (0, 2), (1, 1), (2, 0)}
            ],
        },
        3: {
            Perm((0, 2, 1)): [
                {(1, 2), (2, 3), (2, 1), (3, 2), (0, 1), (1, 0), (3, 0), (0, 3)}
            ],
            Perm((1, 0, 2)): [
                {(2, 3), (3, 2), (0, 1), (1, 2), (1, 0), (2, 1), (3, 0), (0, 3)}
            ],
            Perm((2, 1, 0)): [
                {(0, 1), (2, 3), (1, 0), (3, 2), (0, 3), (1, 2), (2, 1), (3, 0)}
            ],
        },
    }
    assert bisc(A, 3, 5) == {
        2: {
            Perm((0, 1)): [
                {(0, 0), (1, 1), (2, 2), (2, 0), (0, 2), (1, 2), (2, 1), (0, 1), (1, 0)}
            ],
            Perm((1, 0)): [
                {(0, 1), (1, 2), (1, 0), (2, 1), (0, 0), (2, 2), (0, 2), (1, 1), (2, 0)}
            ],
        },
        3: {
            Perm((0, 2, 1)): [
                {
                    (1, 2),
                    (2, 3),
                    (2, 1),
                    (3, 2),
                    (0, 1),
                    (1, 0),
                    (3, 0),
                    (0, 3),
                    (1, 1),
                    (3, 3),
                    (1, 3),
                    (2, 2),
                    (3, 1),
                    (0, 0),
                    (2, 0),
                    (0, 2),
                }
            ],
            Perm((1, 0, 2)): [
                {
                    (2, 3),
                    (3, 2),
                    (0, 1),
                    (1, 2),
                    (1, 0),
                    (2, 1),
                    (3, 0),
                    (0, 3),
                    (3, 3),
                    (0, 0),
                    (2, 2),
                    (1, 3),
                    (3, 1),
                    (0, 2),
                    (1, 1),
                    (2, 0),
                }
            ],
            Perm((2, 1, 0)): [
                {
                    (0, 1),
                    (2, 3),
                    (1, 0),
                    (3, 2),
                    (0, 3),
                    (1, 2),
                    (2, 1),
                    (3, 0),
                    (0, 0),
                    (3, 3),
                    (1, 3),
                    (0, 2),
                    (2, 2),
                    (1, 1),
                    (3, 1),
                    (2, 0),
                }
            ],
        },
    }


def test_yt22():
    """
    Testing permutations with Young tableaux without the shape [2,2]
    Expected answer is
        1032
        1302 (2,2)
        2031 (2,2)
        2301
    Suffices to look at permutations up to length 5
    """

    A = read_bisc_file(ppf + "yt_perm_avoids_22_good_len8")

    # Too short
    assert bisc(A, 3, 4) == {}
    assert bisc(A, 4, 4) == {
        4: {
            Perm((1, 0, 3, 2)): [set()],
            Perm((1, 3, 0, 2)): [set()],
            Perm((2, 0, 3, 1)): [set()],
            Perm((2, 3, 0, 1)): [set()],
        }
    }

    # Should get expected answer
    assert bisc(A, 4, 5) == {
        4: {
            Perm((1, 0, 3, 2)): [set()],
            Perm((1, 3, 0, 2)): [{(2, 2)}],
            Perm((2, 0, 3, 1)): [{(2, 2)}],
            Perm((2, 3, 0, 1)): [set()],
        }
    }
    assert bisc(A, 4, 6) == {
        4: {
            Perm((1, 0, 3, 2)): [set()],
            Perm((1, 3, 0, 2)): [{(2, 2)}],
            Perm((2, 0, 3, 1)): [{(2, 2)}],
            Perm((2, 3, 0, 1)): [set()],
        }
    }
    assert bisc(A, 4, 7) == {
        4: {
            Perm((1, 0, 3, 2)): [set()],
            Perm((1, 3, 0, 2)): [{(2, 2)}],
            Perm((2, 0, 3, 1)): [{(2, 2)}],
            Perm((2, 3, 0, 1)): [set()],
        }
    }

    # Looking for longer patterns
    assert bisc(A, 5, 6) == {
        4: {
            Perm((1, 0, 3, 2)): [set()],
            Perm((1, 3, 0, 2)): [{(2, 2)}],
            Perm((2, 0, 3, 1)): [{(2, 2)}],
            Perm((2, 3, 0, 1)): [set()],
        },
        5: {},
    }
    assert bisc(A, 5, 7) == {
        4: {
            Perm((1, 0, 3, 2)): [set()],
            Perm((1, 3, 0, 2)): [{(2, 2)}],
            Perm((2, 0, 3, 1)): [{(2, 2)}],
            Perm((2, 3, 0, 1)): [set()],
        },
        5: {},
    }


def test_yt32():
    """
    Testing permutations with Young tableaux without the shape [2,2]
    Expected answer is
        25 mesh patterns (some classical)
    Suffices to look at permutations up to length 6
    """

    A = read_bisc_file(ppf + "yt_perm_avoids_32_good_len8")
    B = read_bisc_file(ppf + "yt_perm_avoids_32_bad_len8")

    # Too short
    assert bisc(A, 4, 4) == {}
    assert bisc(A, 5, 5) == {
        5: {
            Perm((0, 2, 1, 4, 3)): [set()],
            Perm((0, 2, 4, 1, 3)): [set()],
            Perm((0, 3, 1, 4, 2)): [set()],
            Perm((0, 3, 4, 1, 2)): [set()],
            Perm((1, 0, 2, 4, 3)): [set()],
            Perm((1, 0, 3, 2, 4)): [set()],
            Perm((1, 0, 3, 4, 2)): [set()],
            Perm((1, 0, 4, 2, 3)): [set()],
            Perm((1, 2, 0, 4, 3)): [set()],
            Perm((1, 2, 4, 0, 3)): [set()],
            Perm((1, 3, 0, 2, 4)): [set()],
            Perm((1, 3, 0, 4, 2)): [set()],
            Perm((1, 3, 4, 0, 2)): [set()],
            Perm((1, 4, 0, 2, 3)): [set()],
            Perm((2, 0, 1, 4, 3)): [set()],
            Perm((2, 0, 3, 1, 4)): [set()],
            Perm((2, 0, 3, 4, 1)): [set()],
            Perm((2, 0, 4, 1, 3)): [set()],
            Perm((2, 3, 0, 1, 4)): [set()],
            Perm((2, 3, 0, 4, 1)): [set()],
            Perm((2, 3, 4, 0, 1)): [set()],
            Perm((2, 4, 0, 1, 3)): [set()],
            Perm((3, 0, 1, 4, 2)): [set()],
            Perm((3, 0, 4, 1, 2)): [set()],
            Perm((3, 4, 0, 1, 2)): [set()],
        }
    }

    # Should get expected answer
    assert bisc(A, 5, 6) == {
        5: {
            Perm((0, 2, 1, 4, 3)): [set()],
            Perm((0, 2, 4, 1, 3)): [{(3, 3)}],
            Perm((0, 3, 1, 4, 2)): [{(3, 3)}],
            Perm((0, 3, 4, 1, 2)): [set()],
            Perm((1, 0, 2, 4, 3)): [set()],
            Perm((1, 0, 3, 2, 4)): [set()],
            Perm((1, 0, 3, 4, 2)): [set()],
            Perm((1, 0, 4, 2, 3)): [set()],
            Perm((1, 2, 0, 4, 3)): [set()],
            Perm((1, 2, 4, 0, 3)): [{(3, 3)}],
            Perm((1, 3, 0, 2, 4)): [{(2, 2)}],
            Perm((1, 3, 0, 4, 2)): [set()],
            Perm((1, 3, 4, 0, 2)): [set()],
            Perm((1, 4, 0, 2, 3)): [{(2, 2)}],
            Perm((2, 0, 1, 4, 3)): [set()],
            Perm((2, 0, 3, 1, 4)): [{(2, 2)}],
            Perm((2, 0, 3, 4, 1)): [{(2, 2)}],
            Perm((2, 0, 4, 1, 3)): [set()],
            Perm((2, 3, 0, 1, 4)): [set()],
            Perm((2, 3, 0, 4, 1)): [set()],
            Perm((2, 3, 4, 0, 1)): [set()],
            Perm((2, 4, 0, 1, 3)): [set()],
            Perm((3, 0, 1, 4, 2)): [{(3, 3)}],
            Perm((3, 0, 4, 1, 2)): [set()],
            Perm((3, 4, 0, 1, 2)): [set()],
        }
    }
    assert bisc(A, 5, 7) == {
        5: {
            Perm((0, 2, 1, 4, 3)): [set()],
            Perm((0, 2, 4, 1, 3)): [{(3, 3)}],
            Perm((0, 3, 1, 4, 2)): [{(3, 3)}],
            Perm((0, 3, 4, 1, 2)): [set()],
            Perm((1, 0, 2, 4, 3)): [set()],
            Perm((1, 0, 3, 2, 4)): [set()],
            Perm((1, 0, 3, 4, 2)): [set()],
            Perm((1, 0, 4, 2, 3)): [set()],
            Perm((1, 2, 0, 4, 3)): [set()],
            Perm((1, 2, 4, 0, 3)): [{(3, 3)}],
            Perm((1, 3, 0, 2, 4)): [{(2, 2)}],
            Perm((1, 3, 0, 4, 2)): [set()],
            Perm((1, 3, 4, 0, 2)): [set()],
            Perm((1, 4, 0, 2, 3)): [{(2, 2)}],
            Perm((2, 0, 1, 4, 3)): [set()],
            Perm((2, 0, 3, 1, 4)): [{(2, 2)}],
            Perm((2, 0, 3, 4, 1)): [{(2, 2)}],
            Perm((2, 0, 4, 1, 3)): [set()],
            Perm((2, 3, 0, 1, 4)): [set()],
            Perm((2, 3, 0, 4, 1)): [set()],
            Perm((2, 3, 4, 0, 1)): [set()],
            Perm((2, 4, 0, 1, 3)): [set()],
            Perm((3, 0, 1, 4, 2)): [{(3, 3)}],
            Perm((3, 0, 4, 1, 2)): [set()],
            Perm((3, 4, 0, 1, 2)): [set()],
        }
    }

    # Looking for longer patterns
    assert bisc(A, 6, 7) == {
        5: {
            Perm((0, 2, 1, 4, 3)): [set()],
            Perm((0, 2, 4, 1, 3)): [{(3, 3)}],
            Perm((0, 3, 1, 4, 2)): [{(3, 3)}],
            Perm((0, 3, 4, 1, 2)): [set()],
            Perm((1, 0, 2, 4, 3)): [set()],
            Perm((1, 0, 3, 2, 4)): [set()],
            Perm((1, 0, 3, 4, 2)): [set()],
            Perm((1, 0, 4, 2, 3)): [set()],
            Perm((1, 2, 0, 4, 3)): [set()],
            Perm((1, 2, 4, 0, 3)): [{(3, 3)}],
            Perm((1, 3, 0, 2, 4)): [{(2, 2)}],
            Perm((1, 3, 0, 4, 2)): [set()],
            Perm((1, 3, 4, 0, 2)): [set()],
            Perm((1, 4, 0, 2, 3)): [{(2, 2)}],
            Perm((2, 0, 1, 4, 3)): [set()],
            Perm((2, 0, 3, 1, 4)): [{(2, 2)}],
            Perm((2, 0, 3, 4, 1)): [{(2, 2)}],
            Perm((2, 0, 4, 1, 3)): [set()],
            Perm((2, 3, 0, 1, 4)): [set()],
            Perm((2, 3, 0, 4, 1)): [set()],
            Perm((2, 3, 4, 0, 1)): [set()],
            Perm((2, 4, 0, 1, 3)): [set()],
            Perm((3, 0, 1, 4, 2)): [{(3, 3)}],
            Perm((3, 0, 4, 1, 2)): [set()],
            Perm((3, 4, 0, 1, 2)): [set()],
        },
        6: {Perm((2, 5, 0, 3, 4, 1)): [set()], Perm((4, 1, 2, 5, 0, 3)): [set()]},
    }

    SG = bisc(A, 6, 8)
    assert SG == {
        5: {
            Perm((0, 2, 1, 4, 3)): [set()],
            Perm((0, 2, 4, 1, 3)): [{(3, 3)}],
            Perm((0, 3, 1, 4, 2)): [{(3, 3)}],
            Perm((0, 3, 4, 1, 2)): [set()],
            Perm((1, 0, 2, 4, 3)): [set()],
            Perm((1, 0, 3, 2, 4)): [set()],
            Perm((1, 0, 3, 4, 2)): [set()],
            Perm((1, 0, 4, 2, 3)): [set()],
            Perm((1, 2, 0, 4, 3)): [set()],
            Perm((1, 2, 4, 0, 3)): [{(3, 3)}],
            Perm((1, 3, 0, 2, 4)): [{(2, 2)}],
            Perm((1, 3, 0, 4, 2)): [set()],
            Perm((1, 3, 4, 0, 2)): [set()],
            Perm((1, 4, 0, 2, 3)): [{(2, 2)}],
            Perm((2, 0, 1, 4, 3)): [set()],
            Perm((2, 0, 3, 1, 4)): [{(2, 2)}],
            Perm((2, 0, 3, 4, 1)): [{(2, 2)}],
            Perm((2, 0, 4, 1, 3)): [set()],
            Perm((2, 3, 0, 1, 4)): [set()],
            Perm((2, 3, 0, 4, 1)): [set()],
            Perm((2, 3, 4, 0, 1)): [set()],
            Perm((2, 4, 0, 1, 3)): [set()],
            Perm((3, 0, 1, 4, 2)): [{(3, 3)}],
            Perm((3, 0, 4, 1, 2)): [set()],
            Perm((3, 4, 0, 1, 2)): [set()],
        },
        6: {Perm((2, 5, 0, 3, 4, 1)): [set()], Perm((4, 1, 2, 5, 0, 3)): [set()]},
    }
    assert patterns_suffice_for_bad(SG, 7, B) == (True, [])
    assert run_clean_up(SG, B, limit_monitors=25) == (
        [
            [
                (5, 0, 0),
                (5, 1, 0),
                (5, 2, 0),
                (5, 3, 0),
                (5, 4, 0),
                (5, 5, 0),
                (5, 6, 0),
                (5, 7, 0),
                (5, 8, 0),
                (5, 9, 0),
                (5, 10, 0),
                (5, 11, 0),
                (5, 12, 0),
                (5, 13, 0),
                (5, 14, 0),
                (5, 15, 0),
                (5, 16, 0),
                (5, 17, 0),
                (5, 18, 0),
                (5, 19, 0),
                (5, 20, 0),
                (5, 21, 0),
                (5, 22, 0),
                (5, 23, 0),
                (5, 24, 0),
            ]
        ],
        {
            (5, 0, 0): (Perm((0, 2, 1, 4, 3)), set()),
            (5, 1, 0): (Perm((0, 2, 4, 1, 3)), {(3, 3)}),
            (5, 2, 0): (Perm((0, 3, 1, 4, 2)), {(3, 3)}),
            (5, 3, 0): (Perm((0, 3, 4, 1, 2)), set()),
            (5, 4, 0): (Perm((1, 0, 2, 4, 3)), set()),
            (5, 5, 0): (Perm((1, 0, 3, 2, 4)), set()),
            (5, 6, 0): (Perm((1, 0, 3, 4, 2)), set()),
            (5, 7, 0): (Perm((1, 0, 4, 2, 3)), set()),
            (5, 8, 0): (Perm((1, 2, 0, 4, 3)), set()),
            (5, 9, 0): (Perm((1, 2, 4, 0, 3)), {(3, 3)}),
            (5, 10, 0): (Perm((1, 3, 0, 2, 4)), {(2, 2)}),
            (5, 11, 0): (Perm((1, 3, 0, 4, 2)), set()),
            (5, 12, 0): (Perm((1, 3, 4, 0, 2)), set()),
            (5, 13, 0): (Perm((1, 4, 0, 2, 3)), {(2, 2)}),
            (5, 14, 0): (Perm((2, 0, 1, 4, 3)), set()),
            (5, 15, 0): (Perm((2, 0, 3, 1, 4)), {(2, 2)}),
            (5, 16, 0): (Perm((2, 0, 3, 4, 1)), {(2, 2)}),
            (5, 17, 0): (Perm((2, 0, 4, 1, 3)), set()),
            (5, 18, 0): (Perm((2, 3, 0, 1, 4)), set()),
            (5, 19, 0): (Perm((2, 3, 0, 4, 1)), set()),
            (5, 20, 0): (Perm((2, 3, 4, 0, 1)), set()),
            (5, 21, 0): (Perm((2, 4, 0, 1, 3)), set()),
            (5, 22, 0): (Perm((3, 0, 1, 4, 2)), {(3, 3)}),
            (5, 23, 0): (Perm((3, 0, 4, 1, 2)), set()),
            (5, 24, 0): (Perm((3, 4, 0, 1, 2)), set()),
            (6, 0, 0): (Perm((2, 5, 0, 3, 4, 1)), set()),
            (6, 1, 0): (Perm((4, 1, 2, 5, 0, 3)), set()),
        },
    )


def test_av_231_and_mesh():
    """
    Testing permutations from the under a certain correspondence
    Expected answer is
        120
        015234 (1,6), (4,5)
    Suffices to look at permutations up to length 7
    """

    A = read_bisc_file(ppf + "av_231_and_mesh_good_len8")

    # Too short
    assert bisc(A, 3, 4) == {3: {Perm((1, 2, 0)): [set()]}}
    assert bisc(A, 5, 7) == {3: {Perm((1, 2, 0)): [set()]}, 4: {}, 5: {}}

    # Should get expected answer
    assert bisc(A, 6, 7) == {
        3: {Perm((1, 2, 0)): [set()]},
        4: {},
        5: {},
        6: {Perm((0, 1, 5, 2, 3, 4)): [{(4, 5), (1, 6)}]},
    }
    assert bisc(A, 6, 8) == {
        3: {Perm((1, 2, 0)): [set()]},
        4: {},
        5: {},
        6: {Perm((0, 1, 5, 2, 3, 4)): [{(4, 5), (1, 6)}]},
    }


def test_quick_sortable():
    """
    Testing quick-sortable permutations
    Expected answer is
        210
        1023 (2,2)
        1302
    Suffices to look at permutations up to length 5
    """

    A = read_bisc_file(ppf + "quick_sortable_good_len8")

    # Too short
    assert bisc(A, 3, 4) == {3: {Perm((2, 1, 0)): [set()]}}
    assert bisc(A, 4, 4) == {
        3: {Perm((2, 1, 0)): [set()]},
        4: {Perm((1, 0, 3, 2)): [set()], Perm((1, 3, 0, 2)): [set()]},
    }

    # Should get expected answer
    assert bisc(A, 4, 5) == {
        3: {Perm((2, 1, 0)): [set()]},
        4: {Perm((1, 0, 3, 2)): [{(2, 2)}], Perm((1, 3, 0, 2)): [set()]},
    }
    assert bisc(A, 4, 6) == {
        3: {Perm((2, 1, 0)): [set()]},
        4: {Perm((1, 0, 3, 2)): [{(2, 2)}], Perm((1, 3, 0, 2)): [set()]},
    }
    assert bisc(A, 5, 6) == {
        3: {Perm((2, 1, 0)): [set()]},
        4: {Perm((1, 0, 3, 2)): [{(2, 2)}], Perm((1, 3, 0, 2)): [set()]},
        5: {},
    }
