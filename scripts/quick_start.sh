#!/bin/bash
set -e

echo "Cloud Splitter Quick Start Setup"
echo "==============================="

# Check Python
echo -n "Checking Python version... "
if command -v python3 >/dev/null 2>&1; then
    python3 --version
else
    echo "Python 3 not found!"
    exit 1
fi

# Create virtual environment
echo -n "Creating virtual environment... "
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "done"
else
    echo "already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install package
echo "Installing Cloud Splitter..."
pip install -e .

# Check FFmpeg
echo -n "Checking FFmpeg... "
if command -v ffmpeg >/dev/null 2>&1; then
    echo "found"
else
    echo "not found"
    echo "Please install FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    exit 1
fi

# Create config directory
echo "Setting up configuration..."
mkdir -p ~/.config/cloud-splitter
if [ ! -f ~/.config/cloud-splitter/config.toml ]; then
    cp config/default.toml ~/.config/cloud-splitter/config.toml
fi

# Run verification
echo "Verifying installation..."
python scripts/verify_install.py

echo ""
echo "Quick Start Guide:"
echo "1. Edit configuration (optional):"
echo "   ~/.config/cloud-splitter/config.toml"
echo ""
echo "2. Start the application:"
echo "   cloud-splitter"
echo ""
echo "3. Try the examples:"
echo "   cd examples"
echo "   ./basic_usage.py"
echo ""
echo "For more information, see:"
echo "  docs/usage.md"
