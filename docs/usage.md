# Cloud Splitter Usage Guide

## Installation

1. Install the package:
```bash
pip install cloud-splitter
```

2. Install system dependencies:
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# For macOS
brew install ffmpeg

# For Windows
# Download and install FFmpeg from https://ffmpeg.org/download.html
```

## Basic Usage

1. Launch the TUI:
```bash
cloud-splitter
```

2. Direct processing from command line:
```bash
cloud-splitter process URL [URL...]
```

## Configuration

The default configuration file is located at:
- Linux/Mac: `~/.config/cloud-splitter/config.toml`
- Windows: `%APPDATA%\cloud-splitter\config.toml`

### Example Configuration

```toml
[paths]
download_dir = "~/Downloads/cloud-splitter"
output_dir = "~/Music/stems"

[download]
format = "bestaudio/best"
keep_original = true
```

## Features

### Download Options
- Highest quality audio/video download
- Batch processing support
- Custom output directory
- Original file retention control

### Stem Separation
- Multiple separator support (demucs/spleeter)
- Custom stem labeling
- GPU acceleration (when available)
- Quality control options

### TUI Features
- Interactive URL input
- Real-time progress monitoring
- Configuration management
- Processing status view

## Troubleshooting

1. FFmpeg not found:
   - Ensure FFmpeg is installed and in your system PATH

2. GPU not detected:
   - Check GPU drivers are installed
   - Verify CUDA/ROCm installation
   - Try CPU-only mode in configuration

3. Permission errors:
   - Check output directory permissions
   - Run with appropriate user permissions

## Support

For issues and feature requests, please visit:
https://github.com/cbwinslow/cloud-splitter/issues
