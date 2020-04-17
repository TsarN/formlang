import time
import os
import sys

from formlang.contextfree import Grammar
from formlang.graph import read_graph_from_file


GRAPHS = {
    "FullGraph": [
        "fullgraph_10",
        "fullgraph_50",
        "fullgraph_100"
    ],
    "SparseGraph": [
        "G5k-0.001",
        "G10k-0.001",
        "G10k-0.01",
        "G10k-0.1",
        "G20k-0.001",
        "G40k-0.001",
        "G80k-0.001"
    ],
    "MemoryAliases": [
        "wc.txt",
        "bzip2.txt",
        "pr.txt",
        "ls.txt",
        "gzip.txt"
    ],
    "WorstCase": [
        "worstcase_4",
        "worstcase_8",
        "worstcase_16",
        "worstcase_32",
    ]
}

ALGORITHMS = ["matrix", "tensor"]


def measure(graph, grammar, algorithm):
    with open(grammar, "r") as f:
        grammar = Grammar.from_file(f)
    with open(graph, "r") as f:
        graph = read_graph_from_file(f)

    t1 = time.time()
    res = grammar.path_query(graph, algorithm)
    t2 = time.time()

    return t2 - t1


def benchmark_cfpq(datapath, ds):
    graphs = GRAPHS[ds]
    grammars = sorted(os.listdir(os.path.join(datapath, ds, "grammars")))
    header = [ds]

    for algorithm in ALGORITHMS:
        for grammar in grammars:
            colname = f"{algorithm}-{grammar}"
            header.append(colname)

    print(*header, sep=",")

    for graph in graphs:
        graph_path = os.path.join(datapath, ds, "graphs", graph)
        rowname = f"{graph}"
        row = []

        for algorithm in ALGORITHMS:
            for grammar in grammars:
                print(algorithm, grammar, graph, file=sys.stderr)
                grammar_path = os.path.join(datapath, ds, "grammars", grammar)
                timing = measure(graph_path, grammar_path, algorithm)
                print("%.5f sec" % timing, file=sys.stderr)
                row.append(timing)

        print(rowname, *row, sep=",")
