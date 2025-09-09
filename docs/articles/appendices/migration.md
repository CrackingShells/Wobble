# Migration Guide

This article covers:
- Detailed migration procedures from existing test runners
- Repository-specific migration strategies
- Rollback procedures and risk mitigation

## Migration Overview

### Migration Philosophy

**Incremental Approach**
Wobble migration follows a gradual, low-risk approach that maintains existing functionality while introducing enhanced capabilities. This ensures continuous development productivity during transition.

**Compatibility First**
All migration strategies prioritize maintaining existing test functionality. Wobble works with existing unittest-based test suites without requiring immediate code changes.

**Validation at Each Step**
Every migration phase includes validation procedures to ensure equivalent functionality and identify issues before proceeding to the next phase.

## Pre-Migration Assessment

### Repository Analysis

**Test Suite Inventory**:
```bash
# Analyze existing test structure
find tests/ -name "test_*.py" | wc -l
find tests/ -name "test_*.py" -exec grep -l "class.*TestCase" {} \;

# Count test methods
grep -r "def test_" tests/ | wc -l

# Identify test categories (if any existing organization)
ls -la tests/
```

**Current Test Runner Analysis**:
```bash
# Document current test execution
python -m unittest discover tests -v > current_test_output.txt

# Time current execution
time python -m unittest discover tests

# Identify any custom test runners or configurations
grep -r "unittest\|pytest" . --include="*.py" --include="*.toml" --include="*.cfg"
```

**Dependency Analysis**:
```bash
# Check for test-related dependencies
grep -i "test\|pytest\|nose" requirements*.txt pyproject.toml setup.py

# Identify custom test utilities
find . -name "*test*" -type f | grep -v __pycache__ | grep -v .git
```

### Risk Assessment

**Low Risk Indicators**:
- Standard unittest-based test suite
- Simple directory structure
- No custom test runners
- Limited test dependencies

**Medium Risk Indicators**:
- Mixed testing frameworks (unittest + pytest)
- Complex directory organization
- Custom test discovery logic
- Extensive test utilities

**High Risk Indicators**:
- Non-standard test frameworks
- Heavy customization of test execution
- Complex CI/CD integration
- Performance-critical test suites

## Migration Strategies

### Strategy 1: Gradual Migration (Recommended)

**Phase 1: Parallel Installation (Week 1)**

Install wobble alongside existing test runner:

```bash
# Add wobble to dependencies
echo "git+https://github.com/CrackingShells/Wobble.git" >> requirements.txt
pip install -r requirements.txt

# Verify parallel functionality
python -m unittest discover tests -v > unittest_results.txt
wobble --verbose > wobble_results.txt

# Compare results
diff unittest_results.txt wobble_results.txt
```

**Phase 2: Test Categorization (Week 2)**

Add wobble decorators to existing tests:

```python
# Before
class TestCoreFeature(unittest.TestCase):
    def test_critical_functionality(self):
        pass

# After
from wobble import regression_test

class TestCoreFeature(unittest.TestCase):
    @regression_test
    def test_critical_functionality(self):
        pass
```

Categorization guidelines:
- Mark critical functionality as `@regression_test`
- Mark API/service interactions as `@integration_test`
- Mark new feature tests as `@development_test`
- Mark slow tests (>5s) as `@slow_test`

**Phase 3: Directory Organization (Week 3)**

Reorganize tests by category:

```bash
# Create category directories
mkdir -p tests/regression tests/integration tests/development

# Move tests to appropriate categories
# (Based on decorator analysis)
mv tests/test_core.py tests/regression/
mv tests/test_api.py tests/integration/
mv tests/test_new_features.py tests/development/

# Verify discovery still works
wobble --discover-only
```

**Phase 4: CI/CD Integration (Week 4)**

Update CI/CD to use wobble:

```yaml
# Before
- name: Run tests
  run: python -m unittest discover tests -v

# After
- name: Run tests
  run: wobble --format json --exclude-ci
```

**Phase 5: Full Migration (Week 5)**

Remove old test runner and finalize migration:

```bash
# Remove old test runner references
# Update documentation
# Remove unused dependencies
# Validate full functionality
```

### Strategy 2: Direct Migration (Small Repositories)

**Day 1: Assessment and Planning**
- Analyze test suite (typically <50 tests)
- Identify categorization strategy
- Plan directory organization

**Day 2: Implementation**
- Install wobble
- Add decorators to all tests
- Reorganize directory structure
- Validate functionality

**Day 3: Integration**
- Update CI/CD configuration
- Update documentation
- Remove old test runner
- Final validation

### Strategy 3: Repository-Specific Migration

**Hatch Repository Migration**:

Current structure:
```
hatch/
├── src/hatch/
├── tests/
│   ├── test_core.py
│   ├── test_cli.py
│   └── test_utils.py
└── pyproject.toml
```

Migration steps:
1. Add wobble to `pyproject.toml` dependencies
2. Categorize tests based on functionality:
   - Core functionality → regression
   - CLI interface → integration
   - Utilities → regression
3. Organize into hierarchical structure
4. Update CI configuration

**Hatchling Repository Migration**:

Current structure:
```
hatchling/
├── src/hatchling/
├── tests/
│   ├── unit/
│   ├── functional/
│   └── performance/
└── pyproject.toml
```

Migration mapping:
- `unit/` → `regression/` (core functionality tests)
- `functional/` → `integration/` (component interaction tests)
- `performance/` → `regression/` with `@slow_test` decorator

## Migration Procedures

### Decorator Addition Procedure

**Automated Decorator Addition**:

```python
# Script to add decorators based on test analysis
import ast
import re
from pathlib import Path

def analyze_test_file(file_path):
    """Analyze test file and suggest decorators."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Heuristics for categorization
    if 'core' in file_path.name or 'basic' in file_path.name:
        return 'regression_test'
    elif 'api' in file_path.name or 'integration' in file_path.name:
        return 'integration_test'
    elif 'new' in file_path.name or 'feature' in file_path.name:
        return 'development_test'
    else:
        return 'regression_test'  # Default to regression

def add_decorators(test_dir):
    """Add decorators to all test files."""
    for test_file in Path(test_dir).glob('test_*.py'):
        decorator = analyze_test_file(test_file)
        # Add import and decorators to file
        # (Implementation details omitted for brevity)
```

**Manual Decorator Addition**:

```python
# Template for adding decorators
from wobble import regression_test, integration_test, development_test, slow_test

class TestExistingFeature(unittest.TestCase):
    
    @regression_test  # Add to critical tests
    def test_core_functionality(self):
        # Existing test code unchanged
        pass
    
    @integration_test(scope="service")  # Add to integration tests
    def test_api_endpoint(self):
        # Existing test code unchanged
        pass
    
    @slow_test  # Add to tests taking >5 seconds
    @regression_test
    def test_performance_benchmark(self):
        # Existing test code unchanged
        pass
```

### Directory Reorganization Procedure

**Safe Directory Reorganization**:

```bash
#!/bin/bash
# Script for safe test file reorganization

# Create backup
cp -r tests/ tests_backup/

# Create new directory structure
mkdir -p tests/regression tests/integration tests/development

# Move files based on decorator analysis
# (This would be customized based on specific repository)

# Verify all tests still discoverable
wobble --discover-only

# If successful, remove backup
# rm -rf tests_backup/
```

### CI/CD Migration Procedure

**GitHub Actions Migration**:

```yaml
# Before
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
      run: pip install -e .
    - name: Run tests
      run: python -m unittest discover tests -v

# After
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
      run: pip install -e .
    - name: Run regression tests
      run: wobble --category regression --format json
    - name: Run integration tests
      run: wobble --category integration --format json --exclude-ci
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: test_results.json
```

## Validation Procedures

### Functional Validation

**Test Discovery Validation**:
```bash
# Compare test counts
OLD_COUNT=$(python -m unittest discover tests --dry-run 2>/dev/null | grep -c "test_")
NEW_COUNT=$(wobble --discover-only --format json | jq '.total_tests')

echo "Old test count: $OLD_COUNT"
echo "New test count: $NEW_COUNT"

if [ "$OLD_COUNT" -eq "$NEW_COUNT" ]; then
    echo "✓ Test discovery validation passed"
else
    echo "✗ Test discovery validation failed"
fi
```

**Execution Validation**:
```bash
# Run same tests with both runners and compare results
python -m unittest discover tests -v 2>&1 | grep -E "(FAIL|ERROR|OK)" > unittest_summary.txt
wobble --verbose 2>&1 | grep -E "(✓|✗|PASS|FAIL)" > wobble_summary.txt

# Manual comparison of results
echo "Compare these files for equivalent results:"
echo "unittest_summary.txt"
echo "wobble_summary.txt"
```

### Performance Validation

**Execution Time Comparison**:
```bash
# Benchmark existing runner
echo "Timing existing test runner:"
time python -m unittest discover tests

echo "Timing wobble test runner:"
time wobble

# Acceptable if wobble is within 20% of existing runner
```

**Memory Usage Validation**:
```bash
# Monitor memory usage (Linux/macOS)
echo "Memory usage - existing runner:"
/usr/bin/time -v python -m unittest discover tests 2>&1 | grep "Maximum resident set size"

echo "Memory usage - wobble runner:"
/usr/bin/time -v wobble 2>&1 | grep "Maximum resident set size"
```

## Rollback Procedures

### Emergency Rollback

If critical issues arise during migration:

**Step 1: Immediate CI/CD Rollback**
```yaml
# Revert CI configuration to use original test runner
- name: Run tests (rollback)
  run: python -m unittest discover tests -v
```

**Step 2: Remove Wobble Dependencies**
```bash
# Remove wobble from requirements
sed -i '/wobble/d' requirements.txt
pip uninstall wobble -y
```

**Step 3: Restore Original Structure**
```bash
# If directory structure was changed
cp -r tests_backup/* tests/
```

### Gradual Rollback

For non-emergency situations:

**Phase 1: Parallel Execution**
- Run both old and new test runners in CI
- Compare results and identify discrepancies
- Fix issues while maintaining both systems

**Phase 2: Issue Resolution**
- Address specific compatibility issues
- Update wobble configuration or code
- Re-validate functionality

**Phase 3: Re-migration**
- Resume migration process
- Apply lessons learned from initial attempt
- Implement additional safeguards

## Risk Mitigation

### Pre-Migration Safeguards

**Comprehensive Backup**:
```bash
# Create complete backup before migration
tar -czf pre_migration_backup.tar.gz tests/ pyproject.toml requirements*.txt .github/
```

**Branch Protection**:
```bash
# Perform migration on feature branch
git checkout -b feat/wobble-migration
# Complete migration
# Validate thoroughly
# Merge only after validation
```

**Staged Rollout**:
- Start with least critical repository
- Validate thoroughly before organization-wide rollout
- Maintain parallel systems during transition

### Monitoring and Validation

**Continuous Monitoring**:
- Monitor test execution times
- Track test success rates
- Monitor CI/CD pipeline stability
- Gather developer feedback

**Success Criteria**:
- All existing tests continue to pass
- Test execution time within acceptable range
- CI/CD integration works correctly
- Developer workflow not disrupted

**Failure Criteria**:
- Test failures not present in original runner
- Significant performance degradation (>50% slower)
- CI/CD pipeline failures
- Developer productivity impact

## Post-Migration Activities

### Documentation Updates

**Update Repository Documentation**:
- README.md with wobble usage instructions
- Contributing guidelines with wobble workflow
- CI/CD documentation with new procedures

**Team Training**:
- Wobble CLI usage training
- New test categorization guidelines
- Updated development workflow documentation

### Optimization

**Performance Optimization**:
- Profile test execution for bottlenecks
- Optimize slow test identification
- Configure appropriate CI/CD timeouts

**Workflow Optimization**:
- Create developer aliases for common commands
- Configure IDE integration
- Establish team conventions for test categorization

### Maintenance

**Regular Validation**:
- Periodic comparison with original test runner
- Monitor for performance regressions
- Validate new test additions follow wobble conventions

**Framework Updates**:
- Keep wobble framework updated
- Monitor for new features and improvements
- Contribute feedback and improvements to wobble project
