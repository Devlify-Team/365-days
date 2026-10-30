"""Print the interpreter and locked pandas version without loading data."""

from importlib.metadata import version
import platform
import sys


def runtime_report():
    """Return a small, deterministic report of selected runtime versions."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "pandas": version("pandas"),
    }


def main():
    info = runtime_report()
    print(f"Python {info['python']} ({info['implementation']})")
    print(f"pandas {info['pandas']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
