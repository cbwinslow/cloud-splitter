#!/bin/bash
set -e

# Activate virtual environment
source venv/bin/activate

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build package
python -m build

echo "Package built successfully in dist/"
