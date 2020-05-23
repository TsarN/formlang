import time
import os
import sys

from formlang.contextfree import Grammar
from formlang.graph import read_graph_from_file
from antlr4.InputStream import InputStream
from formlang.query import ParseError, parse_query
from formlang.db import Executor, FileDatabase


GRAPHS = {
    "FullGraph": [
        "fullgraph_10",
        "fullgraph_50",
        "fullgraph_100",
        "fullgraph_200",
        "fullgraph_500"
    ],
    "MemoryAliases": [
        "wc.txt",
        "bzip2.txt",
        "pr.txt",
        "ls.txt",
    ],
    "WorstCase": [
        "worstcase_4",
        "worstcase_8",
        "worstcase_16",
        "worstcase_32",
        "worstcase_64",
        "worstcase_128",
        "worstcase_256",
    ]
}

ALGORITHMS = ["hellings", "matrix", "tensor"]


def measure(db_path, graph, grammar_path, algorithm):
    grammar = ""
    start = None
    with open(grammar_path, "r") as f:
        for line in f:
            split = line.strip()
            if start is None:
                start = split[0]
            grammar += f"{split[0]} = {split[1:]};\n"

    script = f"""
connect "{db_path}";
{grammar}
select a, b from "{graph}" where path(a, b, {start}) using "{algorithm}";
"""

    print(script)

    t1 = time.time()
    parsed = parse_query(InputStream(script))
    executor = Executor(FileDatabase())
    executor.execute_many(parsed)
    t2 = time.time()

    return t2 - t1


def benchmark_cfpq(datapath):
    for ds in GRAPHS:
        graphs = GRAPHS[ds]
        grammars = sorted(os.listdir(os.path.join(datapath, ds, "grammars")))
        db_path = os.path.join(datapath, ds, "graphs")

        for graph in graphs:
            for algorithm in ALGORITHMS:
                for grammar in grammars:
                    print(algorithm, grammar, graph, file=sys.stderr)
                    try:
                        grammar_path = os.path.join(datapath, ds, "grammars", grammar)
                        timing = measure(db_path, graph, grammar_path, algorithm)
                        print("%.5f sec" % timing, file=sys.stderr)
                    except KeyboardInterrupt:
                        print("Press ^C again to exit, press ENTER to continue", file=sys.stderr)
                        input()
