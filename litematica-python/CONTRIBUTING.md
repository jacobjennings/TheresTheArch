# Contributing to Litematica Python

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/TheresTheArch.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`

## Development Setup

```bash
cd litematica-python
pip install -r requirements.txt
python test_basic.py  # Run tests
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public methods and classes
- Keep line length under 100 characters where reasonable

### Example

```python
def my_function(param: str, optional: Optional[int] = None) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param: Description of param
        optional: Description of optional parameter
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When something goes wrong
    """
    pass
```

## Testing

Before submitting a pull request:

1. Run the basic tests: `python test_basic.py`
2. Test your changes with actual .litematic files
3. Verify compatibility with Litematica mod

### Adding Tests

If you add new features, please add corresponding tests to `test_basic.py` or create new test files.

## Documentation

- Update README.md if you add new features
- Add examples to EXAMPLES.md for complex features
- Update API_REFERENCE.md for API changes
- Keep FORMAT.md current if file format interpretation changes

## Pull Request Process

1. Update documentation as needed
2. Run tests and ensure they pass
3. Update CHANGELOG.md (if it exists) with your changes
4. Submit pull request with clear description of changes
5. Link any related issues

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

## Areas for Contribution

### High Priority

- Additional tests and test coverage
- Performance optimization for large schematics
- Support for more Minecraft versions
- Better error handling and validation

### Medium Priority

- Command-line tools for common operations
- Conversion utilities (Schematica ↔ Litematica)
- Preview image generation
- Compression optimization

### Nice to Have

- GUI tools
- Integration with other libraries
- Advanced region manipulation
- Schematic comparison tools

## Bug Reports

When filing a bug report, please include:

1. Python version
2. Library version
3. Operating system
4. Minimal code to reproduce
5. Expected vs actual behavior
6. Any error messages or stack traces
7. Example .litematic file if relevant (if possible)

### Bug Report Template

```markdown
**Python Version:** 3.10
**OS:** Ubuntu 22.04
**Library Version:** 1.0.0

**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Load schematic
2. Call method X
3. Error occurs

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Error Message:**
```
Paste error here
```

**Additional Context:**
Any other relevant information
```

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists
2. Check existing issues/PRs for similar requests
3. Describe the use case
4. Provide examples if possible
5. Consider contributing the feature yourself!

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

## Questions?

- Open an issue for questions
- Check existing documentation first
- Be specific and provide context

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file (if created)
- Release notes
- README.md acknowledgments section

## Getting Help

If you need help with contributing:
1. Read the documentation (README.md, EXAMPLES.md, etc.)
2. Look at existing code for patterns
3. Check closed issues and PRs
4. Open an issue asking for guidance

Thank you for contributing! 🎉

