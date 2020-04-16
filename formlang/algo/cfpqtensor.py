from copy import deepcopy
from collections import defaultdict

from scipy.sparse import csr_matrix, lil_matrix, kron, eye

from formlang.contextfree import Terminal


def path_query_tensor(grammar, graph):
    # Step 1. Build a RSM

    entries = dict()
    symbols = set()
    term_states = set()
    start_states = set()
    nodes = [dict()]
    m = 0

    for prod in grammar.productions:
        symbols.add(prod.lhs)
        if prod.lhs not in entries:
            entries[prod.lhs] = m
            start_states.add(m)
            nodes.append(dict())
            m += 1
        v = entries[prod.lhs]

        for i, symbol in enumerate(prod.rhs):
            symbols.add(symbol)
            u = nodes[v].get(symbol)
            if u is None:
                u = m
                nodes.append(dict())
                m += 1
            nodes[v][symbol] = u
            v = u
        term_states.add(v)

    sym_states = [set() for _ in range(m)]
    for symbol, v in entries.items():
        sym_states[v].add(symbol)

    # Step 2. Build adjacency matrices for the RSM

    matrices = dict()
    for symbol in symbols:
        rows = []
        cols = []
        data = []

        for v in range(m):
            u = nodes[v].get(symbol)
            if u is None:
                continue
            rows.append(v)
            cols.append(u)
            data.append(True)

        matrices[symbol] = csr_matrix((data, (rows, cols)),
                                      shape=(m, m), dtype=bool)

    # Step 3. Build adjacency matrices for the graph

    n = graph.number_of_nodes()

    g_matrices = dict()
    for symbol in symbols:
        rows = []
        cols = []
        data = []

        if type(symbol) is Terminal:
            for v, u, _symbol in graph.edges(data="symbol"):
                if _symbol != symbol.value:
                    continue
                rows.append(v)
                cols.append(u)
                data.append(True)

        g_matrices[symbol] = csr_matrix((data, (rows, cols)),
                                        shape=(n, n), dtype=bool)

    # Step 4. Populate the matrix with epsilon loopbacks

    eps = grammar.get_epsilon_producers()
    for symbol in eps:
        g_matrices[symbol] += eye(n, dtype=bool, format="csr")

    # Step 5. Do the computation

    keep_going = True
    while keep_going:
        keep_going = False

        k = n * m
        t = csr_matrix((k, k), dtype=bool)
        for symbol in symbols:
            tmp = kron(matrices[symbol], g_matrices[symbol], "csr")
            t += tmp.tocsr()

        # Transitive closure
        factor = t.copy()
        for i in range(k):
            new = t + t * factor
            if (new != t).count_nonzero() == 0:
                break
            t = new

        upd = dict()

        for i in range(k):
            for j in range(k):
                if not t[i, j]:
                    continue
                s = i // n
                f = j // n
                x = i % n
                y = j % n
                if s not in start_states or f not in term_states:
                    continue
                for sym in sym_states[s]:
                    if not g_matrices[sym][x, y]:
                        if sym not in upd:
                            upd[sym] = lil_matrix((n, n), dtype=bool)
                        upd[sym][x, y] = True
                        keep_going = True

        for symbol, x in upd.items():
            g_matrices[symbol] += x.tocsr()

    res = []

    mtx = g_matrices[grammar.start]

    for u in range(n):
        for v in range(n):
            if mtx[u, v]:
                res.append((u, v))

    return res
