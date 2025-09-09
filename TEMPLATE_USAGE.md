# Python Repository Template Usage Guide

## Overview

This minimal Python repository template provides the essential components needed to create a new Cracking Shells Python project. It includes only the proven, necessary patterns extracted from existing organizational repositories.

## Template Variables

When creating a new repository from this template, replace these variables throughout all files:

- `{{PROJECT_NAME}}`: The repository/project name (e.g., "my-awesome-tool")
- `{{PACKAGE_NAME}}`: The Python package name in snake_case (e.g., "my_awesome_tool")
- `{{PROJECT_DESCRIPTION}}`: Brief description of what the project does

## Quick Start

### 1. Create New Repository

1. Copy this template directory to your new project location
2. Replace all template variables in all files
3. Rename the `{{PACKAGE_NAME}}` directory to your actual package name
4. Initialize git repository

### 2. Variable Replacement

Replace these variables in all files:

```bash
# Example replacements:
{{PROJECT_NAME}} → "Hatch-Analytics"
{{PACKAGE_NAME}} → "hatch_analytics"  
{{PROJECT_DESCRIPTION}} → "Analytics tools for Hatch ecosystem data"
```

**Files to update:**

- `pyproject.toml`
- `package.json`
- `README.md`
- `CONTRIBUTING.md`
- `.github/workflows/semantic-release.yml`
- `.github/workflows/commitlint.yml`
- `.commitlintrc.json`
- `.releaserc.json`
- `tests/test_basic.py`
- `{{PACKAGE_NAME}}/__init__.py`
- `{{PACKAGE_NAME}}/core.py`

### 3. Initial Setup

```bash
# Navigate to your new project directory
cd path/to/{{PROJECT_NAME}}

# Install in development mode
pip install -e .

# Install Node.js dependencies for semantic release
npm install

# Run initial tests to verify everything works
python -m unittest discover tests -v

# Test basic import
python -c "import your_package_name; print('Success!')"
```

### 4. First Commit

```bash
# Initialize git repository
git init
git add .

# Use conventional commit format
git commit -m "feat: initial project setup from template"

# Add remote and push
git remote add origin https://github.com/CrackingShells/your-project-name.git
git push -u origin main
```

## What's Included

### Essential Configuration

- **`pyproject.toml`**: Standard Python project configuration with organizational defaults
- **`package.json`**: Semantic release and conventional commit tooling
- **`LICENSE`**: GNU AGPL v3 (organizational standard)

### GitHub Integration

- **`.github/workflows/semantic-release.yml`**: Automated versioning and releases
- **`.github/workflows/commitlint.yml`**: Conventional commit validation
  - **`.commitlintrc.json`**: Commit message linting rules
- **Semantic release configuration**: Automated changelog and version management
  - **`.releaserc.json`**: Release configuration

### Basic Package Structure

- **`{{PACKAGE_NAME}}/`**: Main package directory with `__init__.py` and `core.py`
- **`tests/`**: Unittest-based testing structure (wobble-compatible)
- **Documentation**: README.md and CONTRIBUTING.md with organizational standards

### Development Workflow

- **Conventional commits**: Standardized commit message format
- **Semantic versioning**: Automated version management
- **Basic testing**: Unittest framework compatible with future wobble integration

## What's NOT Included (Future Enhancements)

### Code Quality Tools (Deferred)

- **Black**: Code formatting
- **isort**: Import sorting  
- **flake8**: Linting
- **mypy**: Type checking
- **Pre-commit hooks**: Automated quality enforcement

**Rationale**: These tools add complexity beyond the minimal template goal. They should be added when:

- Repository has multiple contributors
- Code quality becomes a concern
- Organizational standards are established for these tools

### Advanced Testing (Deferred)

- **Enhanced test CLI**: Will be provided by future `wobble` framework
- **Test decorators**: Will be provided by `wobble`
- **Advanced test organization**: Will be provided by `wobble`

**Rationale**: The organization is developing a centralized `wobble` testing framework that will provide these capabilities as a dependency.

### Comprehensive Documentation (Deferred)

- **Full documentation structure**: Can be added when project matures
- **API documentation**: Can be generated when needed
- **Advanced GitHub issue templates**: Can be added based on project needs

## Future Migration Path

### Wobble Integration

When the `wobble` testing framework becomes available:

1. Add `wobble>=1.0.0` to dependencies in `pyproject.toml`
2. `wobble` will provide enhanced CLI, decorators, and test organization
3. Existing unittest tests will continue to work
4. Gradually adopt `wobble` features as needed

### Code Quality Tools

When ready to add code quality tools:

1. Add development dependencies to `pyproject.toml`:

   ```toml
   [project.optional-dependencies]
   dev = [
       "black>=23.0.0",
       "isort>=5.0.0", 
       "flake8>=6.0.0",
       "mypy>=1.0.0",
   ]
   ```

2. Add tool configurations to `pyproject.toml`
3. Add pre-commit hooks configuration
4. Update GitHub workflows to include quality checks

### Documentation Enhancement

When project matures:

1. Create `docs/` directory following organizational guidelines
2. Add comprehensive user and developer documentation
3. Set up documentation generation and deployment
4. Add API reference documentation

## Organizational Compliance

This template ensures compliance with Cracking Shells standards:

- **✅ Semantic release**: Automated versioning and changelog generation
- **✅ Conventional commits**: Standardized commit message format
- **✅ License**: GNU AGPL v3 organizational standard
- **✅ Python version**: Requires Python 3.12+ for consistency
- **✅ Testing framework**: Uses unittest (wobble-compatible)
- **✅ Package structure**: Follows organizational patterns

## Support and Questions

- **Template issues**: Report problems with the template itself
- **Project-specific help**: Use your project's issue tracker
- **Organizational standards**: Refer to `.github/instructions/` documentation
- **Wobble framework**: Wait for official release and documentation

This minimal template provides a solid foundation that can be enhanced as your project grows and organizational standards evolve.
