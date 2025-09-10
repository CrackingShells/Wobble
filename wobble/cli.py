"""Command-line interface for wobble testing framework.

This module provides the main CLI entry point and argument parsing for the
wobble testing framework.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional

from .discovery import TestDiscoveryEngine
from .runner import TestRunner
from .output import OutputFormatter


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for wobble CLI.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog='wobble',
        description='Centralized testing framework for Cracking Shells',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wobble                          # Run all tests
  wobble --category regression    # Run only regression tests
  wobble --exclude-slow          # Skip slow tests
  wobble --format json           # Output results in JSON format
  wobble --discover-only         # Only discover tests, don't run them
        """
    )
    
    # Test selection options
    parser.add_argument(
        '--category', '-c',
        choices=['regression', 'integration', 'development', 'all'],
        default='all',
        help='Test category to run (default: all)'
    )
    
    parser.add_argument(
        '--exclude-slow',
        action='store_true',
        help='Exclude slow-running tests'
    )
    
    parser.add_argument(
        '--exclude-ci',
        action='store_true',
        help='Exclude tests marked to skip in CI'
    )
    
    parser.add_argument(
        '--pattern', '-p',
        default='test*.py',
        help='File pattern for test discovery (default: test*.py)'
    )
    
    # Output options
    parser.add_argument(
        '--format', '-f',
        choices=['standard', 'verbose', 'json', 'minimal'],
        default='standard',
        help='Output format (default: standard)'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    # Discovery options
    parser.add_argument(
        '--discover-only',
        action='store_true',
        help='Only discover tests, do not run them'
    )
    
    parser.add_argument(
        '--list-categories',
        action='store_true',
        help='List available test categories and exit'
    )
    
    # Repository options
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Path to repository root (default: current directory)'
    )
    
    # Verbosity options
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='Increase verbosity (can be used multiple times)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress all output except errors'
    )
    
    return parser


def detect_repository_root(start_path: str = ".") -> Optional[Path]:
    """Detect the repository root directory.
    
    Args:
        start_path: Starting path for detection
        
    Returns:
        Path to repository root, or None if not found
    """
    current = Path(start_path).resolve()
    
    # Look for common repository indicators
    indicators = [
        '.git',
        'pyproject.toml',
        'setup.py',
        'requirements.txt',
        'Pipfile',
        'package.json'
    ]
    
    while current != current.parent:
        for indicator in indicators:
            if (current / indicator).exists():
                return current
        current = current.parent
    
    return None


def main() -> int:
    """Main entry point for wobble CLI.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Detect repository root if not explicitly provided
    if args.path == '.':
        repo_root = detect_repository_root()
        if repo_root:
            args.path = str(repo_root)
    
    # Validate path
    if not Path(args.path).exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        return 1
    
    # Initialize components
    discovery_engine = TestDiscoveryEngine(args.path)
    output_formatter = OutputFormatter(
        format_type=args.format,
        use_color=not args.no_color,
        verbosity=args.verbose,
        quiet=args.quiet
    )
    
    try:
        # Discover tests
        if args.verbose > 0:
            output_formatter.print_info(f"Discovering tests in: {args.path}")
        
        discovered_tests = discovery_engine.discover_tests(pattern=args.pattern)
        
        # Handle list categories option
        if args.list_categories:
            output_formatter.print_test_categories(discovered_tests)
            return 0
        
        # Handle discover-only option
        if args.discover_only:
            output_formatter.print_discovery_summary(discovered_tests)
            return 0
        
        # Filter tests based on arguments
        categories = None if args.category == 'all' else [args.category]
        filtered_tests = discovery_engine.filter_tests(
            categories=categories,
            exclude_slow=args.exclude_slow,
            exclude_ci=args.exclude_ci
        )
        
        if not filtered_tests:
            output_formatter.print_warning("No tests found matching the specified criteria")
            return 0
        
        # Run tests
        test_runner = TestRunner(output_formatter)
        results = test_runner.run_tests(filtered_tests)
        
        # Print results
        output_formatter.print_test_results(results)
        
        # Return appropriate exit code
        if results.get('failures', 0) > 0 or results.get('errors', 0) > 0:
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        output_formatter.print_error("Test execution interrupted by user")
        return 130
    
    except Exception as e:
        output_formatter.print_error(f"Unexpected error: {e}")
        if args.verbose > 1:
            import traceback
            traceback.print_exc()
        return 1


def version() -> str:
    """Get wobble version string.
    
    Returns:
        Version string
    """
    try:
        from . import __version__
        return __version__
    except ImportError:
        return "unknown"


if __name__ == '__main__':
    sys.exit(main())
