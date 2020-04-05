import sys

import click

from formlang.contextfree import Grammar


@click.group()
def cli():
    pass


@cli.command()
@click.argument("source", type=click.File("r"))
@click.argument("output", type=click.File("w"))
def cnf(source, output):
    grammar = Grammar.from_file(source)
    grammar.normalize()
    grammar.write_file(output)


@cli.command()
@click.argument("grammar", type=click.File("r"))
@click.argument("string", type=click.File("r"))
def cyk(grammar, string):
    grammar = Grammar.from_file(grammar)
    string = string.readline().strip().split()
    if grammar.recognize(string):
        print("YES")
    else:
        print("NO")
