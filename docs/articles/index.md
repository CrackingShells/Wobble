# Wobble Documentation

Wobble is a centralized testing framework for the CrackingShells organization, providing unified test discovery, execution, and reporting across all Python repositories.

## Quick Navigation

### For Users
- **[Getting Started](users/GettingStarted.md)** - Installation and basic usage
- **[CLI Reference](users/CLIReference.md)** - Complete command-line interface guide
- **[Test Organization](users/TestOrganization.md)** - How to structure and categorize tests
- **[Integration Guide](users/IntegrationGuide.md)** - Adding wobble to existing repositories

### For Developers
- **[Architecture Overview](devs/architecture/Overview.md)** - System design and components
- **[Contributing Guidelines](devs/contribution_guidelines/Contributing.md)** - How to contribute to wobble
- **[Development Setup](devs/contribution_guidelines/DevelopmentSetup.md)** - Local development environment

### Reference
- **[Glossary](appendices/glossary.md)** - Terms and concepts
- **[Migration Guide](appendices/migration.md)** - Migrating from existing test runners

## What is Wobble?

This article covers:
- Core testing framework concepts
- Organizational testing standardization
- Test categorization and filtering capabilities

Wobble provides a unified testing experience across the CrackingShells organization by:

**Standardizing Test Organization:**
- Hierarchical test structure support (`tests/regression/`, `tests/integration/`)
- Decorator-based test categorization for flat structures
- Consistent test discovery across repositories

**Enhancing Test Execution:**
- Colored output with timing information
- Multiple output formats (standard, verbose, JSON, minimal)
- Advanced filtering by category, performance, and environment

**Simplifying Test Management:**
- Single CLI interface for all test operations
- Repository-agnostic test discovery
- Self-testing capability for framework validation

## Core Concepts

**Test Categories:**
- **Regression Tests**: Permanent tests preventing breaking changes
- **Integration Tests**: Component and system interaction validation
- **Development Tests**: Temporary tests for work-in-progress features

**Test Decorators:**
- `@regression_test` - Mark permanent regression tests
- `@integration_test(scope="...")` - Mark integration tests with scope
- `@development_test(phase="...")` - Mark temporary development tests
- `@slow_test` - Mark tests requiring extended execution time
- `@skip_ci` - Mark tests to skip in CI environments

**Output Formats:**
- **Standard**: Clean, readable output with colors and timing
- **Verbose**: Detailed test information and metadata
- **JSON**: Machine-readable output for CI/CD integration
- **Minimal**: Compact output for quick feedback

## Getting Started

1. **Install wobble** in your repository:
   ```bash
   pip install wobble
   ```

2. **Run tests** with enhanced output:
   ```bash
   python -m wobble.cli --verbose
   ```

3. **Filter by category**:
   ```bash
   python -m wobble.cli --category regression
   ```

4. **Get JSON output** for CI integration:
   ```bash
   python -m wobble.cli --format json
   ```

## Repository Support

Wobble supports both organizational test structure patterns:

**Hierarchical Structure:**
```
tests/
├── regression/
│   ├── test_core_functionality.py
│   └── test_api_stability.py
├── integration/
│   ├── test_service_integration.py
│   └── test_database_integration.py
└── development/
    └── test_new_features.py
```

**Flat Structure with Decorators:**
```
tests/
├── test_core.py          # Uses @regression_test
├── test_integration.py   # Uses @integration_test
└── test_features.py      # Uses @development_test
```

Both patterns work seamlessly with wobble's discovery engine and provide identical functionality through the CLI interface.
