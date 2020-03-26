from formlang.contextfree import *

def test_deserialize():
    assert(Grammar.deserialize("""\
S eps
S a T b T
T c S c
""") == Grammar(Nonterminal("S"), [
    Production(Nonterminal("S"), []),
    Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
    Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
]))


def test_serialize():
    assert(Grammar(Nonterminal("S"), [
    Production(Nonterminal("S"), []),
    Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
    Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
]).serialize() == """\
S eps
S a T b T
T c S c""")

    assert(Grammar(Nonterminal("T"), [
    Production(Nonterminal("S"), []),
    Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
    Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
]).serialize() == """\
T c S c
S eps
S a T b T""")

def test_normalize():
    g = Grammar(Nonterminal("S"), [
        Production(Nonterminal("S"), []),
        Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
        Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
    ])
    assert(not g.is_normalized())
    g.normalize()
    assert(g.is_normalized())
    assert(len(g.productions) == 9)
    g.normalize()
    assert(g.is_normalized())
    assert(len(g.productions) == 9)
