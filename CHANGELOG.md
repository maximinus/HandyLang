# Changelog

All notable changes to the HandyLang project will be documented in this file.

## [0.1.1] - Test Suite Modernization

### Changed
- Refactored the test suite to use standard unittest practices
- Removed custom test frameworks and sys.path manipulation hacks
- Modernized test structure with proper package organization
- Added `setup.py` for editable installs
- Added proper package structure with `__init__.py` files in src/ and tests/

### Fixed
- Updated `test_tokens.py` to handle the new token dictionary format without losing simplicity
- Added `simplify_tokens()` helper function to convert token dictionaries to simple tuples
- Made token tests more robust with flexible assertions for compound operators
- Fixed test_error_reporting_tokenizer.py to work with current implementation
- Fixed test_error_reporting_comprehensive.py with improved assertions and test organization
- Fixed test_error_reporting_unittest.py by breaking up large tests into focused methods

### Removed
- Removed custom test runner (tests/run_error_tests.py)
- Eliminated all sys.path.insert manipulations from test and example files

## [0.1] - Initial Version

- Initial implementation of HandyLang
- Basic tokenizer, parser, and interpreter
- Error reporting system
- Custom test framework
- Example programs in examples/ directory
