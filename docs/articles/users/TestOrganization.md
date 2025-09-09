# Test Organization

This article covers:
- Test categorization strategies and best practices
- Directory structure patterns supported by wobble
- Decorator usage for test classification

## Test Categories

Wobble supports three primary test categories aligned with organizational testing guidelines:

### Regression Tests

**Purpose**: Permanent tests that prevent breaking changes to core functionality.

**Characteristics**:
- Validate stable, established features
- Should continue passing throughout software lifecycle
- Form the foundation of quality assurance
- Critical for release validation

**When to use**:
- Core functionality that must never break
- API contracts and interfaces
- Critical business logic
- Performance benchmarks

### Integration Tests

**Purpose**: Validate interactions between components, services, or systems.

**Scope levels**:
- **Component**: Internal component interactions
- **Service**: External service integrations
- **System**: End-to-end system workflows

**When to use**:
- Database connectivity and operations
- API endpoint interactions
- Third-party service integrations
- Cross-module functionality

### Development Tests

**Purpose**: Temporary tests for work-in-progress features and validation.

**Characteristics**:
- May be removed once features stabilize
- Support active development workflows
- Validate experimental functionality
- Enable rapid iteration

**When to use**:
- New feature development
- Prototype validation
- Experimental functionality
- Temporary debugging aids

## Organization Patterns

Wobble supports two organizational patterns that can be used independently or together:

### Hierarchical Directory Structure

Organize tests by category using directory structure:

```
tests/
├── regression/
│   ├── test_core_functionality.py
│   ├── test_api_stability.py
│   └── test_performance_benchmarks.py
├── integration/
│   ├── component/
│   │   ├── test_module_interactions.py
│   │   └── test_data_flow.py
│   ├── service/
│   │   ├── test_database_integration.py
│   │   └── test_external_apis.py
│   └── system/
│       └── test_end_to_end_workflows.py
└── development/
    ├── test_new_feature_prototype.py
    └── test_experimental_algorithms.py
```

**Benefits**:
- Clear visual organization
- Easy category-based discovery
- Supports subcategorization
- Familiar directory-based navigation

### Flat Structure with Decorators

Organize tests using wobble decorators in a flat structure:

```
tests/
├── test_core.py              # Contains @regression_test methods
├── test_integrations.py      # Contains @integration_test methods
├── test_features.py          # Contains @development_test methods
└── test_performance.py       # Contains @slow_test methods
```

**Benefits**:
- Flexible categorization within files
- Multiple categories per file
- Metadata-driven organization
- Supports complex test classification

## Decorator Usage

### Basic Categorization

```python
import unittest
from wobble import regression_test, integration_test, development_test

class TestCoreFeatures(unittest.TestCase):
    
    @regression_test
    def test_critical_functionality(self):
        """Test that must never break."""
        result = core_function()
        self.assertEqual(result, expected_value)
    
    @integration_test(scope="component")
    def test_module_interaction(self):
        """Test component interactions."""
        result = module_a.interact_with(module_b)
        self.assertIsNotNone(result)
    
    @development_test(phase="feature-validation")
    def test_new_feature(self):
        """Temporary test for new feature."""
        result = new_feature()
        self.assertTrue(result.is_valid())
```

### Advanced Classification

```python
from wobble import regression_test, slow_test, skip_ci

class TestPerformance(unittest.TestCase):
    
    @regression_test
    @slow_test
    def test_performance_benchmark(self):
        """Critical performance test that takes time."""
        start_time = time.time()
        process_large_dataset()
        duration = time.time() - start_time
        self.assertLess(duration, 10.0)  # Must complete in 10 seconds
    
    @integration_test(scope="service")
    @skip_ci
    def test_external_service(self):
        """Test requiring external service access."""
        response = external_api.get_data()
        self.assertEqual(response.status_code, 200)
```

### Combining Patterns

Use both directory structure and decorators for maximum flexibility:

```
tests/
├── regression/
│   └── test_core.py          # @regression_test decorators
├── integration/
│   ├── test_components.py    # @integration_test(scope="component")
│   └── test_services.py      # @integration_test(scope="service")
└── development/
    └── test_features.py      # @development_test decorators
```

## Best Practices

### Test Naming

**File naming**:
- Start with `test_` prefix
- Use descriptive names: `test_user_authentication.py`
- Group related functionality: `test_payment_processing.py`

**Method naming**:
- Start with `test_` prefix
- Use descriptive names: `test_user_login_with_valid_credentials`
- Include expected behavior: `test_payment_fails_with_invalid_card`

### Category Assignment

**Regression tests**:
- Assign to functionality that must remain stable
- Include all critical business logic
- Cover public API contracts
- Include performance benchmarks

**Integration tests**:
- Specify scope clearly: `@integration_test(scope="service")`
- Group by integration level
- Include setup and teardown for external dependencies
- Document external service requirements

**Development tests**:
- Include phase information: `@development_test(phase="prototype")`
- Remove when features stabilize
- Use for temporary validation needs
- Document removal criteria

### Performance Considerations

**Slow test marking**:
```python
@slow_test
@regression_test
def test_comprehensive_workflow(self):
    """Mark tests that take >5 seconds."""
    pass
```

**CI environment handling**:
```python
@skip_ci
@integration_test(scope="service")
def test_requires_local_database(self):
    """Skip tests requiring local resources."""
    pass
```

### Documentation

**Test docstrings**:
```python
@regression_test
def test_user_authentication(self):
    """Test user authentication with valid credentials.
    
    This test validates that users can successfully authenticate
    using valid username/password combinations. This is a critical
    security feature that must never break.
    
    Test data: Uses test_users.json fixture
    Dependencies: User database must be available
    """
    pass
```

## Migration Strategies

### From Existing Test Suites

**Step 1**: Add wobble decorators to existing tests
```python
# Before
def test_important_feature(self):
    pass

# After
@regression_test
def test_important_feature(self):
    pass
```

**Step 2**: Organize by category
- Move regression tests to `tests/regression/`
- Move integration tests to `tests/integration/`
- Keep development tests in `tests/development/`

**Step 3**: Validate with wobble
```bash
# Test discovery
wobble --discover-only

# Run by category
wobble --category regression
```

### Gradual Adoption

**Phase 1**: Add decorators to critical tests
**Phase 2**: Organize directory structure
**Phase 3**: Migrate all tests to wobble execution
**Phase 4**: Remove old test runners

## Validation

### Test Organization Validation

```bash
# Verify test discovery
wobble --discover-only --format json

# Check category distribution
wobble --list-categories

# Validate specific categories
wobble --category regression --discover-only
```

### Quality Checks

**Category coverage**:
- Ensure all critical functionality has regression tests
- Verify integration points have appropriate tests
- Remove obsolete development tests

**Performance validation**:
- Mark slow tests appropriately
- Exclude slow tests from rapid development cycles
- Monitor test execution times

**CI compatibility**:
- Mark environment-specific tests
- Ensure CI can run core test suite
- Validate JSON output format
