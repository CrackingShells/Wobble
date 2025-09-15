"""
Test data utilities for Wobble test suite.

This module provides utilities for loading test configurations, creating fake test
directories, and managing test data following Cracking Shells' testing standards.
"""

import json
import tempfile
import shutil
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class WobbleTestDataLoader:
    """Utility class for loading test data from standardized locations."""
    
    def __init__(self):
        """Initialize the test data loader."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.configs_dir = self.test_data_dir / "configs"
        self.responses_dir = self.test_data_dir / "responses"
        self.events_dir = self.test_data_dir / "events"
        self.fake_test_dirs = self.test_data_dir / "fake_test_dirs"
        
        # Ensure directories exist
        self.configs_dir.mkdir(parents=True, exist_ok=True)
        self.responses_dir.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(parents=True, exist_ok=True)
        self.fake_test_dirs.mkdir(parents=True, exist_ok=True)
    
    def load_discovery_config(self, config_name: str) -> Dict[str, Any]:
        """Load a discovery test configuration file."""
        config_path = self.configs_dir / f"{config_name}.json"
        if not config_path.exists():
            self._create_default_discovery_config(config_name)
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def load_expected_output(self, output_name: str) -> Dict[str, Any]:
        """Load expected output format."""
        response_path = self.responses_dir / f"{output_name}.json"
        if not response_path.exists():
            self._create_default_output_response(output_name)
        
        with open(response_path, 'r') as f:
            return json.load(f)
    
    def load_test_events(self, event_name: str) -> Dict[str, Any]:
        """Load test execution events."""
        event_path = self.events_dir / f"{event_name}.json"
        if not event_path.exists():
            self._create_default_test_events(event_name)
        
        with open(event_path, 'r') as f:
            return json.load(f)
    
    def create_fake_test_directory(self, structure_name: str, 
                                 temp_dir: Optional[Path] = None) -> Path:
        """Create fake test directory structure for discovery testing."""
        if temp_dir is None:
            temp_dir = Path(tempfile.mkdtemp(prefix=f"wobble_test_{uuid.uuid4().hex[:8]}_"))
        
        structure_config = FAKE_TEST_STRUCTURES.get(structure_name)
        if not structure_config:
            raise ValueError(f"Unknown test structure: {structure_name}")
        
        # Create directory structure
        for dir_path, files in structure_config['structure'].items():
            full_dir_path = temp_dir / dir_path
            full_dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create test files
            for file_name in files:
                self._create_fake_test_file(full_dir_path / file_name, structure_name)
        
        return temp_dir
    
    def _create_fake_test_file(self, file_path: Path, structure_name: str):
        """Create a fake test file with realistic content."""
        # Extract class and method names from file name
        file_stem = file_path.stem
        if file_stem.startswith('test_'):
            class_name = file_stem[5:].title().replace('_', '')
            method_name = file_stem[5:]
        else:
            class_name = "Sample"
            method_name = "example"
        
        # Get decorator type based on directory
        decorator_type = self._get_decorator_type_from_path(file_path)
        
        # Get template and fill it
        template = TEST_FILE_TEMPLATES.get(decorator_type, TEST_FILE_TEMPLATES['uncategorized'])
        content = template.format(
            class_name=class_name,
            method_name=method_name,
            method_description=f"{method_name} functionality"
        )
        
        file_path.write_text(content)
    
    def _get_decorator_type_from_path(self, file_path: Path) -> str:
        """Determine decorator type from file path."""
        path_str = str(file_path)
        if 'regression' in path_str:
            return 'regression_test'
        elif 'integration' in path_str:
            return 'integration_test'
        elif 'development' in path_str:
            return 'development_test'
        else:
            return 'uncategorized'
    
    def _create_default_discovery_config(self, config_name: str):
        """Create default discovery configuration."""
        default_configs = {
            'mixed_categories_expected': {
                'regression': 5,
                'integration': 3,
                'development': 2,
                'slow': 2,
                'skip_ci': 1,
                'uncategorized': 4
            },
            'large_suite_expected': {
                'regression': 25,
                'integration': 15,
                'development': 10,
                'slow': 8,
                'skip_ci': 3,
                'uncategorized': 12
            },
            'empty_suite_expected': {
                'regression': 0,
                'integration': 0,
                'development': 0,
                'slow': 0,
                'skip_ci': 0,
                'uncategorized': 0
            }
        }
        
        config = default_configs.get(config_name, {})
        config_path = self.configs_dir / f"{config_name}.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _create_default_output_response(self, output_name: str):
        """Create default output response."""
        default_responses = {
            'discovery_outputs': {
                'level_1': {
                    'format': 'counts_only',
                    'includes_test_names': False,
                    'includes_details': False
                },
                'level_2': {
                    'format': 'uncategorized_details',
                    'includes_test_names': True,
                    'includes_details': True,
                    'scope': 'uncategorized_only'
                },
                'level_3': {
                    'format': 'complete_listing',
                    'includes_test_names': True,
                    'includes_details': True,
                    'scope': 'all_tests'
                }
            }
        }
        
        response = default_responses.get(output_name, {})
        response_path = self.responses_dir / f"{output_name}.json"
        with open(response_path, 'w') as f:
            json.dump(response, f, indent=2)
    
    def _create_default_test_events(self, event_name: str):
        """Create default test events."""
        default_events = {
            'test_execution_events': {
                'test_start': {'event_type': 'test_start', 'timestamp': '2024-01-15T14:30:25'},
                'test_pass': {'event_type': 'test_result', 'status': 'PASS'},
                'test_fail': {'event_type': 'test_result', 'status': 'FAIL'},
                'run_end': {'event_type': 'run_end', 'summary': {}}
            }
        }
        
        events = default_events.get(event_name, {})
        event_path = self.events_dir / f"{event_name}.json"
        with open(event_path, 'w') as f:
            json.dump(events, f, indent=2)


# Predefined fake test directory structures
FAKE_TEST_STRUCTURES = {
    'mixed_categories': {
        'description': 'Test suite with all Wobble categories represented',
        'structure': {
            'tests/regression/': [
                'test_auth.py',
                'test_validation.py', 
                'test_core_functionality.py',
                'test_security.py',
                'test_performance.py'
            ],
            'tests/integration/': [
                'test_workflow.py',
                'test_api_integration.py',
                'test_database_integration.py'
            ],
            'tests/development/': [
                'test_experimental_feature.py',
                'test_prototype.py'
            ],
            'tests/': [
                'test_utils.py',  # uncategorized
                'test_helpers.py',  # uncategorized
                'test_legacy.py',  # uncategorized
                'test_misc.py'  # uncategorized
            ]
        }
    },
    'large_suite': {
        'description': 'Large test suite for performance testing',
        'structure': {
            'tests/regression/': [f'test_regression_{i:02d}.py' for i in range(25)],
            'tests/integration/': [f'test_integration_{i:02d}.py' for i in range(15)],
            'tests/development/': [f'test_development_{i:02d}.py' for i in range(10)],
            'tests/': [f'test_uncategorized_{i:02d}.py' for i in range(12)]
        }
    },
    'empty_suite': {
        'description': 'Empty test suite for edge case testing',
        'structure': {
            'tests/': []
        }
    },
    'unicode_tests': {
        'description': 'Test suite with unicode test names',
        'structure': {
            'tests/': [
                'test_unicode_测试.py',
                'test_emoji_🧪.py',
                'test_accents_café.py'
            ]
        }
    }
}

# Test file content templates
TEST_FILE_TEMPLATES = {
    'regression_test': '''"""Regression test module."""
import unittest
from wobble.decorators import regression_test

class Test{class_name}(unittest.TestCase):
    """Test {class_name} functionality."""
    
    @regression_test
    def test_{method_name}(self):
        """Test {method_description}."""
        self.assertTrue(True)
        
    @regression_test
    def test_{method_name}_edge_case(self):
        """Test {method_description} edge case."""
        self.assertEqual(1, 1)
''',
    'integration_test': '''"""Integration test module."""
import unittest
from wobble.decorators import integration_test, slow_test

class Test{class_name}(unittest.TestCase):
    """Test {class_name} integration."""
    
    @integration_test
    @slow_test
    def test_{method_name}_integration(self):
        """Test {method_description} integration."""
        self.assertTrue(True)
''',
    'development_test': '''"""Development test module."""
import unittest
from wobble.decorators import development_test

class Test{class_name}(unittest.TestCase):
    """Test {class_name} development features."""
    
    @development_test
    def test_{method_name}_experimental(self):
        """Test {method_description} experimental feature."""
        self.assertTrue(True)
''',
    'uncategorized': '''"""Uncategorized test module."""
import unittest

class Test{class_name}(unittest.TestCase):
    """Test {class_name} functionality."""
    
    def test_{method_name}(self):
        """Test {method_description}."""
        self.assertTrue(True)
        
    def test_{method_name}_additional(self):
        """Test additional {method_description}."""
        self.assertEqual(1, 1)
'''
}


def cleanup_fake_directory(directory_path: Path):
    """Clean up fake test directory."""
    if directory_path.exists() and directory_path.is_dir():
        shutil.rmtree(directory_path, ignore_errors=True)


# Global instance for easy access
wobble_test_data = WobbleTestDataLoader()

# Convenience functions following organization standards
def load_discovery_config(config_name: str) -> Dict[str, Any]:
    """Load discovery test configuration."""
    return wobble_test_data.load_discovery_config(config_name)

def load_expected_output(output_name: str) -> Dict[str, Any]:
    """Load expected output format."""
    return wobble_test_data.load_expected_output(output_name)

def create_fake_test_directory(structure_name: str, temp_dir: Optional[Path] = None) -> Path:
    """Create fake test directory structure."""
    return wobble_test_data.create_fake_test_directory(structure_name, temp_dir)

def load_test_events(event_name: str) -> Dict[str, Any]:
    """Load test execution events."""
    return wobble_test_data.load_test_events(event_name)


# Standard test result templates
TEST_RESULT_TEMPLATES = {
    'standard_pass': {
        'name': 'test_pass',
        'classname': 'TestClass',
        'status': 'PASS',
        'duration': 0.1,
        'timestamp': '2024-01-15T14:30:25'
    },
    'standard_fail': {
        'name': 'test_fail',
        'classname': 'TestClass',
        'status': 'FAIL',
        'duration': 0.2,
        'timestamp': '2024-01-15T14:30:25',
        'error_info': {
            'type': 'AssertionError',
            'message': 'Test failed',
            'traceback': 'Traceback...'
        }
    },
    'with_error_info': {
        'name': 'test_example',
        'classname': 'TestClass',
        'status': 'FAIL',
        'duration': 0.123,
        'timestamp': '2024-01-15T14:30:25',
        'error_info': {
            'type': 'AssertionError',
            'message': 'Expected 5, got 3',
            'traceback': 'Traceback (most recent call last)...'
        }
    },
    'test_example': {
        'name': 'test_example',
        'classname': 'TestClass',
        'status': 'PASS',
        'duration': 0.123,
        'timestamp': '2024-01-15T14:30:25'
    },
    'test_failure': {
        'name': 'test_failure',
        'classname': 'TestClass',
        'status': 'FAIL',
        'duration': 0.456,
        'timestamp': '2024-01-15T14:30:25',
        'error_info': {
            'type': 'AssertionError',
            'message': 'Expected 5, got 3',
            'traceback': 'Traceback (most recent call last)...'
        }
    }
}

# CLI test configurations
CLI_TEST_CONFIGS = {
    'category_tests': {
        'valid_categories': ['regression', 'integration', 'development', 'all'],
        'invalid_categories': ['invalid', 'unknown'],
        'default_category': 'all'
    },
    'format_tests': {
        'valid_formats': ['standard', 'verbose', 'json', 'minimal'],
        'invalid_formats': ['invalid', 'xml'],
        'default_format': 'standard'
    },
    'file_output_tests': {
        'test_files': {
            'txt': 'test_output.txt',
            'json': 'custom_results.json',
            'auto_timestamp': '',
            'explicit': 'results.txt'
        },
        'verbosity_levels': [1, 2, 3],
        'invalid_verbosity': [0, 4, 5]
    }
}

# Standard command templates
COMMAND_TEMPLATES = {
    'basic_wobble': 'wobble tests/',
    'category_command': 'wobble --category {category}',
    'format_command': 'wobble --format {format}',
    'file_output_command': 'wobble --log-file {filename}',
    'discovery_command': 'wobble --discover-only --path {path}'
}

# Standard timing configurations
TIMING_CONFIGS = {
    'standard_timestamp': '2024-01-15T14:30:25',
    'standard_datetime': '2024-01-15 14:30:25',
    'test_durations': {
        'fast': 0.001,
        'normal': 0.1,
        'slow': 0.5,
        'very_slow': 2.0
    }
}

# File output configurations
FILE_OUTPUT_CONFIGS = {
    'txt_format': {
        'format': 'txt',
        'verbosity': 1,
        'append': False,
        'headers': {
            'run_header': '=== Wobble Test Run ===',
            'summary_header': '=== Summary ==='
        }
    },
    'json_format': {
        'format': 'json',
        'verbosity': 2,
        'append': False,
        'structure': {
            'run_info': {},
            'test_results': []
        }
    }
}


def get_test_result_template(template_name: str) -> Dict[str, Any]:
    """Get a test result template by name."""
    return TEST_RESULT_TEMPLATES.get(template_name, TEST_RESULT_TEMPLATES['standard_pass'])

def get_cli_config(config_name: str) -> Dict[str, Any]:
    """Get CLI test configuration by name."""
    return CLI_TEST_CONFIGS.get(config_name, {})

def get_command_template(template_name: str, **kwargs) -> str:
    """Get formatted command template."""
    template = COMMAND_TEMPLATES.get(template_name, 'wobble tests/')
    return template.format(**kwargs)

def get_timing_config(config_name: str) -> Any:
    """Get timing configuration by name."""
    return TIMING_CONFIGS.get(config_name)

def get_file_output_config(config_name: str) -> Dict[str, Any]:
    """Get file output configuration by name."""
    return FILE_OUTPUT_CONFIGS.get(config_name, {})
