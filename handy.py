import sys

from src.parser import Parser
from src.tokenizer import tokenize
from src.interpreter import Interpreter
from src.environment import Environment


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 run_handy.py <file.handy>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path) as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()

    env = Environment()
    interp = Interpreter(env)
    interp.run(ast)


if __name__ == "__main__":
    main()
