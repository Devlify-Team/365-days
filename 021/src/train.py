"""Fit a one-feature least-squares line from a tiny CSV and write JSON."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "toy-training.csv"
OUTPUT = ROOT / "models" / "model.json"


def fit_line(rows):
    if len(rows) < 2:
        raise ValueError("at least two rows are required")
    xs = [row["x"] for row in rows]
    ys = [row["y"] for row in rows]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    if denominator == 0:
        raise ValueError("x values must not all be equal")
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator
    intercept = y_mean - slope * x_mean
    return {"slope": slope, "intercept": intercept}


def main():
    with INPUT.open(newline="", encoding="utf-8") as source:
        rows = [{key: float(value) for key, value in row.items()} for row in csv.DictReader(source)]
    model = fit_line(rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {model}")


if __name__ == "__main__":
    main()
