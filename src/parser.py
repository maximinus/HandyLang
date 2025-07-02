from typing import List, Dict, Optional, Any, Tuple, Union

from src.ast_nodes import *


class Parser:
    def __init__(self, tokens: List[Dict[str, Any]], filename: str):
        """
        Initialize a new Parser instance.
        
        Parameters:
            tokens (List[Dict[str, Any]]): List of token dictionaries from the tokenizer.
            filename (str): The name of the file being parsed.
        """
        self.tokens = tokens
        self.pos = 0
        self.filename = filename

    def peek(self) -> Dict[str, Any]:
        """
        Look at the current token without advancing.
        
        Returns:
            Dict[str, Any]: The current token or {'type': None, 'value': None} if at end of tokens.
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return {'type': None, 'value': None}

    def advance(self) -> Dict[str, Any]:
        """
        Get the current token and advance to the next one.
        
        Returns:
            Dict[str, Any]: The current token.
        """
        token = self.peek()
        self.pos += 1
        return token

    def expect(self, kind: str, value: Optional[str] = None) -> Dict[str, Any]:
        """
        Expect a token of a specific kind and optionally with a specific value.
        Raises a SyntaxError if the expectation is not met.
        
        Parameters:
            kind (str): The expected token type.
            value (Optional[str]): The expected token value, if any.
            
        Returns:
            Dict[str, Any]: The token if it matches the expectation.
        Raises:
            SyntaxError: If the token doesn't match the expectation.
        """
        token = self.advance()
        if token['type'] != kind or (value is not None and token['value'] != value):
            expected = f"{kind}"
            if value:
                expected += f" with value '{value}'"
            actual = f"{token['type']}"
            if 'value' in token:
                actual += f" with value '{token['value']}'"
            self._report_error(f"Expected {expected}, got {actual}")
        return token

    def _report_error(self, message: str) -> None:
        """
        Report a syntax error with context information.
        
        Parameters:
            message (str): The error message.
        Raises:
            SyntaxError: Always raised with contextual information.
        """
        # Get the current token or the previous one if we've advanced too far
        if self.pos >= len(self.tokens) and self.pos > 0:
            token = self.tokens[self.pos - 1]
        elif self.pos < len(self.tokens):
            token = self.tokens[self.pos]
        else:
            # No tokens available
            raise SyntaxError(f"{self.filename}: {message}")
        
        line = token.get('line', 0)
        col = token.get('col', 0)
        line_text = token.get('line_text', '')
        
        # Format the error message with file, line, column and code context
        error_msg = f"{self.filename}:{line}:{col}: {message}"
        
        if line_text:
            # Add the line of code
            error_msg += f"\n\n{line}: {line_text}\n"
            
            # Add a pointer to the problematic token
            pointer = " " * (len(str(line)) + 2)  # Account for "line: " prefix
            pointer += " " * (col - 1)  # Position the caret under the token
            pointer += "^"
            error_msg += pointer
            
        raise SyntaxError(error_msg)

    def parse(self) -> Program:
        """
        Parse the entire program.
        
        Returns:
            Program: The AST for the entire program.
        """
        try:
            statements = []
            while self.peek()['type']:
                statements.append(self.parse_statement())
            return Program(statements)
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Parsing error: {str(e)}")
            raise

    def parse_statement(self) -> Any:
        """
        Parse a single statement.
        
        Returns:
            Any: An AST node representing the statement.
        Raises:
            SyntaxError: If the statement cannot be parsed.
        """
        try:
            token = self.peek()
            kind, value = token['type'], token['value']
            
            if kind == 'KEYWORD':
                if value == 'var':
                    return self.parse_var_decl()
                elif value == 'const':
                    return self.parse_const_decl()
                elif value == 'def':
                    return self.parse_function_def()
                elif value == 'if':
                    return self.parse_if_stmt()
                elif value == 'for':
                    return self.parse_for_stmt()
                elif value == 'match':
                    return self.parse_match_stmt()
                elif value == 'return':
                    return self.parse_return_stmt()
                elif value == 'raise':
                    return self.parse_raise_stmt()
                elif value == 'print':
                    return self.parse_print_statement()
                # add more as needed
            return self.parse_expression()
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Error parsing statement: {str(e)}")
            raise

    def parse_var_decl(self) -> VarDecl:
        """
        Parse a variable declaration.
        
        Returns:
            VarDecl: An AST node representing the variable declaration.
        Raises:
            SyntaxError: If the variable declaration cannot be parsed.
        """
        try:
            self.expect('KEYWORD', 'var')
            name = self.expect('IDENT')['value']
            type_ = None
            if self.peek()['type'] == 'COLON':
                self.advance()
                type_ = self.expect('KEYWORD')['value']
            value = None
            if self.peek()['type'] == 'ASSIGN':
                self.advance()
                value = self.parse_expression()
            return VarDecl(name, type_, value)
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Error parsing variable declaration: {str(e)}")
            raise

    def parse_const_decl(self) -> ConstDecl:
        """
        Parse a constant declaration.
        
        Returns:
            ConstDecl: An AST node representing the constant declaration.
        Raises:
            SyntaxError: If the constant declaration cannot be parsed.
        """
        try:
            self.expect('KEYWORD', 'const')
            name = self.expect('IDENT')['value']
            type_ = None
            if self.peek()['type'] == 'COLON':
                self.advance()
                type_ = self.expect('KEYWORD')['value']
            self.expect('ASSIGN')
            value = self.parse_expression()
            return ConstDecl(name, type_, value)
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Error parsing constant declaration: {str(e)}")
            raise

    def parse_function_def(self) -> FunctionDef:
        """
        Parse a function definition.
        
        Returns:
            FunctionDef: An AST node representing the function definition.
        Raises:
            SyntaxError: If the function definition cannot be parsed.
        """
        try:
            self.expect('KEYWORD', 'def')
            name = self.expect('IDENT')['value']
            self.expect('LPAREN')
            params = self.parse_param_list()
            self.expect('RPAREN')
            return_type = None
            if self.peek()['type'] == 'ARROW':
                self.advance()
                return_type = self.expect('KEYWORD')['value']
            body = self.parse_block()
            return FunctionDef(name, params, return_type, body)
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Error parsing function definition: {str(e)}")
            raise

    def parse_param_list(self) -> List[Param]:
        """
        Parse a function parameter list.
        
        Returns:
            List[Param]: A list of parameter AST nodes.
        Raises:
            SyntaxError: If the parameter list cannot be parsed.
        """
        try:
            params = []
            while self.peek()['type'] != 'RPAREN':
                pname = self.expect('IDENT')['value']
                ptype = None
                if self.peek()['type'] == 'COLON':
                    self.advance()
                    ptype = self.expect('KEYWORD')['value']
                default = None
                if self.peek()['type'] == 'ASSIGN':
                    self.advance()
                    default = self.parse_expression()
                params.append(Param(pname, ptype, default))
                if self.peek()['type'] == 'COMMA':
                    self.advance()
            return params
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Error parsing parameter list: {str(e)}")
            raise

    def parse_block(self) -> Block:
        """
        Parse a code block enclosed in braces.
        
        Returns:
            Block: An AST node representing the block of statements.  
        Raises:
            SyntaxError: If the block cannot be parsed.
        """
        try:
            self.expect('LBRACE')
            statements = []
            while self.peek()['type'] != 'RBRACE':
                statements.append(self.parse_statement())
            self.expect('RBRACE')
            return Block(statements)
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Error parsing code block: {str(e)}")
            raise

    def parse_expression(self) -> Union[Literal, Identifier]:
        """
        Parse an expression.
        Note: This is a simplified placeholder implementation.
        
        Returns:
            Union[Literal, Identifier]: An AST node representing the expression.
        Raises:
            SyntaxError: If the expression cannot be parsed.
        """
        try:
            # Simplified placeholder
            token = self.advance()
            kind = token['type']
            value = token['value']
            
            if kind == 'NUMBER':
                return Literal(value)
            elif kind == 'STRING':
                return Literal(value)
            elif kind == 'IDENT':
                return Identifier(value)
            else:
                self._report_error(f"Unexpected token in expression: {kind} with value '{value}'")
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Error parsing expression: {str(e)}")
            raise

    def parse_print_statement(self) -> FunctionCall:
        """
        Parse a print statement.
        
        Returns:
            FunctionCall: An AST node representing the print function call.
        Raises:
            SyntaxError: If the print statement cannot be parsed.
        """
        try:
            self.expect('KEYWORD', 'print')
            self.expect('LPAREN')
            args = []
            while self.peek()['type'] != 'RPAREN':
                args.append(self.parse_expression())
                if self.peek()['type'] == 'COMMA':
                    self.advance()
            self.expect('RPAREN')
            return FunctionCall('print', args)
        except Exception as e:
            if not isinstance(e, SyntaxError):
                self._report_error(f"Error parsing print statement: {str(e)}")
            raise
            
    # Placeholder methods to be implemented
    def parse_if_stmt(self):
        """Placeholder for if statement parsing"""
        self._report_error("If statement parsing not yet implemented")
        
    def parse_for_stmt(self):
        """Placeholder for for loop parsing"""
        self._report_error("For loop parsing not yet implemented")
        
    def parse_match_stmt(self):
        """Placeholder for match statement parsing"""
        self._report_error("Match statement parsing not yet implemented")
        
    def parse_return_stmt(self):
        """Placeholder for return statement parsing"""
        self._report_error("Return statement parsing not yet implemented")
        
    def parse_raise_stmt(self):
        """Placeholder for raise statement parsing"""
        self._report_error("Raise statement parsing not yet implemented")
