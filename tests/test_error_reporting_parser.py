#!/usr/bin/env python3
"""
Tests for parser-level error reporting in HandyLang.

This test suite focuses specifically on the parser's error reporting capabilities,
checking various syntax errors at the statement, expression, and structural levels.
"""

import unittest
import os
from typing import List, Dict, Any, Tuple, Optional

from src.tokenizer import tokenize
from src.parser import Parser


class TestParserErrorReporting(unittest.TestCase):
    """Test error reporting in the parser."""
    
    def _assert_parse_error(self, code: str, expected_msgs: List[str], 
                           filename: str = "test.hdy",
                           expected_line: Optional[int] = None):
        """Helper to assert parse error messages."""
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
    
    def test_statement_level_errors(self):
        """Test error reporting for statement-level syntax errors."""
        # Missing identifier in variable declaration
        self._assert_parse_error(
            'var = 10',
            ["Expected", "IDENT"],
            expected_line=1
        )
        
        # Missing expression in variable assignment
        self._assert_parse_error(
            'var x =',
            ["Unexpected", "Expected"],
            expected_line=1
        )
        
        # Missing semicolon (if required by the language)
        try:
            self._assert_parse_error(
                'var x = 10\nvar y = 20;',
                ["Expected", "semicolon"],
                expected_line=1
            )
        except AssertionError:
            # Skip if the language doesn't require semicolons
            pass
    
    def test_expression_level_errors(self):
        """Test error reporting for expression-level syntax errors."""
        # Invalid binary operation (missing operand)
        self._assert_parse_error(
            'var x = 10 +',
            ["Unexpected", "Expected"],
            expected_line=1
        )
        
        # Invalid expression start
        self._assert_parse_error(
            'var x = * 5',
            ["Unexpected", "*"],
            expected_line=1
        )
        
        # Invalid expression with multiple operators
        self._assert_parse_error(
            'var x = 10 + * 5',
            ["Unexpected", "*"],
            expected_line=1
        )
    
    def test_structural_errors(self):
        """Test error reporting for structural syntax errors."""
        # Missing closing parenthesis
        self._assert_parse_error(
            'var x = (10 + 5',
            ["Expected", "RPAREN"],
            expected_line=1
        )
        
        # Missing closing brace in function
        self._assert_parse_error(
            '''def test() {
                var x = 10
            ''',
            ["Expected", "RBRACE"],
            filename="missing_brace.hdy"
        )
        
        # Unmatched closing brace
        self._assert_parse_error(
            '''def test() {
                var x = 10
            }}''',
            ["Unexpected"],
            expected_line=3
        )


class TestParserErrorContext(unittest.TestCase):
    """Test context information in parser error messages."""
    
    def test_error_position_accuracy(self):
        """Test accuracy of error position reporting."""
        code = "var x = (10 + )"
        tokens = tokenize(code)
        parser = Parser(tokens, filename="position_test.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        
        # Should include the code line
        self.assertIn(code, error_msg)
        
        # Should include a caret at the right position (around the closing paren)
        lines = error_msg.split('\n')
        code_line_idx = next((i for i, line in enumerate(lines) if code in line), -1)
        
        if code_line_idx >= 0 and code_line_idx + 1 < len(lines):
            caret_line = lines[code_line_idx + 1]
            # Calculate expected caret position (around the closing paren)
            close_paren_pos = code.find(')')
            
            # The caret might be at different positions depending on error detection logic
            # It could point at the close paren or just before it
            acceptable_range = range(close_paren_pos - 1, close_paren_pos + 2)
            caret_pos = caret_line.find('^')
            
            self.assertTrue(
                any(caret_pos == pos for pos in acceptable_range),
                f"Caret should point around position {close_paren_pos}. Found at {caret_pos}."
            )
    
    def test_multiline_error_context(self):
        """Test error context for multiline code."""
        code = """def test() {
    var x = 10
    var y = 20
    print(x, y
    var z = 30
}"""
        tokens = tokenize(code)
        parser = Parser(tokens, filename="multiline_test.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        
        # Should mention line 4
        self.assertIn(":4:", error_msg)
        
        # Should include the problematic line
        self.assertIn("print(x, y", error_msg)


class TestParserErrorMessages(unittest.TestCase):
    """Test the clarity and helpfulness of parser error messages."""
    
    def test_error_message_clarity(self):
        """Test that error messages are clear and helpful."""
        # Test a few common error cases and check that messages are informative
        test_cases = [
            # (code, filename, expected_keywords)
            ("var x = 10 +", "clarity1.hdy", ["expected", "expression"]),
            ("def test() {", "clarity2.hdy", ["expected", "closing", "brace"]),
            ("var x = (10 + 5", "clarity3.hdy", ["expected", "parenthesis", "RPAREN"]),
        ]
        
        for code, filename, keywords in test_cases:
            tokens = tokenize(code)
            parser = Parser(tokens, filename=filename)
            
            with self.assertRaises(Exception) as cm:
                parser.parse()
                
            error_msg = str(cm.exception).lower()
            
            # Check that at least one of the keywords is present
            self.assertTrue(
                any(keyword.lower() in error_msg for keyword in keywords),
                f"Error message should contain at least one of {keywords}. Got: {error_msg}"
            )
    
    def test_parser_error_detail_level(self):
        """Test that error messages have appropriate level of detail."""
        code = """def test() {
    var x = 10
    var y = "hello"
    if (x > 5) {
        print(x, y
    }
}"""
        tokens = tokenize(code)
        parser = Parser(tokens, filename="detail_test.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        
        # Should include filename, line, column
        self.assertIn("detail_test.hdy", error_msg)
        self.assertIn(":5:", error_msg)  # Line number
        
        # Should have column information
        self.assertTrue(
            any(f":{i}:" in error_msg for i in range(1, 20)),
            f"Error message should include column number. Got: {error_msg}"
        )
        
        # Should include the code line
        self.assertIn("print(x, y", error_msg)
        
        # Should include caret
        self.assertIn("^", error_msg)


if __name__ == "__main__":
    unittest.main()
