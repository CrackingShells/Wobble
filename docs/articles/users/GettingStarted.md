# Getting Started with Wobble

This article covers:
- Installation and setup procedures
- Basic usage patterns and commands
- File output and logging capabilities
- Initial test execution and validation

## Installation

### Prerequisites

Wobble requires Python 3.7+ and works with existing unittest-based test suites.

### Install from Repository

Since wobble is distributed via GitHub repository rather than PyPI:

```bash
# Install directly from repository
pip install git+https://github.com/CrackingShells/Wobble.git

# Or for development/editable installation
git clone https://github.com/CrackingShells/Wobble.git
cd Wobble
pip install -e .
```

### Verify Installation

Test that wobble is correctly installed:

```bash
# Test package import
python -c "import wobble; print('Wobble installed successfully')"

# Test CLI access
wobble --help
```

## Basic Usage

### Running All Tests

Execute all tests in your repository:

```bash
# Standard output with timing
wobble

# Verbose output with detailed information
wobble --verbose

# Quiet output (errors only)
wobble --quiet
```

### Test Discovery

Understand what tests wobble finds in your repository:

```bash
# Discover tests without running them
wobble --discover-only

# List available test categories
wobble --list-categories

# JSON output for programmatic use
wobble --discover-only --format json
```

### Category-Based Execution

Run specific test categories:

```bash
# Run only regression tests
wobble --category regression

# Run only integration tests
wobble --category integration

# Run only development tests
wobble --category development
```

### Filtering Options

Control which tests execute:

```bash
# Exclude slow-running tests
wobble --exclude-slow

# Exclude tests marked for CI skip
wobble --exclude-ci

# Combine filters
wobble --category regression --exclude-slow
```

## Output Formats

### Standard Format

Default human-readable output with colors and timing:

```bash
wobble --verbose
```

Example output:
```
============================================================
Wobble Test Runner - 2025-09-10 01:39:29
Running 12 test(s)
============================================================

✓ TestBasicFunctionality.test_package_import (0.001s)
✓ TestBasicFunctionality.test_package_structure (0.000s)
✗ TestAdvanced.test_complex_feature (0.045s)
    Failure: Expected 'success' but got 'error'

============================================================
Test Results Summary
============================================================
Tests run: 12
Failures: 1
Errors: 0
Skipped: 0
Success rate: 91.7%
Total time: 0.156s

Overall result: FAILED
```

### JSON Format

Machine-readable output for CI/CD integration:

```bash
wobble --format json
```

Example output:
```json
{
  "timestamp": "2025-09-10T01:39:29.123456",
  "tests_run": 12,
  "failures": 1,
  "errors": 0,
  "skipped": 0,
  "success_rate": 91.7,
  "total_time": 0.156
}
```

### Minimal Format

Compact output for quick feedback:

```bash
wobble --format minimal
```

Example output:
```
..........F.
```

## File Output

### Saving Test Results

Save test results to files for later analysis or CI/CD integration:

```bash
# Auto-timestamped JSON file
wobble --log-file

# Specific filename with text format
wobble --log-file test_results.txt --log-file-format txt

# JSON format for CI integration
wobble --log-file ci_results.json --log-file-format json
```

### File Output Examples

**Basic file logging:**
```bash
# Creates wobble_results_20250912_143022.json
wobble --log-file
```

**Custom filename with text format:**
```bash
wobble --log-file daily_tests.txt --log-file-format txt --log-verbosity 2
```

**High-detail JSON for debugging:**
```bash
wobble --log-file debug_results.json --log-verbosity 3
```

**Continuous logging (append mode):**
```bash
wobble --log-file continuous.log --log-append --log-file-format txt
```

## Repository Integration

### Automatic Repository Detection

Wobble automatically detects your repository root by looking for:
- `.git` directory
- `pyproject.toml` file
- `setup.py` file
- `requirements.txt` file

### Manual Path Specification

Override automatic detection:

```bash
# Specify repository path
wobble --path /path/to/repository

# Use relative path
wobble --path ../other-project
```

### Test Directory Discovery

Wobble searches for tests in common locations:
- `tests/` (primary)
- `test/` (alternative)
- `Tests/` (Windows-style)
- `Test/` (alternative)

## Common Workflows

### Development Workflow

During active development:

```bash
# Quick feedback during development
wobble --category development --format minimal

# Detailed output for debugging
wobble --category development --verbose

# Skip slow tests for rapid iteration
wobble --exclude-slow
```

### CI/CD Integration

For continuous integration with file output:

```bash
# JSON output for parsing with file logging
wobble --format json --log-file ci_results.json --log-verbosity 3 --exclude-ci

# Regression tests with file output
wobble --category regression --log-file regression_results.json --log-file-format json

# Quiet console with detailed file logging
wobble --quiet --log-file detailed.json --log-verbosity 3

# Multiple output destinations
wobble --format minimal --log-file ci_archive.json --log-append
```

### Pre-commit Validation

Before committing changes:

```bash
# Run all tests with verbose output
wobble --verbose

# Focus on regression tests
wobble --category regression --verbose
```

## Troubleshooting

### No Tests Found

If wobble reports no tests found:

1. Verify test directory exists and contains test files
2. Check test file naming (should start with `test_`)
3. Ensure test classes inherit from `unittest.TestCase`
4. Verify repository root detection with `--path` option

### Import Errors

If tests fail with import errors:

1. Ensure your package is installed or in Python path
2. Check relative imports in test files
3. Verify virtual environment activation
4. Use `pip install -e .` for development installations

### Performance Issues

If test discovery or execution is slow:

1. Use `--exclude-slow` to skip long-running tests
2. Run specific categories instead of all tests
3. Check for infinite loops or blocking operations in test setup

## Next Steps

- **[CLI Reference](CLIReference.md)** - Complete command-line options
- **[Test Organization](TestOrganization.md)** - Structure your tests effectively
- **[Integration Guide](IntegrationGuide.md)** - Add wobble to existing projects
