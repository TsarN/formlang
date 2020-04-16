import time
import os
import sys

from formlang.contextfree import Grammar
from formlang.graph import read_graph_from_file


def measure(graph, grammar, algorithm):
    with open(grammar, "r") as f:
        grammar = Grammar.from_file(f)
    with open(graph, "r") as f:
        graph = read_graph_from_file(f)

    t1 = time.time()
    res = grammar.path_query(graph, algorithm)
    t2 = time.time()

    return t2 - t1


def benchmark_cfpq(datapath):
    datasets = sorted(os.listdir(datapath))

    for ds in datasets:
        graphs = sorted(os.listdir(os.path.join(datapath, ds, "graphs")))
        grammars = sorted(os.listdir(os.path.join(datapath, ds, "grammars")))
        header = [ds]

        for algorithm in Grammar.path_query.algorithms:
            for grammar in grammars:
                colname = f"{algorithm}-{grammar}"
                header.append(colname)

        print(*header, sep=",")

        for graph in graphs:
            graph_path = os.path.join(datapath, ds, "graphs", graph)
            rowname = f"{graph}"
            row = []

            for algorithm in Grammar.path_query.algorithms:
                for grammar in grammars:
                    print(algorithm, grammar, graph, file=sys.stderr)
                    grammar_path = os.path.join(datapath, ds, "grammars", grammar)
                    timing = measure(graph_path, grammar_path, algorithm)
                    print("%.5f sec" % timing, file=sys.stderr)
                    row.append(timing)

            print(rowname, *row, sep=",")
