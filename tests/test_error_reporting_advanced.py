#!/usr/bin/env python3
"""
Advanced error reporting tests for HandyLang.

This test suite focuses on more complex edge cases and advanced error scenarios:
1. Nested error contexts 
2. EOF errors in various contexts
3. Error recovery and cascading errors
4. Complex syntactic structures
5. Special characters and escaping
"""

import unittest
import os
import tempfile
from typing import List, Optional, Dict, Any

from src.tokenizer import tokenize
from src.parser import Parser


class TestNestedContextErrors(unittest.TestCase):
    """Test error reporting in nested contexts like functions, blocks, etc."""
    
    def _parse_with_error(self, code: str, filename: str = "test.hdy") -> str:
        """Helper to parse code and return error message."""
        tokens = tokenize(code)
        parser = Parser(tokens, filename=filename)
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        return str(cm.exception)
    
    def test_deeply_nested_function(self):
        """Test error reporting in deeply nested functions."""
        code = """def outer() {
    def middle() {
        def inner() {
            var x = 10
            print(x, y,
            var z = 20
        }
    }
}"""
        error_msg = self._parse_with_error(code)
        
        self.assertIn("5:", error_msg, "Error should point to line 5")
        self.assertIn("print(x, y,", error_msg, "Error should include the line content")
    
    def test_nested_block_statements(self):
        """Test error reporting in nested block statements."""
        code = """def test() {
    if (x > 10) {
        if (y > 20) {
            var z = *
        }
    }
}"""
        error_msg = self._parse_with_error(code)
        
        self.assertIn("4:", error_msg, "Error should point to line 4")
        self.assertIn("var z = *", error_msg, "Error should include the line content")


class TestEOFErrors(unittest.TestCase):
    """Test error reporting for various EOF scenarios."""
    
    def test_eof_in_string(self):
        """Test error reporting for EOF in a string literal."""
        code = 'var s = "unterminated string'
        
        # This might be caught by either tokenizer or parser
        try:
            tokens = tokenize(code)
            parser = Parser(tokens, filename="eof_string.hdy")
            parser.parse()
            self.fail("Should have raised an error for unterminated string")
        except Exception as e:
            error_msg = str(e)
            self.assertTrue(
                "unterminated" in error_msg.lower() or 
                "unexpected" in error_msg.lower() or
                "string" in error_msg.lower(),
                f"Error message should mention unterminated string: {error_msg}"
            )
    
    def test_eof_in_block(self):
        """Test error reporting for EOF in a code block."""
        code = """def test() {
    var x = 10
    print(x)"""  # Missing closing brace
        
        tokens = tokenize(code)
        parser = Parser(tokens, filename="eof_block.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        self.assertTrue(
            "}" in error_msg or 
            "brace" in error_msg.lower() or
            "block" in error_msg.lower() or
            "expected" in error_msg.lower(),
            f"Error message should mention missing brace or block: {error_msg}"
        )


class TestComplexStructures(unittest.TestCase):
    """Test error reporting in complex language structures."""
    
    def _parse_with_error(self, code: str, filename: str = "test.hdy") -> str:
        """Helper to parse code and return error message."""
        tokens = tokenize(code)
        parser = Parser(tokens, filename=filename)
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        return str(cm.exception)
    
    def test_function_with_complex_params(self):
        """Test error reporting in functions with complex parameter lists."""
        code = """def func(a: number, b: string, c: = 10) {
    print(a, b, c)
}"""
        error_msg = self._parse_with_error(code)
        
        self.assertIn("1:", error_msg, "Error should point to line 1")
        self.assertIn("c: =", error_msg, "Error should include the problematic code")
    
    def test_complex_expression(self):
        """Test error reporting in complex expressions."""
        code = """def calc() {
    var result = (10 + 20) * (30 / (40 - )) 
    return result
}"""
        error_msg = self._parse_with_error(code)
        
        self.assertIn("2:", error_msg, "Error should point to line 2")
        self.assertIn(")", error_msg, "Error should mention the problematic token")


class TestSpecialCases(unittest.TestCase):
    """Test error reporting for special cases and language features."""
    
    def test_unmatched_list_brackets(self):
        """Test error reporting for unmatched list brackets."""
        code = "var list = [1, 2, 3, 4"  # Missing closing bracket
        
        tokens = tokenize(code)
        parser = Parser(tokens, filename="list.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        self.assertTrue(
            "]" in error_msg or 
            "bracket" in error_msg.lower() or
            "expected" in error_msg.lower(),
            f"Error message should mention missing bracket: {error_msg}"
        )
    
    def test_dictionary_syntax_error(self):
        """Test error reporting for dictionary syntax errors."""
        code = """var dict = {
    "key1": "value1",
    "key2": 
}"""
        tokens = tokenize(code)
        parser = Parser(tokens, filename="dict.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        self.assertIn("3:", error_msg, "Error should point to line 3")


class TestErrorConsistency(unittest.TestCase):
    """Test consistency of error messages across different error types."""
    
    def _get_error_message(self, code: str, filename: str = "test.hdy") -> str:
        """Helper to get error message from parsing code."""
        try:
            tokens = tokenize(code)
            parser = Parser(tokens, filename=filename)
            parser.parse()
            return ""  # No error
        except Exception as e:
            return str(e)
    
    def test_error_format_consistency(self):
        """Test that all error messages follow a consistent format."""
        test_cases = [
            ("var x = +", "token_error.hdy"),
            ("def test() {\nvar x = 10\n}", "indent_error.hdy"),
            ("var list = [1, 2, 3", "bracket_error.hdy"),
            ("def test() {\nprint(x\n}", "paren_error.hdy"),
        ]
        
        error_messages = []
        for code, filename in test_cases:
            error_msg = self._get_error_message(code, filename)
            if error_msg:
                error_messages.append(error_msg)
        
        # Check that all error messages have the filename
        for i, error_msg in enumerate(error_messages):
            filename = test_cases[i][1]
            self.assertIn(filename, error_msg, 
                         f"Error message should include filename: {error_msg}")
            
            # Check for line number format (should contain something like ":1:")
            self.assertTrue(
                any(f":{n}:" in error_msg for n in range(1, 10)),
                f"Error message should include line number: {error_msg}"
            )
            
            # Check for caret indicator
            self.assertIn("^", error_msg, 
                         f"Error message should include caret pointer: {error_msg}")


if __name__ == "__main__":
    unittest.main()
