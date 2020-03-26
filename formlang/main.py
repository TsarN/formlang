from formlang.contextfree import Grammar

import sys


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    with open(sys.argv[1]) as f:
        grammar = Grammar.deserialize(f.read())
    grammar.normalize()
    print(grammar.serialize())
