#!/usr/bin/env python3
"""Print a friendly greeting without installing any packages."""

import argparse


def greet(name="world"):
    """Return a greeting for a non-empty display name."""
    name = name.strip()
    if not name:
        raise ValueError("Name must not be blank")
    return f"Hello, {name}!"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="world", help="Person to greet (default: world)")
    args = parser.parse_args(argv)
    try:
        result = greet(args.name)
    except ValueError as error:
        parser.error(str(error))
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
