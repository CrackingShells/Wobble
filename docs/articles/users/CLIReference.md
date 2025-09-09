# CLI Reference

This article covers:
- Complete command-line interface options
- Usage patterns and examples
- Configuration and environment variables

## Command Syntax

```bash
python -m wobble.cli [OPTIONS]
```

## Test Selection Options

### Category Selection

Control which test categories to execute:

```bash
--category {regression,integration,development,all}
-c {regression,integration,development,all}
```

**Examples:**
```bash
# Run only regression tests
python -m wobble.cli --category regression

# Run integration tests
python -m wobble.cli -c integration

# Run all tests (default)
python -m wobble.cli --category all
```

### Test Filtering

Exclude specific types of tests:

```bash
--exclude-slow          # Exclude tests marked with @slow_test
--exclude-ci            # Exclude tests marked with @skip_ci
```

**Examples:**
```bash
# Skip slow tests for faster feedback
python -m wobble.cli --exclude-slow

# Skip CI-incompatible tests
python -m wobble.cli --exclude-ci

# Combine filters
python -m wobble.cli --category regression --exclude-slow --exclude-ci
```

### File Pattern Matching

Specify test file patterns:

```bash
--pattern PATTERN       # File pattern for test discovery (default: test*.py)
-p PATTERN
```

**Examples:**
```bash
# Use default pattern (test*.py)
python -m wobble.cli

# Custom pattern for different naming convention
python -m wobble.cli --pattern "*_test.py"

# Specific file pattern
python -m wobble.cli --pattern "test_core*.py"
```

## Output Control Options

### Format Selection

Choose output format:

```bash
--format {standard,verbose,json,minimal}
-f {standard,verbose,json,minimal}
```

**Standard Format** (default):
```bash
python -m wobble.cli --format standard
```
- Clean, readable output with colors
- Test results with timing information
- Summary statistics

**Verbose Format**:
```bash
python -m wobble.cli --format verbose
```
- Detailed test information
- Metadata display
- Extended error messages

**JSON Format**:
```bash
python -m wobble.cli --format json
```
- Machine-readable output
- Structured data for CI/CD integration
- Programmatic parsing support

**Minimal Format**:
```bash
python -m wobble.cli --format minimal
```
- Compact dot notation (., F, E, S)
- Quick feedback for development
- Minimal screen space usage

### Color Control

Control colored output:

```bash
--no-color              # Disable colored output
```

**Examples:**
```bash
# Disable colors for logging or CI
python -m wobble.cli --no-color

# Force colors (default when terminal supports it)
python -m wobble.cli
```

### Verbosity Control

Adjust output detail level:

```bash
--verbose               # Increase verbosity (can be used multiple times)
-v
--quiet                 # Suppress all output except errors
-q
```

**Examples:**
```bash
# Standard verbosity
python -m wobble.cli

# Increased verbosity
python -m wobble.cli --verbose

# Maximum verbosity
python -m wobble.cli -vv

# Quiet mode (errors only)
python -m wobble.cli --quiet
```

## Discovery Options

### Discovery-Only Mode

Analyze tests without executing them:

```bash
--discover-only         # Only discover tests, do not run them
--list-categories       # List available test categories and exit
```

**Examples:**
```bash
# See what tests would be discovered
python -m wobble.cli --discover-only

# Get JSON summary of discovered tests
python -m wobble.cli --discover-only --format json

# List available categories
python -m wobble.cli --list-categories
```

## Repository Options

### Path Specification

Control repository location:

```bash
--path PATH             # Path to repository root (default: current directory)
```

**Examples:**
```bash
# Use current directory (default)
python -m wobble.cli

# Specify absolute path
python -m wobble.cli --path /home/user/projects/myproject

# Specify relative path
python -m wobble.cli --path ../other-project

# Use environment variable
python -m wobble.cli --path $PROJECT_ROOT
```

## Environment Variables

### Color Control

```bash
NO_COLOR=1              # Disable colored output (equivalent to --no-color)
```

### Path Configuration

```bash
WOBBLE_PATH=/path/to/repo    # Default repository path
```

## Exit Codes

Wobble returns standard exit codes:

- **0**: All tests passed successfully
- **1**: Test failures or errors occurred
- **130**: Interrupted by user (Ctrl+C)
- **Other**: Unexpected errors

## Usage Examples

### Development Workflows

**Quick development feedback:**
```bash
python -m wobble.cli --category development --format minimal --exclude-slow
```

**Detailed debugging:**
```bash
python -m wobble.cli --category development --format verbose
```

**Pre-commit validation:**
```bash
python -m wobble.cli --category regression --verbose
```

### CI/CD Integration

**Basic CI execution:**
```bash
python -m wobble.cli --format json --no-color
```

**Regression testing:**
```bash
python -m wobble.cli --category regression --format json --exclude-ci
```

**Full test suite:**
```bash
python -m wobble.cli --format json --exclude-ci
```

### Analysis and Reporting

**Test discovery analysis:**
```bash
python -m wobble.cli --discover-only --format json > test_inventory.json
```

**Category breakdown:**
```bash
python -m wobble.cli --list-categories
```

**Performance analysis:**
```bash
python -m wobble.cli --verbose --format json > test_results.json
```

## Advanced Usage

### Combining Options

Most options can be combined for specific workflows:

```bash
# Fast development iteration
python -m wobble.cli -c development -f minimal --exclude-slow -q

# Comprehensive CI testing
python -m wobble.cli -f json --no-color --exclude-ci -v

# Detailed regression analysis
python -m wobble.cli -c regression -f verbose --path ../project
```

### Scripting Integration

Use wobble in shell scripts:

```bash
#!/bin/bash
# Run tests and capture results
if python -m wobble.cli --format json --quiet > results.json; then
    echo "All tests passed"
    exit 0
else
    echo "Tests failed, see results.json"
    exit 1
fi
```

### IDE Integration

Configure wobble in your IDE:

**VS Code tasks.json:**
```json
{
    "label": "Run Wobble Tests",
    "type": "shell",
    "command": "python",
    "args": ["-m", "wobble.cli", "--verbose"],
    "group": "test"
}
```

## Troubleshooting

### Common Issues

**Command not found:**
- Ensure wobble is installed: `pip install wobble`
- Use full module path: `python -m wobble.cli`

**No tests discovered:**
- Check test file naming (must start with `test_`)
- Verify repository path with `--path`
- Use `--discover-only` to debug discovery

**Import errors:**
- Ensure package is installed or in Python path
- Check virtual environment activation
- Use `pip install -e .` for development

**Performance issues:**
- Use `--exclude-slow` to skip long-running tests
- Run specific categories instead of all tests
- Check for blocking operations in test setup
