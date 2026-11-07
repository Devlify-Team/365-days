"""Small, deterministic summary statistics for numeric readings."""

import math


def summarize(values):
    """Return count, minimum, maximum and mean for finite numeric values."""
    readings = list(values)
    if not readings:
        raise ValueError("at least one reading is required")

    for value in readings:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("readings must be integers or floats")
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            raise ValueError("readings must be finite")

    try:
        mean = math.fsum(readings) / len(readings)
    except OverflowError as error:
        raise ValueError("mean is outside the supported numeric range") from error

    return {
        "count": len(readings),
        "minimum": min(readings),
        "maximum": max(readings),
        "mean": mean,
    }
