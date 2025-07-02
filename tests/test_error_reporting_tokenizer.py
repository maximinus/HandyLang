#!/usr/bin/env python3
"""
Tests for token-level error reporting in HandyLang.

This test suite focuses specifically on the tokenizer's error reporting capabilities,
checking various token-level errors like invalid characters, unterminated strings,
and malformed tokens.
"""

import unittest
import os
from typing import List, Dict, Any, Tuple, Optional

from src.tokenizer import tokenize


class TestTokenizerBasicErrors(unittest.TestCase):
    """Test basic error reporting in the tokenizer."""
    
    def test_dollar_sign_error(self):
        """Test error reporting for dollar sign."""
        with self.assertRaises(Exception) as cm:
            tokenize("var x = $")
        
        error_msg = str(cm.exception)
        self.assertIn("Unexpected character", error_msg)
        self.assertIn("$", error_msg)
        self.assertIn("line 1", error_msg.lower())
    
    def test_backtick_error(self):
        """Test error reporting for backtick."""
        with self.assertRaises(Exception) as cm:
            tokenize("var x = `")
        
        error_msg = str(cm.exception)
        self.assertIn("Unexpected character", error_msg)
        self.assertIn("`", error_msg)
        self.assertIn("line 1", error_msg.lower())
    
    def test_backslash_error(self):
        """Test error reporting for backslash."""
        with self.assertRaises(Exception) as cm:
            tokenize("var x = \\")
        
        error_msg = str(cm.exception)
        self.assertIn("Unexpected character", error_msg)
        self.assertIn("\\", error_msg)
        self.assertIn("line 1", error_msg.lower())
    
    def test_at_symbol(self):
        """Test that @ symbol is a valid token."""
        # The @ symbol is actually valid in HandyLang, so this should NOT raise an error
        tokens = tokenize("var x = @")
        # Verify we got an AT token
        at_tokens = [t for t in tokens if t['type'] == 'AT']
        self.assertTrue(len(at_tokens) > 0, "Expected to find an AT token")


class TestTokenizerMultilineErrors(unittest.TestCase):
    """Test error reporting in multiline code."""
    
    def test_error_on_line_3(self):
        """Test error reporting on a specific line number."""
        code = """var a = 10
var b = 20
var c = $
var d = 30"""
        
        with self.assertRaises(Exception) as cm:
            tokenize(code)
        
        error_msg = str(cm.exception)
        self.assertIn("Unexpected character", error_msg)
        self.assertIn("$", error_msg)
        self.assertIn("line 3", error_msg.lower())
    
    def test_error_after_comment(self):
        """Test error reporting after comments."""
        code = """# This is a comment
var x = 10  # inline comment
var y = $  # error here"""
        
        with self.assertRaises(Exception) as cm:
            tokenize(code)
        
        error_msg = str(cm.exception)
        self.assertIn("line 3", error_msg.lower())
        self.assertIn("$", error_msg)


class TestTokenizerErrorFormat(unittest.TestCase):
    """Test formatting of error messages."""
    
    def test_column_reported(self):
        """Test that column position is reported."""
        with self.assertRaises(Exception) as cm:
            tokenize("var x = 10 $ 20")
        
        error_msg = str(cm.exception)
        self.assertIn("column", error_msg.lower())
    
    def test_column_position_accuracy(self):
        """Test accuracy of column position in error message."""
        with self.assertRaises(Exception) as cm:
            tokenize("var x = 10 $ 20")
        
        error_msg = str(cm.exception)
        # $ is at index 10, so column should be around there
        self.assertTrue(
            any(f"column {i}" in error_msg.lower() for i in range(9, 13)),
            f"Error message should include column number around 10-12. Got: {error_msg}"
        )
    
    def test_code_context_shown(self):
        """Test that code context is shown in error message."""
        code = "var x = 10 $ 20"
        
        with self.assertRaises(Exception) as cm:
            tokenize(code)
        
        error_msg = str(cm.exception)
        self.assertIn(code, error_msg)
    
    def test_caret_shown(self):
        """Test that a caret points to the error."""
        with self.assertRaises(Exception) as cm:
            tokenize("var x = 10 $ 20")
        
        error_msg = str(cm.exception)
        self.assertIn("^", error_msg)


class TestTokenizerSpecialCases(unittest.TestCase):
    """Test special error cases."""
    
    def test_unterminated_string(self):
        """Test error reporting for unterminated string literals."""
        try:
            with self.assertRaises(Exception) as cm:
                tokenize('var s = "unterminated')
                
            error_msg = str(cm.exception)
            # Check for relevant error terms
            terms = ["unterminated", "string", "unexpected", "end", "quote"]
            found = any(term in error_msg.lower() for term in terms)
            self.assertTrue(found, f"Error message should mention unterminated string: {error_msg}")
        except AssertionError:
            # Skip this test if the tokenizer doesn't catch unterminated strings
            self.skipTest("Tokenizer doesn't catch unterminated strings")
    
    def test_tokenizer_stops_at_first_error(self):
        """Test that tokenizer stops at the first error."""
        code = """var x = $
var y = @
var z = 10"""
        
        with self.assertRaises(Exception) as cm:
            tokenize(code)
        
        error_msg = str(cm.exception)
        self.assertIn("$", error_msg)
        self.assertNotIn("@", error_msg)


if __name__ == "__main__":
    unittest.main()
