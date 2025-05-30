# Contributing to Cloud Splitter

Thank you for your interest in contributing to Cloud Splitter! This document provides guidelines and information about contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/cloud-splitter.git
   cd cloud-splitter
   ```

3. Set up development environment:
   ```bash
   ./scripts/setup_dev.sh
   ```

## Development Workflow

1. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes:
   - Follow code style guidelines
   - Add tests for new features
   - Update documentation

3. Run tests:
   ```bash
   pytest
   ```

4. Format code:
   ```bash
   black src tests
   ```

5. Run type checking:
   ```bash
   mypy src
   ```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused and simple
- Comment complex logic

## Testing

- Write tests for new features
- Maintain test coverage
- Use pytest fixtures
- Mock external services

## Documentation

- Update README.md for significant changes
- Add docstrings to new functions/classes
- Update usage documentation
- Include examples for new features

## Pull Request Process

1. Update CHANGELOG.md
2. Ensure tests pass
3. Update documentation
4. Submit pull request
5. Address review comments

## Reporting Issues

- Use issue templates
- Include system information
- Provide clear reproduction steps
- Include relevant logs

## Feature Requests

- Explain the use case
- Describe expected behavior
- Consider alternatives
- Discuss implementation details

## Code of Conduct

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
