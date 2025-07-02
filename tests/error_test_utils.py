"""
Test utilities for HandyLang error reporting.

This module provides helper functions and classes for testing error reporting
functionality in HandyLang tokenizer and parser.
"""

import os
import difflib
from typing import List, Dict, Any, Tuple, Optional, Union
import unittest

from src.tokenizer import tokenize
from src.parser import Parser


class ErrorReportingTestCase(unittest.TestCase):
    """Base class for testing error reporting functionality."""
    
    def assert_tokenize_error(self, code: str, 
                             expected_msgs: List[str], 
                             expected_line: Optional[int] = None):
        """
        Assert that tokenizing the given code raises an error with expected messages.
        
        Parameters:
            code (str): The code to tokenize.
            expected_msgs (List[str]): Substrings expected in the error message.
            expected_line (Optional[int]): The expected line number in the error message.
        """
        with self.assertRaises(Exception) as cm:
            tokenize(code)
        
        error_msg = str(cm.exception)
        for msg in expected_msgs:
            self.assertIn(msg, error_msg, 
                         f"Error message should contain '{msg}'.\nGot: {error_msg}")
        
        if expected_line is not None:
            self.assertIn(f"line {expected_line}", error_msg,
                        f"Error message should mention line {expected_line}.\nGot: {error_msg}")
    
    def assert_parse_error(self, code: str, 
                          expected_msgs: List[str], 
                          filename: str = "test.hdy",
                          expected_line: Optional[int] = None):
        """
        Assert that parsing the given code raises an error with expected messages.
        
        Parameters:
            code (str): The code to parse.
            expected_msgs (List[str]): Substrings expected in the error message.
            filename (str): The filename to use for the parser.
            expected_line (Optional[int]): The expected line number in the error message.
        """
        tokens = tokenize(code)
        parser = Parser(tokens, filename=filename)
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
        
        error_msg = str(cm.exception)
        for msg in expected_msgs:
            self.assertIn(msg, error_msg, 
                         f"Error message should contain '{msg}'.\nGot: {error_msg}")
        
        self.assertIn(filename, error_msg,
                    f"Error message should contain filename '{filename}'.\nGot: {error_msg}")
        
        if expected_line is not None:
            line_indicator = f":{expected_line}:"
            self.assertIn(line_indicator, error_msg,
                        f"Error message should contain '{line_indicator}'.\nGot: {error_msg}")


def create_sample_test_cases():
    """
    Create a list of sample error test cases.
    
    Returns:
        List[Tuple[str, str, List[str], Optional[int]]]: List of (name, code, expected_msgs, line).
    """
    return [
        # Lexical errors
        ("Invalid character", 
         "var x = @", 
         ["Unexpected character", "@"], 
         1),
        
        # Missing closing parenthesis
        ("Missing closing parenthesis", 
         "def test() {\n    print(\"Hello\"\n}", 
         ["Expected RPAREN"], 
         2),
        
        # Missing closing brace
        ("Missing closing brace", 
         "def test() {\n    print(\"Hello\")\n", 
         ["Expected RBRACE"], 
         None),
        
        # Invalid function definition
        ("Invalid function definition", 
         "def 123() {}", 
         ["Expected IDENT"], 
         1),
        
        # Invalid variable assignment
        ("Invalid variable assignment", 
         "var x = ;", 
         ["Unexpected token"], 
         1),
    ]


def run_sample_tests():
    """Run the sample error test cases and print results."""
    class SampleErrorTests(ErrorReportingTestCase):
        pass
    
    # Add test methods to the test class
    test_cases = create_sample_test_cases()
    for i, (name, code, expected_msgs, line) in enumerate(test_cases):
        def create_test_method(code, expected_msgs, line):
            def test_method(self):
                try:
                    self.assert_parse_error(code, expected_msgs, expected_line=line)
                except Exception as e:
                    print(f"❌ {name}: {e}")
                    raise
                print(f"✅ {name}")
            return test_method
        
        test_method = create_test_method(code, expected_msgs, line)
        test_method.__name__ = f"test_{i}_{name.lower().replace(' ', '_')}"
        setattr(SampleErrorTests, test_method.__name__, test_method)
    
    # Run the tests
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleErrorTests)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    run_sample_tests()
