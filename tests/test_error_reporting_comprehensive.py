#!/usr/bin/env python3
"""
Comprehensive tests for error reporting in HandyLang.

This test suite covers:
1. Basic error reporting functionality
2. Edge cases like EOF and missing tokens
3. Consistency of error messages
4. Line and column reporting accuracy
5. Showing relevant code context in errors
"""

import os
import unittest
import tempfile

from src.tokenizer import tokenize
from src.parser import Parser


class TestErrorMessageContent(unittest.TestCase):
    """Test the content and formatting of error messages."""
    
    def _parse_code(self, code: str, filename: str = "test.hdy") -> str:
        """
        Parse the given code and return the error message if an error occurs.
        
        Parameters:
            code (str): The code to parse
            filename (str): The filename to use
        Returns:
            str: The error message
        """
        tokens = tokenize(code)
        parser = Parser(tokens, filename=filename)
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        return str(cm.exception)
        
    def test_error_message_includes_custom_filename(self):
        """Error messages should include the specified filename."""
        filename = "special_test.hdy"
        code = "var x = +"
        error_msg = self._parse_code(code, filename)
        
        self.assertIn(filename, error_msg, 
                     f"Error message should include filename '{filename}'")
    
    def test_error_message_includes_line_number_in_multiline_code(self):
        """Error messages should include the correct line number in multiline code."""
        code = """var a = 10
var b = 20

def test() {
    var c = *
}"""
        error_msg = self._parse_code(code)
        
        # The error could be reported on line 4 or 5, depending on the parser implementation
        self.assertTrue(
            "4" in error_msg or "5" in error_msg,
            "Error message should include either line 4 or 5"
        )
    
    def test_error_message_includes_approximate_column_number(self):
        """Error messages should include an approximate column number."""
        code = "var x = 10 + * 5"
        error_msg = self._parse_code(code)
        
        # Test for column number in a more flexible way
        has_column_indicator = False
        for i in range(11, 16):  # Check columns 11-15
            if f":{i}:" in error_msg or f", {i}:" in error_msg or f" {i}:" in error_msg:
                has_column_indicator = True
                break
        
        self.assertTrue(has_column_indicator, 
                       "Error message should include a column number near the error")
    
    def test_error_message_includes_source_code_line(self):
        """Error messages should include the source code line with the error."""
        code_line = "var x = 10 + * 5"
        error_msg = self._parse_code(code_line)
        
        self.assertIn(code_line, error_msg, 
                     "Error message should include the code line with the error")
    
    def test_error_message_includes_caret_pointer(self):
        """Error messages should include a caret (^) pointing to the error location."""
        code = "var x = 10 + * 5"
        error_msg = self._parse_code(code)
        
        self.assertIn("^", error_msg, 
                     "Error message should include a caret (^) pointing to the error")


class TestTokenizerErrors(unittest.TestCase):
    """Test error reporting from the tokenizer."""
    
    def _tokenize_with_error(self, code: str) -> str:
        """
        Tokenize the given code and return the error message if an error occurs.
        
        Parameters:
            code (str): The code to tokenize
        Returns:
            str: The error message
        """
        with self.assertRaises(Exception) as cm:
            tokenize(code)
            
        return str(cm.exception)
    
    def test_invalid_dollar_sign_reports_unexpected_character(self):
        """Dollar sign character should be reported as invalid with appropriate message."""
        code = "var x = 10 + $ 5"
        error_msg = self._tokenize_with_error(code)
        
        # Check for expected error message patterns
        self.assertTrue(
            "unexpected character" in error_msg.lower() or
            "invalid character" in error_msg.lower() or
            "illegal character" in error_msg.lower(),
            "Error message should mention the unexpected/invalid character"
        )
        self.assertIn("$", error_msg)
    
    def test_invalid_character_error_includes_caret(self):
        """Invalid character errors should include a caret pointer."""
        code = "var x = 10 + $ 5"
        error_msg = self._tokenize_with_error(code)
        self.assertIn("^", error_msg)
    
    def test_multiline_code_error_reports_correct_line(self):
        """For multiline code, the error should report the correct line number."""
        code = """var a = 10
var b = 20
var c = $
var d = 30"""
        error_msg = self._tokenize_with_error(code)
        
        self.assertIn("line 3", error_msg.lower())
    
    def test_multiline_code_error_shows_offending_line(self):
        """For multiline code, the error should show the specific line with the error."""
        code = """var a = 10
var b = 20
var c = $
var d = 30"""
        error_msg = self._tokenize_with_error(code)
        
        self.assertIn("var c = $", error_msg)
    
    def test_multiline_code_error_includes_caret(self):
        """For multiline code, the error should include a caret pointer."""
        code = """var a = 10
var b = 20
var c = $
var d = 30"""
        error_msg = self._tokenize_with_error(code)
        self.assertIn("^", error_msg)


class TestParserErrors(unittest.TestCase):
    """Test error reporting from the parser."""
    
    def _parse_with_error(self, code: str, filename: str = "test.hdy") -> str:
        """
        Parse the given code and return the error message if an error occurs.
        
        Parameters:
            code (str): The code to parse
            filename (str): The filename to use
        Returns:
            str: The error message
        """
        tokens = tokenize(code)
        parser = Parser(tokens, filename=filename)
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        return str(cm.exception)
    
    def test_incomplete_expression_produces_relevant_error(self):
        """Incomplete expressions should produce a relevant error message."""
        code = "var x = 10 +"
        error_msg = self._parse_with_error(code)
        
        # Check that the error mentions something being unexpected or expected
        self.assertTrue(
            "unexpected" in error_msg.lower() or 
            "expected" in error_msg.lower() or
            "missing" in error_msg.lower(),
            "Error message should indicate a problem with the expression"
        )
    
    def test_error_on_expression_with_trailing_operator(self):
        """Expressions with trailing operators should report errors on the correct line."""
        code = """var x = 10
var y = 20 ;
var z = 30 +"""
        error_msg = self._parse_with_error(code)
        
        # Check that the error refers to line 3
        self.assertIn("3", error_msg, 
                     "Error message should reference line 3")
    
    def test_mismatched_braces_in_if_statement(self):
        """Mismatched braces in if statements should produce a relevant error."""
        code = """def test() {
    var x = 10
    if (x > 5) {
        print("Greater than 5")
    
}"""
        error_msg = self._parse_with_error(code)
        
        # The error should be related to block structure or braces
        self.assertTrue(
            "}" in error_msg or 
            "brace" in error_msg.lower() or
            "block" in error_msg.lower() or
            "expected" in error_msg.lower(),
            "Error message should indicate a problem with braces or block structure"
        )


class TestEdgeCases(unittest.TestCase):
    """Test error reporting for edge cases."""
    
    def test_empty_file_parses_successfully(self):
        """An empty file should parse without errors."""
        code = ""
        tokens = tokenize(code)
        parser = Parser(tokens, filename="empty.hdy")
        
        # This should not raise an error
        ast = parser.parse()
        self.assertIsNotNone(ast, "Parsing an empty file should not fail")
    
    def test_eof_in_expression_includes_filename_in_error(self):
        """EOF in an expression should report an error with the filename."""
        code = "var x = 10 +"
        tokens = tokenize(code)
        parser = Parser(tokens, filename="eof.hdy")
        
        with self.assertRaises(Exception) as cm:
            parser.parse()
            
        error_msg = str(cm.exception)
        self.assertIn("eof.hdy", error_msg, 
                     "Error message should include the filename")
    
    def test_extremely_long_line_with_invalid_character(self):
        """A very long line with an invalid character should report the error correctly."""
        # Create a very long expression
        code = "var x = " + " + ".join([f"{i}" for i in range(100)]) + " + $"
        
        # This should raise a tokenizer error due to $
        with self.assertRaises(Exception) as cm:
            tokenize(code)
            
        error_msg = str(cm.exception)
        
        # Test that the error message is informative
        self.assertTrue(
            "unexpected character" in error_msg.lower() or
            "invalid character" in error_msg.lower() or
            "illegal character" in error_msg.lower(),
            "Error message should mention the unexpected/invalid character"
        )
        
        # Test that the problematic character is identified
        self.assertIn("$", error_msg, 
                     "Error message should include the problematic character")


class TestFileIntegration(unittest.TestCase):
    """Test error reporting with file integration."""
    
    def test_error_in_temp_file_includes_filename(self):
        """Errors in a temporary file should include the filename in the error message."""
        with tempfile.NamedTemporaryFile(suffix=".hdy", mode="w+", delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write('''def test() {
    var x = 10
    print(x
}''')
            
        try:
            with open(tmp_path, 'r') as f:
                code = f.read()
                
            tokens = tokenize(code)
            parser = Parser(tokens, filename=tmp_path)
            
            with self.assertRaises(Exception) as cm:
                parser.parse()
                
            error_msg = str(cm.exception)
            
            # Check that the error message includes the filename
            self.assertIn(os.path.basename(tmp_path), error_msg, 
                         "Error message should include the filename")
        finally:
            os.unlink(tmp_path)
    
    def test_error_in_temp_file_shows_code_context(self):
        """Errors in a temporary file should show the code context in the error message."""
        with tempfile.NamedTemporaryFile(suffix=".hdy", mode="w+", delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write('''def test() {
    var x = 10
    print(x
}''')
            
        try:
            with open(tmp_path, 'r') as f:
                code = f.read()
                
            tokens = tokenize(code)
            parser = Parser(tokens, filename=tmp_path)
            
            with self.assertRaises(Exception) as cm:
                parser.parse()
                
            error_msg = str(cm.exception)
            
            # Check that the error message includes some code context from the file
            # The specific context shown may vary depending on the parser implementation
            self.assertTrue(
                "def test" in error_msg or
                "var x" in error_msg or
                "print" in error_msg,
                "Error message should include some code context from the file"
            )
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
