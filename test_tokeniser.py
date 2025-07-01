import os
import sys

from src.tokenizer import tokenize


def process_file(path):
    with open(path, 'r') as f:
        code = f.read()
    tokens = tokenize(code)
    print(f"{path}: {len(tokens)} tokens")


def process_directory(dir_path):
    for root, _, files in os.walk(dir_path):
        print(f"Processing directory: {root}")
        for file in files:
            if file.endswith('.hdy'):
                process_file(os.path.join(root, file))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 handy_tokenize_cli.py <file or directory>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isfile(target):
        process_file(target)
    elif os.path.isdir(target):
        process_directory(target)
    else:
        print(f"{target} is not a valid file or directory")
