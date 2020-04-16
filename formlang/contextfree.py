from collections import defaultdict
from copy import deepcopy
from queue import Queue

from scipy.sparse import csr_matrix, lil_matrix, kron, eye
import numpy as np


class Terminal:
    def __init__(self, value):
        self.value = str(value)

    def __str__(self):
        return self.value

    def __eq__(self, that):
        if type(that) is not Terminal:
            raise ValueError(f"Comparing a Terminal to {type(that)}")
        return self.value == that.value

    def __repr__(self):
        return f"Terminal({self.value!r})"

    def __hash__(self):
        return hash(self.value)


class Nonterminal:
    instances = 0

    def __init__(self, name=None):
        if name:
            self.name = str(name)
        else:
            self.__class__.instances += 1
            n = self.__class__.instances
            self.name = f"A{n}"

    def __str__(self):
        return self.name

    def __eq__(self, that):
        if type(that) is not Nonterminal:
            raise ValueError(f"Comparing a Nonterminal to {type(that)}")
        return self.name == that.name

    def __repr__(self):
        return f"Nonterminal({self.name!r})"

    def __hash__(self):
        return hash(self.name)


class Production:
    def __init__(self, lhs, rhs):
        self.lhs = Nonterminal(lhs)
        self.rhs = list(rhs)

    def __str__(self):
        if not self.rhs:
            return f"{self.lhs} \u2192 \u03b5"
        return f"{self.lhs} \u2192 " + " ".join(map(str, self.rhs))

    def __repr__(self):
        return f"Production({self.lhs!r}, {self.rhs!r})"

    def __eq__(self, that):
        if type(that) != Production:
            raise ValueError(f"Comparing a Production to {type(that)}")
        return self.lhs == that.lhs and self.rhs == that.rhs

    def serialize(self):
        if not self.rhs:
            return f"{self.lhs} eps"
        return f"{self.lhs} " + " ".join(map(str, self.rhs))

    @classmethod
    def deserialize(cls, s):
        sp = s.split(" ")
        lhs = Nonterminal(sp[0])
        rhs = []
        for i in sp[1:]:
            if i.islower():
                if i != "eps":
                    rhs.append(Terminal(i))
            else:
                rhs.append(Nonterminal(i))
        return Production(lhs, rhs)

    def clone(self):
        return Production(self.lhs, self.rhs)

    def split(self):
        """
        Split this Production into many, such
        that each rhs has at most two elements.
        """
        if len(self.rhs) <= 2:
            return [self.clone()]

        rest = Production(None, self.rhs[1:])
        prod = Production(self.lhs, [self.rhs[0], rest.lhs])
        return [prod] + rest.split()


class Grammar:
    def __init__(self, start=None, productions=None):
        if not start:
            start = Nonterminal()
        if not productions:
            productions = []
        self.start = start
        self.productions = list(map(Production.clone, productions))

    def __str__(self):
        return f"{self.start} \u21e8\n" + "\n".join(map(str, self.productions))

    def __eq__(self, that):
        if type(that) != Grammar:
            raise ValueError(f"Comparing a Grammar to {type(that)}")
        return self.start == that.start and \
            sorted(self.productions, key=str) == sorted(that.productions, key=str)

    def __repr__(self):
        return f"Grammar({self.start!r}, {self.productions!r})"

    def clone(self):
        return Grammar(self.start, self.productions)

    def serialize(self):
        res = []
        for prod in self.productions:
            if prod.lhs == self.start:
                res.append(prod.serialize())
        for prod in self.productions:
            if prod.lhs != self.start:
                res.append(prod.serialize())
        return "\n".join(res)

    def write_file(self, file_obj):
        file_obj.write(self.serialize())

    @classmethod
    def deserialize(cls, s):
        res = Grammar()
        start = False
        for line in s.split("\n"):
            if not line:
                continue
            prod = Production.deserialize(line)
            if not start:
                res.start = prod.lhs
                start = True
            res.productions.append(prod)
        return res

    @classmethod
    def from_file(cls, file_obj):
        return cls.deserialize(file_obj.read())

    def produce(self, nonterminal):
        return [i.rhs for i in self.productions if i.lhs == nonterminal]

    def get_epsilon_producers(self):
        result = set()
        prev = -1
        while len(result) != prev:
            prev = len(result)
            for prod in self.productions:
                if all([i in result for i in prod.rhs]):
                    result.add(prod.lhs)
        return result

    def normalize(self, weak=False):
        if self.is_normalized(weak):
            return
        if not weak:
            self.eliminate_start()
        self.eliminate_nonsolitary_terminals()
        self.eliminate_long_productions()
        if not weak:
            self.eliminate_epsilon()
        self.eliminate_unit_rules()
        self.eliminate_repetitions()
        self.eliminate_useless_nonterminals()

    def is_normalized(self, weak=False):
        for prod in self.productions:
            if not prod.rhs and prod.lhs != self.start and not weak:
                return False
            if len(prod.rhs) == 1 and type(prod.rhs[0]) != Terminal:
                return False
            if len(prod.rhs) > 2:
                return False
            if len(prod.rhs) == 2:
                if type(prod.rhs[0]) != Nonterminal or (prod.rhs[0] == self.start and not weak):
                    return False
                if type(prod.rhs[1]) != Nonterminal or (prod.rhs[1] == self.start and not weak):
                    return False
        return True

    def eliminate_start(self):
        new_start = Nonterminal()
        self.productions.append(Production(new_start, [self.start]))
        self.start = new_start

    def eliminate_nonsolitary_terminals(self):
        terminals = dict()
        for prod in self.productions:
            if len(prod.rhs) <= 1:
                continue
            for i in prod.rhs:
                if type(i) is Terminal and i not in terminals:
                    terminals[i] = Nonterminal()

        for prod in self.productions:
            prod.rhs = [terminals.get(i, i) for i in prod.rhs]

        for term, nterm in terminals.items():
            self.productions.append(Production(nterm, [term]))

    def eliminate_long_productions(self):
        prods = []
        for prod in self.productions:
            prods += prod.split()
        self.productions = prods

    def eliminate_epsilon(self):
        eps = self.get_epsilon_producers()
        new_prods = []
        for prod in self.productions:
            rhs_eps = []
            for i, t in enumerate(prod.rhs):
                if t in eps:
                    rhs_eps.append(i)
            for mask in range(1 << len(rhs_eps)):
                banned = set()
                for i, t in enumerate(rhs_eps):
                    if mask & (1 << i):
                        banned.add(t)
                new_prod = [p for i, p in enumerate(prod.rhs) if i not in banned]
                new_prods.append(Production(prod.lhs, new_prod))
        new_prods = [i for i in new_prods if i.rhs]
        if self.start in eps:
            new_prods.append(Production(self.start, []))
        self.productions = new_prods

    def eliminate_unit_rules(self):
        units = set()
        units_dict = defaultdict(set)

        for prod in self.productions:
            units.add((prod.lhs, prod.lhs))
            units_dict[prod.lhs].add(prod.lhs)

        prev = -1
        while prev != len(units):
            prev = len(units)
            for prod in self.productions:
                if len(prod.rhs) != 1:
                    continue
                b = prod.rhs[0]
                if type(b) != Nonterminal:
                    continue
                for a in units_dict[prod.lhs]:
                    pair = (a, b)
                    if pair not in units:
                        units.add(pair)
                        units_dict[b].add(a)

        new_prods = self.productions[:]

        for prod in self.productions:
            b = prod.lhs
            for a in units_dict[b]:
                new_prods.append(Production(a, prod.rhs))

        self.productions = [i for i in new_prods if len(i.rhs) != 1 or type(i.rhs[0]) != Nonterminal]


    def eliminate_useless_nonterminals(self):
        used = set()
        queue = Queue()
        used.add(self.start)
        queue.put(self.start)

        while not queue.empty():
            term = queue.get()
            for prod in self.produce(term):
                for el in prod:
                    if type(el) == Nonterminal and el not in used:
                        used.add(el)
                        queue.put(el)

        self.productions = [i for i in self.productions if i.lhs in used]

    def eliminate_repetitions(self):
        used = set()
        new_prods = []
        for i in self.productions:
            s = str(i)
            if s not in used:
                used.add(s)
                new_prods.append(i)
        self.productions = new_prods

    def get_nonterminals(self):
        res = set()
        for prod in self.productions:
            res.add(prod.lhs)
        return list(res)

    def recognize(self, seq):
        self.normalize()
        seq = list(map(Terminal, seq))
        n = len(seq)

        if n == 0:
            for prod in self.productions:
                if prod.lhs == self.start and prod.rhs == []:
                    return True
            return False

        dp = [[set() for _ in range(n)] for _ in range(n)]

        for i in range(n):
            dp[i][i] = {p.lhs for p in self.productions if p.rhs == [seq[i]]}

        for d in range(1, n):
            for i in range(0, n - d):
                j = i + d
                for k in range(i, j):
                    # looking for productions A -> BC
                    # where B in dp[i][k] and C in dp[k+1][j]
                    for prod in self.productions:
                        if len(prod.rhs) != 2:
                            continue
                        if prod.rhs[0] not in dp[i][k]:
                            continue
                        if prod.rhs[1] not in dp[k + 1][j]:
                            continue
                        dp[i][j].add(prod.lhs)

        return self.start in dp[0][-1]

    def path_query(self, graph, algorithm="matrix"):
        if algorithm == "tensor":
            return self._path_query_tensor(graph)
        if algorithm == "matrix":
            return self._path_query_matrix(graph)
        if algorithm == "hellings":
            return self._path_query_hellings(graph)
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    setattr(path_query, "algorithms", ("hellings", "matrix", "tensor"))

    def _path_query_tensor(self, graph):
        symbols = set()
        def _debug(a, k):
            for i in range(k):
                for j in range(k):
                    s = ""
                    for symbol in symbols:
                        if not a[symbol][i, j]:
                            continue
                        s += str(symbol)
                    if not s:
                        s = "."
                    print(s, end=" ")
                print()
            input()
        # Step 1. Build a RSM

        entries = dict()
        exits = dict()
        term_states = set()
        start_states = set()
        nodes = []
        m = 0

        for prod in self.productions:
            symbols.add(prod.lhs)
            if prod.lhs not in entries:
                entries[prod.lhs] = m
                start_states.add(m)
                nodes.append(dict())
                m += 1
            v = entries[prod.lhs]

            for i, symbol in enumerate(prod.rhs):
                symbols.add(symbol)
                if i == len(prod.rhs) - 1:
                    if prod.lhs not in exits:
                        exits[prod.lhs] = m
                        term_states.add(m)
                        nodes.append(dict())
                        m += 1
                    u = exits[prod.lhs]
                else:
                    u = nodes[v].get(symbol)
                    if u is None:
                        u = m
                        nodes.append(dict())
                        m += 1
                nodes[v][symbol] = u
                v = u

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

        # _debug(matrices, m)

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

        # _debug(g_matrices, n)

        # Step 4. Populate the matrix with epsilon loopbacks

        eps = self.get_epsilon_producers()
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

        mtx = g_matrices[self.start]

        for u in range(n):
            for v in range(n):
                if mtx[u, v]:
                    res.append((u, v))

        return res


    def _path_query_matrix(self, graph):
        self.normalize(weak=True)
        n = graph.number_of_nodes()
        eps = self.get_epsilon_producers()
        pairs = defaultdict(list)

        for i in range(n):
            for el in eps:
                pairs[el].append((i, i))

        for u, v, symbol in graph.edges(data="symbol"):
            for prod in self.productions:
                if prod.rhs == [Terminal(symbol)]:
                    pairs[prod.lhs].append((u, v))

        matrices = dict()
        for symbol in self.get_nonterminals():
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
            for prod in self.productions:
                if len(prod.rhs) != 2:
                    continue
                a = matrices[prod.rhs[0]]
                b = matrices[prod.rhs[1]]
                new = matrices[prod.lhs] + a * b
                if (new != matrices[prod.lhs]).count_nonzero() > 0:
                    matrices[prod.lhs] = new
                    keep_going = True

        res = []

        m = matrices[self.start]

        for u in range(n):
            for v in range(n):
                if m[u, v]:
                    res.append((u, v))

        return res

    def _path_query_hellings(self, graph):
        self.normalize(weak=True)
        n = graph.number_of_nodes()
        dp = list()
        lhs = defaultdict(list)

        eps = self.get_epsilon_producers()

        for i in range(n):
            for el in eps:
                dp.append((el, i, i))

        for u, v, symbol in graph.edges(data="symbol"):
            for prod in self.productions:
                if prod.rhs == [Terminal(symbol)]:
                    dp.append((prod.lhs, u, v))

        for prod in self.productions:
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

        return sorted([(u, v) for n, u, v in dp if n == self.start])
