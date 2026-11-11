"""Command-line runner for the ML starter pipeline."""

import argparse
import json
from pathlib import Path

from ml_template.pipeline import train_and_evaluate


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the ML template example")
    parser.add_argument("--config", type=Path, default=Path("configs/default.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("models"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    metrics = train_and_evaluate(config, args.output_dir)
    print(json.dumps(metrics, indent=2))
