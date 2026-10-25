# Day 007 Greeting Example

A tiny Python command-line program that prints a friendly greeting, with no third-party dependencies.

## Overview

This sample shows how a project's README can help a new reader understand the purpose, start quickly, see expected output, run tests, and find help. The greeting is intentionally small so the exercise can focus on documentation quality rather than setup complexity.

## Getting started

**Requirements:** Python 3.9 or newer. No packages need to be installed.

From the repository root, run:

```bash
python3 007/examples/greeting/hello.py
```

## Usage

Pass a display name with `--name`:

```bash
python3 007/examples/greeting/hello.py --name John
```

Expected output:

```text
Hello, John!
```

When omitted, the name defaults to `world`. A blank or whitespace-only name is rejected with a clear command-line error.

## Testing

From the repository root, run the Day 007 tests:

```bash
python3 -B -m unittest discover -s 007/tests -p 'test_*.py' -v
```

The tests check the README auditor and the sample greeting behavior. A successful run ends with `OK`.

## Help / Support

For context, read the [Day 007 README-writing guide](../../README.md) or the [README template](../../README_TEMPLATE.md). The program is part of a learning exercise rather than a separately supported application; report reproducible problems through the repository's established issue or discussion channel if one is configured.

## Limitations

- This is a command-line example, not a web service or installed Python package.
- It does not persist names or greetings.
- The README audit checks a few structural signals only; it does not verify every factual claim, run commands inside arbitrary documentation, or replace human review.
