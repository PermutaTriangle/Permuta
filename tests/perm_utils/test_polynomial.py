from permuta import Perm
from permuta.perm_utils.polynomial import PolyPerm

expected = {
    frozenset(
        {
            Perm((1, 0, 2, 3)),
            Perm((1, 2, 0, 3)),
            Perm((0, 3, 1, 2)),
            Perm((2, 4, 0, 3, 1)),
            Perm((3, 4, 2, 1, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 0, 3, 1)),
            Perm((1, 0)),
            Perm((3, 2, 0, 1)),
            Perm((0, 1, 2)),
            Perm((0, 3, 1, 2, 4)),
            Perm((1, 2, 3, 0)),
            Perm((3, 0, 4, 1, 2)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((1, 0, 2, 3)),
            Perm((0, 2, 1, 3, 4)),
            Perm((2, 1, 3, 4, 0)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 2, 1, 3)),
            Perm((1, 0, 2, 3)),
            Perm((1, 2, 0, 3)),
            Perm((1, 0, 2)),
            Perm((2, 1, 0)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((3, 0, 1, 2)),
            Perm((2, 0, 1)),
            Perm((0, 1, 3, 2)),
            Perm((0, 3, 1, 2, 4)),
            Perm((2, 4, 3, 1, 0)),
            Perm((1, 2, 0)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((3, 0, 2, 1, 4)),
            Perm((1, 0)),
            Perm((3, 1, 0, 2)),
            Perm((1, 3, 0, 4, 2)),
            Perm((3, 1, 2, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((3, 1, 0, 2, 4)), Perm((0, 1))}): True,
    frozenset({Perm((1, 2, 0, 3)), Perm((0, 1))}): True,
    frozenset(
        {
            Perm((3, 0, 2, 1, 4)),
            Perm((1, 0)),
            Perm((4, 1, 0, 3, 2)),
            Perm((3, 0, 1, 2)),
            Perm((2, 3, 0, 1)),
            Perm((2, 1, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((4, 1, 0, 3, 2)),
            Perm((3, 0, 1, 2)),
            Perm((2, 1, 0, 3)),
            Perm((0, 2, 3, 1)),
            Perm((1, 2, 0, 3, 4)),
            Perm((3, 4, 2, 1, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((2, 1, 0, 4, 3)), Perm((1, 4, 3, 0, 2)), Perm((0, 1))}): True,
    frozenset(
        {
            Perm((4, 3, 2, 0, 1)),
            Perm((1, 0)),
            Perm((4, 1, 3, 2, 0)),
            Perm((3, 0, 1, 2)),
            Perm((3, 0, 2, 1)),
            Perm((0, 1, 3, 2, 4)),
            Perm((0, 2, 3, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0, 2, 3)),
            Perm((3, 0, 2, 1)),
            Perm((3, 2, 0, 1)),
            Perm((0, 1)),
            Perm((0, 1, 2, 3)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 2, 0, 4, 3)),
            Perm((3, 2, 1, 0)),
            Perm((1, 0)),
            Perm((2, 3, 0, 4, 1)),
            Perm((1, 3, 0, 2)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset({Perm((0, 1)), Perm((0, 1, 2)), Perm((1, 0))}): True,
    frozenset(
        {Perm((0, 3, 1, 2)), Perm((4, 0, 2, 3, 1)), Perm((2, 1, 0, 3)), Perm((0, 1))}
    ): True,
    frozenset(
        {Perm((2, 1, 0)), Perm((0, 1, 3, 4, 2)), Perm((0, 1)), Perm((1, 2, 4, 0, 3))}
    ): True,
    frozenset(
        {
            Perm((1, 0, 3, 2, 4)),
            Perm((3, 2, 1, 0)),
            Perm((4, 2, 0, 1, 3)),
            Perm((1, 0, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 0, 1, 3)),
            Perm((2, 3, 1, 4, 0)),
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((2, 0, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((4, 2, 1, 0, 3)),
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((2, 3, 0, 1)),
            Perm((0, 2, 3, 1)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((4, 1, 0, 3, 2)),
            Perm((2, 1, 0, 3)),
            Perm((2, 0, 1)),
            Perm((0, 1, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((0, 1)), Perm((3, 1, 0, 2))}): True,
    frozenset(
        {
            Perm((2, 0, 3, 1)),
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((2, 0, 1, 3, 4)),
            Perm((2, 1, 0)),
            Perm((0, 1)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((4, 1, 0, 3, 2)),
            Perm((2, 3, 1, 0)),
            Perm((0, 1, 2)),
            Perm((0, 2, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((0, 1)), Perm((3, 2, 1, 0, 4)), Perm((1, 0))}): True,
    frozenset(
        {
            Perm((1, 0, 2)),
            Perm((2, 1, 0)),
            Perm((0, 1)),
            Perm((0, 2, 3, 1, 4)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset({Perm((0, 1)), Perm((2, 0, 1)), Perm((0, 2, 1))}): True,
    frozenset(
        {Perm((3, 0, 1, 2)), Perm((1, 0, 2, 4, 3)), Perm((0, 2, 3, 1)), Perm((0, 1))}
    ): True,
    frozenset(
        {
            Perm((2, 0, 1, 3)),
            Perm((4, 2, 1, 0, 3)),
            Perm((2, 0, 3, 1)),
            Perm((1, 0)),
            Perm((1, 0, 2, 3)),
            Perm((4, 0, 2, 1, 3)),
            Perm((0, 2, 3, 1, 4)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((0, 1)), Perm((1, 0))}): True,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((2, 0, 1, 3)),
            Perm((4, 1, 3, 0, 2)),
            Perm((1, 4, 0, 3, 2)),
            Perm((1, 3, 0, 4, 2)),
            Perm((4, 1, 2, 3, 0)),
            Perm((2, 0, 1)),
            Perm((0, 2, 3, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((3, 1, 0, 2)),
            Perm((2, 0, 1)),
            Perm((0, 1, 2)),
            Perm((0, 2, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((1, 0, 2)), Perm((1, 2, 0)), Perm((0, 2, 1))}): True,
    frozenset(
        {
            Perm((1, 0, 4, 2, 3)),
            Perm((1, 0)),
            Perm((3, 1, 0, 2)),
            Perm((1, 0, 2)),
            Perm((3, 0, 2, 1)),
            Perm((1, 2, 4, 0, 3)),
            Perm((1, 0, 3, 2)),
        }
    ): True,
    frozenset({Perm((0, 1, 2, 3)), Perm((0, 1))}): True,
    frozenset({Perm((0, 1)), Perm((0, 2, 1))}): True,
    frozenset(
        {
            Perm((2, 0, 1, 3)),
            Perm((1, 0)),
            Perm((0, 2, 1, 3)),
            Perm((1, 0, 2)),
            Perm((3, 1, 2, 0)),
            Perm((0, 2, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((4, 0, 1, 3, 2)),
            Perm((2, 1, 0, 3, 4)),
            Perm((0, 1, 2, 3)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 1, 2, 4, 3)),
            Perm((3, 2, 4, 0, 1)),
            Perm((1, 2, 0)),
            Perm((3, 2, 1, 0)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 0, 3, 1)),
            Perm((2, 1, 3, 0, 4)),
            Perm((3, 0, 1, 2, 4)),
            Perm((3, 1, 2, 0)),
            Perm((0, 1, 2)),
        }
    ): True,
    frozenset(
        {Perm((2, 3, 0, 1)), Perm((3, 0, 4, 1, 2)), Perm((0, 1)), Perm((0, 1, 3, 2))}
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((1, 0, 2, 3)),
            Perm((1, 3, 0, 2, 4)),
            Perm((4, 2, 1, 3, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((1, 0)),
            Perm((3, 1, 0, 2)),
            Perm((0, 3, 2, 1)),
            Perm((0, 1, 2, 3)),
            Perm((0, 3, 1, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((1, 0)), Perm((3, 1, 0, 4, 2))}): True,
    frozenset({Perm((1, 3, 4, 0, 2)), Perm((1, 0, 4, 3, 2)), Perm((0, 1))}): True,
    frozenset(
        {
            Perm((1, 0, 4, 2, 3)),
            Perm((2, 4, 0, 3, 1)),
            Perm((0, 2, 3, 1)),
            Perm((1, 2, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((2, 1, 0, 3, 4)), Perm((2, 0, 1, 3)), Perm((0, 1))}): True,
    frozenset(
        {
            Perm((0, 3, 1, 4, 2)),
            Perm((1, 0, 2)),
            Perm((2, 0, 1, 3, 4)),
            Perm((0, 1, 2)),
            Perm((1, 3, 0, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((4, 1, 3, 0, 2)),
            Perm((2, 0, 3, 1)),
            Perm((1, 0)),
            Perm((0, 4, 2, 3, 1)),
            Perm((3, 2, 4, 1, 0)),
            Perm((0, 2, 3, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 4, 2, 1, 3)),
            Perm((2, 3, 1, 4, 0)),
            Perm((0, 3, 2, 1)),
            Perm((2, 0, 1)),
            Perm((0, 1, 2)),
        }
    ): True,
    frozenset({Perm((1, 0, 2)), Perm((1, 0))}): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((3, 1, 2, 0)),
            Perm((2, 0, 1)),
            Perm((0, 1, 3, 2)),
            Perm((0, 1, 2)),
            Perm((1, 2, 3, 0)),
            Perm((1, 4, 2, 3, 0)),
            Perm((0, 3, 2, 1, 4)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((1, 0))}): True,
    frozenset(
        {
            Perm((3, 2, 1, 4, 0)),
            Perm((4, 3, 2, 1, 0)),
            Perm((1, 0, 2)),
            Perm((4, 1, 2, 3, 0)),
            Perm((0, 1, 2)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset(
        {Perm((3, 2, 4, 1, 0)), Perm((1, 0)), Perm((2, 0, 1)), Perm((0, 4, 3, 1, 2))}
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((0, 2, 3, 4, 1)),
            Perm((1, 0, 3, 4, 2)),
            Perm((1, 2, 0)),
            Perm((0, 1, 2, 3)),
        }
    ): True,
    frozenset(
        {
            Perm((3, 1, 2, 0)),
            Perm((3, 0, 2, 1)),
            Perm((1, 4, 2, 0, 3)),
            Perm((0, 1)),
            Perm((0, 1, 2, 3)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((1, 0)),
            Perm((2, 0, 1)),
            Perm((0, 2, 4, 1, 3)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 3, 1, 0)),
            Perm((0, 1, 2)),
            Perm((1, 4, 3, 0, 2)),
            Perm((2, 1, 0)),
            Perm((1, 3, 4, 2, 0)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset({Perm((0, 2, 3, 1)), Perm((1, 0))}): True,
    frozenset({Perm((2, 1, 3, 0)), Perm((1, 0))}): True,
    frozenset(
        {
            Perm((2, 0, 3, 1)),
            Perm((3, 1, 4, 0, 2)),
            Perm((0, 3, 2, 4, 1)),
            Perm((2, 0, 1)),
            Perm((2, 1, 0, 3, 4)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((3, 2, 0, 1)),
            Perm((0, 1, 2)),
            Perm((2, 1, 0)),
            Perm((0, 2, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 2, 3, 4, 1)),
            Perm((3, 0, 2, 1)),
            Perm((3, 2, 0, 1)),
            Perm((2, 3, 1, 0)),
            Perm((0, 3, 1, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((4, 2, 1, 0, 3)),
            Perm((2, 3, 1, 4, 0)),
            Perm((4, 3, 2, 1, 0)),
            Perm((1, 0, 2)),
            Perm((3, 0, 1, 4, 2)),
            Perm((1, 2, 0)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((3, 1, 0, 4, 2)),
            Perm((1, 0, 2, 4, 3)),
            Perm((0, 1, 2)),
            Perm((2, 1, 0)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 1, 2, 3, 4)),
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((3, 1, 2, 0)),
            Perm((0, 1)),
            Perm((1, 0, 3, 2)),
            Perm((0, 2, 1)),
            Perm((0, 1, 4, 3, 2)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((0, 4, 2, 1, 3)),
            Perm((1, 0)),
            Perm((2, 0, 1)),
            Perm((2, 1, 0)),
            Perm((3, 4, 0, 2, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 3, 2, 1)),
            Perm((2, 0, 4, 3, 1)),
            Perm((1, 2, 0, 3)),
            Perm((0, 3, 1, 2)),
            Perm((1, 3, 0, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((2, 4, 3, 0, 1)),
            Perm((4, 1, 0, 2, 3)),
            Perm((2, 1, 0, 3, 4)),
            Perm((0, 3, 1, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((2, 1, 0, 3)),
            Perm((1, 2, 0, 3)),
            Perm((2, 3, 1, 0)),
            Perm((2, 1, 0)),
            Perm((0, 3, 4, 2, 1)),
            Perm((1, 2, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {Perm((3, 2, 1, 4, 0)), Perm((0, 2, 1)), Perm((1, 2, 0, 3)), Perm((0, 1))}
    ): True,
    frozenset(
        {
            Perm((2, 0, 1, 3)),
            Perm((4, 2, 0, 1, 3)),
            Perm((0, 1, 2)),
            Perm((2, 1, 0)),
            Perm((0, 2, 3, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((3, 0, 1, 2)),
            Perm((2, 1, 0, 3)),
            Perm((2, 0, 1)),
            Perm((0, 1, 2)),
            Perm((1, 4, 3, 2, 0)),
            Perm((4, 0, 3, 1, 2)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((4, 3, 2, 1, 0)),
            Perm((2, 0, 1)),
            Perm((1, 0, 2, 4, 3)),
            Perm((3, 2, 4, 0, 1)),
            Perm((2, 1, 0)),
            Perm((0, 2, 3, 1)),
            Perm((0, 2, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((3, 1, 2, 4, 0)), Perm((0, 1, 2)), Perm((0, 1))}): True,
    frozenset({Perm((2, 1, 0)), Perm((1, 0))}): True,
    frozenset({Perm((0, 3, 1, 2)), Perm((1, 2, 0)), Perm((1, 0))}): True,
    frozenset(
        {
            Perm((2, 1, 4, 3, 0)),
            Perm((0, 1, 2)),
            Perm((1, 2, 3, 0)),
            Perm((0, 2, 1)),
            Perm((1, 2, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((1, 2, 0, 3)),
            Perm((3, 0, 2, 1)),
            Perm((2, 3, 1, 0)),
            Perm((0, 1, 2)),
            Perm((2, 1, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 0, 3, 1)),
            Perm((4, 1, 2, 3, 0)),
            Perm((2, 0, 1, 4, 3)),
            Perm((2, 3, 1, 0)),
            Perm((1, 3, 0, 2)),
            Perm((0, 2, 4, 1, 3)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((3, 1, 0, 4, 2)),
            Perm((1, 2, 3, 0)),
            Perm((2, 1, 0)),
            Perm((1, 2, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((0, 1)), Perm((0, 3, 2, 1)), Perm((0, 1, 2)), Perm((1, 0))}): True,
    frozenset({Perm((3, 4, 0, 1, 2)), Perm((1, 0))}): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((3, 1, 0, 4, 2)),
            Perm((2, 3, 1, 0)),
            Perm((1, 2, 0)),
            Perm((1, 2, 3, 0)),
            Perm((0, 3, 4, 2, 1)),
            Perm((2, 1, 3, 4, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 0, 1, 3)),
            Perm((3, 2, 0, 1)),
            Perm((0, 1, 2)),
            Perm((0, 2, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 0, 3, 1, 4)),
            Perm((1, 0)),
            Perm((3, 2, 1, 0)),
            Perm((0, 2, 1, 3)),
            Perm((2, 1, 0, 3)),
            Perm((3, 0, 4, 2, 1)),
            Perm((2, 1, 0)),
            Perm((0, 1)),
            Perm((0, 2, 3, 1)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset({Perm((2, 1, 3, 0)), Perm((2, 0, 1, 3)), Perm((0, 1))}): True,
    frozenset(
        {
            Perm((3, 1, 0, 2)),
            Perm((1, 2, 0, 3)),
            Perm((2, 0, 1)),
            Perm((2, 1, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 2, 0, 4, 3)),
            Perm((3, 2, 1, 0)),
            Perm((1, 0)),
            Perm((2, 1, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset({Perm((1, 0, 2)), Perm((0, 1, 2)), Perm((0, 2, 1)), Perm((1, 0))}): True,
    frozenset(
        {
            Perm((1, 0, 3, 2, 4)),
            Perm((3, 2, 1, 0)),
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((0, 1, 2)),
            Perm((1, 2, 0, 3, 4)),
            Perm((3, 0, 4, 1, 2)),
            Perm((0, 2, 3, 1)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((4, 0, 3, 2, 1)),
            Perm((1, 0)),
            Perm((2, 0, 1)),
            Perm((0, 1, 2)),
            Perm((1, 3, 0, 2, 4)),
            Perm((1, 2, 0)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((2, 0, 1, 3)),
            Perm((2, 0, 1)),
            Perm((1, 2, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 3, 2, 4, 1)),
            Perm((1, 0, 2, 3)),
            Perm((2, 1, 0, 3)),
            Perm((2, 1, 0)),
            Perm((0, 3, 4, 1, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((2, 3, 1, 0)),
            Perm((0, 1, 2)),
            Perm((4, 2, 3, 0, 1)),
            Perm((0, 3, 4, 1, 2)),
            Perm((1, 2, 0)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((3, 2, 1, 0, 4)),
            Perm((1, 0)),
            Perm((1, 0, 2)),
            Perm((1, 2, 0, 3)),
            Perm((3, 2, 0, 1, 4)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 1)),
            Perm((0, 1, 3, 2, 4)),
            Perm((3, 0, 4, 1, 2)),
            Perm((1, 2, 0)),
            Perm((0, 2, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((3, 2, 1, 0)),
            Perm((1, 0)),
            Perm((0, 1, 2)),
            Perm((2, 3, 4, 1, 0)),
            Perm((3, 0, 4, 1, 2)),
            Perm((0, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0)),
            Perm((0, 2, 1, 3)),
            Perm((0, 1, 2)),
            Perm((2, 1, 0)),
            Perm((0, 2, 3, 1)),
        }
    ): True,
    frozenset({Perm((0, 2, 1, 3))}): False,
    frozenset({Perm((2, 3, 0, 1, 4))}): False,
    frozenset(
        {
            Perm((1, 0, 2, 3)),
            Perm((2, 0, 4, 1, 3)),
            Perm((2, 3, 4, 1, 0)),
            Perm((3, 4, 1, 0, 2)),
        }
    ): False,
    frozenset(
        {Perm((1, 0, 3, 4, 2)), Perm((3, 4, 1, 2, 0)), Perm((0, 1, 3, 2))}
    ): False,
    frozenset({Perm((2, 1, 0)), Perm((3, 0, 2, 4, 1))}): False,
    frozenset(
        {
            Perm((0, 4, 1, 2, 3)),
            Perm((3, 4, 2, 1, 0)),
            Perm((1, 3, 0, 2)),
            Perm((2, 0, 1)),
        }
    ): False,
    frozenset({Perm((1, 0, 2)), Perm((1, 2, 0)), Perm((0, 4, 2, 3, 1))}): False,
    frozenset({Perm((2, 0, 1, 3)), Perm((1, 3, 0, 2)), Perm((2, 1, 3, 0, 4))}): False,
    frozenset({Perm((2, 1, 0)), Perm((4, 1, 2, 3, 0)), Perm((3, 1, 0, 2))}): False,
    frozenset({Perm((1, 0, 2)), Perm((0, 2, 1))}): False,
    frozenset({Perm((1, 4, 2, 3, 0)), Perm((0, 2, 1))}): False,
    frozenset({Perm((3, 1, 2, 0)), Perm((2, 0, 1))}): False,
    frozenset(
        {Perm((2, 1, 0)), Perm((2, 0, 1, 3)), Perm((1, 3, 4, 0, 2)), Perm((1, 3, 2, 0))}
    ): False,
    frozenset({Perm((0, 1, 2))}): False,
    frozenset({Perm((3, 1, 2, 0)), Perm((1, 2, 0))}): False,
    frozenset({Perm((0, 3, 1, 2)), Perm((1, 3, 0, 2)), Perm((0, 2, 3, 1))}): False,
    frozenset({Perm((0, 4, 2, 3, 1))}): False,
    frozenset({Perm((0, 3, 4, 1, 2)), Perm((3, 2, 1, 0))}): False,
    frozenset({Perm((1, 3, 2, 0))}): False,
    frozenset({Perm((0, 2, 1)), Perm((0, 1, 2, 3))}): False,
    frozenset({Perm((2, 3, 1, 4, 0)), Perm((2, 0, 1))}): False,
    frozenset({Perm((1, 0, 2)), Perm((2, 3, 0, 1, 4))}): False,
    frozenset({Perm((2, 3, 0, 1)), Perm((3, 1, 2, 0))}): False,
    frozenset(
        {Perm((1, 0, 2, 3)), Perm((2, 4, 0, 3, 1)), Perm((2, 4, 3, 0, 1))}
    ): False,
    frozenset({Perm((3, 0, 1, 2))}): False,
    frozenset({Perm((2, 1, 0))}): False,
    frozenset({Perm((1, 2, 0))}): False,
    frozenset({Perm((2, 0, 1, 3)), Perm((0, 3, 2, 1)), Perm((4, 3, 0, 1, 2))}): False,
    frozenset({Perm((3, 2, 1, 0, 4))}): False,
    frozenset(
        {Perm((0, 3, 2, 1)), Perm((3, 1, 2, 4, 0)), Perm((0, 2, 3, 1)), Perm((0, 2, 1))}
    ): False,
    frozenset(
        {
            Perm((2, 1, 0)),
            Perm((2, 4, 0, 3, 1)),
            Perm((3, 0, 2, 1)),
            Perm((2, 0, 1, 4, 3)),
        }
    ): False,
    frozenset({Perm((2, 0, 3, 1, 4))}): False,
    frozenset({Perm((0, 1, 3, 4, 2)), Perm((2, 4, 0, 1, 3))}): False,
    frozenset({Perm((0, 2, 1)), Perm((2, 4, 3, 0, 1)), Perm((4, 0, 2, 1, 3))}): False,
    frozenset({Perm((1, 0, 2))}): False,
    frozenset({Perm((0, 1, 2)), Perm((0, 2, 1))}): False,
    frozenset({Perm((0, 1, 2)), Perm((2, 0, 3, 1))}): False,
    frozenset(
        {Perm((1, 0, 2)), Perm((1, 2, 0)), Perm((1, 0, 2, 4, 3)), Perm((2, 4, 0, 1, 3))}
    ): False,
    frozenset(
        {
            Perm((0, 1, 2, 4, 3)),
            Perm((3, 0, 2, 1)),
            Perm((1, 2, 0, 3)),
            Perm((0, 1, 2)),
            Perm((1, 3, 0, 2)),
        }
    ): False,
    frozenset({Perm((1, 0, 2)), Perm((0, 1, 2))}): False,
    frozenset(
        {Perm((1, 2, 3, 4, 0)), Perm((1, 3, 0, 2)), Perm((1, 2, 0, 3)), Perm((0, 1, 2))}
    ): False,
    frozenset({Perm((3, 0, 2, 1)), Perm((1, 2, 4, 0, 3))}): False,
    frozenset({Perm((2, 1, 0)), Perm((2, 4, 0, 3, 1)), Perm((1, 2, 0))}): False,
    frozenset(
        {
            Perm((4, 1, 3, 0, 2)),
            Perm((1, 4, 0, 3, 2)),
            Perm((1, 0, 2, 3)),
            Perm((3, 1, 2, 0)),
            Perm((2, 0, 1, 4, 3)),
            Perm((3, 2, 0, 1, 4)),
            Perm((0, 3, 1, 2)),
            Perm((0, 4, 1, 2, 3)),
        }
    ): False,
    frozenset({Perm((1, 2, 0, 3, 4)), Perm((1, 2, 0)), Perm((1, 3, 2, 0))}): False,
    frozenset(
        {
            Perm((2, 4, 0, 1, 3)),
            Perm((1, 2, 0, 3)),
            Perm((1, 0, 2, 4, 3)),
            Perm((2, 3, 1, 0)),
            Perm((1, 2, 3, 0)),
            Perm((0, 2, 1)),
        }
    ): False,
    frozenset({Perm((1, 0, 2, 3))}): False,
    frozenset({Perm((1, 3, 4, 0, 2)), Perm((3, 2, 1, 4, 0))}): False,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((4, 0, 1, 3, 2)),
            Perm((3, 0, 2, 1)),
            Perm((3, 4, 2, 0, 1)),
            Perm((2, 0, 1)),
            Perm((4, 1, 0, 2, 3)),
            Perm((1, 4, 2, 0, 3)),
            Perm((2, 3, 1, 0)),
        }
    ): False,
    frozenset(
        {
            Perm((2, 0, 1)),
            Perm((1, 4, 2, 0, 3)),
            Perm((2, 3, 4, 1, 0)),
            Perm((3, 0, 4, 2, 1)),
            Perm((1, 2, 0)),
        }
    ): False,
    frozenset({Perm((0, 2, 1, 3)), Perm((3, 1, 2, 0)), Perm((3, 2, 0, 1))}): False,
    frozenset({Perm((0, 2, 1))}): False,
    frozenset({Perm((4, 2, 3, 1, 0)), Perm((2, 0, 1)), Perm((2, 0, 3, 1))}): False,
    frozenset({Perm((0, 3, 4, 1, 2))}): False,
    frozenset(
        {
            Perm((4, 3, 2, 0, 1)),
            Perm((3, 0, 1, 2, 4)),
            Perm((2, 0, 1)),
            Perm((0, 4, 1, 2, 3)),
            Perm((1, 2, 0)),
        }
    ): False,
    frozenset({Perm((0, 3, 2, 1))}): False,
    frozenset({Perm((1, 4, 3, 2, 0)), Perm((0, 2, 1))}): False,
    frozenset({Perm((1, 3, 0, 4, 2)), Perm((3, 0, 4, 1, 2))}): False,
    frozenset({Perm((3, 2, 0, 1, 4)), Perm((1, 3, 2, 0))}): False,
    frozenset({Perm((2, 4, 0, 1, 3))}): False,
    frozenset({Perm((0, 3, 1, 2)), Perm((0, 4, 1, 2, 3)), Perm((0, 1, 2))}): False,
    frozenset({Perm((1, 3, 0, 2)), Perm((4, 1, 2, 3, 0)), Perm((2, 0, 1))}): False,
    frozenset({Perm((0, 3, 2, 1)), Perm((0, 2, 3, 1))}): False,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((0, 3, 2, 1)),
            Perm((1, 0, 2)),
            Perm((0, 1, 4, 2, 3)),
            Perm((0, 2, 1)),
        }
    ): False,
    frozenset(
        {
            Perm((1, 4, 0, 3, 2)),
            Perm((3, 0, 1, 2)),
            Perm((1, 0, 2)),
            Perm((4, 1, 0, 2, 3)),
            Perm((0, 1, 3, 2)),
            Perm((0, 1, 2)),
        }
    ): False,
    frozenset({Perm((0, 1, 2)), Perm((1, 3, 2, 4, 0))}): False,
    frozenset({Perm((1, 3, 0, 2))}): False,
    frozenset({Perm((2, 3, 0, 1))}): False,
    frozenset(
        {
            Perm((1, 2, 3, 0, 4)),
            Perm((1, 3, 0, 2)),
            Perm((0, 2, 3, 1)),
            Perm((2, 0, 1, 4, 3)),
        }
    ): False,
    frozenset(
        {
            Perm((0, 3, 2, 1)),
            Perm((2, 0, 1)),
            Perm((3, 2, 4, 1, 0)),
            Perm((2, 0, 1, 4, 3)),
        }
    ): False,
    frozenset({Perm((1, 0, 2)), Perm((2, 1, 0, 3)), Perm((1, 2, 0))}): False,
    frozenset({Perm((2, 1, 0, 3))}): False,
    frozenset({Perm((3, 1, 0, 2))}): False,
    frozenset(
        {Perm((1, 2, 3, 4, 0)), Perm((0, 2, 3, 1, 4)), Perm((0, 1, 3, 2))}
    ): False,
    frozenset(
        {
            Perm((3, 0, 1, 2)),
            Perm((2, 3, 1, 4, 0)),
            Perm((4, 3, 1, 2, 0)),
            Perm((4, 3, 2, 1, 0)),
        }
    ): False,
    frozenset(
        {
            Perm((0, 2, 1, 3)),
            Perm((0, 4, 1, 2, 3)),
            Perm((0, 2, 4, 3, 1)),
            Perm((0, 1, 3, 2)),
        }
    ): False,
    frozenset({Perm((3, 0, 1, 2)), Perm((4, 0, 1, 3, 2))}): False,
    frozenset(
        {
            Perm((2, 0, 1, 3)),
            Perm((2, 1, 0, 3)),
            Perm((0, 1, 2)),
            Perm((0, 4, 2, 3, 1)),
            Perm((0, 3, 4, 2, 1)),
        }
    ): False,
    frozenset({Perm((0, 2, 1)), Perm((1, 4, 2, 0, 3))}): False,
    frozenset(
        {Perm((1, 0, 2)), Perm((2, 3, 0, 1, 4)), Perm((0, 2, 1)), Perm((3, 4, 1, 0, 2))}
    ): False,
    frozenset({Perm((0, 3, 2, 1)), Perm((1, 0, 2)), Perm((0, 4, 2, 1, 3))}): False,
    frozenset(
        {
            Perm((4, 2, 3, 1, 0)),
            Perm((1, 2, 4, 3, 0)),
            Perm((3, 4, 2, 0, 1)),
            Perm((2, 0, 1)),
            Perm((1, 2, 3, 0)),
            Perm((2, 1, 0)),
        }
    ): False,
    frozenset({Perm((2, 3, 0, 1)), Perm((0, 1, 2)), Perm((4, 1, 0, 2, 3))}): False,
    frozenset({Perm((3, 4, 0, 1, 2)), Perm((0, 2, 1, 4, 3))}): False,
    frozenset({Perm((0, 3, 1, 2)), Perm((0, 1, 2))}): False,
    frozenset({Perm((4, 0, 3, 2, 1))}): False,
    frozenset({Perm((1, 2, 3, 4, 0))}): False,
    frozenset(
        {
            Perm((3, 1, 2, 4, 0)),
            Perm((2, 0, 3, 1)),
            Perm((2, 1, 0)),
            Perm((2, 3, 1, 0)),
            Perm((1, 2, 3, 0)),
            Perm((2, 1, 0, 4, 3)),
            Perm((3, 0, 1, 4, 2)),
        }
    ): False,
    frozenset(
        {Perm((4, 2, 3, 0, 1)), Perm((2, 1, 0, 3)), Perm((3, 2, 4, 1, 0))}
    ): False,
    frozenset({Perm((2, 1, 3, 4, 0)), Perm((0, 4, 3, 1, 2))}): False,
    frozenset(
        {
            Perm((4, 1, 3, 0, 2)),
            Perm((2, 0, 3, 1)),
            Perm((3, 1, 0, 2)),
            Perm((0, 2, 1, 3)),
            Perm((3, 2, 0, 1)),
        }
    ): False,
    frozenset({Perm((2, 0, 1))}): False,
    frozenset({Perm((2, 3, 0, 1)), Perm((0, 1, 2))}): False,
    frozenset(
        {Perm((4, 3, 1, 0, 2)), Perm((1, 2, 3, 0, 4)), Perm((1, 3, 2, 0))}
    ): False,
    frozenset(
        {
            Perm((2, 1, 3, 0)),
            Perm((2, 0, 1)),
            Perm((2, 3, 0, 1)),
            Perm((2, 1, 0)),
            Perm((1, 2, 0, 3, 4)),
        }
    ): False,
    frozenset(
        {
            Perm((2, 3, 0, 1)),
            Perm((2, 3, 0, 1, 4)),
            Perm((3, 4, 1, 2, 0)),
            Perm((1, 0, 4, 2, 3)),
        }
    ): False,
    frozenset({Perm((4, 2, 3, 1, 0)), Perm((4, 3, 2, 0, 1))}): False,
    frozenset({Perm((1, 0, 3, 2, 4))}): False,
    frozenset({Perm((2, 1, 0)), Perm((2, 0, 4, 3, 1)), Perm((0, 4, 2, 3, 1))}): False,
    frozenset({Perm((3, 2, 0, 1, 4)), Perm((2, 4, 3, 0, 1)), Perm((1, 2, 0))}): False,
    frozenset(
        {
            Perm((0, 1, 3, 4, 8, 6, 2, 7, 5)),
            Perm((4, 3, 2, 1, 0)),
            Perm((1, 3, 2, 0, 4)),
            Perm((2, 1, 0, 3, 4)),
            Perm((0, 1, 3, 2, 4)),
            Perm((2, 1, 0, 5, 3, 4)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 8, 5, 7, 4, 3, 1, 6, 0, 9)),
            Perm((4, 3, 2, 0, 1)),
            Perm((0, 1, 2, 3, 4)),
            Perm((3, 1, 4, 0, 2)),
            Perm((0, 2, 1, 4, 5, 3)),
            Perm((2, 0, 7, 3, 1, 8, 4, 6, 5)),
            Perm((2, 3, 5, 7, 0, 8, 1, 4, 6)),
            Perm((3, 2, 4, 0, 1)),
            Perm((3, 4, 0, 2, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 1, 2, 4, 3)),
            Perm((4, 3, 2, 1, 0)),
            Perm((1, 3, 0, 5, 6, 4, 2)),
            Perm((3, 4, 2, 0, 1)),
            Perm((2, 3, 4, 5, 0, 1)),
            Perm((5, 3, 8, 1, 0, 7, 6, 2, 4)),
            Perm((4, 0, 2, 1, 3)),
            Perm((6, 2, 0, 8, 1, 3, 7, 5, 4)),
            Perm((9, 3, 7, 0, 4, 5, 8, 1, 2, 6)),
        }
    ): True,
    frozenset(
        {
            Perm((4, 3, 2, 0, 1)),
            Perm((0, 4, 3, 2, 1)),
            Perm((9, 1, 3, 7, 8, 0, 2, 5, 6, 4)),
            Perm((2, 3, 1, 0, 4)),
            Perm((7, 5, 8, 1, 0, 6, 4, 9, 2, 3)),
            Perm((7, 5, 4, 3, 0, 1, 6, 2)),
            Perm((0, 3, 1, 2, 4)),
            Perm((5, 0, 2, 4, 3, 1)),
            Perm((0, 1, 3, 2, 4)),
            Perm((6, 9, 0, 5, 3, 8, 7, 2, 1, 4)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 3, 4, 0, 5, 8, 1, 7, 6)),
            Perm((4, 3, 2, 1, 0)),
            Perm((2, 3, 1, 0, 4)),
            Perm((2, 0, 1, 3, 4)),
            Perm((7, 1, 6, 5, 4, 2, 3, 0)),
            Perm((0, 2, 1, 3, 4, 6, 5)),
            Perm((2, 3, 1, 4, 5, 0)),
            Perm((3, 2, 1, 4, 6, 5, 0)),
            Perm((5, 7, 2, 4, 0, 6, 1, 3)),
            Perm((8, 0, 3, 5, 1, 7, 9, 2, 6, 4)),
        }
    ): True,
    frozenset(
        {
            Perm((4, 3, 2, 0, 1)),
            Perm((0, 1, 2, 3, 4)),
            Perm((5, 0, 4, 2, 1, 3)),
            Perm((4, 1, 2, 0, 3)),
            Perm((2, 1, 4, 5, 0, 3)),
            Perm((0, 5, 6, 2, 4, 7, 8, 3, 1)),
            Perm((6, 2, 0, 3, 1, 4, 5)),
        }
    ): True,
    frozenset(
        {
            Perm((1, 0, 4, 2, 5, 3)),
            Perm((0, 1, 2, 3, 4)),
            Perm((6, 2, 1, 3, 5, 4, 7, 0)),
            Perm((1, 3, 4, 0, 2)),
            Perm((5, 4, 3, 2, 0, 1)),
            Perm((1, 2, 0, 6, 4, 5, 3)),
            Perm((2, 1, 3, 5, 0, 4)),
            Perm((2, 3, 4, 0, 1)),
            Perm((1, 5, 4, 6, 3, 0, 2)),
            Perm((5, 0, 4, 2, 3, 6, 7, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((4, 3, 2, 0, 1)),
            Perm((0, 1, 4, 5, 6, 3, 2)),
            Perm((0, 4, 3, 1, 5, 2)),
            Perm((4, 1, 3, 2, 0)),
            Perm((7, 0, 6, 8, 5, 1, 2, 4, 3)),
            Perm((3, 1, 2, 0, 4)),
            Perm((1, 0, 2, 3, 4)),
            Perm((2, 4, 0, 3, 5, 1)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 1, 2, 3, 5, 4)),
            Perm((6, 8, 0, 3, 5, 7, 2, 1, 9, 4)),
            Perm((4, 3, 2, 1, 0)),
            Perm((1, 0, 5, 7, 3, 6, 2, 8, 9, 4)),
            Perm((2, 0, 1, 3, 4)),
            Perm((1, 8, 3, 7, 4, 5, 6, 2, 0, 9)),
            Perm((4, 0, 3, 1, 2, 5, 6)),
            Perm((2, 0, 1, 8, 7, 4, 6, 3, 5)),
            Perm((6, 4, 7, 5, 0, 2, 1, 3)),
        }
    ): True,
    frozenset(
        {
            Perm((0, 2, 4, 3, 1)),
            Perm((4, 3, 2, 1, 0)),
            Perm((2, 4, 5, 3, 0, 1)),
            Perm((3, 1, 2, 4, 0, 5)),
            Perm((2, 3, 4, 1, 0)),
            Perm((5, 4, 0, 6, 3, 7, 2, 1)),
            Perm((0, 1, 3, 2, 4)),
            Perm((4, 1, 3, 0, 5, 2)),
        }
    ): True,
    frozenset(
        {
            Perm((5, 2, 0, 4, 3, 7, 1, 6)),
            Perm((2, 8, 0, 7, 3, 6, 5, 1, 4)),
            Perm((0, 2, 3, 4, 1)),
            Perm((7, 4, 8, 3, 2, 5, 6, 1, 0)),
            Perm((3, 4, 0, 1, 2)),
            Perm((4, 3, 2, 5, 0, 1)),
            Perm((1, 0, 2, 5, 4, 3)),
            Perm((7, 6, 0, 8, 1, 4, 2, 3, 9, 5)),
        }
    ): False,
    frozenset(
        {
            Perm((2, 7, 3, 1, 0, 4, 5, 8, 9, 6)),
            Perm((3, 6, 2, 7, 0, 1, 4, 5)),
            Perm((2, 0, 3, 1, 4)),
            Perm((6, 2, 4, 5, 3, 1, 0)),
            Perm((4, 3, 0, 2, 5, 1)),
            Perm((5, 4, 0, 3, 1, 2)),
            Perm((2, 0, 4, 1, 3, 5)),
            Perm((9, 2, 0, 5, 7, 1, 6, 8, 3, 4)),
            Perm((5, 0, 3, 4, 2, 1)),
        }
    ): False,
    frozenset(
        {
            Perm((4, 1, 3, 5, 2, 6, 0)),
            Perm((4, 6, 5, 1, 0, 2, 3)),
            Perm((0, 1, 6, 2, 3, 8, 4, 5, 7)),
            Perm((1, 0, 3, 4, 6, 5, 2)),
            Perm((5, 1, 3, 4, 0, 2)),
            Perm((3, 4, 5, 7, 0, 8, 2, 1, 6)),
            Perm((0, 3, 6, 4, 1, 5, 2)),
            Perm((1, 2, 5, 4, 3, 0)),
            Perm((3, 5, 0, 7, 4, 6, 1, 2)),
            Perm((7, 2, 5, 3, 0, 6, 4, 8, 1)),
        }
    ): False,
    frozenset(
        {
            Perm((2, 0, 1, 6, 5, 3, 7, 4)),
            Perm((4, 3, 1, 2, 0)),
            Perm((0, 1, 7, 2, 8, 5, 3, 6, 4)),
            Perm((8, 0, 5, 6, 4, 1, 2, 7, 3)),
            Perm((9, 6, 0, 4, 2, 8, 7, 5, 3, 1)),
            Perm((2, 1, 0, 3, 4)),
            Perm((1, 5, 0, 3, 2, 6, 4)),
            Perm((4, 0, 6, 2, 5, 3, 1)),
        }
    ): False,
    frozenset(
        {
            Perm((5, 3, 4, 0, 1, 7, 6, 8, 9, 2)),
            Perm((0, 4, 2, 1, 3)),
            Perm((5, 7, 3, 4, 2, 6, 1, 0)),
            Perm((1, 4, 5, 2, 3, 0)),
            Perm((5, 4, 0, 1, 3, 2)),
            Perm((4, 1, 2, 3, 0, 6, 5, 7)),
        }
    ): False,
    frozenset(
        {
            Perm((1, 0, 4, 2, 3)),
            Perm((7, 9, 2, 1, 5, 8, 0, 3, 4, 6)),
            Perm((3, 2, 5, 1, 0, 4)),
            Perm((1, 0, 2, 6, 7, 4, 3, 5)),
            Perm((9, 2, 3, 6, 1, 7, 8, 4, 5, 0)),
            Perm((3, 2, 0, 6, 5, 1, 4)),
            Perm((2, 4, 1, 0, 3, 5)),
            Perm((3, 7, 4, 6, 8, 0, 2, 5, 1)),
            Perm((7, 1, 5, 6, 3, 0, 2, 4, 8)),
        }
    ): False,
    frozenset(
        {
            Perm((0, 4, 1, 3, 2)),
            Perm((5, 2, 3, 4, 6, 7, 0, 1)),
            Perm((3, 1, 2, 0, 4)),
            Perm((2, 0, 3, 4, 5, 1)),
            Perm((3, 0, 2, 1, 5, 4, 6)),
            Perm((0, 6, 3, 8, 1, 4, 2, 5, 7)),
        }
    ): False,
    frozenset(
        {
            Perm((1, 5, 4, 7, 0, 6, 2, 3)),
            Perm((1, 2, 0, 4, 3)),
            Perm((1, 3, 5, 4, 6, 0, 2)),
            Perm((6, 5, 7, 4, 0, 1, 2, 3, 9, 8)),
            Perm((6, 7, 5, 3, 1, 0, 4, 2)),
            Perm((3, 0, 2, 4, 1)),
            Perm((6, 1, 4, 7, 2, 3, 0, 5)),
            Perm((5, 3, 1, 2, 4, 0, 9, 7, 6, 8)),
            Perm((0, 1, 4, 3, 2)),
            Perm((1, 3, 0, 5, 4, 2)),
        }
    ): False,
    frozenset(
        {
            Perm((4, 0, 1, 2, 3)),
            Perm((4, 0, 1, 2, 5, 3)),
            Perm((5, 4, 1, 0, 2, 3)),
            Perm((5, 2, 0, 4, 3, 1)),
            Perm((5, 6, 3, 0, 7, 1, 2, 4)),
            Perm((6, 2, 4, 3, 0, 5, 7, 1, 8)),
            Perm((1, 3, 2, 0, 8, 5, 6, 7, 4)),
        }
    ): False,
    frozenset(
        {
            Perm((0, 1, 5, 6, 3, 2, 7, 4)),
            Perm((3, 7, 4, 8, 9, 5, 0, 2, 6, 1)),
            Perm((3, 5, 0, 7, 1, 4, 2, 6)),
            Perm((0, 1, 2, 4, 9, 6, 7, 5, 3, 8)),
            Perm((8, 4, 3, 6, 0, 2, 7, 1, 9, 5)),
            Perm((2, 6, 8, 1, 4, 3, 5, 0, 7)),
        }
    ): False,
    frozenset(
        {
            Perm((0, 1, 2, 3, 4)),
            Perm((4, 3, 1, 2, 0)),
            Perm((4, 1, 2, 0, 5, 3)),
            Perm((0, 4, 3, 5, 6, 1, 2, 7)),
            Perm((0, 1, 2, 4, 3)),
            Perm((6, 1, 2, 5, 4, 3, 0)),
            Perm((2, 8, 7, 4, 6, 0, 1, 3, 5)),
            Perm((3, 0, 2, 4, 5, 1)),
            Perm((0, 6, 3, 4, 2, 1, 5, 7)),
            Perm((1, 0, 2, 3, 4, 5)),
            Perm((3, 4, 2, 6, 1, 0, 8, 9, 7, 5)),
            Perm((8, 4, 2, 6, 3, 7, 5, 0, 1)),
            Perm((7, 3, 4, 1, 2, 5, 0, 6)),
            Perm((0, 8, 3, 7, 2, 1, 4, 5, 6)),
            Perm((1, 7, 2, 6, 3, 4, 0, 5)),
            Perm((6, 2, 0, 1, 3, 4, 5)),
            Perm((8, 3, 0, 5, 2, 1, 7, 4, 6)),
        }
    ): True,
    frozenset(
        {
            Perm((2, 4, 1, 3, 5, 0)),
            Perm((0, 4, 6, 8, 5, 1, 3, 7, 2)),
            Perm((6, 4, 2, 0, 5, 3, 1)),
            Perm((6, 0, 5, 2, 4, 1, 3)),
            Perm((0, 4, 2, 1, 3)),
            Perm((5, 0, 3, 1, 2, 4, 6)),
            Perm((3, 1, 4, 0, 2)),
            Perm((0, 4, 3, 1, 6, 7, 2, 8, 5)),
            Perm((4, 2, 0, 3, 1)),
            Perm((7, 6, 3, 0, 4, 1, 2, 5)),
            Perm((6, 3, 7, 4, 0, 8, 5, 9, 2, 1)),
            Perm((6, 0, 4, 2, 1, 3, 5)),
            Perm((7, 6, 0, 1, 4, 2, 5, 3)),
            Perm((7, 6, 8, 2, 4, 1, 3, 9, 5, 0)),
            Perm((2, 3, 5, 0, 4, 1)),
            Perm((5, 6, 0, 7, 4, 3, 1, 2, 8)),
            Perm((4, 3, 2, 5, 1, 0, 6, 7)),
        }
    ): False,
}


def test_is_polynomial():
    for k, v in expected.items():
        assert PolyPerm.is_polynomial(k) == v
        assert PolyPerm.is_non_polynomial(k) != v
