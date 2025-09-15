# Glossary

This article covers:
- Key terms and concepts used throughout wobble documentation
- Technical definitions and organizational context
- Cross-references to detailed documentation

## Core Concepts

### Test Categories

**Development Test**
Temporary test used during active feature development. These tests validate work-in-progress functionality and may be removed once features stabilize. Marked with `@development_test(phase="...")` decorator.

**Integration Test**
Test that validates interactions between components, services, or systems. Scope can be component-level (internal interactions), service-level (external service integration), or system-level (end-to-end workflows). Marked with `@integration_test(scope="...")` decorator.

**Regression Test**
Permanent test that prevents breaking changes to established functionality. These tests form the foundation of quality assurance and should continue passing throughout the software lifecycle. Marked with `@regression_test` decorator.

### Test Organization

**Decorator-Based Organization**
Test categorization approach using wobble decorators (`@regression_test`, `@integration_test`, etc.) within test methods. Allows flexible categorization within flat directory structures.

**Hierarchical Organization**
Test categorization approach using directory structure (`tests/regression/`, `tests/integration/`, `tests/development/`). Provides visual organization and supports subcategorization.

**Test Discovery**
Process of locating and categorizing test files and methods within a repository. Wobble supports both hierarchical directory scanning and decorator-based metadata extraction.

### Framework Components

**CLI Interface**
Command-line interface providing access to wobble functionality. Supports test execution, filtering, output formatting, and discovery operations through `wobble`.

**Discovery Engine**
Core component responsible for locating test files, extracting metadata, and categorizing tests. Supports both hierarchical and flat repository structures.

**Output Formatter**
Component responsible for formatting test results in multiple formats (standard, verbose, JSON, minimal) with cross-platform color support.

**Test Runner**
Enhanced unittest runner that executes tests with timing information, metadata tracking, and performance metrics collection.

**File Output System**
Concurrent file writing system that saves test results to files while maintaining console output. Supports multiple formats (JSON, text) with configurable verbosity levels and file management options.

**Output Observer**
Component implementing the Observer pattern to coordinate output between multiple destinations (console and file). Enables simultaneous output to different formats and locations.

**Threaded File Writer**
Background file writing component that uses queue-based operations to write test results without blocking test execution. Provides ordered processing and graceful shutdown handling.

## Technical Terms

### Metadata

**Test Metadata**
Information attached to test methods through wobble decorators, including category, scope, phase, performance characteristics, and environment requirements.

**Decorator Attributes**
Function attributes added by wobble decorators (e.g., `_wobble_regression`, `_wobble_category`) that store test classification information.

### Output Formats

**JSON Format**
Machine-readable output format providing structured test results for CI/CD integration and programmatic processing.

**Minimal Format**
Compact output format using dot notation (`.` for pass, `F` for fail, `E` for error, `S` for skip) for quick feedback during development.

**Standard Format**
Default human-readable output format with colors, timing information, and summary statistics.

**Verbose Format**
Detailed output format including test metadata, extended error messages, and comprehensive result information.

### Performance Classification

**Slow Test**
Test marked with `@slow_test` decorator indicating execution time exceeding 5 seconds. Can be excluded from rapid development cycles using `--exclude-slow` option.

**CI Skip Test**
Test marked with `@skip_ci` decorator indicating incompatibility with CI environments (e.g., requires local resources). Excluded using `--exclude-ci` option.

## Organizational Context

### CrackingShells Organization

**Centralized Testing Framework**
Organizational strategy to standardize testing infrastructure across multiple Python repositories (Hatch, Hatchling, Hatch-Validator) using wobble.

**Repository Template**
Standardized project structure (`py-repo-template`) used as foundation for new repositories and wobble development.

**Testing Standards**
Organizational guidelines defined in `.github/instructions/testing.instructions.md` that wobble implements and enforces.

### Repository Patterns

**Hatch Pattern**
Repository structure following Hatch project conventions with `src/` directory, `tests/` directory, and `pyproject.toml` configuration.

**Hatchling Pattern**
Repository structure for Hatchling project with complex test organization including unit, functional, and performance test categories.

**Hatch-Validator Pattern**
Repository structure for validation tools with emphasis on integration testing and external service validation.

## Command-Line Interface

### CLI Options

**Category Selection**
Options for running specific test categories: `--category {regression,integration,development,all}` or `-c`.

**Filtering Options**
Options for excluding specific test types: `--exclude-slow` (skip slow tests), `--exclude-ci` (skip CI-incompatible tests).

**Format Selection**
Options for output format control: `--format {standard,verbose,json,minimal}` or `-f`.

**Discovery Options**
Options for test analysis without execution: `--discover-only` (analyze tests), `--list-categories` (show available categories).

### Environment Variables

**NO_COLOR**
Environment variable to disable colored output, equivalent to `--no-color` CLI option.

**WOBBLE_PATH**
Environment variable to specify default repository path for test discovery.

## File and Directory Conventions

### Test File Naming

**Test File Pattern**
Standard pattern `test_*.py` for test file discovery. Configurable through `--pattern` CLI option.

**Test Method Naming**
Convention requiring `test_` prefix for test method discovery by unittest framework.

### Directory Structure

**Repository Root**
Top-level directory containing `pyproject.toml`, `.git`, or other repository indicators. Automatically detected by wobble.

**Tests Directory**
Primary location for test files, typically `tests/` but supports alternatives like `test/`, `Tests/`, `Test/`.

**Category Directories**
Subdirectories within tests directory for hierarchical organization: `regression/`, `integration/`, `development/`.

## Integration Concepts

### CI/CD Integration

**Exit Codes**
Standard exit codes returned by wobble: 0 (success), 1 (test failures), 130 (user interruption).

**JSON Output**
Structured output format for CI/CD pipeline integration, providing machine-readable test results and metadata.

**Environment Compatibility**
Cross-platform support for Windows, macOS, and Linux environments with appropriate path handling and color support.

### Package Management

**Development Installation**
Installation method using `pip install -e .` for local development with immediate code changes reflected.

**Repository Distribution**
Distribution method using GitHub repository rather than PyPI, installed via `pip install git+https://github.com/...`.

## Quality Assurance

### Self-Testing

**Dogfooding**
Practice of using wobble to test itself, validating framework functionality through real-world usage.

**Bootstrap Testing**
Ability to test wobble using basic unittest functionality before full wobble features are available.

### Validation Procedures

**Cross-Platform Testing**
Testing wobble functionality across different operating systems and Python versions.

**Performance Benchmarking**
Comparing wobble performance against existing test runners to ensure no significant regression.

**Real Repository Validation**
Testing wobble against actual organizational repositories (Hatch, Hatchling, Hatch-Validator) to validate real-world compatibility.

## Migration and Adoption

### Migration Strategies

**Gradual Migration**
Incremental adoption approach allowing parallel execution of old and new test runners during transition period.

**Direct Migration**
Complete replacement of existing test runner with wobble for smaller repositories or new projects.

### Compatibility

**Backward Compatibility**
Wobble's ability to work with existing unittest-based test suites without requiring code changes.

**Forward Compatibility**
Design considerations ensuring wobble can evolve without breaking existing test suites or organizational workflows.
