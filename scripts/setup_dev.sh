#!/bin/bash
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .

# Create necessary directories
mkdir -p ~/.config/cloud-splitter
mkdir -p downloads
mkdir -p output

# Copy default config if it doesn't exist
if [ ! -f ~/.config/cloud-splitter/config.toml ]; then
    cp config/default.toml ~/.config/cloud-splitter/config.toml
fi

echo "Development environment setup complete!"
