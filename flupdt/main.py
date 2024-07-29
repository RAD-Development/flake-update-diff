#!/usr/bin/env python3

from flupdt.flake_show import get_derivations
from flupdt.cli import parse_inputs


def main():
    args = parse_inputs()
    print(get_derivations(args.flake_path))


if __name__ == "__main__":
    main()
