# Integration Guide

This article covers:
- Adding wobble to existing repositories
- Migration from current test runners
- CI/CD integration patterns

## Repository Integration

### Prerequisites

Before integrating wobble into your repository:

**Python Requirements**:
- Python 3.7 or higher
- Existing unittest-based test suite
- Virtual environment recommended

**Repository Structure**:
- Tests located in `tests/` directory
- Test files following `test_*.py` naming convention
- Test classes inheriting from `unittest.TestCase`

### Installation Steps

**Step 1**: Add wobble dependency

For repositories using `pyproject.toml`:
```toml
[project]
dependencies = [
    "wobble @ git+https://github.com/CrackingShells/Wobble.git",
    # ... other dependencies
]
```

For repositories using `requirements.txt`:
```txt
git+https://github.com/CrackingShells/Wobble.git
```

**Step 2**: Install in development environment
```bash
pip install -e .
# or
pip install -r requirements.txt
```

**Step 3**: Verify installation
```bash
python -c "import wobble; print('Wobble installed successfully')"
python -m wobble.cli --help
```

### Basic Integration

**Test wobble with existing tests**:
```bash
# Discover existing tests
python -m wobble.cli --discover-only

# Run all tests with wobble
python -m wobble.cli --verbose

# Compare with existing test runner
python -m unittest discover tests -v
```

**Validate compatibility**:
- All existing tests should be discovered
- Test execution should produce equivalent results
- No import errors or compatibility issues

## Migration Strategies

### Gradual Migration Approach

**Phase 1: Parallel Execution**
- Keep existing test runner
- Add wobble as alternative execution method
- Validate identical results

```bash
# Existing approach
python -m unittest discover tests -v

# New wobble approach
python -m wobble.cli --verbose

# Compare results
```

**Phase 2: Add Test Categorization**
- Add wobble decorators to critical tests
- Organize tests by category
- Validate category-based execution

```python
# Add decorators to existing tests
from wobble import regression_test, integration_test

class TestExistingFeature(unittest.TestCase):
    
    @regression_test  # Add to critical tests
    def test_core_functionality(self):
        # Existing test code unchanged
        pass
    
    @integration_test(scope="service")  # Add to integration tests
    def test_api_integration(self):
        # Existing test code unchanged
        pass
```

**Phase 3: Directory Reorganization**
- Move tests to category directories
- Update import statements if needed
- Validate discovery and execution

```bash
# Create category directories
mkdir -p tests/regression tests/integration tests/development

# Move tests to appropriate categories
mv tests/test_core.py tests/regression/
mv tests/test_api.py tests/integration/
```

**Phase 4: Full Migration**
- Replace existing test runner with wobble
- Update CI/CD configurations
- Remove old test runner dependencies

### Direct Migration Approach

For smaller repositories or new projects:

**Step 1**: Install wobble and validate compatibility
**Step 2**: Add decorators to all tests
**Step 3**: Update CI/CD to use wobble
**Step 4**: Remove old test runner

## CI/CD Integration

### GitHub Actions

Replace existing test runner with wobble:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -e .
        
    - name: Run tests with wobble
      run: |
        python -m wobble.cli --format json --exclude-ci > test_results.json
        
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: test_results.json
```

### Advanced CI Configuration

**Matrix testing with wobble**:
```yaml
strategy:
  matrix:
    python-version: [3.7, 3.8, 3.9, '3.10', '3.11']
    test-category: [regression, integration]

steps:
- name: Run category tests
  run: |
    python -m wobble.cli --category ${{ matrix.test-category }} --format json
```

**Conditional test execution**:
```yaml
- name: Run regression tests
  run: python -m wobble.cli --category regression --format json
  
- name: Run integration tests
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  run: python -m wobble.cli --category integration --format json --exclude-slow
```

### Other CI Systems

**Jenkins Pipeline**:
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'python -m wobble.cli --format json --exclude-ci'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test_results.json'
                }
            }
        }
    }
}
```

**GitLab CI**:
```yaml
test:
  script:
    - python -m wobble.cli --format json --exclude-ci
  artifacts:
    reports:
      junit: test_results.json
```

## Repository-Specific Patterns

### Hatch Repository Pattern

For repositories following the Hatch pattern:

```
project/
├── src/
│   └── package/
├── tests/
│   ├── regression/
│   ├── integration/
│   └── development/
├── pyproject.toml
└── README.md
```

**Integration steps**:
1. Add wobble to `pyproject.toml` dependencies
2. Categorize existing tests with decorators
3. Move tests to category directories
4. Update CI to use wobble

### Hatchling Repository Pattern

For repositories with complex test structures:

```
project/
├── src/
├── tests/
│   ├── unit/
│   ├── functional/
│   └── performance/
└── pyproject.toml
```

**Migration approach**:
1. Map existing categories to wobble categories:
   - `unit/` → `regression/`
   - `functional/` → `integration/`
   - `performance/` → `regression/` with `@slow_test`
2. Add appropriate decorators
3. Gradually reorganize directory structure

## Configuration Management

### Environment-Specific Configuration

**Development environment**:
```bash
# Quick feedback during development
alias wt='python -m wobble.cli --category development --format minimal --exclude-slow'

# Detailed debugging
alias wtv='python -m wobble.cli --category development --verbose'
```

**CI environment**:
```bash
# Set environment variables
export NO_COLOR=1
export WOBBLE_PATH=/workspace

# Run tests
python -m wobble.cli --format json --exclude-ci
```

### IDE Integration

**VS Code configuration** (`.vscode/tasks.json`):
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
            "label": "Run Regression Tests",
            "type": "shell",
            "command": "python",
            "args": ["-m", "wobble.cli", "--category", "regression", "--verbose"],
            "group": "test"
        }
    ]
}
```

**PyCharm configuration**:
- Add wobble as external tool
- Configure run configurations for different categories
- Set up test templates with wobble decorators

## Validation and Testing

### Integration Validation

**Test discovery validation**:
```bash
# Compare test counts
python -m unittest discover tests --dry-run | wc -l
python -m wobble.cli --discover-only --format json | jq '.total_tests'
```

**Execution validation**:
```bash
# Run same tests with both runners
python -m unittest discover tests -v > unittest_results.txt
python -m wobble.cli --verbose > wobble_results.txt

# Compare results (should be equivalent)
```

### Performance Validation

**Execution time comparison**:
```bash
# Time existing runner
time python -m unittest discover tests

# Time wobble runner
time python -m wobble.cli
```

**Memory usage monitoring**:
```bash
# Monitor memory usage during test execution
/usr/bin/time -v python -m wobble.cli
```

## Troubleshooting

### Common Integration Issues

**Import path problems**:
- Ensure package is installed or in Python path
- Check relative imports in test files
- Verify virtual environment activation

**Test discovery issues**:
- Verify test file naming (`test_*.py`)
- Check test class inheritance (`unittest.TestCase`)
- Validate directory structure

**CI/CD integration problems**:
- Check environment variable configuration
- Verify wobble installation in CI environment
- Validate JSON output parsing

### Migration Rollback

If issues arise during migration:

**Step 1**: Revert CI/CD configuration to use original test runner
**Step 2**: Remove wobble decorators (tests remain functional)
**Step 3**: Restore original directory structure if changed
**Step 4**: Address issues and retry migration

## Best Practices

### Incremental Integration

- Start with non-critical repositories
- Validate thoroughly before organization-wide rollout
- Maintain parallel execution during transition
- Document repository-specific patterns

### Team Coordination

- Communicate migration timeline to team
- Provide training on wobble usage
- Update development documentation
- Establish new testing workflows

### Monitoring and Maintenance

- Monitor test execution performance
- Track adoption across repositories
- Gather feedback from development teams
- Maintain wobble framework updates
