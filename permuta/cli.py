import argparse
import signal
import sys
import types

from permuta import Av, Basis
from permuta.permutils import InsertionEncodablePerms, PolyPerms, lex_min


def sigint_handler(sig: int, _frame: types.FrameType) -> None:
    """For terminating infinite task."""
    if sig == signal.SIGINT:
        print("\nExiting.")
        sys.exit(0)


def enumerate_class(args: argparse.Namespace) -> None:
    """Enumerate a perm class indefinitely, one length at a time."""
    signal.signal(signal.SIGINT, sigint_handler)
    perm_class = Av.from_string(args.basis)
    print(f"Enumerating {perm_class}. Press Ctrl+C to exit.")
    n = 0
    while True:
        print(perm_class.count(n), end=", ", flush=True)
        n += 1


def has_regular_insertion_encoding(args: argparse.Namespace) -> None:
    """Check if a perm class has a regular insertion encoding."""
    basis = Basis.from_string(args.basis)
    perm_class = Av(basis)
    if InsertionEncodablePerms.is_insertion_encodable_maximum(basis):
        print(f"The class {perm_class} has a regular topmost insertion encoding")
    if InsertionEncodablePerms.is_insertion_encodable_rightmost(basis):
        print(f"The class {perm_class} has a regular rightmost insertion encoding")
    if not InsertionEncodablePerms.is_insertion_encodable(basis):
        print(f"{perm_class} does not have a regular insertion encoding")


def get_lex_min(args: argparse.Namespace) -> None:
    """Prints the 0-based lexicographically minimal representation of the basis."""
    basis = Basis.from_string(args.basis)
    print("_".join(str(perm) for perm in lex_min(basis)))


def has_poly_growth(args: argparse.Namespace) -> None:
    """Prints whether perm class from basis has polynomial growth."""
    basis = Basis.from_string(args.basis)
    poly = PolyPerms.is_polynomial(basis)
    print(f"Av({basis}) is {'' if poly else 'not '}polynomial")


def get_parser() -> argparse.ArgumentParser:
    """Construct and return parser."""
    basis_str: str = (
        "The basis as a string where the permutations are separated any token, "
        "(e.g. '231_4321', '0132:43210')"
    )

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="A set of tools to work with permutations"
    )
    subparsers = parser.add_subparsers(title="subcommands")

    # The count command
    count_parser: argparse.ArgumentParser = subparsers.add_parser(
        "count",
        description="A tool to quickly get the enumeration of permutation classes",
    )
    count_parser.set_defaults(func=enumerate_class)
    count_parser.add_argument("basis", help=basis_str)

    # The insenc command
    insenc_parser: argparse.ArgumentParser = subparsers.add_parser(
        "insenc",
        description="A tool to check if a permutation class has a regular insertion"
        " encoding.",
    )
    insenc_parser.set_defaults(func=has_regular_insertion_encoding)
    insenc_parser.add_argument("basis", help=basis_str)

    # The lexmin command
    lexmin_parser: argparse.ArgumentParser = subparsers.add_parser(
        "lexmin",
        description="A tool that returns the 0-based lexicographically minimal "
        "representation of the basis.",
    )
    lexmin_parser.set_defaults(func=get_lex_min)
    lexmin_parser.add_argument("basis", help=basis_str)

    # The poly command
    poly_parser: argparse.ArgumentParser = subparsers.add_parser(
        "poly",
        description="A tool to check if permutation class has polynomial growth.",
    )
    poly_parser.set_defaults(func=has_poly_growth)
    poly_parser.add_argument("basis", help=basis_str)

    return parser


def main() -> None:
    """Entry point."""
    parser = get_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.error("Invalid command")
    args.func(args)


if __name__ == "__main__":
    main()
