# CLI Reference

This article covers:
- Complete command-line interface options
- Usage patterns and examples
- Configuration and environment variables

## Table of Contents

- [Command Syntax](#command-syntax)
- [Test Selection Options](#test-selection-options)
- [Output Format Options](#output-format-options)
- [Discovery Options](#discovery-options)
- [Repository Options](#repository-options)
- [File Output Options](#file-output-options)
- [Environment Variables](#environment-variables)

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
--discover-only                    # Only discover tests, do not run them
--discover-verbosity {1,2,3}      # Control discovery output detail level
--list-categories                  # List available test categories and exit
```

### Discovery Verbosity Levels

Control the amount of detail in discovery output:

- **Level 1 (Default)**: Test counts by category
- **Level 2**: Level 1 + detailed uncategorized test listings
- **Level 3**: Level 2 + complete test listings with file paths and decorators

**Examples:**
```bash
# Basic discovery (counts only)
wobble --discover-only

# Show uncategorized test details
wobble --discover-only --discover-verbosity 2

# Complete discovery report with all details
wobble --discover-only --discover-verbosity 3

# List available categories
wobble --list-categories
```

### Discovery Output Formats

Discovery results can be output in different formats:

```bash
# Console output with file logging
wobble --discover-only --log-file discovery.txt

# JSON format for programmatic use
wobble --discover-only --log-file discovery.json --log-file-format json

# Different verbosity for console vs file
wobble --discover-only --discover-verbosity 1 --log-file detailed.txt --log-verbosity 3
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

## File Output Options

### Log File Configuration

Control test result logging to files:

```bash
--log-file [LOG_FILE]           # Enable file output (auto-timestamp if no filename)
--log-file-format {txt,json,auto}  # Output format for log files
--log-verbosity {1,2,3}         # Verbosity level for file output
--log-append                    # Append to existing file
--log-overwrite                 # Overwrite existing file (default)
```

**Examples:**
```bash
# Auto-timestamped JSON output
wobble --log-file

# Specific filename with text format
wobble --log-file results.txt --log-file-format txt

# High verbosity JSON for CI
wobble --log-file ci_results.json --log-file-format json --log-verbosity 3

# Append to existing log file
wobble --log-file daily_tests.txt --log-append

# Overwrite previous results (default behavior)
wobble --log-file test_results.json --log-overwrite
```

### File Output Formats

**Text Format** (human-readable):
```bash
wobble --log-file results.txt --log-file-format txt
```
- Clean test results with timing information
- Error details and stack traces
- Summary statistics
- Ideal for manual review and debugging

**JSON Format** (machine-readable):
```bash
wobble --log-file results.json --log-file-format json
```
- Structured test results with metadata
- Complete test execution information
- CI/CD integration support
- Programmatic parsing and analysis

**Auto Format** (intelligent detection):
```bash
wobble --log-file results.json --log-file-format auto
```
- JSON for .json file extensions
- Text for all other extensions
- Convenient default behavior

### File Output Verbosity Levels

Control the amount of detail in file output:

```bash
--log-verbosity 1               # Basic results (default)
--log-verbosity 2               # Include test metadata and timing
--log-verbosity 3               # Full details with error traces
```

**Verbosity Level Examples:**
```bash
# Level 1: Basic test results
wobble --log-file basic.json --log-verbosity 1

# Level 2: Include metadata and detailed timing
wobble --log-file detailed.json --log-verbosity 2

# Level 3: Full information including error traces
wobble --log-file complete.json --log-verbosity 3
```

### Discovery Mode File Output

When using `--discover-only`, file output behavior adapts to discovery mode:

```bash
# Discovery with independent console/file verbosity
wobble --discover-only --discover-verbosity 1 --log-file discovery.json --log-verbosity 3

# JSON discovery output with complete test details
wobble --discover-only --log-file discovery.json --log-file-format json --log-verbosity 3

# Text discovery output with basic counts
wobble --discover-only --log-file discovery.txt --log-file-format txt --log-verbosity 1
```

**Discovery Verbosity Mapping:**
- `--log-verbosity 1`: Test counts by category
- `--log-verbosity 2`: Counts + uncategorized test details
- `--log-verbosity 3`: Complete test listings with file paths and decorators

### File Management Options

Control how files are handled:

```bash
# Append mode - add to existing file
wobble --log-file continuous.txt --log-append

# Overwrite mode - replace existing file (default)
wobble --log-file fresh_results.json --log-overwrite

# Auto-timestamped files (prevents overwrites)
wobble --log-file  # Creates wobble_results_YYYYMMDD_HHMMSS.json
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
