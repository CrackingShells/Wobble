"""Test runner for wobble framework.

This module provides the core test execution functionality with enhanced
output formatting and timing capabilities.
"""

import unittest
import time
import sys
from typing import List, Dict, Any, Optional, Union
from io import StringIO
from datetime import datetime

from .output import OutputFormatter
from .enhanced_output import EnhancedOutputFormatter
from .data_structures import TestResult, TestStatus, ErrorInfo


class WobbleTestResult(unittest.TestResult):
    """Enhanced test result class with timing and metadata tracking."""

    def __init__(self, output_formatter: Union[OutputFormatter, EnhancedOutputFormatter]):
        super().__init__()
        self.output_formatter = output_formatter
        self.test_timings = {}
        self.test_metadata = {}
        self.start_time = None
        self.current_test = None
        self._test_execution_count = {}  # Track execution count per test
        self.enhanced_mode = isinstance(output_formatter, EnhancedOutputFormatter)

    def startTest(self, test):
        """Called when a test starts."""
        super().startTest(test)
        self.current_test = test
        self.start_time = time.time()

        # Track execution count for this test
        test_id = self._get_test_id(test)
        self._test_execution_count[test_id] = self._test_execution_count.get(test_id, 0) + 1

        # Extract test metadata (only on first execution)
        if self._test_execution_count[test_id] == 1:
            test_method = getattr(test, test._testMethodName, None)
            if test_method:
                try:
                    from .decorators import get_test_metadata
                    self.test_metadata[test] = get_test_metadata(test_method)
                except ImportError:
                    # Decorators module may not exist yet
                    self.test_metadata[test] = {}

        # Notify output formatter of test start
        if self.enhanced_mode:
            self.output_formatter.notify_test_start(test)
        else:
            self.output_formatter.print_test_start(test)

    def stopTest(self, test):
        """Called when a test ends."""
        super().stopTest(test)

        if self.start_time:
            duration = time.time() - self.start_time
            test_id = self._get_test_id(test)

            # Store timing with execution count to avoid overwrites
            timing_key = f"{test_id}_exec_{self._test_execution_count[test_id]}"
            self.test_timings[timing_key] = duration

            # Also store the most recent timing for the test object (for compatibility)
            self.test_timings[test] = duration

        self.current_test = None
        self.start_time = None

    def _get_test_id(self, test):
        """Generate a unique identifier for a test."""
        return f"{test.__class__.__module__}.{test.__class__.__name__}.{test._testMethodName}"

    def _calculate_current_test_duration(self):
        """Calculate the duration of the currently running test."""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0
    
    def addSuccess(self, test):
        """Called when a test passes."""
        super().addSuccess(test)
        duration = self._calculate_current_test_duration()

        if self.enhanced_mode:
            # Create TestResult and notify enhanced formatter
            test_result = self._create_test_result(test, TestStatus.PASS, duration)
            self.output_formatter.notify_test_end(test_result)
        else:
            self.output_formatter.print_test_success(test, duration)

    def addError(self, test, err):
        """Called when a test has an error."""
        super().addError(test, err)
        duration = self._calculate_current_test_duration()

        if self.enhanced_mode:
            # Create TestResult with error info and notify enhanced formatter
            error_info = self._create_error_info(err)
            test_result = self._create_test_result(test, TestStatus.ERROR, duration, error_info)
            self.output_formatter.notify_test_end(test_result)
        else:
            self.output_formatter.print_test_error(test, err, duration)

    def addFailure(self, test, err):
        """Called when a test fails."""
        super().addFailure(test, err)
        duration = self._calculate_current_test_duration()

        if self.enhanced_mode:
            # Create TestResult with error info and notify enhanced formatter
            error_info = self._create_error_info(err)
            test_result = self._create_test_result(test, TestStatus.FAIL, duration, error_info)
            self.output_formatter.notify_test_end(test_result)
        else:
            self.output_formatter.print_test_failure(test, err, duration)

    def addSkip(self, test, reason):
        """Called when a test is skipped."""
        super().addSkip(test, reason)
        duration = self.test_timings.get(test, 0)

        if self.enhanced_mode:
            # Create TestResult for skip and notify enhanced formatter
            test_result = self._create_test_result(test, TestStatus.SKIP, duration)
            test_result.metadata['skip_reason'] = reason
            self.output_formatter.notify_test_end(test_result)
        else:
            self.output_formatter.print_test_skip(test, reason, duration)

    def _get_test_id(self, test):
        """Get a unique identifier for a test case.

        Args:
            test: unittest.TestCase instance

        Returns:
            String identifier for the test
        """
        return f"{test.__class__.__module__}.{test.__class__.__name__}.{test._testMethodName}"

    def _create_test_result(self, test, status: TestStatus, duration: float,
                          error_info: Optional[ErrorInfo] = None) -> TestResult:
        """Create a TestResult from a test case.

        Args:
            test: unittest.TestCase instance
            status: Test status
            duration: Test execution time
            error_info: Optional error information

        Returns:
            TestResult instance
        """
        return TestResult(
            name=test._testMethodName,
            classname=test.__class__.__name__,
            status=status,
            duration=duration,
            timestamp=datetime.now(),
            metadata=self.test_metadata.get(test, {}),
            error_info=error_info
        )

    def _create_error_info(self, err_info) -> ErrorInfo:
        """Create ErrorInfo from error tuple.

        Args:
            err_info: Error information tuple (type, value, traceback)

        Returns:
            ErrorInfo instance
        """
        import traceback

        exc_type, exc_value, exc_traceback = err_info

        return ErrorInfo(
            type=exc_type.__name__,
            message=str(exc_value),
            traceback=''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        )


class TestRunner:
    """Core test runner for wobble framework."""

    def __init__(self, output_formatter: Union[OutputFormatter, EnhancedOutputFormatter]):
        """Initialize the test runner.

        Args:
            output_formatter: Output formatter instance for test results
        """
        self.output_formatter = output_formatter
        self.total_start_time = None
        self.enhanced_mode = isinstance(output_formatter, EnhancedOutputFormatter)
        
    def run_tests(self, test_infos: List[Dict]) -> Dict[str, Any]:
        """Run a list of tests and return results.
        
        Args:
            test_infos: List of test information dictionaries from discovery
            
        Returns:
            Dictionary containing test execution results and statistics
        """
        if not test_infos:
            return {
                'tests_run': 0,
                'failures': 0,
                'errors': 0,
                'skipped': 0,
                'success_rate': 100.0,
                'total_time': 0.0,
                'results': []
            }
        
        # Create test suite from test infos
        suite = self._create_test_suite(test_infos)
        
        # Create custom test result
        result = WobbleTestResult(self.output_formatter)

        # Start test run (enhanced mode handles command reconstruction)
        if self.enhanced_mode:
            # Try to reconstruct the command from CLI args
            try:
                from .cli import reconstruct_command
                command = reconstruct_command()
            except:
                command = "wobble"  # Fallback
            self.output_formatter.start_test_run(command, len(test_infos))
        else:
            self.output_formatter.print_test_run_header(len(test_infos))

        # Run tests
        self.total_start_time = time.time()
        suite.run(result)
        total_time = time.time() - self.total_start_time
        
        # Calculate statistics
        success_rate = 0.0
        if result.testsRun > 0:
            successful_tests = result.testsRun - len(result.failures) - len(result.errors)
            success_rate = (successful_tests / result.testsRun) * 100.0
        
        # End test run for enhanced mode
        if self.enhanced_mode:
            exit_code = 1 if (len(result.failures) > 0 or len(result.errors) > 0) else 0
            self.output_formatter.end_test_run(exit_code)

        # Compile results
        results = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped),
            'success_rate': success_rate,
            'total_time': total_time,
            'test_timings': result.test_timings,
            'test_metadata': result.test_metadata,
            'failure_details': result.failures,
            'error_details': result.errors,
            'skip_details': result.skipped
        }

        return results
    
    def _create_test_suite(self, test_infos: List[Dict]) -> unittest.TestSuite:
        """Create a test suite from test information.
        
        Args:
            test_infos: List of test information dictionaries
            
        Returns:
            unittest.TestSuite containing the tests
        """
        suite = unittest.TestSuite()
        
        for test_info in test_infos:
            test_case = test_info.get('test_case')
            if test_case:
                suite.addTest(test_case)
        
        return suite
    
    def run_single_test(self, test_case) -> Dict[str, Any]:
        """Run a single test case.
        
        Args:
            test_case: unittest.TestCase instance
            
        Returns:
            Dictionary containing single test results
        """
        suite = unittest.TestSuite([test_case])
        result = WobbleTestResult(self.output_formatter)
        
        start_time = time.time()
        suite.run(result)
        total_time = time.time() - start_time
        
        return {
            'test_case': test_case,
            'passed': len(result.failures) == 0 and len(result.errors) == 0,
            'failure': result.failures[0] if result.failures else None,
            'error': result.errors[0] if result.errors else None,
            'skipped': result.skipped[0] if result.skipped else None,
            'duration': total_time,
            'metadata': result.test_metadata.get(test_case, {})
        }
    
    def validate_test_environment(self) -> Dict[str, bool]:
        """Validate the test environment and dependencies.
        
        Returns:
            Dictionary with validation results
        """
        validations = {}
        
        # Check Python version
        validations['python_version'] = sys.version_info >= (3, 7)
        
        # Check unittest availability
        try:
            import unittest
            validations['unittest_available'] = True
        except ImportError:
            validations['unittest_available'] = False
        
        # Check colorama availability (for colored output)
        try:
            import colorama
            validations['colorama_available'] = True
        except ImportError:
            validations['colorama_available'] = False
        
        return validations
    
    def get_performance_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance summary from test results.
        
        Args:
            results: Test results dictionary
            
        Returns:
            Dictionary containing performance metrics
        """
        timings = results.get('test_timings', {})
        
        if not timings:
            return {
                'total_tests': 0,
                'total_time': 0.0,
                'average_time': 0.0,
                'fastest_test': None,
                'slowest_test': None
            }
        
        times = list(timings.values())
        
        # Find fastest and slowest tests
        fastest_test = min(timings.items(), key=lambda x: x[1])
        slowest_test = max(timings.items(), key=lambda x: x[1])
        
        return {
            'total_tests': len(timings),
            'total_time': sum(times),
            'average_time': sum(times) / len(times),
            'fastest_test': {
                'name': self._get_test_name(fastest_test[0]),
                'time': fastest_test[1]
            },
            'slowest_test': {
                'name': self._get_test_name(slowest_test[0]),
                'time': slowest_test[1]
            }
        }
    
    def _get_test_name(self, test_case) -> str:
        """Get a readable name for a test case.
        
        Args:
            test_case: unittest.TestCase instance
            
        Returns:
            Human-readable test name
        """
        if hasattr(test_case, '_testMethodName'):
            class_name = test_case.__class__.__name__
            method_name = test_case._testMethodName
            return f"{class_name}.{method_name}"
        
        return str(test_case)
