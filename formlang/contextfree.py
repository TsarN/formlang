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
        return self.start == that.start and self.productions == that.productions

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

    def normalize(self):
        self.eliminate_start()
        self.eliminate_nonsolitary_terminals()
        self.eliminate_long_productions()
        self.eliminate_epsilon()
        self.eliminate_unit_rules()

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
        epsilon = set()
        for prod in self.productions:
            if prod.lhs != self.start and not prod.rhs:
                epsilon.add(prod.lhs)
        if not epsilon:
            return
        for prod in self.productions:
            prod.rhs = [i for i in prod.rhs if i not in epsilon]
        self.productions = [i for i in self.productions if i.rhs or i.lhs == self.start]
        self.eliminate_epsilon()

    def eliminate_unit_rules(self):
        units = dict()
        for prod in self.productions:
            if len(prod.rhs) != 1:
                continue
            rhs = prod.rhs[0]
            if type(rhs) is not Nonterminal:
                continue
            if rhs not in units:
                units[rhs] = set()
            units[rhs].add(prod.lhs)

        if not units:
            return

        new_prods = []

        for prod in self.productions:
            for lhs in units.get(prod.lhs, []):
                if lhs in units:
                    continue
                new_prods.append(Production(lhs, prod.rhs))
            if len(prod.rhs) == 1 and type(prod.rhs[0]) == Nonterminal:
                continue
            new_prods.append(Production(prod.lhs, prod.rhs))

        self.productions = new_prods
        self.eliminate_unit_rules()
