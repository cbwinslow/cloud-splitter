# Cloud Splitter Examples

This directory contains example scripts demonstrating different ways to use Cloud Splitter.

## Basic Usage

The `basic_usage.py` script shows how to use Cloud Splitter programmatically for simple tasks:

```bash
./basic_usage.py
```

## Batch Processing

The `batch_processing.py` script demonstrates how to process multiple URLs from a file:

```bash
./batch_processing.py example_urls.txt
```

### URL File Format

The URL file should contain one URL per line. Lines starting with `#` are treated as comments:

```text
# Comments start with #
https://www.youtube.com/watch?v=example1
https://www.youtube.com/watch?v=example2
```

## Configuration

These examples use the default configuration. To use a custom configuration:

1. Copy the default config:
```bash
cp ~/.config/cloud-splitter/config.toml myconfig.toml
```

2. Edit the configuration:
```bash
vim myconfig.toml
```

3. Set the config path in your script:
```python
config = ConfigLoader.load_config(Path("myconfig.toml"))
```

## Error Handling

The examples include basic error handling and logging. Logs are written to:
- `~/.config/cloud-splitter/logs/cloud-splitter.log`

## Requirements

- Python 3.8+
- FFmpeg
- cloud-splitter package installed
