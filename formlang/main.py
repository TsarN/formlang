import sys

import click

from formlang.contextfree import Grammar
from formlang.graph import read_graph_from_file
from formlang.benchmark import benchmark_cfpq


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
@click.argument("output", type=click.File("w"))
@click.option("-a", "--algorithm", required=True,
              type=click.Choice(Grammar.path_query.algorithms))
def cfpq(grammar, graph, output, algorithm):
    grammar = Grammar.from_file(grammar)
    graph = read_graph_from_file(graph)
    res = grammar.path_query(graph, algorithm)
    print(grammar.serialize(), file=output)
    print("\n".join(map("{0[0]} {0[1]}".format, res)), file=output)


@cli.command()
@click.argument("path", type=click.Path(file_okay=False, exists=True))
@click.argument("ds")
def benchmark(path, ds):
    benchmark_cfpq(path, ds)
