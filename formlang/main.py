import sys

import click

from formlang.contextfree import Grammar
from formlang.graph import read_graph_from_file


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

@cli.command()
@click.argument("grammar", type=click.File("r"))
@click.argument("graph", type=click.File("r"))
def hellings(grammar, graph):
    grammar = Grammar.from_file(grammar)
    graph = read_graph_from_file(graph)
    res = grammar.path_query(graph)
    print("\n".join(map("{0[0]} {0[1]}".format, res)))
