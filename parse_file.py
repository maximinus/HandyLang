#!/usr/bin/env python3

import sys
from typing import Any, List, Dict, Optional, Union

from src.tokenizer import tokenize
from src.parser import Parser


def main() -> None:
    """
    Main function for parsing HandyLang files and printing the AST.
    
    Reads a file, tokenizes and parses it, then prints the resulting AST
    for debugging and analysis purposes.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 parse_file.py <file.hdy>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, 'r') as f:
            code = f.read()

        tokens = tokenize(code)
        parser = Parser(tokens, filename=path)
        ast = parser.parse()

        print_ast(ast)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)


def print_ast(node: Any, indent: int = 0) -> None:
    """
    Simple AST printer for debugging.
    
    Parameters:
        node (Any): The AST node to print.
        indent (int): The current indentation level.
    """
    pad = "  " * indent
    if isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    elif hasattr(node, '__dict__'):
        print(f"{pad}{node.__class__.__name__}:")
        for k, v in node.__dict__.items():
            print(f"{pad}  {k}:")
            print_ast(v, indent + 2)
    else:
        print(f"{pad}{node}")


if __name__ == "__main__":
    main()
