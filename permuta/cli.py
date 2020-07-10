import argparse
import signal
import sys

from permuta import Av, Perm
from permuta.perm_utils import InsertionEncodablePerms, lex_min


def signal_handler(sig, frame):
    print()
    print("Exiting.")
    sys.exit(0)


def parse_basis(args):
    basis = []
    for perm_str in args.basis.split("_"):
        perm_tuple = tuple(map(int, perm_str))
        if 0 not in perm_tuple:
            perm_tuple = tuple(i - 1 for i in perm_tuple)
        perm = Perm.from_iterable_validated(perm_tuple)
        basis.append(perm)
    return basis


def enumerate_class(args):
    basis = parse_basis(args)
    perm_class = Av(basis)
    n = 0
    print(f"Enumerating {perm_class}. Press Ctrl+C to exit.")
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        num = len(list(perm_class.of_length(n)))
        print(f"{num}, ", end="", flush=True)
        n += 1


def has_regular_insertion_encoding(args):
    basis = parse_basis(args)
    perm_class = Av(basis)
    if InsertionEncodablePerms.is_insertion_encodable_maximum(basis):
        print(f"The class {perm_class} has a regular topmost insertion encoding")
    if InsertionEncodablePerms.is_insertion_encodable_rightmost(basis):
        print(f"The class {perm_class} has a regular rightmost insertion encoding")
    if not InsertionEncodablePerms.is_insertion_encodable(basis):
        print(f"{perm_class} does not have a regular insertion encoding")


def get_lex_min(args):
    basis = parse_basis(args)
    print("_".join(str(p) for p in lex_min(basis)))


basis_str = (
    "The basis as a string where the permutations are separated by '_'"
    " (e.g. '231_4321')"
)

parser = argparse.ArgumentParser(description="A set of tools to work with permutations")
subparsers = parser.add_subparsers(title="subcommands")


# The count command
count_parser = subparsers.add_parser(
    "count", description="A tool to quickly get the enumeration of permutation classes"
)
count_parser.set_defaults(func=enumerate_class)
count_parser.add_argument(
    "basis", help=basis_str,
)

# The insenc command
insenc_parser = subparsers.add_parser(
    "insenc",
    description="A tool to check if a permutation class has a regular insertion"
    " encoding.",
)
insenc_parser.set_defaults(func=has_regular_insertion_encoding)
insenc_parser.add_argument(
    "basis", help=basis_str,
)

# The lexmin command
lexmin_parser = subparsers.add_parser(
    "lexmin",
    description="A tool that returns the 0-based lexicographically minimal "
    "representation of the basis.",
)
lexmin_parser.set_defaults(func=get_lex_min)
lexmin_parser.add_argument(
    "basis", help=basis_str,
)


def main():
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.error("Invalid command")
    args.func(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
