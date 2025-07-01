#!/usr/bin/env python3

import sys

from src.tokenizer import tokenize
from src.parser import Parser


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parse_file.py <file.handy>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()

    print_ast(ast)


def print_ast(node, indent=0):
    """Simple AST printer for debugging."""
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
