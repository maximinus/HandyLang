# Handy Programming Language Project Overview

Handy is a programming language project that aims to combine the readability of Python with strong typing and modern language features. This document provides an overview of the project's current state and design.

## Current Implementation Status

The project currently has:
- A tokenizer implementation (src/tokenizer.py)
- A test harness for the tokenizer (test_tokeniser.py)
- Example files showcasing language syntax
- Comprehensive language design documentation

## Language Design Features

### Type System
- Strong typing with optional type annotations
- Base types: bool, int, float, number, string, list, dict
- Support for custom types with inheritance
- Type inference for untyped variables
- Special 'number' type for exact numeric representation
- Null value support across all types

### Variables and Constants
- Variables can be typed or untyped
- Constants with optional type annotations
- Trailing comma support in lists and dicts
- Implicit type casting where safe
- Default values for uninitialized typed variables

### Functions and Code Blocks
- Python-like function definitions with type annotations
- Optional return type annotations
- Support for default argument values
- Lambda expressions and assignable code blocks
- Closure support with current environment access

### Control Flow
- If-else statements
- For loops with 'in' iterator
- Pattern matching with 'match' statements
- Exception handling with try-except blocks
- Multiple exception type handling

### Macro System
- Compile-time macro support
- Runtime macro evaluation with @macro syntax
- Backtick syntax for code insertion
- Support for compile-time evaluation

### Testing
- Built-in test blocks
- Assertion functions (assertEqual, assertNotEqual, etc.)
- Inline test definitions

## Technical Implementation

### Tokenizer Details
The tokenizer (src/tokenizer.py) implements:
- Comprehensive token specification using regex patterns
- Support for block comments and line comments
- Number and string literal parsing
- Keyword recognition
- Operator and symbol tokenization
- Error detection for mismatched tokens

Token types include:
- Comments (block and line)
- Numbers
- Strings
- Booleans
- Identifiers
- Operators
- Brackets and delimiters
- Keywords

### Project Structure
```
project/
├── src/
│   ├── __init__.py
│   └── tokenizer.py
├── docs/
│   ├── doc_design.txt    # Language design documentation
│   └── grammar.txt       # Formal language grammar
├── examples/            # Example code files
│   └── *.hdy
├── test_tokeniser.py   # Tokenizer test harness
└── ai_docs/            # AI-generated documentation
```

## Future Development

Areas that appear to be pending implementation:
1. Parser implementation
2. AST (Abstract Syntax Tree) generation
3. Interpreter/Compiler
4. Standard library
5. Development tools and IDE integration

The project has a solid foundation with well-documented language design and initial tokenizer implementation. The formal grammar and comprehensive documentation provide a clear roadmap for implementing the remaining components of the language.
