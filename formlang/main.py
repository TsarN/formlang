from formlang.contextfree import Grammar

import sys


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input> <output>")
        return
    with open(sys.argv[1]) as f:
        grammar = Grammar.from_file(f)
    grammar.normalize()
    with open(sys.argv[2], "w") as f:
        grammar.write_file(f)
