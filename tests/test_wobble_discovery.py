"""Tests for wobble test discovery functionality.

This module tests the test discovery engine that finds and categorizes tests
across different repository structures.
"""

import unittest
import tempfile
import os
from pathlib import Path
from wobble.discovery import TestDiscoveryEngine


class TestWobbleDiscoveryEngine(unittest.TestCase):
    """Test wobble test discovery engine."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.discovery_engine = TestDiscoveryEngine(self.temp_dir)
        # Generate unique module name for this test instance
        import uuid
        self.unique_id = str(uuid.uuid4())[:8]
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        import sys
        
        # Clean up any modules that may have been imported from temp directories
        modules_to_remove = []
        for module_name in sys.modules:
            if self.temp_dir in str(sys.modules[module_name].__file__ if hasattr(sys.modules[module_name], '__file__') and sys.modules[module_name].__file__ else ''):
                modules_to_remove.append(module_name)
        
        for module_name in modules_to_remove:
            del sys.modules[module_name]
        
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_discovery_engine_initialization(self):
        """Test that discovery engine initializes correctly."""
        engine = TestDiscoveryEngine(".")
        self.assertIsNotNone(engine.root_path)
        self.assertEqual(engine.test_suites, {})
        self.assertEqual(engine.discovered_tests, [])
    
    def test_find_test_directories(self):
        """Test finding test directories."""
        # Create test directory structure
        test_dir = Path(self.temp_dir) / "tests"
        test_dir.mkdir()
        
        # Create a test file with unique name
        test_file = test_dir / f"test_sample_{self.unique_id}.py"
        test_file.write_text(f"""
import unittest

class TestSample{self.unique_id.title()}(unittest.TestCase):
    def test_example(self):
        self.assertTrue(True)
""")
        
        # Test discovery
        test_dirs = self.discovery_engine._find_test_directories()
        
        # Should find the tests directory
        self.assertTrue(any(str(test_dir) in str(d) for d in test_dirs))
    
    def test_supports_hierarchical_structure_detection(self):
        """Test detection of hierarchical test structure."""
        # Create hierarchical structure
        base_tests = Path(self.temp_dir) / "tests"
        base_tests.mkdir()
        
        regression_dir = base_tests / "regression"
        regression_dir.mkdir()
        
        integration_dir = base_tests / "integration"
        integration_dir.mkdir()
        
        # Create test files with unique names
        (regression_dir / f"test_core_{self.unique_id}.py").write_text(f"""
import unittest
class TestCore{self.unique_id.title()}(unittest.TestCase):
    def test_functionality(self):
        pass
""")
        
        (integration_dir / f"test_api_{self.unique_id}.py").write_text(f"""
import unittest
class TestAPI{self.unique_id.title()}(unittest.TestCase):
    def test_endpoint(self):
        pass
""")
        
        # Test hierarchical detection
        self.assertTrue(self.discovery_engine.supports_hierarchical_structure())
    
    def test_get_test_count_summary(self):
        """Test getting test count summary."""
        # Create a simple test structure
        test_dir = Path(self.temp_dir) / "tests"
        test_dir.mkdir()
        
        test_file = test_dir / f"test_sample_{self.unique_id}.py"
        test_file.write_text(f"""
import unittest

class TestSample{self.unique_id.title()}(unittest.TestCase):
    def test_one(self):
        self.assertTrue(True)
    
    def test_two(self):
        self.assertTrue(True)
""")
        
        # Get summary
        summary = self.discovery_engine.get_test_count_summary()
        
        # Should have discovered tests
        total_tests = sum(summary.values())
        self.assertGreater(total_tests, 0)
    
    def test_filter_tests_by_category(self):
        """Test filtering tests by category."""
        # This test validates the filtering mechanism
        # In a real scenario, tests would be categorized by decorators or directory structure
        
        # Discover all tests first
        self.discovery_engine.discover_tests()
        
        # Test filtering (should not crash even with no categorized tests)
        filtered = self.discovery_engine.filter_tests(categories=['regression'])
        self.assertIsInstance(filtered, list)
        
        # Test excluding slow tests
        filtered_no_slow = self.discovery_engine.filter_tests(exclude_slow=True)
        self.assertIsInstance(filtered_no_slow, list)
        
        # Test excluding CI tests
        filtered_no_ci = self.discovery_engine.filter_tests(exclude_ci=True)
        self.assertIsInstance(filtered_no_ci, list)


class TestWobbleDiscoveryIntegration(unittest.TestCase):
    """Integration tests for discovery engine with real test files."""
    
    def test_discover_current_repository_tests(self):
        """Test discovering tests in the current repository."""
        # Use current directory (should find our own tests)
        engine = TestDiscoveryEngine(".")
        
        discovered = engine.discover_tests()
        
        # Should find test categories
        self.assertIsInstance(discovered, dict)
        self.assertIn('uncategorized', discovered)
        
        # Should find some tests (at least our own)
        total_tests = sum(len(tests) for tests in discovered.values())
        self.assertGreater(total_tests, 0)
    
    def test_discovery_with_different_patterns(self):
        """Test discovery with different file patterns."""
        engine = TestDiscoveryEngine(".")
        
        # Test with default pattern
        default_tests = engine.discover_tests(pattern="test*.py")
        
        # Test with alternative pattern
        alt_tests = engine.discover_tests(pattern="*test.py")
        
        # Both should return valid results
        self.assertIsInstance(default_tests, dict)
        self.assertIsInstance(alt_tests, dict)
    
    def test_categorization_logic(self):
        """Test the test categorization logic."""
        engine = TestDiscoveryEngine(".")
        engine.discover_tests()
        
        # Test the categorization method with sample test info
        sample_test_info = {
            'metadata': {'category': 'regression'},
            'directory': Path('tests/regression')
        }
        
        category = engine._determine_category(sample_test_info)
        self.assertEqual(category, 'regression')
        
        # Test directory-based categorization
        dir_test_info = {
            'metadata': {},
            'directory': Path('tests/integration')
        }
        
        category = engine._determine_category(dir_test_info)
        self.assertEqual(category, 'integration')
        
        # Test uncategorized
        uncategorized_info = {
            'metadata': {},
            'directory': Path('tests')
        }
        
        category = engine._determine_category(uncategorized_info)
        self.assertEqual(category, 'uncategorized')


if __name__ == '__main__':
    unittest.main(verbosity=2)
