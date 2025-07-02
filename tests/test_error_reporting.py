#!/usr/bin/env python3

import os
import unittest

from src.tokenizer import tokenize
from src.parser import Parser


class TestErrorReporting(unittest.TestCase):
    """Test error reporting in the parser with sample code that contains errors."""
    
    def test_error_messages(self):
        """Test that parser errors contain expected messages."""
        # Sample code with a syntax error
        code_samples = [
            # Missing closing brace
            (
                "sample1.hdy",
                """def test() {
    print("Hello")
    var x = 10
""",
                "Expected RBRACE"
            ),
            # Incorrect function call
            (
                "sample2.hdy",
                """def test() {
    print(
    var x = 10
}""",
                "Expected RPAREN"
            ),
            # Invalid expression
            (
                "sample3.hdy",
                """def test() {
    var x = *
}""",
                "Unexpected token in expression"
            )
        ]
        
        for filename, code, expected_error in code_samples:
            with self.subTest(filename=filename):
                try:
                    tokens = tokenize(code)
                    parser = Parser(tokens, filename=filename)
                    ast = parser.parse()
                    self.fail(f"Expected syntax error but parsing succeeded: {ast}")
                except Exception as e:
                    self.assertIn(expected_error, str(e), 
                                 f"Error message does not contain expected text: '{expected_error}'")


if __name__ == "__main__":
    unittest.main()
