# Cloud Splitter

A powerful TUI-based tool for downloading and processing audio stems from videos using yt-dlp and demucs/spleeter.

## Features

- Download videos/audio in highest quality using yt-dlp
- Process audio through multiple stem separators (demucs, spleeter)
- Interactive TUI interface for easy management
- Batch processing support
- Flexible configuration options
- Intelligent file naming and organization

## Requirements

- Python 3.8+
- FFmpeg
- ROCm (for AMD GPUs) or CUDA (for NVIDIA GPUs)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cloud-splitter.git
cd cloud-splitter
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install the package and dependencies:
```bash
pip install -e .
```

For development installation:
```bash
pip install -e ".[dev]"
```

## Usage

1. Launch the TUI:
```bash
cloud-splitter tui
```

2. Direct processing from command line:
```bash
cloud-splitter process URL [URL...]
```

## Configuration

Configuration can be managed through the TUI or by editing the config file at:
- Linux/Mac: `~/.config/cloud-splitter/config.toml`
- Windows: `%APPDATA%\cloud-splitter\config.toml`

### Default Configuration

```toml
[paths]
download_dir = "~/Downloads/cloud-splitter"
output_dir = "~/Music/stems"

[download]
format = "bestaudio/best"
keep_original = true
batch_enabled = true

[processing]
separator = "demucs"
stems = ["vocals", "drums", "bass", "other"]
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black src tests
```

4. Type checking:
```bash
mypy src
```

## License

MIT License
