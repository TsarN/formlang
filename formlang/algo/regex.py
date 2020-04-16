from formlang.contextfree import Terminal, Nonterminal, Production, Grammar


class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def eof(self):
        return self.position >= len(self.tokens)

    def peek(self):
        if self.eof():
            return None
        return self.tokens[self.position]

    def get(self):
        self.position += 1
        return self.tokens[self.position - 1]


def tokenize(s):
    res = []
    cur = ""

    for ch in s:
        if not ch.isalnum():
            if cur and cur != "eps":
                res.append(cur)
            if not ch.isspace():
                res.append(ch)
            cur = ""
        else:
            cur += ch

    if cur and cur != "eps":
        res.append(cur)

    return res


def productions_from_regex(lhs, regex):
    tokens = tokenize(regex)
    return _expr(TokenStream(tokens), lhs)


def _expr(s, lhs):
    ch = s.peek()
    if ch in [None, "|", "*", ")"]:
        return [Production(lhs, [])]

    t = _seq(s, lhs)
    if s.peek() == "|":
        s.get()
        t += _expr(s, lhs)
    return t


def _seq(s, lhs):
    t = _star(s, lhs)
    ch = s.peek()

    if ch in [None, "|", "*", ")"]:
        return t

    follow = Nonterminal()
    t2 = _seq(s, follow)

    res = []

    for i in t:
        if i.lhs != lhs:
            res.append(i)

    for i in t2:
        if i.lhs == follow:
            for j in t:
                if j.lhs == lhs:
                    res.append(Production(lhs, j.rhs + i.rhs))
        else:
            t.append(i)

    return res


def _star(s, lhs):
    t = _unit(s, lhs)
    if s.peek() != "*":
        return t

    s.get()
    repeat = Nonterminal()

    for i in t:
        if i.lhs == lhs:
            i.lhs = repeat

    t.append(Production(lhs, []))
    t.append(Production(lhs, [repeat, lhs]))

    return t


def _unit(s, lhs):
    ch = s.peek()

    if ch in [None, "|", "*", ")"]:
        raise ValueError("Invalid regex")

    s.get()
    if ch == "(":
        t = _expr(s, lhs)
        if s.get() != ")":
            raise ValueError("Invalid regex")
        return t

    if ch.isupper():
        ch = Nonterminal(ch)
    else:
        ch = Terminal(ch)

    return [Production(lhs, [ch])]
