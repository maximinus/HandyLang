# HandyLang

HandyLang is a programming language implementation written in Python that provides a flexible and expressive syntax for writing programs.

## Features

- First-class functions with lambda support
- Pattern matching capabilities
- Macro system
- Flexible type system with type inference
- Rich control flow with if-else statements
- Support for dictionaries and lists
- Variable declarations with optional type annotations
- Function definitions with default arguments
- Special character and escaped string support

## Project Structure

```
.
├── src/              # Core language implementation
│   ├── tokenizer.py  # Lexical analysis
│   ├── parser.py     # Syntax parsing
│   └── interpreter.py # Language runtime
├── examples/         # Example programs and code snippets
├── tests/           # Test suite
└── docs/            # Language documentation
```

## Installation

Clone the repository and ensure you have Python installed. No additional dependencies are required.

## Usage

Run a HandyLang program using:

```bash
python handy.py your_program.hdy
```

Example programs can be found in the `examples/` directory.

## Examples

Here's a simple HandyLang program:

```handy
# examples/programs/first_program.hdy
const PI: float = 3.141
var radius: int = 2.0

print(PI)
print(radius)
```

For more examples, check out the `examples/` directory which contains various code samples demonstrating language features.

## License

See the [LICENSE](LICENSE) file for details.
