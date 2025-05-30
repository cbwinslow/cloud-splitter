# Cloud Splitter Setup Checklist

## Prerequisites

- [ ] Python 3.8 or higher installed
- [ ] FFmpeg installed and available in PATH
- [ ] Git installed (for development)
- [ ] GPU drivers installed (optional, for faster processing)
      - NVIDIA CUDA for NVIDIA GPUs
      - ROCm for AMD GPUs
      - Metal for Apple Silicon

## Installation Steps

1. Basic Installation:
   - [ ] Clone repository: `git clone https://github.com/cbwinslow/cloud-splitter.git`
   - [ ] Run quick start script: `./scripts/quick_start.sh`
   - [ ] Verify installation: `./scripts/verify_install.py`

2. Configuration:
   - [ ] Check config file at `~/.config/cloud-splitter/config.toml`
   - [ ] Set appropriate download directory
   - [ ] Set appropriate output directory
   - [ ] Configure GPU/CPU preferences
   - [ ] Verify stem separator options

3. System Setup:
   - [ ] FFmpeg accessible from command line
   - [ ] Write permissions in output directory
   - [ ] Sufficient disk space for downloads
   - [ ] GPU properly recognized (if using)

## Testing the Installation

1. Basic Functionality:
   - [ ] Launch application: `cloud-splitter`
   - [ ] TUI interface loads properly
   - [ ] Configuration view accessible
   - [ ] Status view accessible

2. Download Test:
   - [ ] Add test URL to queue
   - [ ] Verify download starts
   - [ ] Check download directory
   - [ ] Verify file quality

3. Processing Test:
   - [ ] Process downloaded file
   - [ ] Check stem separation
   - [ ] Verify output files
   - [ ] Test different stem types

## Common Issues

1. FFmpeg Issues:
   - [ ] Check FFmpeg installation: `ffmpeg -version`
   - [ ] Verify PATH includes FFmpeg
   - [ ] Test basic FFmpeg functionality

2. GPU Issues:
   - [ ] Check GPU recognition: `nvidia-smi` or `rocm-smi`
   - [ ] Verify PyTorch GPU support
   - [ ] Test GPU processing

3. Permission Issues:
   - [ ] Check directory permissions
   - [ ] Verify user rights
   - [ ] Test file creation/deletion

## Development Setup (Optional)

1. Development Environment:
   - [ ] Install dev dependencies: `pip install -e ".[dev]"`
   - [ ] Run tests: `pytest`
   - [ ] Check code formatting: `black src tests`
   - [ ] Verify type hints: `mypy src`

2. Documentation:
   - [ ] Read usage guide: `docs/usage.md`
   - [ ] Check examples: `examples/`
   - [ ] Review development guide: `docs/development.md`

## Next Steps

After completing the checklist:

1. Try the examples:
   ```bash
   cd examples
   ./basic_usage.py
   ./batch_processing.py example_urls.txt
   ```

2. Customize your setup:
   - Edit configuration file
   - Set up custom stem labels
   - Configure processing options

3. Start using the application:
   ```bash
   cloud-splitter
   ```

If you encounter any issues, check:
- Application logs: `~/.config/cloud-splitter/logs/`
- GitHub issues
- Documentation in `docs/`
