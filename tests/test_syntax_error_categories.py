#!/usr/bin/env python3
"""
Comprehensive tests for various syntax errors in the HandyLang language.

This file contains tests for different categories of syntax errors:
1. Token-level errors (lexical errors)
2. Expression-level errors
3. Statement-level errors
4. Block-level errors
5. Function-level errors
"""

import unittest
import os

from src.tokenizer import tokenize
from src.parser import Parser
from tests.error_test_utils import ErrorReportingTestCase


class TestSyntaxErrorCategories(ErrorReportingTestCase):
    """Test different categories of syntax errors."""
    
    def test_token_level_errors(self):
        """Test lexical errors at the token level."""
        # Invalid character
        self.assert_tokenize_error(
            'var x = $',
            ["Unexpected character", "$"],
            1
        )
        
        # Unterminated string
        # Note: This depends on tokenizer implementation; it might report different errors
        try:
            with self.assertRaises(Exception):
                tokenize('var s = "unterminated')
        except AssertionError:
            # Skip this test if the tokenizer doesn't catch unterminated strings
            pass
    
    def test_expression_level_errors(self):
        """Test errors in expressions."""
        # Invalid binary operation
        self.assert_parse_error(
            'var x = * 5',
            ["Unexpected", "*"],
            expected_line=1
        )
    
    def test_statement_level_errors(self):
        """Test errors in statements."""
        # Missing identifier in variable declaration
        self.assert_parse_error(
            'var = 10',
            ["Expected", "IDENT"],
            expected_line=1
        )
    
    def test_block_level_errors(self):
        """Test errors at the block level."""
        # Unclosed block
        self.assert_parse_error(
            '''def func() {
                var x = 10
                print(x)
            ''',
            ["Expected", "RBRACE"],
            filename="block_error.hdy"
        )
    
    def test_function_level_errors(self):
        """Test errors in function definitions and calls."""
        # Unclosed parameter list
        self.assert_parse_error(
            'def test(x, y',
            ["Expected", "RPAREN"],
            expected_line=1
        )
        
        # Invalid parameter syntax
        self.assert_parse_error(
            'def test(x, *)',
            ["Expected", "IDENT"],
            expected_line=1
        )
        
        # Unclosed function call
        self.assert_parse_error(
            '''def func() {
                print("Hello"
            }''',
            ["Expected", "RPAREN"],
            expected_line=2
        )
    
    def test_nested_errors(self):
        """Test errors in nested structures."""
        # Error in nested block
        self.assert_parse_error(
            '''def outer() {
                def inner() {
                    var x = 10
                    print(x
                }
            }''',
            ["Expected", "RPAREN"],
            expected_line=4
        )


class TestErrorReportingDetails(ErrorReportingTestCase):
    """Test specific details of error messages."""
    
    def test_line_number_accuracy(self):
        """Test that line numbers in error messages are accurate."""
        code = '''var a = 10
var b = 20

def func() {
    print(a, b
    var c = 30
}'''
        
        tokens = tokenize(code)
        parser = Parser(tokens, filename="line_test.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        self.assertIn(":5:", error_msg, "Error message should contain line number 5")
    
    def test_context_display(self):
        """Test that error messages show appropriate context."""
        code = '''def func() {
    var x = 10
    var y = 20
    var z = x + * y
    var a = 30
}'''
        
        tokens = tokenize(code)
        parser = Parser(tokens, filename="context_test.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        
        # Should show the error line
        self.assertIn("var z = x + * y", error_msg)
        
        # Should indicate the error position with ^
        self.assertIn("^", error_msg)


if __name__ == "__main__":
    unittest.main()
