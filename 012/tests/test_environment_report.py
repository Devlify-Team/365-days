"""Tests for environment reporting; no data is loaded or generated."""

import importlib.metadata
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from environment_report import runtime_report


def test_report_lists_python_and_the_locked_pandas_distribution():
    report = runtime_report()
    assert report == {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "pandas": importlib.metadata.version("pandas"),
    }


def test_cli_reports_runtime_versions():
    project_root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, str(project_root / "environment_report.py")],
        cwd=project_root,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Python " in completed.stdout
    assert "pandas " in completed.stdout
    assert completed.stderr == ""
