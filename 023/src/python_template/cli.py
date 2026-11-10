"""Command-line interface for the starter package."""

import argparse

from .core import greet


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.add_argument("--name", default="world", help="name to greet")
    args = parser.parse_args()
    try:
        print(greet(args.name))
    except (TypeError, ValueError) as error:
        parser.error(str(error))
