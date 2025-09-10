"""Test discovery engine for wobble framework.

This module provides functionality to discover and categorize tests across
different repository structures and organizational patterns.
"""

import os
import unittest
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from .decorators import get_test_metadata, has_wobble_metadata


class TestDiscoveryEngine:
    """Core test discovery engine for wobble framework.
    
    Supports both hierarchical (tests/regression/, tests/integration/) and
    flat (tests/ with decorator-based categorization) directory structures.
    """
    
    def __init__(self, root_path: str = "."):
        """Initialize the discovery engine.
        
        Args:
            root_path: Root directory to search for tests (default: current directory)
        """
        self.root_path = Path(root_path).resolve()
        self.test_suites = {}
        self.discovered_tests = []
        
    def discover_tests(self, pattern: str = "test*.py") -> Dict[str, List]:
        """Discover all tests in the repository.
        
        Args:
            pattern: File pattern to match test files (default: "test*.py")
            
        Returns:
            Dictionary categorizing discovered tests by type
            
        Example:
            engine = TestDiscoveryEngine()
            tests = engine.discover_tests()
            print(f"Found {len(tests['regression'])} regression tests")
        """
        self.discovered_tests = []
        
        # Find all test directories
        test_dirs = self._find_test_directories()
        
        # Discover tests in each directory
        for test_dir in test_dirs:
            self._discover_in_directory(test_dir, pattern)
        
        # Categorize discovered tests
        categorized = self._categorize_tests()
        
        return categorized
    
    def _find_test_directories(self) -> List[Path]:
        """Find all directories containing tests.
        
        Returns:
            List of Path objects pointing to test directories
        """
        test_dirs = []
        
        # Look for common test directory patterns
        common_patterns = [
            "tests",
            "test", 
            "Tests",
            "Test"
        ]
        
        for pattern in common_patterns:
            test_dir = self.root_path / pattern
            if test_dir.exists() and test_dir.is_dir():
                test_dirs.append(test_dir)
                
                # Also check for subdirectories (hierarchical structure)
                for subdir in test_dir.iterdir():
                    if subdir.is_dir() and not subdir.name.startswith('.'):
                        test_dirs.append(subdir)
        
        return test_dirs
    
    def _discover_in_directory(self, directory: Path, pattern: str) -> None:
        """Discover tests in a specific directory.
        
        Args:
            directory: Directory to search
            pattern: File pattern to match
        """
        try:
            # Use unittest's discovery mechanism
            loader = unittest.TestLoader()
            suite = loader.discover(str(directory), pattern=pattern)
            
            # Extract test information
            for test_group in suite:
                if hasattr(test_group, '_tests'):
                    for test_case in test_group._tests:
                        if hasattr(test_case, '_tests'):
                            for individual_test in test_case._tests:
                                self._process_test(individual_test, directory)
                        else:
                            self._process_test(test_case, directory)
                            
        except Exception as e:
            # Log discovery errors but continue
            print(f"Warning: Could not discover tests in {directory}: {e}")
    
    def _process_test(self, test_case, directory: Path) -> None:
        """Process an individual test case.
        
        Args:
            test_case: The unittest test case
            directory: Directory where the test was found
        """
        test_info = {
            'test_case': test_case,
            'test_method': test_case._testMethodName,
            'test_class': test_case.__class__.__name__,
            'test_module': test_case.__class__.__module__,
            'directory': directory,
            'file_path': None,
            'metadata': {}
        }
        
        # Try to get the actual test method
        try:
            test_method = getattr(test_case, test_case._testMethodName)
            test_info['metadata'] = get_test_metadata(test_method)
            
            # Try to determine file path
            if hasattr(test_case.__class__, '__file__'):
                test_info['file_path'] = Path(test_case.__class__.__file__)
                
        except AttributeError:
            pass
        
        self.discovered_tests.append(test_info)
    
    def _categorize_tests(self) -> Dict[str, List]:
        """Categorize discovered tests by type.
        
        Returns:
            Dictionary with test categories as keys and test lists as values
        """
        categories = {
            'regression': [],
            'integration': [],
            'development': [],
            'uncategorized': []
        }
        
        for test_info in self.discovered_tests:
            category = self._determine_category(test_info)
            categories[category].append(test_info)
        
        return categories
    
    def _determine_category(self, test_info: Dict) -> str:
        """Determine the category of a test.
        
        Args:
            test_info: Test information dictionary
            
        Returns:
            Category string ('regression', 'integration', 'development', 'uncategorized')
        """
        # Check decorator-based categorization first
        metadata = test_info.get('metadata', {})
        if metadata.get('category'):
            return metadata['category']
        
        # Check directory-based categorization
        directory = test_info.get('directory')
        if directory:
            dir_name = directory.name.lower()
            
            if 'regression' in dir_name:
                return 'regression'
            elif 'integration' in dir_name:
                return 'integration'
            elif 'development' in dir_name or 'dev' in dir_name:
                return 'development'
        
        # Default to uncategorized
        return 'uncategorized'
    
    def get_test_count_summary(self) -> Dict[str, int]:
        """Get a summary of test counts by category.
        
        Returns:
            Dictionary with category names and test counts
        """
        if not self.discovered_tests:
            self.discover_tests()
        
        categorized = self._categorize_tests()
        return {category: len(tests) for category, tests in categorized.items()}
    
    def filter_tests(self, 
                    categories: Optional[List[str]] = None,
                    exclude_slow: bool = False,
                    exclude_ci: bool = False) -> List[Dict]:
        """Filter tests based on criteria.
        
        Args:
            categories: List of categories to include (None = all)
            exclude_slow: Whether to exclude slow tests
            exclude_ci: Whether to exclude CI-skipped tests
            
        Returns:
            List of filtered test information dictionaries
        """
        if not self.discovered_tests:
            self.discover_tests()
        
        filtered = []
        
        for test_info in self.discovered_tests:
            # Check category filter
            if categories:
                test_category = self._determine_category(test_info)
                if test_category not in categories:
                    continue
            
            # Check slow test filter
            metadata = test_info.get('metadata', {})
            if exclude_slow and metadata.get('slow'):
                continue
            
            # Check CI skip filter
            if exclude_ci and metadata.get('skip_ci'):
                continue
            
            filtered.append(test_info)
        
        return filtered
    
    def supports_hierarchical_structure(self) -> bool:
        """Check if the repository uses hierarchical test structure.
        
        Returns:
            True if hierarchical structure is detected, False otherwise
        """
        test_dirs = self._find_test_directories()
        
        hierarchical_indicators = [
            'regression', 'integration', 'development', 'unit'
        ]
        
        for test_dir in test_dirs:
            if any(indicator in test_dir.name.lower() 
                   for indicator in hierarchical_indicators):
                return True
        
        return False
    
    def supports_decorator_structure(self) -> bool:
        """Check if the repository uses decorator-based test categorization.
        
        Returns:
            True if decorator-based structure is detected, False otherwise
        """
        if not self.discovered_tests:
            self.discover_tests()
        
        # Check if any tests have wobble metadata
        for test_info in self.discovered_tests:
            if test_info.get('metadata'):
                return True
        
        return False
