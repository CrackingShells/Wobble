# Development Setup

This article covers:
- Local development environment configuration
- Testing and validation procedures
- Development workflow optimization

## Environment Setup

### Prerequisites

**System Requirements**:
- Python 3.7 or higher
- Git 2.20 or higher
- Terminal/Command Prompt access
- Text editor or IDE (VS Code, PyCharm, etc.)

**Python Environment**:
```bash
# Verify Python version
python --version  # Should be 3.7+

# Verify pip is available
pip --version

# Install virtual environment if not available
python -m pip install virtualenv
```

### Repository Setup

**Clone and Initialize**:
```bash
# Clone the repository
git clone https://github.com/CrackingShells/Wobble.git
cd Wobble

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Verify virtual environment
which python  # Should point to venv/bin/python or venv\Scripts\python.exe
```

**Install Dependencies**:
```bash
# Install wobble in development mode
pip install -e .

# Verify installation
python -c "import wobble; print('Wobble installed successfully')"
wobble --help
```

### Development Dependencies

**Optional Development Tools**:
```bash
# Code formatting and linting
pip install black isort flake8

# Type checking
pip install mypy

# Testing tools
pip install coverage pytest  # Optional, wobble uses unittest

# Documentation tools
pip install sphinx sphinx-rtd-theme  # If building docs locally
```

## IDE Configuration

### VS Code Setup

**Recommended Extensions**:
- Python (Microsoft)
- Python Docstring Generator
- GitLens
- Markdown All in One

**Settings Configuration** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.unittestEnabled": true,
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./tests",
        "-p",
        "test_*.py"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

**Tasks Configuration** (`.vscode/tasks.json`):
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Wobble Tests",
            "type": "shell",
            "command": "python",
            "args": ["-m", "wobble.cli", "--verbose"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Format Code",
            "type": "shell",
            "command": "black",
            "args": ["wobble/", "tests/"],
            "group": "build"
        }
    ]
}
```

### PyCharm Setup

**Project Configuration**:
1. Open project in PyCharm
2. Configure Python interpreter to use virtual environment
3. Set project structure:
   - Mark `wobble/` as Sources Root
   - Mark `tests/` as Test Sources Root

**Run Configurations**:
- Create run configuration for wobble CLI
- Create test configurations for different test categories
- Set up debugging configurations

## Development Workflow

### Code Formatting

**Automatic Formatting**:
```bash
# Format all Python files
black wobble/ tests/

# Sort imports
isort wobble/ tests/

# Check formatting without changes
black --check wobble/ tests/
```

**Pre-commit Hook** (optional):
```bash
# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
black --check wobble/ tests/
if [ $? -ne 0 ]; then
    echo "Code formatting check failed. Run 'black wobble/ tests/' to fix."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

### Testing Workflow

**Run All Tests**:
```bash
# Use wobble to test itself
wobble --verbose

# Alternative: use unittest directly
python -m unittest discover tests -v
```

**Run Specific Test Categories**:
```bash
# Run only regression tests
wobble --category regression

# Run only integration tests
wobble --category integration

# Run development tests
wobble --category development
```

**Test Individual Modules**:
```bash
# Test specific module
python -m unittest tests.test_wobble_decorators -v

# Test specific test class
python -m unittest tests.test_wobble_decorators.TestDecorators -v

# Test specific test method
python -m unittest tests.test_wobble_decorators.TestDecorators.test_regression_decorator -v
```

### Debugging Setup

**Debug Configuration**:
```python
# Add to test files for debugging
import pdb; pdb.set_trace()  # Python debugger

# Or use IDE breakpoints
```

**Verbose Output for Debugging**:
```bash
# Maximum verbosity
wobble --verbose --format verbose

# JSON output for analysis
wobble --format json > debug_results.json
```

## Validation Procedures

### Code Quality Checks

**Linting**:
```bash
# Check code style
flake8 wobble/ tests/

# Type checking (if mypy installed)
mypy wobble/
```

**Import Validation**:
```bash
# Test all imports work
python -c "
import wobble
from wobble import decorators, discovery, runner, output, cli
print('All imports successful')
"
```

### Functional Validation

**CLI Functionality**:
```bash
# Test CLI help
wobble --help

# Test discovery
wobble --discover-only

# Test different output formats
wobble --format json
wobble --format minimal
```

**Cross-Platform Testing**:
```bash
# Test path handling
python -c "
from pathlib import Path
from wobble.cli import detect_repository_root
print(f'Repository root: {detect_repository_root()}')
"
```

### Performance Validation

**Execution Timing**:
```bash
# Time test execution
time wobble

# Compare with unittest
time python -m unittest discover tests -v
```

**Memory Usage** (if available):
```bash
# Monitor memory usage
/usr/bin/time -v wobble  # Linux/macOS
```

## Development Best Practices

### Code Organization

**Module Development**:
- Keep modules focused on single responsibility
- Use clear, descriptive function and class names
- Add comprehensive docstrings
- Include type hints for public APIs

**Test Development**:
- Write tests before implementing features (TDD)
- Use wobble's own decorators for self-testing
- Include both positive and negative test cases
- Test error conditions and edge cases

### Documentation

**Inline Documentation**:
```python
def discover_tests(self, pattern: str = "test*.py") -> Dict[str, List]:
    """Discover tests matching the specified pattern.
    
    This method searches for test files in the configured test directory
    and returns a categorized list of discovered tests.
    
    Args:
        pattern: File pattern for test discovery (default: "test*.py")
        
    Returns:
        Dictionary mapping test categories to lists of test information
        
    Raises:
        ImportError: If test modules cannot be imported
        FileNotFoundError: If test directory does not exist
        
    Example:
        >>> engine = TestDiscoveryEngine(Path("tests"))
        >>> tests = engine.discover_tests("test_*.py")
        >>> print(tests.keys())
        dict_keys(['regression', 'integration', 'development'])
    """
    pass
```

**Commit Messages**:
```bash
# Good commit messages
git commit -m "feat: add JSON output format for CI integration"
git commit -m "fix: resolve Windows path handling in discovery engine"
git commit -m "docs: update CLI reference with new filtering options"

# Poor commit messages (avoid)
git commit -m "fix stuff"
git commit -m "update"
git commit -m "changes"
```

### Debugging Techniques

**Print Debugging**:
```python
# Use verbose output for debugging
def debug_discovery(self):
    print(f"Searching in directory: {self.tests_dir}")
    print(f"Found test files: {list(self.tests_dir.glob('test_*.py'))}")
```

**Test Isolation**:
```python
# Create isolated test environments
def setUp(self):
    self.temp_dir = tempfile.mkdtemp()
    self.test_dir = Path(self.temp_dir) / "tests"
    self.test_dir.mkdir()

def tearDown(self):
    shutil.rmtree(self.temp_dir)
```

## Troubleshooting

### Common Issues

**Import Errors**:
```bash
# Ensure wobble is installed in development mode
pip install -e .

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify virtual environment
which python
```

**Test Discovery Issues**:
```bash
# Check test file naming
ls tests/test_*.py

# Verify test class inheritance
grep -r "unittest.TestCase" tests/

# Test discovery manually
python -c "
import unittest
loader = unittest.TestLoader()
suite = loader.discover('tests', pattern='test_*.py')
print(f'Found {suite.countTestCases()} tests')
"
```

**Path Issues**:
```bash
# Check current directory
pwd

# Verify repository structure
ls -la  # Should show wobble/, tests/, pyproject.toml

# Test path detection
python -c "
from wobble.cli import detect_repository_root
print(f'Detected root: {detect_repository_root()}')
"
```

### Performance Issues

**Slow Test Discovery**:
- Check for large test directories
- Verify test file patterns
- Look for import-time side effects

**Slow Test Execution**:
- Use `@slow_test` decorator for long-running tests
- Profile test execution with timing
- Check for blocking operations

### Getting Help

**Documentation Resources**:
- User documentation: `docs/articles/users/`
- Architecture overview: `docs/articles/devs/architecture/`
- Contributing guidelines: `docs/articles/devs/contribution_guidelines/`

**Community Support**:
- GitHub Issues for bug reports
- GitHub Discussions for questions
- Code review feedback in pull requests
