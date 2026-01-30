# Contributing to GNC Autonomous System

Thank you for considering contributing to this project! This guide will help you get started.

## Code of Conduct

Be respectful, professional, and constructive in all interactions.

## How to Contribute

### Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and dependencies
- Relevant code snippets or error messages

### Suggesting Enhancements

Enhancement suggestions should include:
- Clear use case
- Expected behavior
- Potential implementation approach
- References to relevant standards or papers

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest tests/`
6. Update documentation as needed
7. Commit with clear messages: `git commit -m 'Add feature X'`
8. Push to your fork: `git push origin feature/your-feature`
9. Submit a pull request

## Development Guidelines

### Code Style

Follow PEP 8 style guidelines:
```bash
pip install flake8
flake8 src/
```

### Documentation

- Add docstrings to all functions and classes
- Follow Google or NumPy docstring format
- Update README.md for major changes
- Add examples for new features

### Testing

- Write unit tests for new functions
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use pytest fixtures for common setups

Example test structure:
```python
def test_gnc_system_initialization():
    """Test GNC system initializes correctly"""
    gnc = GNCSystem()
    assert gnc.mode == GNCMode.SAFE
    assert gnc.authority == ControlAuthority.GROUND
```

### Requirements Traceability

When adding features:
1. Identify relevant requirements from requirements.py
2. Document which requirements are satisfied
3. Add verification tests
4. Update requirements compliance checks

## Project Structure

```
gnc-autonomous-system/
├── src/                    # Source code
│   ├── functional_analysis/  # MBSE and requirements
│   ├── system_architecture/  # GNC components
│   ├── navigation/           # State estimation
│   ├── guidance/             # Trajectory planning
│   └── control/              # Control algorithms
├── tests/                  # Test suite
├── examples/               # Usage examples
├── docs/                   # Documentation
└── data/                   # Test data and parameters
```

## Standards Compliance

When contributing, ensure compliance with:
- ECSS standards (referenced in docs)
- Requirements defined in requirements.py
- Safety guidelines from the thesis

## References

Before contributing, familiarize yourself with:
- Thesis Chapters 4 & 5 (source material)
- ECSS-E-ST-60-30C (GNC standard)
- Hayabusa2 and OSIRIS-REx mission papers

## Questions?

Open an issue for:
- Clarification on requirements
- Design decisions
- Implementation approaches
- Testing strategies

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
