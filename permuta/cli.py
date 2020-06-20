import argparse
import signal
import sys

from permuta import Av, Perm


def signal_handler(sig, frame):
    print()
    print("Exiting.")
    sys.exit(0)


def enumerate_class(args):
    basis = []
    for perm_str in args.basis.split("_"):
        perm_tuple = tuple(map(int, perm_str))
        if 0 not in perm_tuple:
            perm_tuple = tuple(i - 1 for i in perm_tuple)
        perm = Perm(perm_tuple, check=True)
        basis.append(perm)
    perm_class = Av(basis)
    n = 0
    print(f"Enumerating {perm_class}. Press Ctrl+C to exit.")
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        num = len(list(perm_class.of_length(n)))
        print(f"{num}, ", end="", flush=True)
        n += 1


parser = argparse.ArgumentParser(description="A set of tools to work with permutations")
subparsers = parser.add_subparsers(title="subcommands")


# The count command
count_parser = subparsers.add_parser(
    "count", description="A tool to quickly get the enumeration of permutation classes"
)
count_parser.set_defaults(func=enumerate_class)
count_parser.add_argument(
    "basis",
    help="The basis as a string where the permutations are separated by '_' "
    "(e.g. '231_4321')",
)


def main():
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.error("Invalid command")
    args.func(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
