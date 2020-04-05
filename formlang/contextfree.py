from collections import defaultdict
from queue import Queue


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
        self.productions = list(productions)

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
        return Grammar(self.productions)

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

    def normalize(self):
        if not self.is_normalized():
            self.eliminate_start()
            self.eliminate_nonsolitary_terminals()
            self.eliminate_long_productions()
            self.eliminate_epsilon()
            self.eliminate_unit_rules()
        self.eliminate_repetitions()
        self.eliminate_useless_nonterminals()

    def is_normalized(self):
        for prod in self.productions:
            if not prod.rhs and prod.lhs != self.start:
                return False
            if len(prod.rhs) == 1 and type(prod.rhs[0]) != Terminal:
                return False
            if len(prod.rhs) > 2:
                return False
            if len(prod.rhs) == 2:
                if type(prod.rhs[0]) != Nonterminal or prod.rhs[0] == self.start:
                    return False
                if type(prod.rhs[1]) != Nonterminal or prod.rhs[1] == self.start:
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
                        banned.add(prod.rhs[t])
                new_prod = [i for i in prod.rhs if i not in banned]
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
