#!/bin/bash
set -e

# Activate virtual environment
source venv/bin/activate

# Run tests with coverage
pytest --cov=cloud_splitter --cov-report=term-missing --cov-report=html

echo "Test results and coverage report generated in htmlcov/index.html"
