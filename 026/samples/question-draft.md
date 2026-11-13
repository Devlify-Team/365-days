# Why does the test pass locally but fail in CI?

## Goal

I want the same test suite to pass on my laptop and in the repository's continuous-integration workflow.

## Context

The project uses Python 3.12. The workflow installs the test dependencies from the checked-in project configuration and runs `python -m pytest` on Ubuntu.

## What I tried

I reran the failing test locally and checked that the workflow uses the expected Python version. The failure only appears in the CI log so far.

## Question

What environment details or log sections should I compare next to narrow down the difference?
