#!/bin/bash
set -e

# Activate virtual environment
source venv/bin/activate

# Format code with black
black src tests

# Run flake8
flake8 src tests

# Run mypy
mypy src
