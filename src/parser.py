from src.ast_nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    def expect(self, kind, value=None):
        tok = self.advance()
        if tok[0] != kind or (value and tok[1] != value):
            raise SyntaxError(f"Expected {kind} {value}, got {tok}")
        return tok

    def parse(self):
        statements = []
        while self.peek()[0]:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        kind, value = self.peek()
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

    def parse_var_decl(self):
        self.expect('KEYWORD', 'var')
        name = self.expect('IDENT')[1]
        type_ = None
        if self.peek()[0] == 'COLON':
            self.advance()
            type_ = self.expect('KEYWORD')[1]
        value = None
        if self.peek()[0] == 'ASSIGN':
            self.advance()
            value = self.parse_expression()
        return VarDecl(name, type_, value)

    def parse_const_decl(self):
        self.expect('KEYWORD', 'const')
        name = self.expect('IDENT')[1]
        type_ = None
        if self.peek()[0] == 'COLON':
            self.advance()
            type_ = self.expect('KEYWORD')[1]
        self.expect('ASSIGN')
        value = self.parse_expression()
        return ConstDecl(name, type_, value)

    def parse_function_def(self):
        self.expect('KEYWORD', 'def')
        name = self.expect('IDENT')[1]
        self.expect('LPAREN')
        params = self.parse_param_list()
        self.expect('RPAREN')
        return_type = None
        if self.peek()[0] == 'ARROW':
            self.advance()
            return_type = self.expect('KEYWORD')[1]
        body = self.parse_block()
        return FunctionDef(name, params, return_type, body)

    def parse_param_list(self):
        params = []
        while self.peek()[0] != 'RPAREN':
            pname = self.expect('IDENT')[1]
            ptype = None
            if self.peek()[0] == 'COLON':
                self.advance()
                ptype = self.expect('KEYWORD')[1]
            default = None
            if self.peek()[0] == 'ASSIGN':
                self.advance()
                default = self.parse_expression()
            params.append(Param(pname, ptype, default))
            if self.peek()[0] == 'COMMA':
                self.advance()
        return params

    def parse_block(self):
        self.expect('LBRACE')
        statements = []
        while self.peek()[0] != 'RBRACE':
            statements.append(self.parse_statement())
        self.expect('RBRACE')
        return Block(statements)

    def parse_expression(self):
        # Simplified placeholder
        tok = self.advance()
        if tok[0] == 'NUMBER':
            return Literal(tok[1])
        elif tok[0] == 'STRING':
            return Literal(tok[1])
        elif tok[0] == 'IDENT':
            return Identifier(tok[1])
        else:
            raise SyntaxError(f"Unexpected token in expression: {tok}")

    def parse_print_statement(self):
        self.expect('KEYWORD', 'print')
        self.expect('LPAREN')
        args = []
        while self.peek()[0] != 'RPAREN':
            args.append(self.parse_expression())
            if self.peek()[0] == 'COMMA':
                self.advance()
        self.expect('RPAREN')
        return FunctionCall('print', args)
