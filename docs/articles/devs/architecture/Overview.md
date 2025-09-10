# Architecture Overview

This article covers:
- System design and component architecture
- Module responsibilities and interactions
- Design patterns and architectural decisions

## System Architecture

Wobble follows a modular architecture with clear separation of concerns:

```
wobble/
├── __init__.py          # Package initialization and public API
├── decorators.py        # Test categorization decorators
├── discovery.py         # Test discovery engine
├── runner.py           # Test execution engine
├── output.py           # Output formatting and display
└── cli.py              # Command-line interface
```

## Core Components

### Test Discovery Engine (`discovery.py`)

**Responsibility**: Locate and categorize tests across different repository structures.

**Key Classes**:
- `TestDiscoveryEngine`: Main discovery coordinator
- Supports hierarchical (`tests/regression/`) and flat (decorator-based) structures
- Provides filtering capabilities by category, performance, and environment

**Design Patterns**:
- **Strategy Pattern**: Different discovery strategies for hierarchical vs. flat structures
- **Factory Pattern**: Test suite creation from discovered test information
- **Filter Pattern**: Composable test filtering by multiple criteria

**Key Methods**:
```python
def discover_tests(pattern: str) -> Dict[str, List]
def filter_tests(categories: List[str], exclude_slow: bool, exclude_ci: bool) -> List[Dict]
def supports_hierarchical_structure() -> bool
def supports_decorator_structure() -> bool
```

### Decorator System (`decorators.py`)

**Responsibility**: Provide test categorization and metadata attachment.

**Core Decorators**:
- `@regression_test`: Mark permanent regression tests
- `@integration_test(scope="...")`: Mark integration tests with scope
- `@development_test(phase="...")`: Mark temporary development tests
- `@slow_test`: Mark performance-intensive tests
- `@skip_ci`: Mark tests to skip in CI environments

**Design Patterns**:
- **Decorator Pattern**: Non-invasive test enhancement
- **Metadata Pattern**: Attribute-based test classification
- **Composition Pattern**: Multiple decorators can be combined

**Metadata Structure**:
```python
{
    'category': 'regression|integration|development',
    'scope': 'component|service|system',  # integration only
    'phase': 'string',                    # development only
    'slow': bool,
    'skip_ci': bool
}
```

### Test Runner (`runner.py`)

**Responsibility**: Execute tests with enhanced result tracking and timing.

**Key Classes**:
- `WobbleTestResult`: Enhanced unittest.TestResult with timing and metadata
- `TestRunner`: Main test execution coordinator

**Design Patterns**:
- **Observer Pattern**: Test result collection and notification
- **Template Method**: Standardized test execution workflow
- **Command Pattern**: Test execution as discrete operations

**Enhanced Features**:
- Individual test timing
- Metadata-aware result processing
- Performance metrics collection
- Custom result formatting

### Output Formatter (`output.py`)

**Responsibility**: Format and display test results in multiple formats.

**Supported Formats**:
- **Standard**: Human-readable with colors and timing
- **Verbose**: Detailed information with metadata
- **JSON**: Machine-readable for CI/CD integration
- **Minimal**: Compact dot notation for quick feedback

**Design Patterns**:
- **Strategy Pattern**: Different formatting strategies per output type
- **Builder Pattern**: Incremental result formatting
- **Adapter Pattern**: Cross-platform color support

**Color Support**:
- Cross-platform color handling via colorama
- Automatic color detection and fallback
- Environment variable override support

### CLI Interface (`cli.py`)

**Responsibility**: Provide command-line interface and argument processing.

**Key Functions**:
- Argument parsing and validation
- Repository root detection
- Component coordination
- Error handling and exit codes

**Design Patterns**:
- **Facade Pattern**: Simplified interface to complex subsystems
- **Command Pattern**: CLI operations as discrete commands
- **Chain of Responsibility**: Argument processing pipeline

## Component Interactions

### Test Execution Flow

```
CLI Interface
    ↓ (parse arguments)
Discovery Engine
    ↓ (find and categorize tests)
Test Runner
    ↓ (execute with timing)
Output Formatter
    ↓ (format results)
Terminal/File Output
```

### Data Flow

**Discovery Phase**:
1. CLI specifies discovery parameters
2. Discovery engine locates test files
3. Decorator metadata extracted from test methods
4. Tests categorized and filtered
5. Test suite created for execution

**Execution Phase**:
1. Test runner receives filtered test suite
2. Individual tests executed with timing
3. Results collected with metadata
4. Performance metrics calculated
5. Results passed to output formatter

**Output Phase**:
1. Output formatter receives results and metadata
2. Format selected based on CLI arguments
3. Results formatted according to strategy
4. Output written to terminal or file

## Design Decisions

### Minimalist Dependencies

**Decision**: Use only standard library plus colorama for cross-platform color support.

**Rationale**:
- Reduces installation complexity
- Minimizes version conflicts
- Ensures broad compatibility
- Simplifies maintenance

**Trade-offs**:
- More implementation code required
- Limited to unittest framework
- Manual cross-platform handling

### Decorator-Based Metadata

**Decision**: Use function attributes for test metadata storage.

**Rationale**:
- Non-invasive test enhancement
- Compatible with existing unittest tests
- Allows multiple decorators per test
- Simple implementation and debugging

**Trade-offs**:
- Metadata not visible in test code inspection
- Requires wobble-specific decorators
- Limited to Python function attributes

### Dual Structure Support

**Decision**: Support both hierarchical directories and flat decorator-based organization.

**Rationale**:
- Accommodates existing organizational patterns
- Enables gradual migration
- Provides flexibility for different repository needs
- Maintains backward compatibility

**Trade-offs**:
- Increased complexity in discovery engine
- Potential confusion about which pattern to use
- More test cases required for validation

### JSON Output Format

**Decision**: Provide structured JSON output for CI/CD integration.

**Rationale**:
- Enables programmatic result processing
- Supports CI/CD pipeline integration
- Allows custom reporting tools
- Industry standard format

**Trade-offs**:
- Additional formatting complexity
- Requires JSON schema maintenance
- May not include all human-readable information

## Extension Points

### Custom Decorators

Add repository-specific decorators:

```python
def performance_test(benchmark: str):
    """Custom decorator for performance benchmarks."""
    def decorator(func):
        func._wobble_performance = True
        func._wobble_benchmark = benchmark
        return func
    return decorator
```

### Custom Output Formats

Extend output formatting:

```python
class CustomOutputFormatter(OutputFormatter):
    def format_results(self, results: Dict) -> str:
        # Custom formatting logic
        pass
```

### Discovery Extensions

Add custom discovery patterns:

```python
class CustomDiscoveryEngine(TestDiscoveryEngine):
    def _find_test_directories(self) -> List[Path]:
        # Custom directory discovery logic
        pass
```

## Performance Considerations

### Discovery Optimization

- Lazy loading of test modules
- Cached directory scanning
- Parallel test file processing
- Efficient metadata extraction

### Execution Optimization

- Minimal overhead test result tracking
- Efficient timing measurement
- Memory-conscious result storage
- Streaming output for large test suites

### Output Optimization

- Buffered output writing
- Conditional color processing
- Efficient JSON serialization
- Terminal width detection caching

## Testing Strategy

### Self-Testing Architecture

Wobble tests itself using its own framework:

- Discovery engine tested with synthetic test structures
- Decorator functionality validated through metadata inspection
- Output formatting tested with mock results
- CLI interface tested with argument combinations

### Integration Testing

- Real repository validation (Hatch, Hatchling, Hatch-Validator)
- Cross-platform compatibility testing
- Performance benchmarking against existing solutions
- CI/CD integration validation

### Regression Testing

- Comprehensive test suite for all components
- Backward compatibility validation
- Performance regression detection
- Output format stability testing

## Future Architecture Considerations

### Scalability

- Plugin architecture for custom extensions
- Distributed test execution support
- Result aggregation across multiple runs
- Large test suite optimization

### Extensibility

- Custom reporter plugins
- Additional output formats
- Integration with external tools
- Repository-specific customizations

### Maintainability

- Clear module boundaries
- Comprehensive documentation
- Automated testing coverage
- Performance monitoring
