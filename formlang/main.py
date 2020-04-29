import sys

from antlr4 import InputStream
import click

from formlang.contextfree import Grammar
from formlang.graph import read_graph_from_file
from formlang.benchmark import benchmark_cfpq
from formlang.query import parse_query, print_tree_as_dot


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
@click.argument("query", type=click.File("r"))
def parsequery(query):
    stream = InputStream(query.read())
    parsed = parse_query(stream)
    if not parsed:
        sys.exit(1)
    print_tree_as_dot(parsed)


@cli.command()
@click.argument("path", type=click.Path(file_okay=False, exists=True))
@click.argument("ds")
def benchmark(path, ds):
    benchmark_cfpq(path, ds)
