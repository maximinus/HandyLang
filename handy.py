import sys
from typing import Dict, List, Any

from src.parser import Parser
from src.tokenizer import tokenize
from src.interpreter import Interpreter
from src.environment import Environment


def main() -> None:
    """
    Main entry point for the HandyLang interpreter.
    
    Parses command-line arguments, reads the source file,
    tokenizes, parses, and interprets the code.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 handy.py <file.hdy>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path) as f:
            code = f.read()

        tokens = tokenize(code)
        parser = Parser(tokens, filename=path)
        ast = parser.parse()

        env = Environment()
        interp = Interpreter(env)
        interp.run(ast)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
