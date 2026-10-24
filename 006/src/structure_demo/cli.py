"""A tiny dependency-free example of code under src/."""

import argparse


def greet(name="world"):
    """Return a friendly greeting; reject names containing only whitespace."""
    name = name.strip()
    if not name:
        raise ValueError("Name must not be blank")
    return f"Hello, {name}!"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="world", help="Who to greet")
    args = parser.parse_args(argv)
    try:
        message = greet(args.name)
    except ValueError as error:
        parser.error(str(error))
    print(message)
    return 0
