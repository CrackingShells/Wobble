# Contributing Guidelines

This article covers:
- Development workflow and contribution process
- Code standards and quality requirements
- Testing and validation procedures

## Development Workflow

### Getting Started

**Prerequisites**:
- Python 3.7+ installed
- Git configured with your credentials
- Virtual environment tool (venv, conda, etc.)

**Setup Development Environment**:

```bash
# Clone the repository
git clone https://github.com/CrackingShells/Wobble.git
cd Wobble

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt  # If exists

# Verify installation
python -c "import wobble; print('Development setup complete')"
wobble --help
```

### Branch Management

**Branch Naming Convention**:
- `feat/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation changes
- `refactor/component-name` - Code refactoring
- `test/test-improvement` - Test additions or improvements

**Workflow**:
```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feat/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add new feature description"

# Push and create pull request
git push origin feat/your-feature-name
```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions or improvements
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Examples**:
```bash
feat: add JSON output format support
fix: resolve test discovery issue with Windows paths
docs: update CLI reference with new options
refactor: simplify discovery engine logic
test: add comprehensive decorator tests
```

## Code Standards

### Python Code Style

**PEP 8 Compliance**:
- Line length: 88 characters (Black formatter standard)
- Indentation: 4 spaces
- Import organization: isort standard
- Docstring format: Google style

**Type Hints**:
```python
from typing import List, Dict, Optional, Union

def discover_tests(self, 
                  pattern: str = "test*.py",
                  categories: Optional[List[str]] = None) -> Dict[str, List]:
    """Discover tests with optional filtering.
    
    Args:
        pattern: File pattern for test discovery
        categories: Test categories to include
        
    Returns:
        Dictionary mapping categories to test lists
    """
    pass
```

**Docstring Standards**:
```python
def integration_test(scope: str = "component") -> Callable:
    """Mark test as integration test with scope specification.
    
    Integration tests validate interactions between components or systems.
    The scope parameter specifies the level of integration being tested.
    
    Args:
        scope: The scope of integration testing
               - "component": Tests interaction between internal components
               - "service": Tests interaction with external services
               - "system": Tests end-to-end system integration
               
    Returns:
        Decorator function that marks tests as integration tests
        
    Example:
        @integration_test(scope="service")
        def test_api_integration(self):
            response = api_client.get("/health")
            self.assertEqual(response.status_code, 200)
    """
    pass
```

### Code Organization

**Module Structure**:
- Keep modules focused on single responsibility
- Use clear, descriptive names
- Maintain consistent import patterns
- Group related functionality

**Import Organization**:
```python
# Standard library imports
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Third-party imports
import colorama

# Local imports
from .decorators import get_test_metadata
from .output import OutputFormatter
```

### Error Handling

**Exception Handling**:
```python
def discover_tests(self, directory: Path) -> None:
    """Discover tests with proper error handling."""
    try:
        loader = unittest.TestLoader()
        suite = loader.discover(str(directory), pattern=pattern)
        # Process suite
    except ImportError as e:
        print(f"Warning: Could not import tests from {directory}: {e}")
    except Exception as e:
        print(f"Error: Unexpected error during discovery: {e}")
        raise
```

**Logging and Output**:
- Use print() for user-facing messages
- Include context in error messages
- Provide actionable error information
- Use appropriate verbosity levels

## Testing Requirements

### Test Coverage

**Minimum Requirements**:
- All new features must include tests
- Bug fixes must include regression tests
- Test coverage should not decrease
- Critical paths must have comprehensive tests

**Test Categories**:
```python
# Use wobble's own decorators for self-testing
from wobble import regression_test, integration_test, development_test

class TestNewFeature(unittest.TestCase):
    
    @regression_test
    def test_core_functionality(self):
        """Test that must never break."""
        pass
    
    @integration_test(scope="component")
    def test_component_interaction(self):
        """Test component interactions."""
        pass
    
    @development_test(phase="feature-validation")
    def test_new_feature_behavior(self):
        """Temporary test for new feature."""
        pass
```

### Test Execution

**Local Testing**:
```bash
# Run all tests
wobble --verbose

# Run specific categories
wobble --category regression
wobble --category integration

# Run with coverage (if coverage tool available)
coverage run -m wobble.cli
coverage report
```

**Pre-commit Validation**:
```bash
# Comprehensive test suite
wobble --verbose

# Check for import issues
python -c "import wobble; print('All imports successful')"

# Validate CLI functionality
wobble --help
wobble --discover-only
```

### Test Quality Standards

**Test Naming**:
```python
def test_discovery_engine_finds_hierarchical_tests(self):
    """Test names should be descriptive and specific."""
    pass

def test_decorator_preserves_function_metadata(self):
    """Include expected behavior in test name."""
    pass
```

**Test Structure**:
```python
def test_feature_behavior(self):
    """Follow Arrange-Act-Assert pattern."""
    # Arrange
    test_data = create_test_data()
    expected_result = "expected_value"
    
    # Act
    actual_result = feature_function(test_data)
    
    # Assert
    self.assertEqual(actual_result, expected_result)
```

## Pull Request Process

### Before Submitting

**Code Quality Checklist**:
- [ ] Code follows PEP 8 standards
- [ ] All functions have docstrings
- [ ] Type hints added where appropriate
- [ ] Error handling implemented
- [ ] Tests added for new functionality
- [ ] All tests pass locally

**Documentation Checklist**:
- [ ] User-facing changes documented
- [ ] API changes documented
- [ ] Examples updated if needed
- [ ] README updated if needed

### Pull Request Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

**Review Criteria**:
- Code quality and style compliance
- Test coverage and quality
- Documentation completeness
- Backward compatibility
- Performance impact

**Review Timeline**:
- Initial review within 2 business days
- Follow-up reviews within 1 business day
- Approval required from at least one maintainer

## Development Guidelines

### Adding New Features

**Feature Development Process**:
1. Create issue describing feature and requirements
2. Discuss design approach with maintainers
3. Create feature branch and implement
4. Add comprehensive tests
5. Update documentation
6. Submit pull request

**Design Considerations**:
- Maintain backward compatibility
- Follow existing architectural patterns
- Consider performance impact
- Ensure cross-platform compatibility

### Bug Fixes

**Bug Fix Process**:
1. Reproduce the bug with a test case
2. Implement minimal fix
3. Verify fix resolves issue
4. Ensure no regression in existing functionality
5. Update documentation if needed

### Refactoring

**Refactoring Guidelines**:
- Maintain existing functionality
- Improve code clarity and maintainability
- Add tests if coverage is lacking
- Update documentation for API changes
- Consider performance implications

## Release Process

### Version Management

Wobble uses semantic versioning (semver):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### Release Checklist

**Pre-release**:
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] Changelog updated
- [ ] Performance benchmarks validated

**Release**:
- [ ] Tag created with version number
- [ ] Release notes published
- [ ] Distribution packages created
- [ ] Installation instructions verified

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Request Comments**: Code review and implementation discussion

### Documentation

- **User Documentation**: `docs/articles/users/`
- **Developer Documentation**: `docs/articles/devs/`
- **API Reference**: Auto-generated from docstrings
- **Architecture Overview**: `docs/articles/devs/architecture/`

### Mentorship

New contributors are welcome and encouraged:
- Start with "good first issue" labels
- Ask questions in GitHub Discussions
- Request code review feedback
- Participate in design discussions
