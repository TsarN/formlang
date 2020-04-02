import io

from formlang.contextfree import *

def test_from_file():
    # I think there's no reason to test reading/writing actual files
    assert(Grammar.from_file(io.StringIO("""\
S eps
S a T b T
T c S c
""")) == Grammar(Nonterminal("S"), [
    Production(Nonterminal("S"), []),
    Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
    Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
]))


def test_write_file():
    # I think there's no reason to test reading/writing actual files
    file_obj = io.StringIO()
    Grammar(Nonterminal("S"), [
        Production(Nonterminal("S"), []),
        Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
        Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
    ]).write_file(file_obj)
    file_obj.seek(0)
    assert(file_obj.read() == """\
S eps
S a T b T
T c S c""")

    file_obj = io.StringIO()
    Grammar(Nonterminal("T"), [
        Production(Nonterminal("S"), []),
        Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
        Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
    ]).write_file(file_obj)
    file_obj.seek(0)
    assert(file_obj.read() == """\
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

    # CFG equivalence is undecidable, so I use overly restrictive test here
    assert(g == Grammar(Nonterminal('A2'), [
        Production(Nonterminal('A2'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('S'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('A6'), [Nonterminal('T'), Nonterminal('A7')]),
        Production(Nonterminal('A7'), [Nonterminal('A4'), Nonterminal('T')]),
        Production(Nonterminal('T'), [Nonterminal('A5'), Nonterminal('A8')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A3'), [Terminal('a')]),
        Production(Nonterminal('A4'), [Terminal('b')]),
        Production(Nonterminal('A5'), [Terminal('c')]),
        Production(Nonterminal('A2'), [])])
    )


def test_normalize_step_by_step():
    Nonterminal.instances = 1
    g = Grammar(Nonterminal("S"), [
        Production(Nonterminal("S"), []),
        Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
        Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
    ])

    # CFG equivalence is undecidable, so I use overly restrictive tests here

    g.eliminate_start()
    assert(g == Grammar(Nonterminal('A2'), [
        Production(Nonterminal('S'), []),
        Production(Nonterminal('S'), [Terminal('a'), Nonterminal('T'), Terminal('b'), Nonterminal('T')]),
        Production(Nonterminal('T'), [Terminal('c'), Nonterminal('S'), Terminal('c')]),
        Production(Nonterminal('A2'), [Nonterminal('S')])]))

    g.eliminate_nonsolitary_terminals()
    assert(g == Grammar(Nonterminal('A2'), [
        Production(Nonterminal('S'), []),
        Production(Nonterminal('S'), [Nonterminal('A3'), Nonterminal('T'), Nonterminal('A4'), Nonterminal('T')]),
        Production(Nonterminal('T'), [Nonterminal('A5'), Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A2'), [Nonterminal('S')]),
        Production(Nonterminal('A3'), [Terminal('a')]),
        Production(Nonterminal('A4'), [Terminal('b')]),
        Production(Nonterminal('A5'), [Terminal('c')])]))

    g.eliminate_long_productions()
    assert(g == Grammar(Nonterminal('A2'), [
        Production(Nonterminal('S'), []), Production(Nonterminal('S'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('A6'), [Nonterminal('T'), Nonterminal('A7')]),
        Production(Nonterminal('A7'), [Nonterminal('A4'), Nonterminal('T')]),
        Production(Nonterminal('T'), [Nonterminal('A5'), Nonterminal('A8')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A2'), [Nonterminal('S')]),
        Production(Nonterminal('A3'), [Terminal('a')]),
        Production(Nonterminal('A4'), [Terminal('b')]),
        Production(Nonterminal('A5'), [Terminal('c')])]))

    g.eliminate_epsilon()
    assert(g == Grammar(Nonterminal('A2'), [
        Production(Nonterminal('S'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('A6'), [Nonterminal('T'), Nonterminal('A7')]),
        Production(Nonterminal('A7'), [Nonterminal('A4'), Nonterminal('T')]),
        Production(Nonterminal('T'), [Nonterminal('A5'), Nonterminal('A8')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A2'), [Nonterminal('S')]),
        Production(Nonterminal('A2'), [Nonterminal('S')]),
        Production(Nonterminal('A3'), [Terminal('a')]),
        Production(Nonterminal('A4'), [Terminal('b')]),
        Production(Nonterminal('A5'), [Terminal('c')]),
        Production(Nonterminal('A2'), [])]))

    g.eliminate_unit_rules()
    assert(g == Grammar(Nonterminal('A2'), [
        Production(Nonterminal('A2'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('S'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('A6'), [Nonterminal('T'), Nonterminal('A7')]),
        Production(Nonterminal('A7'), [Nonterminal('A4'), Nonterminal('T')]),
        Production(Nonterminal('T'), [Nonterminal('A5'), Nonterminal('A8')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A3'), [Terminal('a')]),
        Production(Nonterminal('A4'), [Terminal('b')]),
        Production(Nonterminal('A5'), [Terminal('c')]),
        Production(Nonterminal('A2'), [])]))

    g.eliminate_useless_nonterminals()
    assert(g == Grammar(Nonterminal('A2'), [
        Production(Nonterminal('A2'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('S'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('A6'), [Nonterminal('T'), Nonterminal('A7')]),
        Production(Nonterminal('A7'), [Nonterminal('A4'), Nonterminal('T')]),
        Production(Nonterminal('T'), [Nonterminal('A5'), Nonterminal('A8')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A3'), [Terminal('a')]),
        Production(Nonterminal('A4'), [Terminal('b')]),
        Production(Nonterminal('A5'), [Terminal('c')]),
        Production(Nonterminal('A2'), [])]))

    g.eliminate_repetitions()
    assert(g == Grammar(Nonterminal('A2'), [
        Production(Nonterminal('A2'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('S'), [Nonterminal('A3'), Nonterminal('A6')]),
        Production(Nonterminal('A6'), [Nonterminal('T'), Nonterminal('A7')]),
        Production(Nonterminal('A7'), [Nonterminal('A4'), Nonterminal('T')]),
        Production(Nonterminal('T'), [Nonterminal('A5'), Nonterminal('A8')]),
        Production(Nonterminal('A8'), [Nonterminal('S'), Nonterminal('A5')]),
        Production(Nonterminal('A3'), [Terminal('a')]),
        Production(Nonterminal('A4'), [Terminal('b')]),
        Production(Nonterminal('A5'), [Terminal('c')]),
        Production(Nonterminal('A2'), [])])
    )

