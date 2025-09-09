# CLI Reference

This article covers:
- Complete command-line interface options
- Usage patterns and examples
- Configuration and environment variables

## Command Syntax

```bash
wobble [OPTIONS]
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
wobble --category regression

# Run integration tests
wobble -c integration

# Run all tests (default)
wobble --category all
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
wobble --exclude-slow

# Skip CI-incompatible tests
wobble --exclude-ci

# Combine filters
wobble --category regression --exclude-slow --exclude-ci
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
wobble

# Custom pattern for different naming convention
wobble --pattern "*_test.py"

# Specific file pattern
wobble --pattern "test_core*.py"
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
wobble --format standard
```
- Clean, readable output with colors
- Test results with timing information
- Summary statistics

**Verbose Format**:
```bash
wobble --format verbose
```
- Detailed test information
- Metadata display
- Extended error messages

**JSON Format**:
```bash
wobble --format json
```
- Machine-readable output
- Structured data for CI/CD integration
- Programmatic parsing support

**Minimal Format**:
```bash
wobble --format minimal
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
wobble --no-color

# Force colors (default when terminal supports it)
wobble
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
wobble

# Increased verbosity
wobble --verbose

# Maximum verbosity
wobble -vv

# Quiet mode (errors only)
wobble --quiet
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
wobble --discover-only

# Get JSON summary of discovered tests
wobble --discover-only --format json

# List available categories
wobble --list-categories
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
wobble

# Specify absolute path
wobble --path /home/user/projects/myproject

# Specify relative path
wobble --path ../other-project

# Use environment variable
wobble --path $PROJECT_ROOT
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
wobble --category development --format minimal --exclude-slow
```

**Detailed debugging:**
```bash
wobble --category development --format verbose
```

**Pre-commit validation:**
```bash
wobble --category regression --verbose
```

### CI/CD Integration

**Basic CI execution:**
```bash
wobble --format json --no-color
```

**Regression testing:**
```bash
wobble --category regression --format json --exclude-ci
```

**Full test suite:**
```bash
wobble --format json --exclude-ci
```

### Analysis and Reporting

**Test discovery analysis:**
```bash
wobble --discover-only --format json > test_inventory.json
```

**Category breakdown:**
```bash
wobble --list-categories
```

**Performance analysis:**
```bash
wobble --verbose --format json > test_results.json
```

## Advanced Usage

### Combining Options

Most options can be combined for specific workflows:

```bash
# Fast development iteration
wobble -c development -f minimal --exclude-slow -q

# Comprehensive CI testing
wobble -f json --no-color --exclude-ci -v

# Detailed regression analysis
wobble -c regression -f verbose --path ../project
```

### Scripting Integration

Use wobble in shell scripts:

```bash
#!/bin/bash
# Run tests and capture results
if wobble --format json --quiet > results.json; then
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
- Use full module path: `wobble`

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
