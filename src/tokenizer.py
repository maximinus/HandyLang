import re
from typing import List, Tuple, Union, Pattern, Match, Dict, Any

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
get_token: Pattern = re.compile(tok_regex).match

# Keywords
keywords = {
    'var', 'const', 'def', 'macro', 'comptime', 'type', 'extends',
    'if', 'else', 'for', 'in', 'match', 'try', 'except', 'raise',
    'return', 'test', 'assertEqual', 'assertNotEqual', 'assertTrue',
    'assertFalse', 'assertRaises', 'print', 'null', 'True', 'False',
    'number', 'float', 'int', 'string', 'bool', 'list', 'dict'
}

def tokenize(code: str) -> List[Dict[str, Any]]:
    """
    Tokenize the input code into a list of tokens.
    
    Each token includes information for error reporting such as line number,
    column position, and the full text of the line containing the token.
    
    Parameters:
        code (str): The source code to tokenize.
        
    Returns:
        List[Dict[str, Any]]: A list of token dictionaries with type, value, and location info.
        
    Raises:
        RuntimeError: If an unexpected character is encountered.
    """
    pos = 0
    tokens = []
    line = 1
    line_start = 0
    
    # Split the code into lines for context reporting
    code_lines = code.split('\n')
    
    mo: Union[Match, None] = get_token(code, pos)
    
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        col = mo.start() - line_start + 1
        
        # Get the text of the current line
        line_idx = line - 1  # Convert to 0-based indexing
        line_text = code_lines[line_idx] if line_idx < len(code_lines) else ""
        
        if kind == 'NEWLINE':
            line += 1
            line_start = mo.end()
        elif kind in ('COMMENT', 'BLOCK_COMMENT', 'SKIP'):
            # Skip these tokens but count newlines in block comments
            if kind == 'BLOCK_COMMENT':
                newlines = value.count('\n')
                if newlines > 0:
                    line += newlines
                    last_newline = value.rfind('\n')
                    if last_newline >= 0:
                        line_start = pos + last_newline + 1
        elif kind == 'NUMBER':
            tokens.append({
                'type': 'NUMBER',
                'value': value,
                'line': line,
                'col': col,
                'line_text': line_text
            })
        elif kind == 'STRING':
            tokens.append({
                'type': 'STRING',
                'value': value,
                'line': line,
                'col': col,
                'line_text': line_text
            })
        elif kind == 'BOOL':
            tokens.append({
                'type': 'BOOL',
                'value': value,
                'line': line,
                'col': col,
                'line_text': line_text
            })
        elif kind == 'NULL':
            tokens.append({
                'type': 'NULL',
                'value': value,
                'line': line,
                'col': col,
                'line_text': line_text
            })
        elif kind == 'IDENT':
            token_type = 'KEYWORD' if value in keywords else 'IDENT'
            tokens.append({
                'type': token_type,
                'value': value,
                'line': line,
                'col': col,
                'line_text': line_text
            })
        elif kind in ('AT', 'OP', 'ASSIGN', 'ARROW', 'COLON', 'COMMA',
                    'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
                    'LBRACKET', 'RBRACKET'):
            tokens.append({
                'type': kind,
                'value': value,
                'line': line,
                'col': col,
                'line_text': line_text
            })
        elif kind == 'MISMATCH':
            error_msg = f"Unexpected character '{value}' at line {line}, column {col}"
            error_msg += f"\n{line}: {line_text}"
            error_msg += "\n" + " " * (col + len(str(line)) + 1) + "^"
            raise RuntimeError(error_msg)
            
        pos = mo.end()
        mo = get_token(code, pos)
        
    return tokens
