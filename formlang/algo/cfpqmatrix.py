from copy import deepcopy
from collections import defaultdict

from scipy.sparse import csr_matrix

from formlang.contextfree import Terminal


def path_query_matrix(grammar, graph):
    grammar.normalize(weak=True)
    n = graph.number_of_nodes()
    eps = grammar.get_epsilon_producers()
    pairs = defaultdict(list)

    for i in range(n):
        for el in eps:
            pairs[el].append((i, i))

    for u, v, symbol in graph.edges(data="symbol"):
        for prod in grammar.productions:
            if prod.rhs == [Terminal(symbol)]:
                pairs[prod.lhs].append((u, v))

    matrices = dict()
    for symbol in grammar.get_nonterminals():
        rows = []
        cols = []
        data = []
        for r, c in pairs[symbol]:
            rows.append(r)
            cols.append(c)
            data.append(True)
        matrices[symbol] = csr_matrix((data, (rows, cols)),
                                      shape=(n, n), dtype=bool)

    keep_going = True
    while keep_going:
        keep_going = False
        for prod in grammar.productions:
            if len(prod.rhs) != 2:
                continue
            a = matrices[prod.rhs[0]]
            b = matrices[prod.rhs[1]]
            new = matrices[prod.lhs] + a * b
            if (new != matrices[prod.lhs]).count_nonzero() > 0:
                matrices[prod.lhs] = new
                keep_going = True

    res = []

    m = matrices[grammar.start]

    for u in range(n):
        for v in range(n):
            if m[u, v]:
                res.append((u, v))

    return res
