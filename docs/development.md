# Cloud Splitter Development Guide

## Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/cbwinslow/cloud-splitter.git
cd cloud-splitter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Project Structure

```
cloud-splitter/
├── src/
│   └── cloud_splitter/
│       ├── core/           # Core processing logic
│       ├── tui/            # TUI components
│       ├── utils/          # Utility functions
│       └── cli.py          # Command-line interface
├── tests/                  # Test suite
├── config/                 # Default configurations
└── docs/                   # Documentation
```

## Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and run tests:
```bash
pytest
```

3. Format code:
```bash
black src tests
```

4. Run type checking:
```bash
mypy src
```

## Testing

- Run full test suite:
```bash
pytest
```

- Run with coverage:
```bash
pytest --cov=cloud_splitter
```

- Run specific test:
```bash
pytest tests/test_specific.py
```

## Adding New Features

1. Core Components:
   - Add new processor in `core/`
   - Update factory if needed
   - Add configuration options

2. TUI Components:
   - Add new views in `tui/`
   - Update app.py for integration
   - Add CSS styling

3. Utils:
   - Add utility functions in `utils/`
   - Update validation if needed

## Documentation

- Update usage.md for user-facing changes
- Update development.md for developer changes
- Add docstrings to new functions/classes
- Update README.md for significant changes

## Release Process

1. Update version:
   - Update version in setup.py
   - Update CHANGELOG.md

2. Run checks:
   - Run full test suite
   - Check documentation
   - Verify examples

3. Create release:
   - Tag version
   - Create GitHub release
   - Upload to PyPI

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused
- Add tests for new features

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit pull request

## Resources

- [Textual Documentation](https://textual.textualize.io/)
- [Demucs Documentation](https://github.com/facebookresearch/demucs)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
