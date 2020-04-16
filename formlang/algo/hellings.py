from copy import deepcopy
from collections import defaultdict

from formlang.contextfree import Terminal


def path_query_hellings(grammar, graph):
    grammar.normalize(weak=True)
    n = graph.number_of_nodes()
    dp = list()
    lhs = defaultdict(list)

    eps = grammar.get_epsilon_producers()

    for i in range(n):
        for el in eps:
            dp.append((el, i, i))

    for u, v, symbol in graph.edges(data="symbol"):
        for prod in grammar.productions:
            if prod.rhs == [Terminal(symbol)]:
                dp.append((prod.lhs, u, v))

    for prod in grammar.productions:
        if len(prod.rhs) != 2:
            continue
        lhs[tuple(prod.rhs)].append(prod.lhs)

    rem = deepcopy(dp)

    while rem:
        n1, u, v = rem.pop(0)

        for n2, w, _u in dp:
            if _u != u:
                continue
            for n3 in lhs[n2, n1]:
                new = (n3, w, v)
                if new in dp:
                    continue
                dp.append(new)
                rem.append(new)

        for n2, _v, w in dp:
            if _v != v:
                continue
            for n3 in lhs[n1, n2]:
                new = (n3, u, w)
                if new in dp:
                    continue
                dp.append(new)
                rem.append(new)

    return sorted([(u, v) for n, u, v in dp if n == grammar.start])
