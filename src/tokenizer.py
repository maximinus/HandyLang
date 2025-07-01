import re

# Define token specifications
token_specification = [
    ('BLOCK_COMMENT', r'"""(.|\n)*?"""'),
    ('COMMENT',       r'#.*'),
    ('NUMBER',        r'\d+(\.\d+)?'),
    ('STRING',        r'"([^"\\]|\\.)*"'),
    ('BOOL',          r'\b(True|False)\b'),
    ('NULL',          r'\bnull\b'),
    ('IDENT',         r'[A-Za-z_][A-Za-z0-9_]*'),
    ('AT',            r'@'),
    ('ASSIGN',        r'='),
    ('OP',            r'==|!=|>=|<=|//|[\+\-\*/%<>]'),
    ('ARROW',         r'->'),
    ('COLON',         r':'),
    ('COMMA',         r','),
    ('SEMICOLON',     r';'),
    ('LPAREN',        r'\('),
    ('RPAREN',        r'\)'),
    ('LBRACE',        r'\{'),
    ('RBRACE',        r'\}'),
    ('LBRACKET',      r'\['),
    ('RBRACKET',      r'\]'),
    ('NEWLINE',       r'\n'),
    ('SKIP',          r'[ \t]+'),
    ('MISMATCH',      r'.'),
]

# Compile regex
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

# Keywords
keywords = {
    'var', 'const', 'def', 'macro', 'comptime', 'type', 'extends',
    'if', 'else', 'for', 'in', 'match', 'try', 'except', 'raise',
    'return', 'test', 'assertEqual', 'assertNotEqual', 'assertTrue',
    'assertFalse', 'assertRaises', 'print', 'null', 'True', 'False',
    'number', 'float', 'int', 'string', 'bool', 'list', 'dict'
}

def tokenize(code):
    """Return a list of tokens as (TYPE, VALUE)."""
    pos = 0
    tokens = []
    line = 1
    mo = get_token(code, pos)
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind in ('COMMENT', 'BLOCK_COMMENT', 'SKIP', 'NEWLINE'):
            if kind == 'NEWLINE':
                line += 1
            pass
        elif kind == 'NUMBER':
            tokens.append(('NUMBER', value))
        elif kind == 'STRING':
            tokens.append(('STRING', value))
        elif kind == 'BOOL':
            tokens.append(('BOOL', value))
        elif kind == 'NULL':
            tokens.append(('NULL', value))
        elif kind == 'IDENT':
            if value in keywords:
                tokens.append(('KEYWORD', value))
            else:
                tokens.append(('IDENT', value))
        elif kind in ('AT', 'OP', 'ASSIGN', 'ARROW', 'COLON', 'COMMA',
                      'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
                      'LBRACKET', 'RBRACKET'):
            tokens.append((kind, value))
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line}')
        pos = mo.end()
        mo = get_token(code, pos)
    return tokens
